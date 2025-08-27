# hook-flask_login.py
from PyInstaller.utils.hooks import collect_submodules

# Collect all submodules of flask_login
hiddenimports = collect_submodules('flask_login')