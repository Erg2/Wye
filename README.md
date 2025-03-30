# Wye
Wye in-3d character implementation language
(currently only works on monitor, not in HMD)

# prebuilt exe
The prebuilt Windows .exe runs the default library TestLib.py.  
User defined libraries are in the UserLibraries subdirectory in the same location as the .EXE
See the example library zip file

# Running from Python
python WyeMain.py
WyeMain accepts user defined libraries on the command line as: -l yourlib.py
If there is a library on the command line, the default TestLib.py will not be loaded.

# PyInstaller distribution build
Tested for Windows 11

pyinstaller Wye_V0.9.exe.spec