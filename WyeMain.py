# Building up direct compiled version of Wye

# consolidating compiled code into one block

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d
from importlib.machinery import SourceFileLoader    # to load libs from files
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
#from pandac.PandaModules import *
#from panda3d.core import loadPrcFileData


from WyeCore import WyeCore
import sys, os

version = "0.1"

libLoadList = [] #["TestLib.py",]
startObjList = [] #["TestLib.TestLib.testObj", "TestLib.TestLib.testObj2"]

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


# if the user supplied a list of libs and or start objs
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
else:
    libLoadList = ["TestLib.py","TestLib2.py"]
    startObjList = ["TestLib.TestLib.testObj", "TestLib.TestLib.testObj2", "TestLib2.TestLib2.testObj3"]

# import libraries
for libFile in libLoadList:
    #print("Load lib '", libFile, "'")
    libName = libFile.split(".")[0]
    #print("Lib name '", libName, "'")
    path = libFile
    #path = WyeCore.Utils.resourcePath(libFile)
    libModule = SourceFileLoader(libName, path).load_module()

    #try:
    #    path = resourcePath(libFile)
    #    libModule = SourceFileLoader(libName, path).load_module()
    #except:
    #    print("Failed to load class ", libName, " From file ", libFile)
    #    continue

    #print("libModule ", libModule)
    libClass = getattr(libModule, libName)
    #print("libClass ", libClass)
    WyeCore.World.libs.append(libClass)

# load starting objects
WyeCore.World.startObjs.extend(startObjList)

pandaRunner = PandaRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

