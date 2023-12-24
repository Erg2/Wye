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


#        print("worldInit: Call testObj inline")
#
#        print("worldInit: load object")
#        f = WyeTestLib.testLib.testLoader.start(stack)
#        WyeTestLib.testLib.testLoader.run(f)

        obj = {}
        #print("worldInit: compile loader2 and load object")
        #f = WyeTestLib.testLib.testLoader2.start(stack)
        #WyeTestLib.testLib.testLoader2.run(f)
        #print("worldInit: compile loader3 and load object")
        #f = WyeTestLib.testLib.testLoader3.start(stack)
        #f.params.append([obj])
        #f.params.append(["flyer_01.glb"])
        #f.params.append([[-1,15,1.5]])
        #f.params.append([[5.,5.,5.]])
        #WyeTestLib.testLib.testLoader3.run(f)
        #print("worldInit: done it")


        print("worldInit: Call testObj inline")

        f = WyeTestLib.testLib.testObj.start(stack)
        #print("worldInit: testObj start f.params ", f.params)
        f.params = [[0],]        # place to put return param
        #f.debug = "frame made by testObj.start"
        print("worldInit: testObj pre-run: f.params ", f.params)
        WyeTestLib.testLib.testObj.run(f)
        print("worldInit: testObj post run: f.params ", f.params)
        print("worldInit: testObj returned ", f.params[0])


# run the world
class PandaRunner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)     # Init Panda3d
        taskMgr.add(worldRunner)

# main program, run 3d
print("Start")
pandaRunner = PandaRunner()
print("Started, now run")
pandaRunner.run()
print("Done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
