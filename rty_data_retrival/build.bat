@echo off
echo Building FPY Dashboard executable...
echo.

REM Activate virtual environment
call rty1_env\Scripts\activate.bat

REM Set the hook path
set PYINSTALLER_HOOKS_PATH=%CD%

REM Run the build script
python build_exe.py

echo.
echo Build process completed!
pause