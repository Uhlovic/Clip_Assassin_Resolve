@echo off
echo ========================================
echo   CLIP ASSASSIN - DaVinci Resolve
echo   Cuts. Without mercy.
echo ========================================
echo.

REM Try to find Python
where python >nul 2>&1
if %errorLevel% equ 0 (
    echo Python found! Starting Clip Assassin...
    echo.
    python clip_assassin.py
) else (
    echo Python not found in PATH.
    echo.
    echo Please install Python 3.6+ or use DaVinci Resolve's Python:
    echo.
    echo Windows path example:
    echo "C:\Program Files\Blackmagic Design\DaVinci Resolve\python.exe" clip_assassin.py
    echo.
    pause
)
