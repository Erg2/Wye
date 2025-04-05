# Wye
Wye in-3d character implementation language
(currently only works on monitor, not in HMD)

# prebuilt exe
The prebuilt Windows .exe runs the default library TestLib.py.  
User defined libraries are in the WyeUserLibraries subdirectory in the same location as the .EXE
See the example library zip file

# Running from Python
python WyeMain.py
WyeMain accepts user defined libraries on the command line as: -l yourlib.py
If there is a library on the command line, the default TestLib.py will not be loaded.

# PyInstaller distribution build
Tested for Windows 11

pyinstaller Wye_V0.9.exe.spec

pyinstaller -F --onefile --windowed --add-data 'C:\Panda3D-1.10.14-x64\etc\Config.prc;etc' --add-data 'C:\Panda3D-1.10.14-x64\etc\Confauto.prc;etc' --add-data 'C:\Panda3D-1.10.14-x64\bin\libpandagl.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\CgGL.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3windisplay.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3openal_audio.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3assimp.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\bin\libp3ptloader.dll;.' --add-data 'C:\Panda3D-1.10.14-x64\pandac\PandaModules.py;pandac' --add-data 'C:\Panda3D-1.10.14-x64\panda3d\physics.pyd;panda3d' --add-data 'WyeUILib.py;.'  --add-data 'WyeUIUtilsLib.py;.'  --add-data 'Wye3dObjsLib.py;.'  --add-data 'flyer_01.glb;.' --add-data 'fish.glb;.' --add-data 'fish1a.glb;.' --add-data 'WyeLib.py;.' --add-data 'TestLib.py;.' --add-data 'base.py;.' --add-data 'sphere.py;.' --add-data '*.wav;.' WyeMain.py --name "Wye_V0.9.1.exe"