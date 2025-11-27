"""
DaVinci Resolve Connection Diagnostic Tool
Tests all possible causes of connection failures and provides solutions
"""

import sys
import os
import platform

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    import codecs
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
    # Fallback for older Python versions
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("  CLIP ASSASSIN - DaVinci Resolve Connection Diagnostics")
print("=" * 70)
print()

# Track issues found
issues_found = []
warnings_found = []
success_checks = []

# ============================================================================
# TEST 1: Python Version
# ============================================================================
print("[1/8] Checking Python version...")
py_version = sys.version_info
py_version_str = f"{py_version.major}.{py_version.minor}.{py_version.micro}"
print(f"      Python version: {py_version_str}")

if py_version.major == 3 and 9 <= py_version.minor <= 10:
    print("      [OK] Python version is compatible (3.9 or 3.10)")
    success_checks.append("Python version is compatible")
elif py_version.major == 3 and py_version.minor == 11:
    print("      [!] WARNING: Python 3.11 may have compatibility issues")
    print("      Recommendation: Install Python 3.10")
    warnings_found.append("Python 3.11 detected - may cause issues")
elif py_version.major == 3 and py_version.minor >= 12:
    print("      [X] PROBLEM: Python 3.12+ is NOT supported by Resolve 18/19/20")
    print("      Solution: Install Python 3.10 from https://www.python.org/downloads/")
    issues_found.append("Python version too new (3.12+)")
elif py_version.major == 3 and py_version.minor < 9:
    print("      [!] WARNING: Python version is older than recommended")
    print("      Recommendation: Install Python 3.10")
    warnings_found.append("Python version older than 3.9")
else:
    print("      [X] PROBLEM: Incompatible Python version")
    issues_found.append(f"Incompatible Python version: {py_version_str}")

print()

# ============================================================================
# TEST 2: Operating System
# ============================================================================
print("[2/8] Checking operating system...")
os_name = platform.system()
print(f"      OS: {os_name} ({platform.platform()})")

if os_name == "Windows":
    api_path = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
    lib_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    resolve_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve"
elif os_name == "Darwin":  # macOS
    api_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
    lib_path = None  # Not used on macOS
    resolve_path = "/Applications/DaVinci Resolve"
elif os_name == "Linux":
    api_path = "/opt/resolve/Developer/Scripting/Modules"
    lib_path = None
    resolve_path = "/opt/resolve"
else:
    print(f"      [X] PROBLEM: Unsupported OS: {os_name}")
    issues_found.append(f"Unsupported operating system: {os_name}")
    api_path = None
    lib_path = None
    resolve_path = None

print(f"      [OK] Detected {os_name}")
print()

# ============================================================================
# TEST 3: Resolve Installation
# ============================================================================
print("[3/8] Checking DaVinci Resolve installation...")
if resolve_path and os.path.exists(resolve_path):
    print(f"      [OK] Resolve found at: {resolve_path}")
    success_checks.append("DaVinci Resolve is installed")
else:
    print(f"      [X] PROBLEM: Resolve NOT found at: {resolve_path}")
    print("      Solution: Install DaVinci Resolve Studio 18/19/20")
    issues_found.append("DaVinci Resolve not installed or not found")
print()

# ============================================================================
# TEST 4: Python API Path
# ============================================================================
print("[4/8] Checking Python API installation...")
if api_path and os.path.exists(api_path):
    print(f"      [OK] API found at: {api_path}")
    success_checks.append("Python API is installed")

    # Check if path is in sys.path
    if api_path in sys.path:
        print(f"      [OK] API path is in Python sys.path")
    else:
        print(f"      [!]  WARNING: API path NOT in sys.path (will be added automatically)")
        print(f"      Adding to sys.path now...")
        sys.path.append(api_path)
else:
    print(f"      [X] PROBLEM: API NOT found at: {api_path}")
    print("      Solution: Reinstall DaVinci Resolve Studio")
    issues_found.append("Python API not found - Resolve may not be properly installed")
print()

# ============================================================================
# TEST 5: Fusion Script Library (Windows only)
# ============================================================================
if os_name == "Windows":
    print("[5/8] Checking Fusion Script Library...")
    if lib_path and os.path.exists(lib_path):
        print(f"      [OK] fusionscript.dll found at: {lib_path}")
        success_checks.append("Fusion script library found")
    else:
        print(f"      [X] PROBLEM: fusionscript.dll NOT found at: {lib_path}")
        print("      Solution: Reinstall DaVinci Resolve Studio")
        issues_found.append("fusionscript.dll not found")
    print()
else:
    print("[5/8] Checking Fusion Script Library...")
    print(f"      [i]  Not applicable on {os_name}")
    print()

# ============================================================================
# TEST 6: Import DaVinciResolveScript
# ============================================================================
print("[6/8] Testing DaVinciResolveScript import...")
try:
    import DaVinciResolveScript as dvr
    print("      [OK] DaVinciResolveScript imported successfully")
    success_checks.append("DaVinciResolveScript module loads correctly")
except ImportError as e:
    print(f"      [X] PROBLEM: Cannot import DaVinciResolveScript")
    print(f"      Error: {e}")
    print("      Solutions:")
    print("         1. Make sure DaVinci Resolve Studio is installed")
    print("         2. Set RESOLVE_SCRIPT_API environment variable")
    print(f"         3. Add to PYTHONPATH: {api_path}")
    issues_found.append(f"Cannot import DaVinciResolveScript: {e}")
    dvr = None
print()

# ============================================================================
# TEST 7: Connect to Resolve
# ============================================================================
print("[7/8] Testing connection to DaVinci Resolve...")
print("      NOTE: Resolve MUST be running with a project open!")
print()

if dvr:
    try:
        resolve = dvr.scriptapp("Resolve")
        if resolve:
            print("      [OK] Connected to Resolve successfully!")
            success_checks.append("Connection to Resolve established")

            # Get version info
            try:
                pm = resolve.GetProjectManager()
                if pm:
                    proj = pm.GetCurrentProject()
                    if proj:
                        proj_name = proj.GetName()
                        print(f"      [OK] Current project: {proj_name}")
                        success_checks.append(f"Project '{proj_name}' is open")

                        # Check media pool
                        media_pool = proj.GetMediaPool()
                        if media_pool:
                            root_folder = media_pool.GetRootFolder()
                            clips = root_folder.GetClipList()
                            if clips and len(clips) > 0:
                                print(f"      [OK] Found {len(clips)} clip(s) in Media Pool")
                                success_checks.append(f"{len(clips)} clips in Media Pool")
                            else:
                                print(f"      [!]  WARNING: No clips in Media Pool")
                                warnings_found.append("No clips in Media Pool - import a video first")
                    else:
                        print("      [!]  WARNING: No project is open")
                        print("      Solution: Open or create a project in Resolve")
                        warnings_found.append("No project open in Resolve")
            except Exception as e:
                print(f"      [!]  WARNING: Could not get project info: {e}")

        else:
            print("      [X] PROBLEM: Could not connect to Resolve")
            print("      Possible causes:")
            print("         1. Resolve is not running")
            print("         2. No project is open")
            print("         3. External scripting is disabled")
            print("         4. Using Free version instead of Studio")
            print()
            print("      Solutions:")
            print("         1. Launch DaVinci Resolve Studio")
            print("         2. Open or create a project")
            print("         3. Enable external scripting:")
            print("            Preferences → System → General")
            print("            'External scripting using' → set to 'Local'")
            print("         4. Restart Resolve after changing preferences")
            issues_found.append("Cannot connect to Resolve - check if running with project open")
    except Exception as e:
        print(f"      [X] PROBLEM: Connection error: {e}")
        print("      This usually means:")
        print("         - Resolve is not running")
        print("         - External scripting is disabled")
        print("         - You're using the Free version (Studio required)")
        issues_found.append(f"Connection exception: {e}")
else:
    print("      [>>]  Skipped (DaVinciResolveScript import failed)")
print()

# ============================================================================
# TEST 8: Environment Variables
# ============================================================================
print("[8/8] Checking environment variables...")
resolve_api = os.environ.get("RESOLVE_SCRIPT_API")
resolve_lib = os.environ.get("RESOLVE_SCRIPT_LIB")
pythonpath = os.environ.get("PYTHONPATH")

if resolve_api:
    print(f"      [OK] RESOLVE_SCRIPT_API = {resolve_api}")
else:
    print(f"      [i]  RESOLVE_SCRIPT_API not set (optional)")

if os_name == "Windows":
    if resolve_lib:
        print(f"      [OK] RESOLVE_SCRIPT_LIB = {resolve_lib}")
    else:
        print(f"      [!]  RESOLVE_SCRIPT_LIB not set")
        print(f"      Recommended: set RESOLVE_SCRIPT_LIB={lib_path}")
        warnings_found.append("RESOLVE_SCRIPT_LIB not set")

if pythonpath:
    print(f"      [i]  PYTHONPATH = {pythonpath}")
else:
    print(f"      [i]  PYTHONPATH not set (will use default)")

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 70)
print("  DIAGNOSTIC SUMMARY")
print("=" * 70)
print()

if success_checks:
    print(f"PASSING CHECKS ({len(success_checks)}):")
    for check in success_checks:
        print(f"   [OK] {check}")
    print()

if warnings_found:
    print(f"WARNINGS ({len(warnings_found)}):")
    for warning in warnings_found:
        print(f"   [!] {warning}")
    print()

if issues_found:
    print(f"CRITICAL ISSUES ({len(issues_found)}):")
    for issue in issues_found:
        print(f"   [X] {issue}")
    print()
    print("=" * 70)
    print("  RECOMMENDED ACTIONS:")
    print("=" * 70)
    print()

    # Provide specific recommendations based on issues
    if any("Python version" in issue for issue in issues_found):
        print("1. Install Python 3.10:")
        print("   Download from: https://www.python.org/downloads/")
        print("   During installation, check 'Add Python to PATH'")
        print()

    if any("API not found" in issue or "Resolve not installed" in issue for issue in issues_found):
        print("2. Reinstall DaVinci Resolve Studio:")
        print("   Download from: https://www.blackmagicdesign.com/products/davinciresolve")
        print("   Make sure to install STUDIO version, not Free")
        print()

    if any("Cannot connect" in issue or "Connection" in issue for issue in issues_found):
        print("3. Enable External Scripting in Resolve:")
        print("   a. Launch DaVinci Resolve Studio")
        print("   b. Open Preferences (Ctrl+, or Cmd+,)")
        print("   c. Go to: System → General")
        print("   d. Find 'External scripting using'")
        print("   e. Change from 'None' to 'Local'")
        print("   f. Restart Resolve")
        print()
        print("4. Verify Resolve Studio version:")
        print("   Help → About DaVinci Resolve")
        print("   Should say 'DaVinci Resolve Studio' (not just 'DaVinci Resolve')")
        print()

    if any("fusionscript.dll" in issue for issue in issues_found):
        print("5. Check Resolve installation path:")
        print(f"   Expected: {lib_path}")
        print("   If Resolve is installed elsewhere, update the path")
        print()

else:
    print("SUCCESS! ALL CRITICAL CHECKS PASSED!")
    print()
    if warnings_found:
        print("However, there are some warnings above that you may want to address.")
        print()
    else:
        print("Your system is properly configured for Clip Assassin!")
        print("If you still experience issues:")
        print("  1. Make sure Resolve is running")
        print("  2. Open a project in Resolve")
        print("  3. Import at least one video clip")
        print("  4. Then launch Clip Assassin")
        print()

print("=" * 70)
print()
print("For more help, visit:")
print("https://github.com/Uhlovic/Clip_Assassin_Resolve/issues")
print()
