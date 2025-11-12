# ⚔️ CLIP ASSASSIN for DaVinci Resolve

**Version 1.0** - For DaVinci Resolve 18+ (Python API)

**Cuts. Without mercy.**

Automatically cut video clips based on time ranges in DaVinci Resolve. No manual cutting, no framerate headaches.

---

## ☕ Support

**Did I save you time?** Consider buying me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/Uhlovic)

**[buymeacoffee.com/Uhlovic](https://buymeacoffee.com/Uhlovic)**

---

## ✨ Features

- ✅ **Multiple time formats supported:**
  - `1m57-2m08` (minutes with "m")
  - `1:57-2:08` (colon format)
  - `0:02:25-0:02:45` (with hours)
  - `1h15m30-1h16m00` (with "h")
- ✅ **Works with ANY framerate** (29.97, 59.94, 25, 24, 30, 60 fps...)
- ✅ **Automatic timeline creation** from your clip
- ✅ **Precision cutting** based on time ranges
- ✅ **Keeps only selected parts** - everything else is eliminated
- ✅ **All dash types supported** (-, –, —) and spaces too
- ✅ **Dark theme GUI** matching Resolve's aesthetic
- ✅ **Real-time connection** to Resolve API

---

## 🚀 Installation

### System Requirements

#### For Windows (.exe version - Recommended):
- ✅ **DaVinci Resolve 18+** (Free or Studio)
- ✅ **Windows 7/8/10/11**
- ❌ **Python NOT required!**

#### For macOS/Linux (Python version):
- ✅ **DaVinci Resolve 18+** (Free or Studio)
- ✅ **Python 3.6+** (usually pre-installed)
- ✅ **macOS 10.12+ or Linux**

#### What's Included with Resolve:
- ✅ **DaVinci Resolve Python API** - Automatically installed in:
  - Windows: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\`
  - macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/`
  - Linux: `/opt/resolve/Developer/Scripting/`

### Quick Start - Windows (Easiest!)

1. **Download `Clip Assassin.exe`** from [Releases](https://github.com/Uhlovic/Clip_Assassin_Resolve/releases)
2. **Open DaVinci Resolve** with a project
3. **Double-click `Clip Assassin.exe`**
4. **Done!** No Python installation needed!

### Quick Start - macOS/Linux (Python Required)

If you're on macOS or Linux, or prefer to run from source:

### Step 1: Locate Python

DaVinci Resolve includes Python with the API. Find it here:

**Windows:**
```
C:\Program Files\Blackmagic Design\DaVinci Resolve\
```

**macOS:**
```
/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Frameworks/Python.framework/Versions/3.6/bin/python3
```

**Linux:**
```
/opt/resolve/libs/Fusion/
```

### Step 2: Setup Python Path

**Option A - Use system Python:**
If you have Python 3.6+ installed, the script should work directly.

**Option B - Use Resolve's Python:**
Run the script using Resolve's bundled Python (see paths above).

### Step 3: Install Clip Assassin

1. **Download** or clone this repository
2. **Extract** to a folder (e.g., `Clip_Assassin_Resolve`)
3. **Done!** No installation needed - it's a standalone Python script

---

## 💡 Usage

### Quick Start

1. **Open DaVinci Resolve**
2. **Open or create a project**
3. **Import a video clip** to your Media Pool
4. **Run Clip Assassin:**
   ```bash
   python clip_assassin.py
   ```
   Or on macOS with Resolve's Python:
   ```bash
   "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Frameworks/Python.framework/Versions/3.6/bin/python3" clip_assassin.py
   ```

5. **Enter time ranges** (one per line):
   ```
   1m57-2m08
   3m10-3m22
   4m27-4m43
   ```

6. **Click "🗡️ RUN THE BLADES"**

7. **New timeline created** with only your selected segments!

### GUI Overview

```
┌─────────────────────────────────────┐
│     ⚔️ CLIP ASSASSIN               │
│     Cuts. Without mercy.            │
│     for DaVinci Resolve             │
├─────────────────────────────────────┤
│ 1. Resolve Connection               │
│    ✓ Connected to project: My Edit  │
│    [🔄 Reconnect]                   │
├─────────────────────────────────────┤
│ 2. Mark Your Targets                │
│    1m57-2m08                        │
│    3m10-3m22                        │
│    4m27-4m43                        │
├─────────────────────────────────────┤
│ 3. Execute                          │
│    [🗡️ RUN THE BLADES]             │
├─────────────────────────────────────┤
│ Mission Status                      │
│  ✓ Timeline created successfully!   │
│    3 segments added                 │
└─────────────────────────────────────┘
```

---

## 📋 Supported Time Formats

All these formats work:

```
✅ 1m57-2m08           (minutes m seconds)
✅ 1:57-2:08           (colons)
✅ 0:02:25-0:02:45     (with hours)
✅ 1h15m30-1h16m00     (with "h")
✅ 1m57 - 2m08         (with spaces)
✅ 1m57–2m08           (en dash)
✅ 1m57—2m08           (em dash)
✅ 1m57-2:08           (mixed formats)
✅ 90-120              (just seconds)
```

**Format structure:** `start-end`
- **start** = beginning of range
- **end** = end of range
- **-** = any dash type (-, –, —)

---

## 🎬 How It Works

1. Script connects to DaVinci Resolve via Python API
2. Finds first video clip in your Media Pool
3. Parses your time ranges
4. Creates new empty timeline
5. Adds only the specified segments to the timeline
6. Result: Clean timeline with ONLY your selected parts

**Example:**

```
Original video: 30 minutes

Time ranges:
  1m57-2m08    (11 seconds)
  3m10-3m22    (12 seconds)
  4m27-4m43    (16 seconds)

Result timeline: "Assassinated - [clip name]"
  [Segment 1: 11s] [Segment 2: 12s] [Segment 3: 16s]
  Total: 39 seconds
```

---

## 🛠️ Troubleshooting

**"Could not connect to DaVinci Resolve"**
- Make sure Resolve is running
- Make sure a project is open
- Try clicking "🔄 Reconnect"

**"DaVinci Resolve Python API not found"**

⚠️ **Important:** The Python API is installed automatically with DaVinci Resolve in:
- **Windows:** `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules`
- **macOS:** `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules`
- **Linux:** `/opt/resolve/Developer/Scripting/Modules`

If you get this error:
1. **Check if Resolve is properly installed** - try opening Resolve first
2. **Verify the API folder exists** at the paths above
3. **If using .exe version:** This should work automatically
4. **If running Python scripts:** The script automatically adds these paths, but you can manually set:
   ```bash
   # Windows
   set RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting

   # macOS/Linux
   export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
   ```
5. **Reinstall Resolve** if the API folder is missing (it should install automatically)

**"No video clip found in Media Pool"**
- Import at least one video clip to Media Pool
- Make sure it's a video file (not just audio or image)

**Wrong timing / segments don't match**
- Double-check your time format: `start-end`
- Make sure times are within video duration
- Note: Frame precision depends on clip framerate

**Timeline already exists**
- Script automatically adds `(2)`, `(3)`, etc. to avoid conflicts
- Check your timeline list in Resolve

---

## 📂 Project Structure

```
Clip_Assassin_Resolve/
├── clip_assassin.py       # Main GUI application
├── resolve_core.py        # Resolve API integration
├── time_parser.py         # Time format parser
├── README.md              # This file
├── INSTALL.bat            # Windows quick launcher
└── install.sh             # macOS/Linux quick launcher
```

---

## 🔧 Advanced Usage

### Command Line Mode (No GUI)

You can also use the modules directly in your own scripts:

```python
from resolve_core import ResolveConnection

rc = ResolveConnection()
success, msg = rc.connect()

if success:
    timecodes = """
    1m57-2m08
    3m10-3m22
    4m27-4m43
    """
    success, result = rc.cut_video(timecodes)
    print(result)
```

### Testing Individual Modules

```bash
# Test time parser
python time_parser.py

# Test Resolve connection
python resolve_core.py
```

---

## 📝 Tips

- Mix formats freely: `1m57-2:08` works perfectly
- Spaces are automatically removed
- All dash types accepted (-, –, —)
- Copy time ranges from spreadsheets/notes directly
- Works with high framerates (59.94, 120fps) without issues
- Script validates ranges against clip duration
- Multiple timelines can be created (auto-numbered)

---

## ⚔️ About

**Clip Assassin for DaVinci Resolve** eliminates unwanted footage with surgical precision.

**Version:** 1.0
**Date:** 2025-11-12
**For:** DaVinci Resolve 18+
**API:** Python 3.6+
**License:** Free to use and modify

---

## 🔗 Related Projects

- [Clip Assassin for Premiere Pro](https://github.com/Uhlovic/Clip_Assassin) - CEP plugin version

---

## 📄 License

MIT License - Free to use and modify

---

*Cuts. Without mercy.*
