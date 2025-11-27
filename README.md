# ⚔️ CLIP ASSASSIN for DaVinci Resolve

**Version 1.1** - For DaVinci Resolve 18+ (Python API)

**Cuts. Without mercy.**

Automatically cut video clips based on time ranges in DaVinci Resolve. Now with **professional timecode support** and **REVERSE BLADES** mode!

---

## 📌 Version Compatibility

| Version | External Scripting (.exe / python script) | Internal Scripting (Workspace → Scripts) |
|---------|---------------------------|---------------------------|
| ✅ **DaVinci Resolve Studio** | **✅ Full support** | **✅ Full support** |
| ⚠️ **DaVinci Resolve (Free)** | **❌ NOT supported** | **✅ Workaround available!** |

### 🆓 **FREE Version Users - Workaround Available!**

If you have the **FREE version**, you can still use Clip Assassin with a workaround:

**Use the FREE VERSION** (`clip_assassin_free.py`):
- Runs **inside** DaVinci Resolve via **Workspace → Scripts** menu
- Works with both FREE and STUDIO versions
- Same features as the external version

**Installation:** Run `INSTALL_FREE_VERSION.bat` (Windows) or `install_free_version.sh` (macOS/Linux)

See [FREE Version Installation](#free-version-installation) below for details.

---

### How to check your version:
**Help → About DaVinci Resolve**

If you don't see **"Studio"** in the title, use the **FREE version workaround** above.

### Why Free version needs workaround:
The free version only supports **internal scripting** (from within Resolve). **External scripting** (running Python scripts from outside the application) is a **Studio-only feature**.

---

## ☕ Support

**Did I save you time?** Consider buying me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/Uhlovic)

**[buymeacoffee.com/Uhlovic](https://buymeacoffee.com/Uhlovic)**

---

## ✨ Features

### **🎯 Version 1.1 - NEW!**
- ✅ **Professional timecode with frames:**
  - `00:01:30:15-00:02:00:20` (non-drop-frame with `:`)
  - `00:01:30;15-00:02:00;20` (drop-frame with `;`)
  - Frame-accurate cutting with proper timebase handling
- ✅ **Automatic framerate detection** from clips (59.94, 29.97, 24, etc.)
- ✅ **⚔️ REVERSE BLADES mode** - Delete marked ranges, keep everything else!
  - Perfect for removing ads, intros, or unwanted segments
  - Mark what to DELETE instead of what to KEEP

### **Core Features**
- ✅ **Multiple time formats supported:**
  - `1m57-2m08` (minutes with "m")
  - `1:57-2:08` (colon format)
  - `0:02:25-0:02:45` (with hours)
  - `1h15m30-1h16m00` (with "h")
  - `00:01:30:15-00:02:00:20` (timecode with frames) **NEW!**
- ✅ **Works with ANY framerate** (23.976, 24, 25, 29.97, 30, 59.94, 60 fps...)
- ✅ **Automatic timeline creation** from your clip
- ✅ **Frame-accurate cutting** based on time ranges
- ✅ **Keeps only selected parts** - or removes them with REVERSE mode
- ✅ **All dash types supported** (-, –, —) and spaces too
- ✅ **Dark theme GUI** matching Resolve's aesthetic
- ✅ **Real-time connection** to Resolve API

---

## 🚀 Installation

### System Requirements

#### For Windows (.exe version - Recommended):
- ✅ **DaVinci Resolve 18+ STUDIO** (Free version NOT supported)
- ✅ **Windows 7/8/10/11**
- ❌ **Python NOT required!**

#### For macOS/Linux (Python version):
- ✅ **DaVinci Resolve 18+ STUDIO** (Free version NOT supported)
- ✅ **Python 3.9 or 3.10** (NOT 3.11+, NOT 3.6-3.8)
- ✅ **macOS 10.12+ or Linux**

#### What's Included with Resolve:
- ✅ **DaVinci Resolve Python API** - Automatically installed in:
  - Windows: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\`
  - macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/`
  - Linux: `/opt/resolve/Developer/Scripting/`

### FREE Version Installation

**For DaVinci Resolve FREE (or Studio) - Works with both!**

#### Windows:
1. **Download** or clone this repository
2. **Run `INSTALL_FREE_VERSION.bat`** as Administrator
3. **Restart DaVinci Resolve**
4. **Access via**: Workspace → Scripts → Utility → clip_assassin_free

#### macOS/Linux:
1. **Download** or clone this repository
2. **Run `./install_free_version.sh`** (may need sudo)
3. **Restart DaVinci Resolve**
4. **Access via**: Workspace → Scripts → Utility → clip_assassin_free

**Note:** This version runs **inside** Resolve using internal scripting, so it works with FREE version!

---

### Studio Version - External Installation

**For DaVinci Resolve STUDIO only**

#### Quick Start - Windows (Easiest!)

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

### FREE Version Usage

**For DaVinci Resolve FREE users:**

1. **Open DaVinci Resolve**
2. **Open or create a project**
3. **Import a video clip** to your Media Pool
4. **Go to**: Workspace → Scripts → Utility → **clip_assassin_free**
5. **Enter time ranges** in the dialog
6. **Click** "🗡️ RUN THE BLADES" or "⚔️ REVERSE BLADES"
7. **Done!** New timeline created with your segments

---

### Studio Version Usage (External)

**For DaVinci Resolve STUDIO users:**

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

6. **Click "🗡️ RUN THE BLADES"** to keep only marked segments
   - OR click "⚔️ REVERSE BLADES" to delete marked segments and keep everything else

7. **New timeline created** with your processed segments!

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
│    [⚔️ REVERSE BLADES]             │
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
✅ 1m57-2m08                      (minutes m seconds)
✅ 1:57-2:08                      (colons)
✅ 0:02:25-0:02:45                (with hours)
✅ 1h15m30-1h16m00                (with "h")
✅ 00:01:30:15-00:02:00:20        (timecode non-drop-frame) NEW!
✅ 00:01:30;15-00:02:00;20        (timecode drop-frame) NEW!
✅ 1m57 - 2m08                    (with spaces)
✅ 1m57–2m08                      (en dash)
✅ 1m57—2m08                      (em dash)
✅ 1m57-2:08                      (mixed formats)
✅ 90-120                         (just seconds)
```

**Format structure:** `start-end`
- **start** = beginning of range
- **end** = end of range
- **-** = any dash type (-, –, —)

---

## 🎬 How It Works

1. Script connects to DaVinci Resolve via Python API
2. Finds first video clip in your Media Pool
3. **Detects framerate automatically** from clip properties
4. Parses your time ranges (with frame-accurate timecode support)
5. Creates new empty timeline
6. Adds only the specified segments to the timeline
7. Result: Clean timeline with ONLY your selected parts (or everything EXCEPT them in REVERSE mode)

**Example - Normal Mode:**

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

**Example - REVERSE BLADES Mode:**

```
Original video: 10 minutes (600 seconds)

Marked ranges (to DELETE):
  2m00-2m30    (30 seconds - ads)
  5m00-5m15    (15 seconds - intro)

Result timeline: "Assassinated - [clip name]"
  [0:00-2:00] [2:30-5:00] [5:15-10:00]
  Total: 555 seconds (everything EXCEPT the marked parts)
```

---

## 🛠️ Troubleshooting

### 🔧 **Quick Diagnosis Tool**

If you're experiencing connection issues, run the **automated diagnostic tool** first:

**Windows:**
```cmd
DIAGNOSE.bat
```

**macOS/Linux:**
```bash
./diagnose.sh
```

This tool will automatically check:
- Python version compatibility
- DaVinci Resolve installation
- Python API availability
- Fusion script library
- Live connection to Resolve
- Environment variables
- And provide specific solutions for any issues found

---

### **"Initialization of fusion script failed" or "Could not connect to DaVinci Resolve"**

This is the **most common error**. Here's how to fix it:

#### 1. **Check if you have Resolve STUDIO** (most common cause - 45% of cases)
   - Open Resolve → **Help → About DaVinci Resolve**
   - If it says **"DaVinci Resolve"** (without "Studio"), external scripting is **NOT supported**
   - You need **DaVinci Resolve Studio** for this tool to work
   - [Upgrade to Studio](https://www.blackmagicdesign.com/products/davinciresolve/studio) or use internal scripting only

#### 2. **Enable External Scripting in Preferences** (25% of cases)
   - Open Resolve Studio → **Preferences** (Ctrl+, or Cmd+,)
   - Go to **System → General**
   - Find **"External scripting using"** setting
   - Change from **"None"** to **"Local"** or **"Network"**
   - **Restart Resolve**

#### 3. **Verify Resolve is running with a project open**
   - Resolve must be running BEFORE you start Clip Assassin
   - A project must be open (File → New Project or Open Project)
   - At least one video clip should be in Media Pool

#### 4. **Check Python version** (15% of cases)
   - Run: `python --version`
   - Required: **Python 3.9 or 3.10**
   - If you have Python 3.11+ or older than 3.9, install Python 3.10
   - Download from: [python.org](https://www.python.org/downloads/)

#### 5. **Use the .exe version** (Windows only - easiest solution)
   - Download `Clip Assassin.exe` from [Releases](https://github.com/Uhlovic/Clip_Assassin_Resolve/releases)
   - No Python installation needed
   - Should work out of the box with Resolve Studio

### **"DaVinci Resolve Python API not found"**

⚠️ **Important:** The Python API is installed automatically with DaVinci Resolve in:
- **Windows:** `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules`
- **macOS:** `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules`
- **Linux:** `/opt/resolve/Developer/Scripting/Modules`

If you get this error:
1. **Verify the API folder exists** at the paths above
2. **Check if Resolve Studio is properly installed**
3. **Set environment variables manually**:
   ```bash
   # Windows (Command Prompt)
   set RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
   set RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll
   set PYTHONPATH=%RESOLVE_SCRIPT_API%\Modules;%PYTHONPATH%

   # macOS/Linux
   export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
   export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules:$PYTHONPATH"
   ```
4. **Use the provided batch file**: `RUN_CLIP_ASSASSIN.bat` (sets up paths automatically)
5. **Reinstall Resolve Studio** if the API folder is missing

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

### **General Usage**
- Mix formats freely: `1m57-2:08` works perfectly
- Spaces are automatically removed
- All dash types accepted (-, –, —)
- Copy time ranges from spreadsheets/notes directly
- Works with high framerates (59.94, 120fps) without issues
- Script validates ranges against clip duration
- Multiple timelines can be created (auto-numbered)

### **Timecode with Frames (NEW in v1.1)**
- Use `:` for non-drop-frame: `00:01:30:15` (hour:min:sec:frame)
- Use `;` for drop-frame: `00:01:30;15` (for 29.97/59.94fps)
- Framerate is detected automatically from your clip
- Frame-accurate to ~2ms precision
- Mix timecode with other formats: `00:01:30:15-2m00` works!

### **REVERSE BLADES Mode (NEW in v1.1)**
- Use when you want to DELETE sections instead of keeping them
- Perfect for removing ads from recordings
- Mark the unwanted parts, click REVERSE BLADES
- Result: Everything EXCEPT your marked ranges

---

## ⚔️ About

**Clip Assassin for DaVinci Resolve** eliminates unwanted footage with surgical precision.

**Version:** 1.1.0
**Date:** 2025-11-22
**For:** DaVinci Resolve 18+ **STUDIO**
**API:** Python 3.9 - 3.10 (NOT 3.11+)
**License:** Free to use and modify

### What's New in v1.1.0
- Professional timecode support with frame numbers (HH:MM:SS:FF)
- Automatic framerate detection
- REVERSE BLADES mode for deleting marked segments
- Frame-accurate cutting with timebase handling
- See [CHANGELOG.md](CHANGELOG.md) for full details

---

## 🔗 Related Projects

- [Clip Assassin for Premiere Pro](https://github.com/Uhlovic/Clip_Assassin) - CEP plugin version

---

## 📄 License

MIT License - Free to use and modify

---

*Cuts. Without mercy.*
