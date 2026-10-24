# -*- mode: python ; coding: utf-8 -*-
import os
import esptool

ESPTOOL_TARGETS = os.path.join(os.path.dirname(esptool.__file__), 'targets')


a = Analysis(
    ['updater.py'],
    pathex=[],
    binaries=[],
    datas=[(ESPTOOL_TARGETS, 'esptool\\targets'), ('updater.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['updater.ico'],
)
