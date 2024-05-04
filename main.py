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

LibLoadList = ["TestLib.py",]
startObjList = ["WyeTestLib.TestLib.testObj", "WyeTestLib.TestLib.testObj2"]

###########
############

# run the world
class PandaRunner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)     # Init Panda3d
        taskMgr.add(WyeCore.world.worldRun)
        WyeCore.base = self      # world needs this to do panda3d stuff

# main program, run 3d
#print("Start")
loadPrcFileData('', 'win-size 1024 768')           # set size of window
loadPrcFileData('', 'show-frame-rate-meter #t')    # turn on frame rate display

# import libraries
for libFile in LibLoadList:
    print("Load lib '", libFile, "'")
    libName = libFile.split(".")[0]
    print("Lib name '", libName, "'")
    libModule = SourceFileLoader(libName, libFile).load_module()
    print("libModule ", libModule)
    libClass = getattr(libModule, libName)
    print("libClass ", libClass)
    WyeCore.world.libs.append(libClass)

# load starting objects
WyeCore.world.startObjs.extend(startObjList)

pandaRunner = PandaRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

