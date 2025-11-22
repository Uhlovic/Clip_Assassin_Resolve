@echo off
echo ========================================
echo   CLIP ASSASSIN v1.1 - DaVinci Resolve
echo   Cuts. Without mercy.
echo ========================================
echo.

REM Set Python path to include Resolve API
set "RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
set "PYTHONPATH=%RESOLVE_SCRIPT_API%;%PYTHONPATH%"

echo Setting up Resolve API path...
echo Path: %RESOLVE_SCRIPT_API%
echo.

REM Check if Resolve is running
tasklist /FI "IMAGENAME eq Resolve.exe" 2>NUL | find /I /N "Resolve.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] DaVinci Resolve is running
    echo.
) else (
    echo [WARNING] DaVinci Resolve is NOT running!
    echo Please start Resolve with a project open first.
    echo.
    pause
    exit /b 1
)

REM Check for Python
where python >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Python found! Starting Clip Assassin...
    echo.
    python clip_assassin.py
) else (
    echo [ERROR] Python not found in PATH.
    echo.
    echo Please install Python 3.6+ from python.org
    echo.
    pause
)
