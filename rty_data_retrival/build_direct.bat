@echo off
echo Building FPY Dashboard executable...
echo.

REM Activate virtual environment
call rty1_env\Scripts\activate.bat

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
for %%f in (*.spec) do del %%f

echo Cleaned previous builds.

REM Build the executable
echo Building executable...
py -3.11 -m PyInstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --hidden-import=flask --hidden-import=flask_login --hidden-import=flask_login.utils --hidden-import=flask_login.login_manager --hidden-import=flask_login.mixins --hidden-import=flask_login.signals --hidden-import=flask_login.views --hidden-import=flask_sqlalchemy --hidden-import=werkzeug --hidden-import=jinja2 --hidden-import=markupsafe --hidden-import=click --hidden-import=itsdangerous --hidden-import=pandas --hidden-import=numpy --hidden-import=openpyxl --hidden-import=requests --hidden-import=apscheduler --hidden-import=sqlalchemy --hidden-import=chartjs --hidden-import=bootstrap --hidden-import=datatables --hidden-import=pywin32_ctypes --hidden-import=win32api --hidden-import=win32con --hidden-import=win32file --hidden-import=win32com --hidden-import=xhtml2pdf --hidden-import=reportlab --hidden-import=reportlab.graphics.barcode.code128 --hidden-import=reportlab.graphics.barcode.code39 --hidden-import=reportlab.graphics.barcode.code93 --hidden-import=reportlab.graphics.barcode.qr --hidden-import=reportlab.graphics.barcode.usps --hidden-import=reportlab.graphics.barcode.usps4s --hidden-import=reportlab.graphics.barcode.eanbc --hidden-import=reportlab.graphics.barcode.i2of5 --hidden-import=reportlab.graphics.barcode.ecc200datamatrix --hidden-import=pywebview.platforms.winforms --hidden-import=utils.api --hidden-import=utils.helpers --hidden-import=routes.auth --hidden-import=routes.dashboard --hidden-import=routes.api --hidden-import=extensions --hidden-import=models --hidden-import=config --collect-all flask_login --collect-all flask_sqlalchemy --collect-all pandas --collect-all numpy --collect-all openpyxl --collect-all requests --collect-all apscheduler --collect-all sqlalchemy --name "FPY_Dashboard" app.py

echo.
echo Build process completed!
echo Executable location: %CD%\dist\FPY_Dashboard.exe
pause