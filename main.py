# Building up direct compiled version of Wye

# consolidating compiled code into one block

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d
from direct.task import Task
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

import WyeTestLib as WyeTestLib

##########################
# Per frame world exec
##########################

worldInit = True

def worldRunner(task):
    global worldInit

    if worldInit:
        print("World task running")
        worldInit = False

        #print("Attributes of WyeTestLib\n", print(dir(WyeTestLib)))

        WyeTestLib.testLib.build()

        # initialize the world
        libs = {}  # Create library context for compiled code
        libs["testLib"] = WyeTestLib.testLib

        stack = []  # sequential stack


#        print("doit: Call testObj inline")
#
#        print("doit: load object")
#        f = WyeTestLib.testLib.testLoader.start(stack)
#        WyeTestLib.testLib.testLoader.run(f)

        print("doit: compile loader2 and load object")
        f = WyeTestLib.testLib.testLoader2.start(stack)
        WyeTestLib.testLib.testLoader2.run(f)
        print("doit: done it")


        print("doit: Call testObj inline")

        f = WyeTestLib.testLib.testObj.start(stack)
        f.params = [[0]]
        f.debug = "frame made by testObj.start"
        WyeTestLib.testLib.testObj.run(f)
        print("doit: testObj returned ", f.params[0])


# doit calls testObj with one return parameter
class PandaRunner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)     # Init Panda3d
        taskMgr.add(worldRunner)


pandaRunner = PandaRunner()
print("Started")

pandaRunner.run()
print("Done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
