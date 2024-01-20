# Building up direct compiled version of Wye

# consolidating compiled code into one block

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d
from direct.task import Task
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
import sys

from Wye import Wye
import WyeTestLib as WyeTestLib
from WyeCore import WyeCore

##########################
# Per frame world exec
##########################

worldInit = True

class universe:
    mode = Wye.mode.SINGLE_CYCLE
    dataType = Wye.type.NONE
    paramDescr = ()
    varDescr = ()
    codeDescr = ()

    # universe specific
    libs =  [WyeTestLib.testLib]
    startObjs = ["WyeTestLib.testLib.testObj", "WyeTestLib.testLib.testObj2"]
    objs = []       # runnable objects
    objStacks = []  # objects run in parallel so each one gets a stack

# called once per frame
# runs all active objects in parallel
def worldRunner(task):
    global worldInit

    property_names = [p for p in dir(Wye) if isinstance(getattr(Wye, p), property)]
    #print("Wye contains ", property_names)

    if worldInit:
        print("worldRunner: World Init")
        worldInit = False

        #print("Attributes of WyeTestLib\n", print(dir(WyeTestLib)))

        # build all libraries
        for lib in universe.libs:
            lib.build()

        #print("sys.modules ", sys.modules)
        #print("globals ", globals())

        print("worldRunner:  start ", len(universe.startObjs), " objs")
        for objStr in universe.startObjs:
            namStrs = objStr.split(".")
#            print("worldRunner: namStrs ", namStrs)
#            print("worldRunner: globals()[namStrs[0]", globals()[namStrs[0]])
            mod = globals()[namStrs[0]]
            lib = getattr(mod, namStrs[1])
            obj = getattr(lib, namStrs[2])
#            print("worldRunner: start object ", obj.__name__)
            universe.objs.append(obj)
            f = obj.start()
            stk = [f]
            f.SP = stk      # put ptr to stack in frame
            f.params = [[0], ]  # place to put return param
            universe.objStacks.append(stk)   # put obj's stack on list and put obj's frame on the stack
        print("worldRunner done World Init")

    # run
    else:
#        print("worldRunner: run ", len(universe.objStacks), " stacks")
        stackNum = 0
        for stack in universe.objStacks:
            sLen = len(stack)
            if sLen > 0: # if there's something on the stack
                # run the frame furthest down the stack
                frame = stack[len(stack)-1]
#                print("worldRunner stack # ", stackNum, " frame ", frame, " status ", WyeCore.utils.printStatus(frame.status), " stackLen ", sLen,
#                      " stack ", WyeCore.utils.printStack(stack))
                if frame.status == Wye.status.CONTINUE:
                    frame.verb.run(frame)
#                    print("worldRunner: run ", frame.verb.__name__, " returned status ", WyeCore.utils.printStatus(frame.status),
#                          " returned param ", frame.params[0])
                else:
#                    print("worldRunner: status = ", WyeCore.utils.printStatus(frame.status))
                    if sLen > 1:     # if there's a parent on the list, let them know their called word has exited
                        pFrame = stack[len(stack)-2]
#                        print("worldRunner: return from call, run frame one back from bottom ", pFrame.verb.__name__)
                        pFrame.verb.run(pFrame)  # parent will remove child frame
                    else:   # no parent, do the dirty work ourselves
#                        print("worldRunner: done with top frame on stack.  Clean up stack")
                        stack.remove(frame)

        #print("World Run")
        #f = WyeTestLib.testLib.testObj2.start()
        ##print("worldInit: testObj start f.params ", f.params)
        #f.params = [[0],]        # place to put return param
        ##f.debug = "frame made by testObj2.start"
        #WyeTestLib.testLib.testObj2.run(f)
        #print("worldInit: testObj2 returned ", f.params[0])

    return Task.cont

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
