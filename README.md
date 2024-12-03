# Wye
Wye in-3d character implementation language
(currently only works on monitor, not in HMD)

# Engine requires at least one library and start object on command line.  Ex:
python WyeMain.py -l TestLib.py -o TestLib.TestLib.testObj -o TestLib.TestLib.testObj2

# Two attempts to build, 2nd mostly works

# Pand3D dist - doesn't build
python setup.py build_apps
# PyInstaller dist - works
pyinstaller -F --onefile --windowed  --add-data 'C:\Panda3D-1.10.14-x64\etc\Config.prc;etc'  --add-data 'C:\Panda3D-1.10.14-x64\etc\Confauto.prc;etc' --add-data 'C:\Panda3D-1.10.14-x64\bin\libpandagl.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\CgGL.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3windisplay.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3openal_audio.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3assimp.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3ptloader.dll;.' --add-data 'WyeUI.py;.'  --add-data 'flyer_01.glb;.' --add-data 'TestLib.py;.' --add-data 'TestLib2.py;.' --add-data '*.wav;.' WyeMain.py --name "Wye_V0.3.exe"
