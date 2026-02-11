# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# PyInstaller runs the spec from the project root
project_root = Path.cwd()

# ---------------------------
# Bundle YOUR repo files
# ---------------------------
datas = [
    (str(project_root / "assets"), "assets"),
    (str(project_root / "titanium_data.json"), "."),
    (str(project_root / "app"), "app"),
]

# ---------------------------
# Collect PySide6 fully
# ---------------------------
pyside6 = collect_all("PySide6")

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=pyside6["binaries"],
    datas=datas + pyside6["datas"],
    hiddenimports=pyside6["hiddenimports"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Dashboard",
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

app = BUNDLE(
    exe,
    a.binaries,
    a.datas,
    name="Dashboard.app",
    bundle_identifier="com.nzc0der.dashboard",
)
