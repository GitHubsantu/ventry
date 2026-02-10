# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Collect all assets
assets_datas = []
if os.path.exists('assets'):
    for file in os.listdir('assets'):
        if file.endswith(('.ico', '.png', '.jpg', '.jpeg')):
            assets_datas.append((os.path.join('assets', file), 'assets'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=assets_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Ventry',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/ventry_icon.ico' if os.path.exists('assets/ventry_icon.ico') else None,
)
