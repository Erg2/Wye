# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['WyeMain.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Panda3D-1.10.14-x64\\etc\\Config.prc', 'etc'), ('C:\\Panda3D-1.10.14-x64\\etc\\Confauto.prc', 'etc'), ('C:\\Panda3D-1.10.14-x64\\bin\\libpandagl.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\CgGL.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3windisplay.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3openal_audio.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3assimp.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\bin\\libp3ptloader.dll', '.'), ('C:\\Panda3D-1.10.14-x64\\pandac\\PandaModules.py', 'pandac'), ('C:\\Panda3D-1.10.14-x64\\panda3d\\physics.pyd', 'panda3d'), ('WyeUILib.py', '.'), ('flyer_01.glb', '.'), ('WyeLib.py', '.'), ('TestLib.py', '.'), ('EditLib.py', '.'), ('base.py', '.'), ('sphere.py', '.'), ('*.wav', '.')],
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
    name='Wye_V0.3.exe',
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
