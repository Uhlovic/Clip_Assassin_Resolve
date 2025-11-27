@echo off
title Clip Assassin - FREE Version Installer
color 0F

echo.
echo ======================================================================
echo   CLIP ASSASSIN - FREE VERSION INSTALLER
echo ======================================================================
echo.
echo This will install Clip Assassin for DaVinci Resolve FREE version
echo (also works with STUDIO version)
echo.
echo The script will be installed to:
echo %ProgramData%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\
echo.
pause

set "DEST_DIR=%ProgramData%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility"

REM Check if destination directory exists
if not exist "%DEST_DIR%" (
    echo.
    echo ERROR: Destination directory not found!
    echo %DEST_DIR%
    echo.
    echo Make sure DaVinci Resolve is installed.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing files...
echo.

REM Copy main script
copy /Y "clip_assassin_free.py" "%DEST_DIR%\clip_assassin_free.py"
if errorlevel 1 (
    echo ERROR: Failed to copy clip_assassin_free.py
    echo You may need to run this as Administrator
    pause
    exit /b 1
)
echo [OK] Copied clip_assassin_free.py

REM Copy time parser (optional, has fallback)
copy /Y "time_parser.py" "%DEST_DIR%\time_parser.py" 2>nul
if errorlevel 1 (
    echo [!] Could not copy time_parser.py (using built-in fallback)
) else (
    echo [OK] Copied time_parser.py
)

echo.
echo ======================================================================
echo   INSTALLATION COMPLETE!
echo ======================================================================
echo.
echo To use Clip Assassin FREE version:
echo.
echo 1. Open DaVinci Resolve (FREE or STUDIO)
echo 2. Open a project
echo 3. Import a video clip to Media Pool
echo 4. Go to: Workspace -^> Scripts -^> Utility -^> clip_assassin_free
echo.
echo If the script doesn't appear, restart DaVinci Resolve.
echo.
pause
