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
import sys, os

version = "0.2"

libLoadList = ["WyeLib.py", "WyeUI.py"] # list of lib files to load on start.  libList on cmd line added to it
startObjList = []           # list of lib objs from command line to load on start

############

# run the world
class PandaRunner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)     # Init Panda3d
        taskMgr.add(WyeCore.World.worldRun)
        WyeCore.base = self      # world needs this to do panda3d stuff

        #props = WindowProperties()
        #props.setTitle("Wye V" + version)
        #WyeCore.base.win.requestProperties(props)


# main program, run 3d


#print("Start")
loadPrcFileData('', 'win-size 1200 800')           # set size of window
loadPrcFileData('', 'show-frame-rate-meter #t')    # turn on frame rate display
loadPrcFileData('', 'window-title Wye V'+version)


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
    libLoadList.extend(["TestLib.py", "TestLib2.py", "TestLib3.py"])
    startObjList = [] #"TestLib.TestLib.testObj", "TestLib.TestLib.testObj2", "TestLib2.TestLib2.testObj3", "TestLib2.TestLib2.testPar"]

# import libraries
for libFile in libLoadList:
    #print("Load lib '", libFile, "'")
    libName = libFile.split(".")[0]
    #print("Lib name '", libName, "'")
    #path = libFile
    path = WyeCore.Utils.resourcePath(libFile)
    try:
        libModule = SourceFileLoader(libName, path).load_module()
        # print("libModule ", libModule)
        libClass = getattr(libModule, libName)
        # print("libClass ", libClass)
        WyeCore.World.libList.append(libClass)
        #print("Loaded library ", libName, " from file ", path, " into lib class ", libClass)
    except:
        print("Failed to load class ", libName, " From file ", path)
        ex = sys.exception()
        traceback.print_exception(ex)

# load starting objects
WyeCore.World.startObjs.extend(startObjList)

#print("Loaded libList:", WyeCore.World.libList)
#print("start objs:", WyeCore.World.startObjs)

pandaRunner = PandaRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

