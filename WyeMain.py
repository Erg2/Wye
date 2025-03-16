# Building up direct compiled version of Wye

# consolidating compiled code into one block

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d
from importlib.machinery import SourceFileLoader    # to load libList from files
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
#from pandac.PandaModules import *
#from panda3d.core import loadPrcFileData
import traceback


from WyeCore import WyeCore
from Wye import Wye
import sys, os

libLoadList = ["WyeLib.py", "WyeUILib.py", "WyeUIUtilsLib.py", "Wye3dObjsLib.py"] # list of lib files to load on start.  libList on cmd line added to it
startObjList = []           # list of lib objs from command line to load on start


############# run the world
#
# Note: Wye's static class structure means we need this instantiated class
# to derive from ShowBase to access all the Panda3d runstime stuff
class WorldRunner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)     # Init Panda3d
        taskMgr.add(WyeCore.World.worldRun)
        WyeCore.base = self      # world needs this to do panda3d stuff

        # TURN OFF DEFAULT CAMERA CONTROLS
        WyeCore.base.disableMouse() # turn off default mouse move

        #props = WindowProperties()
        #props.setTitle("Wye V" + version)
        #WyeCore.base.win.requestProperties(props)


# main program, set up and run the world

#print("Start")
loadPrcFileData('', 'win-size 1200 800')           # set size of window
loadPrcFileData('', 'show-frame-rate-meter #t')    # turn on frame rate display
loadPrcFileData('', 'window-title Wye V'+Wye.version)


# if the user supplied a list of libList and or start objs
if len(sys.argv) > 1:
    for ix in range(1, len(sys.argv), 2):
        sw = sys.argv[ix]
        val = sys.argv[ix+1]
        match sw:
            case "-l":
                #print("cmd line lib ", val)
                libLoadList.append(val)
            case "-o":
                #print("cmd line start obj ", val)
                startObjList.append(val)

# No parameters, load default libs and start default objs
else:
    libLoadList.extend(["TestLib.py", "EditLib.py"])
    startObjList = []

# import libraries
for libFile in libLoadList:
    #print("Load lib '", libFile, "'")
    libName = libFile.split(".")[0]


    #path = libFile
    path = WyeCore.Utils.resourcePath(libFile)[2:]
    #print("Load library '" + path + "'")
    try:
        libModule = SourceFileLoader(libName, path).load_module()
        # print("libModule ", libModule)
        libClass = getattr(libModule, libName)
        #print("add libClass", libClass, " to libList")
        WyeCore.World.libList.append(libClass)
        #print("Loaded library ", libName, " from file ", path, " into lib class ", libClass)
    except:
    #    pass    # if fail to load module, keep going
        print("Failed to load class ", libName, " From file ", path)
        ex = sys.exception()
        traceback.print_exception(ex)

print("Known libraries:", WyeCore.World.libList)

# load starting objects
WyeCore.World.startObjs.extend(startObjList)

#print("Loaded libList:", WyeCore.World.libList)
#print("start objs:", WyeCore.World.startObjs)

pandaRunner = WorldRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

