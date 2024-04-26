# Building up direct compiled version of Wye

# consolidating compiled code into one block

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d

from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
#from pandac.PandaModules import *
#from panda3d.core import loadPrcFileData

#from Wye import Wye
import WyeTestLib as WyeTestLib
from WyeCore import WyeCore



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

# need to figure out better way to to start up?
WyeCore.world.libs.append(WyeTestLib.testLib)
WyeCore.world.startObjs.extend(["WyeTestLib.testLib.testObj", "WyeTestLib.testLib.testObj2"])

pandaRunner = PandaRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
