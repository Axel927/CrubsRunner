# -*- mode: python ; coding: utf-8 -*-
# usage :
#  * Linux : python3 -m PyInstaller setup.spec

block_cipher = None

a = Analysis(
    ['src/CrubsRunner.py'],
    pathex=[],
    binaries=[],
    datas=[('icon/*.png','icon'), ('3d_files/*.stl', '3d_files'), ('src/*', 'src')],
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
    name='CrubsRunner',
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
    icon='icon/icon_app.ico'
)
