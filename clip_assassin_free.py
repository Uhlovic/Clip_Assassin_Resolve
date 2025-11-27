"""
Clip Assassin for DaVinci Resolve - FREE VERSION
Works with both FREE and STUDIO versions via internal scripting

INSTALLATION:
1. Copy this file to:
   Windows: %ProgramData%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\
   macOS: /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
   Linux: /opt/resolve/Fusion/Scripts/Utility/

2. Restart DaVinci Resolve

3. Run from: Workspace → Scripts → Utility → clip_assassin_free
"""

import sys

# Try to get Resolve instance using the workaround for FREE version
try:
    # This works in both FREE and STUDIO versions when run from within Resolve
    # Uses the undocumented 'app' variable available in the scripting environment
    resolve = app.GetResolve()
    if not resolve:
        print("ERROR: Could not get Resolve instance")
        print("Make sure you're running this from Workspace → Scripts menu")
        sys.exit(1)
except NameError:
    print("ERROR: 'app' variable not available")
    print("This script must be run from within DaVinci Resolve")
    print("Go to: Workspace → Scripts → Utility → clip_assassin_free")
    sys.exit(1)

# Import UI modules
try:
    from PySide6 import QtCore, QtWidgets, QtGui
    QT_VERSION = 6
except ImportError:
    try:
        from PySide2 import QtCore, QtWidgets, QtGui
        QT_VERSION = 2
    except ImportError:
        print("ERROR: PySide6 or PySide2 not found")
        print("DaVinci Resolve should include these by default")
        sys.exit(1)

# Import time parser from the main project
try:
    # Try to import from the same directory
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    from time_parser import parse_timecodes, format_seconds
except ImportError:
    # Fallback: inline simplified time parser
    import re

    def parse_timecodes(text, fps=30.0):
        """Simplified time parser"""
        ranges = []
        errors = []

        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Split by dash
            parts = re.split(r'[-–—]', line)
            if len(parts) != 2:
                errors.append(f"Invalid format: {line}")
                continue

            try:
                start_sec = parse_time(parts[0].strip(), fps)
                end_sec = parse_time(parts[1].strip(), fps)

                if start_sec >= end_sec:
                    errors.append(f"Invalid range: {line} (start >= end)")
                    continue

                ranges.append((start_sec, end_sec))
            except Exception as e:
                errors.append(f"Parse error in '{line}': {e}")

        return ranges, errors

    def parse_time(time_str, fps=30.0):
        """Parse various time formats to seconds"""
        time_str = time_str.strip()

        # Format: 1m57 or 2m08
        if 'm' in time_str:
            parts = time_str.replace('m', ':').split(':')
            if len(parts) == 2:
                mins = int(parts[0])
                secs = int(parts[1])
                return mins * 60 + secs

        # Format: 1:57 or 0:02:25
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                mins = int(parts[0])
                secs = int(parts[1])
                return mins * 60 + secs
            elif len(parts) == 3:
                hours = int(parts[0])
                mins = int(parts[1])
                secs = int(parts[2])
                return hours * 3600 + mins * 60 + secs
            elif len(parts) == 4:
                # Timecode with frames: HH:MM:SS:FF
                hours = int(parts[0])
                mins = int(parts[1])
                secs = int(parts[2])
                frames = int(parts[3])
                return hours * 3600 + mins * 60 + secs + frames / fps

        # Format: just seconds
        return float(time_str)

    def format_seconds(seconds):
        """Format seconds as MM:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"


class ClipAssassinFree(QtWidgets.QDialog):
    def __init__(self, resolve_instance, parent=None):
        super(ClipAssassinFree, self).__init__(parent)

        self.resolve = resolve_instance
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()

        if not self.project:
            QtWidgets.QMessageBox.critical(
                None,
                "No Project",
                "No project is open. Please open a project first."
            )
            raise RuntimeError("No project open")

        self.media_pool = self.project.GetMediaPool()

        self.setWindowTitle("Clip Assassin - FREE Version")
        self.setMinimumSize(550, 700)

        self.setup_ui()

    def setup_ui(self):
        """Create the UI"""
        layout = QtWidgets.QVBoxLayout()

        # Header
        header = QtWidgets.QLabel("⚔️ CLIP ASSASSIN")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff4444;")
        header.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(header)

        tagline = QtWidgets.QLabel("Cuts. Without mercy.")
        tagline.setStyleSheet("font-size: 10px; font-style: italic; color: #999999;")
        tagline.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(tagline)

        subtitle = QtWidgets.QLabel("FREE Version - Internal Scripting")
        subtitle.setStyleSheet("font-size: 9px; color: #44ff44;")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Project info
        proj_name = self.project.GetName()
        info_label = QtWidgets.QLabel(f"✓ Project: {proj_name}")
        info_label.setStyleSheet("color: #44ff44;")
        layout.addWidget(info_label)

        layout.addSpacing(10)

        # Instructions
        instructions = QtWidgets.QLabel("Enter time ranges (one per line):")
        instructions.setStyleSheet("font-weight: bold;")
        layout.addWidget(instructions)

        format_info = QtWidgets.QLabel("Formats: 1m57-2m08 / 1:57-2:08 / 00:01:30:15-00:02:00:20")
        format_info.setStyleSheet("font-size: 8px; color: #999999;")
        layout.addWidget(format_info)

        # Time ranges input
        self.timecodes_text = QtWidgets.QPlainTextEdit()
        self.timecodes_text.setPlaceholderText("1m57-2m08\n3m10-3m22\n4m27-4m43")
        self.timecodes_text.setMinimumHeight(150)
        layout.addWidget(self.timecodes_text)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()

        self.run_btn = QtWidgets.QPushButton("🗡️ RUN THE BLADES")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                font-weight: bold;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        self.run_btn.clicked.connect(lambda: self.execute_cutting(False))
        btn_layout.addWidget(self.run_btn)

        self.reverse_btn = QtWidgets.QPushButton("⚔️ REVERSE BLADES")
        self.reverse_btn.setStyleSheet("""
            QPushButton {
                background-color: #8800cc;
                color: white;
                font-weight: bold;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #aa00ff;
            }
        """)
        self.reverse_btn.clicked.connect(lambda: self.execute_cutting(True))
        btn_layout.addWidget(self.reverse_btn)

        layout.addLayout(btn_layout)

        reverse_help = QtWidgets.QLabel("REVERSE: Keep everything EXCEPT marked ranges")
        reverse_help.setStyleSheet("font-size: 7px; color: #999999;")
        reverse_help.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(reverse_help)

        layout.addSpacing(10)

        # Results
        results_label = QtWidgets.QLabel("Mission Status:")
        results_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(results_label)

        self.result_text = QtWidgets.QPlainTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(150)
        self.result_text.setPlaceholderText("Ready to execute...")
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def get_first_video_clip(self):
        """Find first video clip in media pool"""
        def search_folder(folder):
            clips = folder.GetClipList()
            for clip in clips:
                clip_property = clip.GetClipProperty()
                if clip_property and clip_property.get("Video Codec"):
                    return clip

            subfolders = folder.GetSubFolderList()
            for subfolder in subfolders:
                found = search_folder(subfolder)
                if found:
                    return found
            return None

        root_folder = self.media_pool.GetRootFolder()
        return search_folder(root_folder)

    def execute_cutting(self, reverse_mode=False):
        """Execute the cutting operation"""
        timecodes = self.timecodes_text.toPlainText().strip()

        if not timecodes:
            QtWidgets.QMessageBox.warning(self, "No Targets", "Please enter time ranges first.")
            return

        self.run_btn.setEnabled(False)
        self.reverse_btn.setEnabled(False)

        if reverse_mode:
            self.result_text.setPlainText("⚔️ REVERSE mode activated...\n🎯 Processing...\n")
        else:
            self.result_text.setPlainText("🎯 Locking on targets...\nProcessing...\n")

        QtCore.QCoreApplication.processEvents()

        try:
            success, message = self.cut_video(timecodes, reverse_mode)

            self.result_text.setPlainText(message)

            if success:
                QtWidgets.QMessageBox.information(self, "Mission Accomplished",
                    "Timeline created successfully!\nCheck your project timelines.")
            else:
                QtWidgets.QMessageBox.critical(self, "Mission Failed", message)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.result_text.setPlainText(error_msg)
            QtWidgets.QMessageBox.critical(self, "Error", error_msg)

        finally:
            self.run_btn.setEnabled(True)
            self.reverse_btn.setEnabled(True)

    def cut_video(self, timecodes_text, reverse_mode=False):
        """Main cutting logic"""
        try:
            # Get source clip
            source_clip = self.get_first_video_clip()
            if not source_clip:
                return False, "No video clip found in Media Pool. Please import a video first."

            clip_name = source_clip.GetName()

            # Get clip framerate
            clip_property = source_clip.GetClipProperty()
            fps = float(clip_property.get("FPS", 30))
            duration_frames = int(clip_property.get("Frames", 0))
            duration_seconds = duration_frames / fps

            # Parse time ranges
            ranges, errors = parse_timecodes(timecodes_text, fps)

            if not ranges:
                error_msg = "No valid time ranges found."
                if errors:
                    error_msg += "\n\nErrors:\n" + "\n".join(errors)
                return False, error_msg

            # Validate ranges
            invalid_ranges = []
            for i, (start, end) in enumerate(ranges):
                if end > duration_seconds:
                    invalid_ranges.append(
                        f"Range {i+1}: {format_seconds(start)}-{format_seconds(end)} "
                        f"exceeds clip duration ({format_seconds(duration_seconds)})"
                    )

            if invalid_ranges:
                return False, "Some ranges exceed clip duration:\n" + "\n".join(invalid_ranges)

            # REVERSE MODE: Convert to inverse ranges
            if reverse_mode:
                inverse_ranges = []
                last_end = 0

                for start, end in ranges:
                    if last_end < start:
                        inverse_ranges.append((last_end, start))
                    last_end = end

                if last_end < duration_seconds:
                    inverse_ranges.append((last_end, duration_seconds))

                ranges = inverse_ranges

                if not ranges:
                    return False, "REVERSE mode: No segments to keep. Marked ranges cover entire clip."

            # Create new timeline
            timeline_name = f"Assassinated - {clip_name}"

            # Check if timeline exists
            existing_count = 1
            original_name = timeline_name
            timeline_count = self.project.GetTimelineCount()

            while True:
                exists = False
                for i in range(1, timeline_count + 1):
                    timeline = self.project.GetTimelineByIndex(i)
                    if timeline and timeline.GetName() == timeline_name:
                        exists = True
                        break

                if not exists:
                    break

                existing_count += 1
                timeline_name = f"{original_name} ({existing_count})"

            # Create timeline
            new_timeline = self.media_pool.CreateEmptyTimeline(timeline_name)
            if not new_timeline:
                return False, "Failed to create new timeline."

            self.project.SetCurrentTimeline(new_timeline)

            # Add clips
            for start_sec, end_sec in ranges:
                in_frame = round(start_sec * fps)
                out_frame = round(end_sec * fps)

                clip_info = {
                    "mediaPoolItem": source_clip,
                    "startFrame": in_frame,
                    "endFrame": out_frame,
                }

                result = self.media_pool.AppendToTimeline([clip_info])
                if not result:
                    result = self.media_pool.AppendToTimeline([source_clip])

                if not result:
                    return False, f"Failed to add segment {format_seconds(start_sec)}-{format_seconds(end_sec)}"

            # Generate summary
            total_duration = sum(end - start for start, end in ranges)
            summary = f"✓ Mission accomplished!\n\n"
            summary += f"Timeline: {timeline_name}\n"
            summary += f"Clip: {clip_name}\n"
            summary += f"Framerate: {fps:.2f} fps\n"
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


# Main execution
if __name__ == "__main__":
    try:
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            app_instance = QtWidgets.QApplication(sys.argv)

        window = ClipAssassinFree(resolve)
        window.exec_()

    except Exception as e:
        print(f"ERROR: {e}")
        QtWidgets.QMessageBox.critical(None, "Error", str(e))
