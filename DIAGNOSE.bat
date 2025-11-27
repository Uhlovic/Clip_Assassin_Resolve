@echo off
title Clip Assassin - Resolve Connection Diagnostics
color 0F

REM Set Resolve API paths (in case they're needed)
set "RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
set "RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
set "PYTHONPATH=%RESOLVE_SCRIPT_API%\Modules;%PYTHONPATH%"

echo.
echo Running diagnostics...
echo.

python diagnose_resolve.py

if errorlevel 1 (
    echo.
    echo ERROR: Python may not be installed or not in PATH
    echo Please install Python 3.10 from https://www.python.org/downloads/
    echo.
    pause
)
