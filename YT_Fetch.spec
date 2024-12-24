# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],  
    pathex=['.'],  
    binaries=[],
    datas=[
        ('config.py', '.'),       
        ('downloader.py', '.'),   
        ('settings.py', '.'),     
        ('utils.py', '.'),        
        ('icon.ico', '.'), 
        ('data/*', 'data/'),
    ],
    hiddenimports=[
        'yt_dlp', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'
    ],
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
    name='YT_Fetch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Disable console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # App icon
)

app = BUNDLE(
    exe,
    name='YT Fetch.app',
    icon='icon.icns',  
    bundle_identifier='com.williams.ytfetch',
)

