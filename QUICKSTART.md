# 🚀 Quick Start Guide - Clip Assassin for DaVinci Resolve

Get started in under 2 minutes!

---

## Step 1: Prerequisites

✅ **DaVinci Resolve 18+** installed and running
✅ **A project open** in Resolve
✅ **At least one video clip** imported to Media Pool

---

## Step 2: Launch Clip Assassin

### Windows:
Double-click **`INSTALL.bat`**

Or open Command Prompt in this folder:
```bash
python clip_assassin.py
```

### macOS/Linux:
Open Terminal in this folder:
```bash
chmod +x install.sh
./install.sh
```

Or:
```bash
python3 clip_assassin.py
```

---

## Step 3: Enter Your Time Ranges

In the GUI window, enter your time ranges (one per line):

```
1m57-2m08
3m10-3m22
4m27-4m43
5m28-5m36
```

**Supported formats:**
- `1m57-2m08` (with 'm' for minutes)
- `1:57-2:08` (colon format)
- `0:02:25-0:02:45` (hours:minutes:seconds)
- `1h30m-1h31m` (with 'h' for hours)

---

## Step 4: Execute!

Click the big red button: **🗡️ RUN THE BLADES**

---

## Step 5: Check Resolve

A new timeline will be created in your Resolve project:
- Name: `Assassinated - [your clip name]`
- Contains: Only the segments you specified
- Duration: Sum of all your time ranges

**Done!**

---

## Example

**Original clip:** `my_video.mp4` (30 minutes long)

**Time ranges entered:**
```
1m57-2m08     (11 seconds)
3m10-3m22     (12 seconds)
4m27-4m43     (16 seconds)
```

**Result:**
New timeline: `Assassinated - my_video`
- Total duration: 39 seconds
- 3 segments seamlessly joined

---

## Troubleshooting

**"Could not connect to Resolve"**
- ✅ Make sure Resolve is running
- ✅ Make sure a project is open
- ✅ Click "🔄 Reconnect" button

**"Python not found"**
- Use DaVinci Resolve's bundled Python (see README.md)

**"No video clip found"**
- Import a video to Media Pool first

---

## Tips

✨ Mix and match time formats: `1m57-2:08` works!
✨ Copy/paste from spreadsheets or notes
✨ Works with any framerate
✨ Multiple timelines? Script auto-numbers them!

---

**Questions?** Check the full **README.md**

*Cuts. Without mercy.*
