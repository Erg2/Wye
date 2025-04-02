# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['WyeMain.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Panda3D-1.10.14-x64\\etc\\Config.prc', 'etc'), ('C:\\Panda3D-1.10.14-x64\\etc\\Confauto.prc', 'etc'), ('C:\\Panda3D-1.10.14-x64\\bin\\libpandagl.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\CgGL.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3windisplay.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3openal_audio.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3assimp.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3ptloader.dll', '.'), ('WyeUILib.py', '.'), ('flyer_01.glb', '.'), ('TestLib.py', '.'), ('TestLib2.py', '.'), ('*.wav', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Wye_V0.1.exe',
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
)
