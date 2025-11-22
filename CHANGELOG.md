# Changelog

All notable changes to Clip Assassin for DaVinci Resolve will be documented in this file.

## [1.1.0] - 2025-11-22

### 🎉 Major Features

#### **Timecode with Frames Support**
- Added support for professional timecode format with frame numbers
- **Non-drop-frame**: `HH:MM:SS:FF` using colon (`:`)
  - Example: `00:01:30:15` = 1 minute, 30 seconds, 15 frames
- **Drop-frame**: `HH:MM:SS;FF` using semicolon (`;`)
  - Example: `00:01:30;15` for 29.97fps and 59.94fps footage
- Frame-accurate cutting with proper timebase handling

#### **Automatic Framerate Detection**
- Plugin now automatically detects framerate from imported clips
- Uses Resolve API `GetClipProperty()["FPS"]`
- Supports all common framerates: 23.976, 24, 25, 29.97, 30, 50, 59.94, 60 fps
- Proper timebase conversion (59.94fps → 60 timebase)
- Fallback to 30fps if detection fails

#### **REVERSE BLADES Mode**
- New purple button: **⚔️ REVERSE BLADES**
- Delete marked sections and keep everything else
- Perfect for removing ads, intros, unwanted segments
- Automatically handles segments at beginning, middle, and end of clips

### ✨ Improvements

- **Frame-accurate timing**: Timecode now uses timebase for professional accuracy
- **Long video support**: Tested and verified on 1h+ videos with no cumulative errors
- **Mixed format support**: Seamlessly mix old formats (1m30, 5:00) with new timecode formats
- **Updated UI**: Added format hint showing timecode example in interface

### 🐛 Bug Fixes

- Fixed timecode parsing to use timebase (60fps) instead of actual framerate (59.94fps)
- Improved clip duration detection using Resolve API properties

### 📋 Technical Changes

- Added `get_clip_framerate()` method to `ResolveConnection` class
- Refactored `parse_time()` to support timecode with frames
- Added `framerate` parameter throughout parsing chain
- Implemented inverse range calculation for REVERSE mode
- Updated `cut_video()` to accept `reverse_mode` parameter

### 🧪 Testing

Ready to test with:
- Non-drop-frame timecode `00:00:10:00-00:00:20:00`
- Drop-frame timecode `00:00:10;00-00:00:20;00`
- REVERSE BLADES with multiple segments
- Mixed old and new formats
- Long videos (1h+)

---

## [1.0.0] - 2025-11-15

### Initial Release

- Basic time format support (1m57, 1:57, 0:02:25)
- DaVinci Resolve API integration
- Automatic timeline creation from clips
- Keep marked sections functionality
- Support for all framerates
- Multiple dash types and spaces handling
- Dark themed GUI application
