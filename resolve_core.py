"""
DaVinci Resolve API Integration for Clip Assassin
Handles timeline operations and clip cutting
"""

import sys
from time_parser import parse_timecodes, format_seconds


class ResolveConnection:
    """Handles connection to DaVinci Resolve"""

    def __init__(self):
        self.resolve = None
        self.project = None
        self.media_pool = None
        self.project_manager = None

    def connect(self):
        """
        Establish connection to DaVinci Resolve

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Import DaVinci Resolve script module
            try:
                import DaVinciResolveScript as dvr
            except ImportError:
                return False, "DaVinci Resolve Python API not found. Make sure Resolve is installed."

            # Get Resolve instance
            self.resolve = dvr.scriptapp("Resolve")
            if not self.resolve:
                return False, "Could not connect to DaVinci Resolve. Make sure Resolve is running."

            # Get project manager
            self.project_manager = self.resolve.GetProjectManager()
            if not self.project_manager:
                return False, "Could not access Project Manager."

            # Get current project
            self.project = self.project_manager.GetCurrentProject()
            if not self.project:
                return False, "No project is open. Please open a project in Resolve."

            # Get media pool
            self.media_pool = self.project.GetMediaPool()
            if not self.media_pool:
                return False, "Could not access Media Pool."

            return True, f"Connected to project: {self.project.GetName()}"

        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def get_first_video_clip(self):
        """
        Find the first video clip in the media pool

        Returns:
            MediaPoolItem or None
        """
        if not self.media_pool:
            return None

        root_folder = self.media_pool.GetRootFolder()
        return self._find_video_clip_recursive(root_folder)

    def _find_video_clip_recursive(self, folder):
        """Recursively search for video clip in folders"""
        # Check clips in current folder
        clips = folder.GetClipList()
        for clip in clips:
            # Check if it's a video clip (has video track)
            clip_property = clip.GetClipProperty()
            if clip_property and clip_property.get("Video Codec"):
                return clip

        # Search subfolders
        subfolders = folder.GetSubFolderList()
        for subfolder in subfolders:
            found = self._find_video_clip_recursive(subfolder)
            if found:
                return found

        return None

    def cut_video(self, timecodes_text, source_clip=None):
        """
        Create a new timeline with only the specified time ranges

        Args:
            timecodes_text: Multi-line string with time ranges
            source_clip: MediaPoolItem to use (if None, uses first video clip)

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Parse time ranges
            ranges, errors = parse_timecodes(timecodes_text)

            if not ranges:
                error_msg = "No valid time ranges found."
                if errors:
                    error_msg += "\n\nErrors:\n" + "\n".join(errors)
                return False, error_msg

            # Get source clip
            if not source_clip:
                source_clip = self.get_first_video_clip()

            if not source_clip:
                return False, "No video clip found in Media Pool. Please import a video first."

            clip_name = source_clip.GetName()

            # Get clip properties
            clip_property = source_clip.GetClipProperty()
            fps = float(clip_property.get("FPS", 30))
            duration_frames = int(clip_property.get("Frames", 0))
            duration_seconds = duration_frames / fps

            # Validate ranges against clip duration
            invalid_ranges = []
            for i, (start, end) in enumerate(ranges):
                if end > duration_seconds:
                    invalid_ranges.append(f"Range {i+1}: {format_seconds(start)}-{format_seconds(end)} exceeds clip duration ({format_seconds(duration_seconds)})")

            if invalid_ranges:
                return False, "Some ranges exceed clip duration:\n" + "\n".join(invalid_ranges)

            # Create new timeline
            timeline_name = f"Assassinated - {clip_name}"

            # Check if timeline with this name already exists
            existing_count = 1
            original_name = timeline_name
            while self._timeline_exists(timeline_name):
                existing_count += 1
                timeline_name = f"{original_name} ({existing_count})"

            # Set current timeline (create empty one first)
            new_timeline = self.media_pool.CreateEmptyTimeline(timeline_name)

            if not new_timeline:
                return False, "Failed to create new timeline."

            # Set as current timeline
            self.project.SetCurrentTimeline(new_timeline)

            # Add clips at specified ranges
            track_position = 0  # in frames

            for start_sec, end_sec in ranges:
                # Convert seconds to frames
                in_frame = int(start_sec * fps)
                out_frame = int(end_sec * fps)

                # Create clip info for AppendToTimeline
                clip_info = {
                    "mediaPoolItem": source_clip,
                    "startFrame": in_frame,
                    "endFrame": out_frame,
                    "trackIndex": 1,
                    "recordFrame": track_position
                }

                # Add clip to timeline
                success = self.media_pool.AppendToTimeline([clip_info])

                if not success:
                    return False, f"Failed to add segment {format_seconds(start_sec)}-{format_seconds(end_sec)}"

                # Move position forward
                segment_duration = out_frame - in_frame
                track_position += segment_duration

            # Generate summary
            total_duration = sum(end - start for start, end in ranges)
            summary = f"✓ Mission accomplished!\n\n"
            summary += f"Timeline: {timeline_name}\n"
            summary += f"Segments: {len(ranges)}\n"
            summary += f"Total duration: {format_seconds(total_duration)}\n\n"
            summary += "Segments:\n"
            for i, (start, end) in enumerate(ranges, 1):
                summary += f"  {i}. {format_seconds(start)} - {format_seconds(end)} ({format_seconds(end-start)})\n"

            if errors:
                summary += f"\n⚠ Warnings:\n" + "\n".join(f"  - {e}" for e in errors)

            return True, summary

        except Exception as e:
            return False, f"Error during cutting: {str(e)}"

    def _timeline_exists(self, name):
        """Check if a timeline with given name exists"""
        timeline_count = self.project.GetTimelineCount()
        for i in range(1, timeline_count + 1):
            timeline = self.project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() == name:
                return True
        return False

    def get_project_info(self):
        """Get current project information"""
        if not self.project:
            return "No project connected"

        info = f"Project: {self.project.GetName()}\n"
        info += f"Timeline Count: {self.project.GetTimelineCount()}\n"

        current_timeline = self.project.GetCurrentTimeline()
        if current_timeline:
            info += f"Current Timeline: {current_timeline.GetName()}\n"

        return info


# Testing
if __name__ == "__main__":
    print("Testing Resolve Connection...")
    print("-" * 50)

    rc = ResolveConnection()
    success, msg = rc.connect()

    if success:
        print(f"✓ {msg}")
        print()
        print(rc.get_project_info())
        print()

        # Try to find first clip
        clip = rc.get_first_video_clip()
        if clip:
            print(f"✓ Found video clip: {clip.GetName()}")
            props = clip.GetClipProperty()
            print(f"  Duration: {props.get('Frames')} frames")
            print(f"  FPS: {props.get('FPS')}")
            print(f"  Resolution: {props.get('Resolution')}")
        else:
            print("✗ No video clip found in Media Pool")
    else:
        print(f"✗ {msg}")
