# Clip Assassin Resolve v1.1.0 - Frame-Perfect Edition

**Release Date:** November 22, 2025

---

## What's New

### Professional Timecode Support

Never worry about frame accuracy again! Version 1.1 brings full professional timecode support with frame numbers:

**Non-drop-frame timecode** (`:`):
```
00:01:30:15-00:02:00:20
```
Perfect for 24fps, 25fps, 30fps, and 60fps footage.

**Drop-frame timecode** (`;`):
```
00:01:30;15-00:02:00;20
```
Ideal for 23.976fps, 29.97fps, and 59.94fps footage.

**Frame-accurate cutting** with proper timebase handling - tested and verified on long-form content (1h+).

---

### REVERSE BLADES Mode

Introducing the new **⚔️ REVERSE BLADES** button!

Instead of keeping marked sections, **delete them and keep everything else**.

**Perfect for:**
- Removing ads from recordings
- Cutting out unwanted intros/outros
- Eliminating mistakes or dead air
- Cleaning up long interviews

**Example:**
```
Mark: 00:05:00-00:06:00 (ads)
      00:15:00-00:16:00 (ads)

Result: Everything EXCEPT those 2 minutes
```

---

### Automatic Framerate Detection

No more manual framerate configuration! The plugin now:
- Automatically detects framerate from your clips
- Handles all common framerates (23.976, 24, 25, 29.97, 30, 50, 59.94, 60 fps)
- Uses proper timebase conversion for professional accuracy
- Maintains frame-perfect accuracy even on 1+ hour videos

---

## Improvements

- **Frame-accurate timing**: Sub-frame precision (~2ms accuracy)
- **Long video support**: Tested on 1h+ footage with zero drift
- **Mixed format support**: Combine old and new formats in the same session
  ```
  1m30-2m00
  00:03:00:00-00:03:30:15
  5:00-5:30
  ```
- **Better error handling**: Clear messages for invalid inputs

---

## Installation

### Windows:
1. Download `Clip_Assassin_Resolve.exe`
2. Open DaVinci Resolve with a project
3. Double-click the exe
4. Done!

### macOS/Linux:
1. Download and extract the source files
2. Run: `python clip_assassin.py`
3. Make sure DaVinci Resolve is running

---

## Supported Formats

```
1m57-2m08                      (minutes + seconds)
1:57-2:08                      (colon format)
0:02:25-0:02:45                (with hours)
00:01:30:15-00:02:00:20        (timecode with frames - non-drop) NEW
00:01:30;15-00:02:00;20        (timecode with frames - drop-frame) NEW
Mix any formats together!
```

---

## Testing

Successfully tested with:
- 59.94fps footage (1h+ duration)
- Frame-accurate cuts (sub-frame precision)
- Drop-frame and non-drop-frame timecode
- Reverse mode with multiple segments
- Mixed format inputs
- Long video stability (no cumulative errors)

---

## Documentation

- **Full README**: See `README.md` for complete usage guide
- **Changelog**: See `CHANGELOG.md` for detailed technical changes

---

*Cuts. Without mercy.*

**Version:** 1.1.0
**Date:** 2025-11-22
**For:** DaVinci Resolve 18+
**License:** MIT - Free to use and modify
