# Wye Core
# static single class lib
#
# license: We don't need no stinking license
#

from Wye import Wye
import inspect      # for debugging
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerQueue, CollisionNode
from panda3d.core import CollisionRay, GeomNode
#from panda3d.core import CollisionPlane, CollisionSphere, Plane, Vec3, Point3, BitMask32

# WyeCore class is a static container for the core Wye Classes that is never instantiated

# Building it this way prevents the editor from accidentally writing over the core because
# editing one of the contained libs will create an external file for just that lib.
# Incorporating the result requires external editing.

# used to make unique ids
_nextId = 0



class WyeCore(Wye.staticObj):
    # used to detect first call for initialization
    worldInitialized = False

    picker = None   # object picker object
    base = None     # panda3d base - set by application

    class world(Wye.staticObj):
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = ()
        codeDescr = ()

        # universe specific
        libs = []
        startObjs = []
        objs = []  # runnable objects
        objStacks = []  # objects run in parallel so each one gets a stack

        eventDict = {}

        ##########################
        # Per frame world exec
        #
        # called once per frame
        # runs all active objects in parallel
        def worldRun(task):

            property_names = [p for p in dir(Wye) if isinstance(getattr(Wye, p), property)]
            # print("Wye contains ", property_names)

            # init world on first frame
            if not WyeCore.worldInitialized:
                print("worldRunner: World Init")
                WyeCore.worldInitialized = True  # Only do this once
                libDict = {}        # lib name -> lib lookup dictionary

                # build all libraries - compiles any Wye code words in each lib
                for lib in WyeCore.world.libs:
                    lib.build()         # build all Wye code segments in code words
                    #print("build lib ", lib.__name__)
                    libDict[lib.__name__] = lib     # build lib name -> lib lookup dictionary

                # parse starting object names and find the objects in the known libraries
                # print("worldRunner:  start ", len(world.startObjs), " objs")
                for objStr in WyeCore.world.startObjs:
                    namStrs = objStr.split(".")                     # parse name of object
                    obj = getattr(libDict[namStrs[1]], namStrs[2])  # get object from library
                    WyeCore.world.objs.append(obj)                  # add to list of runtime objects
                    f = obj.start()                                 # start the object and get its stack frame
                    stk = [f]                                       # create a stack for it
                    f.SP = stk                                      # put ptr to stack in frame
                    f.params = [[0], ]                              # place to put return param
                    WyeCore.world.objStacks.append(stk)             # put obj's stack on list and put obj's frame on the stack
                # print("worldRunner done World Init")

                # create picker object
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

            # run
            else:
                #        print("worldRunner: run ", len(world.objStacks), " stacks")
                # debug
                # stackNum = 0
                for stack in WyeCore.world.objStacks:
                    sLen = len(stack)
                    if sLen > 0:  # if there's something on the stack
                        # run the frame furthest down the stack
                        frame = stack[-1]
                        # print("worldRunner stack # ", stackNum, " frame ", frame, " status ", WyeCore.utils.printStatus(frame.status), " stackLen ", sLen,
                        #       " stack ", WyeCore.utils.printStack(stack))
                        if frame.status == Wye.status.CONTINUE:
                            frame.verb.run(frame)
                        # print("worldRunner: run ", frame.verb.__name__, " returned status ", WyeCore.utils.printStatus(frame.status),
                        #       " returned param ", frame.params[0])
                        else:
                            # print("worldRunner: status = ", WyeCore.utils.printStatus(frame.status))
                            if sLen > 1:  # if there's a parent frame on the stack list, let them know their called word has exited
                                pFrame = stack[-2]
                                # print("worldRunner: return from call, run frame one back from bottom ", pFrame.verb.__name__)
                                pFrame.verb.run(pFrame)  # parent will remove child frame
                            else:  # no parent frame, do the dirty work ourselves
                                # print("worldRunner: done with top frame on stack.  Clean up stack")
                                stack.remove(frame)

            return Task.cont    # tell panda3d we want to run next frame too

        ##########################
        # Event Manager
        ##########################
        def setEventCallback(eventName, eventFrame, data=None):
            if eventName in WyeCore.world.eventDict:
                WyeCore.world.eventDict[eventName].append([eventFrame, data])
            else:
                WyeCore.world.eventDict[eventName] = [[eventFrame, data]]


    ##########################
    # Picker code does odd stuff when included, figure out why
    ##########################

    # For reasons I don't fully understand, Picker deriving from DirectObject causes
    class Picker(DirectObject):
        def __init__(self, app):
            # setup collision stuff

            self.app = app
            self.picker = CollisionTraverser()
            self.queue = CollisionHandlerQueue()

            self.pickerNode = CollisionNode('mouseRay')
            self.pickerNP = self.app.camera.attachNewNode(self.pickerNode)

            self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

            self.pickerRay = CollisionRay()

            self.pickerNode.addSolid(self.pickerRay)

            self.picker.addCollider(self.pickerNP, self.queue)

            # this holds the object that has been picked
            self.pickedObj = None

            self.accept('mouse1', self.printMe)

            self.pickerEnable = True

        # this function is meant to flag an object as being somthing we can pick
        def makePickable(self, newObj):
            print("picker:  set 'pickable' on ", newObj)
            newObj.setTag('pickable', 'true')

        # DEBUG test for known tags on object
        def tagDebug(self, obj):
            print("obj path depth ", obj.getNumNodes(), " node() ", obj.node())
            hasTag = False
            if obj.getTag('pickable'):
                print("'", obj, "' has tag ", " pickable")
                hasTag = True
            if obj.getTag('wyeTag'):
                print("'", obj, "' has tag ", " wyeTag")
                hasTag = True
            if not hasTag:
                print("'", obj, "' has no known tags")

        # this function finds the closest object to the camera that has been hit by our ray
        def getObjectHit(self, mpos):  # mpos is the position of the mouse on the screen
            global render

            self.pickedObj = None  # be sure to reset this
            self.pickerRay.setFromLens(WyeCore.base.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(render)
            if self.queue.getNumEntries() > 0:
                # print(self.queue.getNumEntries(), " entries in picker queue")
                self.queue.sortEntries()
                # print("Queue contains ", self.queue)
                self.pickedObj = self.queue.getEntry(0).getIntoNodePath()

                # parent=self.pickedObj.getParent()
                parent = self.pickedObj
                self.pickedObj = None

                # print("First obj in queue '", parent, "'")
                while parent != render:
                    # self.tagDebug(parent)  # DEBUG print tags on object
                    if parent.getTag('pickable') == 'true':
                        self.pickedObj = parent
                        return parent
                    else:
                        parent = parent.getParent()
            return None

        def getPickedObj(self):
            return self.pickedObj

        def printMe(self):
            # print("printMe called")
            if self.pickerEnable:
                self.getObjectHit(WyeCore.base.mouseWatcherNode.getMouse())
                if self.pickedObj is None:
                    print("No object picked")
                else:
                    wyeID = self.pickedObj.getTag('wyeTag')
                    print("Picked object: '", self.pickedObj, "', wyeID ", wyeID)
                    # self.tagDebug(self.pickedObj)

                    # need to match to object!
                    if "click" in WyeCore.world.eventDict:
                        list = WyeCore.world.eventDict["click"]
                        print("Got click list ", list)
                        for evt in list:
                            evt[0].PC += 1
                        list.clear()

        # else:
        #     print("Object picking disabled")

    class utils(Wye.staticObj):

        def getId():
            global _nextId

            _nextId += 1
            return _nextId

        # Take a Wye code description tuple and return compilable Python code
        # Resulting code pushes all the params to the frame, then runs the function
        # Recurses to handle nested param tuples
        def parseWyeTuple(wyeTuple, fNum):
            # Wye verb
            if wyeTuple[0]:
                eff = "f"+str(fNum)         # eff is frame var.  fNum keeps frame var names unique in nested code
                codeText = eff+" = " + wyeTuple[0] + ".start()\n"
                #print("parseWyeTuple: 1 codeText =", codeText[0])
                if len(wyeTuple) > 1:
                    for paramIx in range(1, len(wyeTuple)):
                        #print("parseWyeTuple: 2a paramIx ", paramIx, " out of ", len(wyeTuple)-1)
                        paramDesc = wyeTuple[paramIx]
                        #print("parseWyeTuple: 2 parse paramDesc ", paramDesc)
                        if paramDesc[0] is None:        # constant/var (leaf node)
                            #print("parseWyeTuple: 3a add paramDesc[1]=", paramDesc[1])
                            codeText += eff+".params.append(" + paramDesc[1] + ")\n"
                            #print("parseWyeTuple: 3 codeText=", codeText[0])
                        else:                           # recurse to parse nested code tuple
                            #print("parseWyeTuple: 4 - Can't get here")
                            codeText += WyeCore.utils.parseWyeTuple(paramDesc, fNum+1) + "\n" + eff+".params.append(" + \
                                "f"+str(fNum+1)+".params[0])\n"
                codeText += wyeTuple[0] + ".run("+eff+")\n"
            # Raw Python code
            else:
                if len(wyeTuple) > 1:
                    codeText = wyeTuple[1]+"\n"
                else:
                    print("Wye Warning - parseTuple null verb but no raw code supplied")

            return codeText

        def buildCodeText(codeDescr):
            codeText = [""]
            #print("WyeCore buildCodeText compile code=", codeDescr)

            for wyeTuple in codeDescr:
                # DEBUG start vvv
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
#                print('WyeCore buildCodeText caller:', calframe[1][3])
#                print('WyeCore buildCodeText caller:', calframe[1][3])
#                print("WyeCore buildCodeText: compile tuple=", wyeTuple)
                # DEBUG end ^^^^
                codeText[0] += WyeCore.utils.parseWyeTuple(wyeTuple, 0)

#            print("buildCodeText complete.  codeText=\n", codeText[0])
            return codeText[0]

        # Take Python code for a Wye word and return compiled code
        def compileCodeText(codeText):
 #           print("WyeCore.compileCodeText: compile ", codeText)
            code = compile(codeText, "<string>", "exec")
 #           if code:
 #               print("WyeCore.compileCodeText: Compiled successfully")
            return code


        def printStatus(stat):
            match stat:
                case Wye.status.CONTINUE:
                    return "CONTINUE"
                case Wye.status.SUCCESS:
                    return "SUCCESS"
                case Wye.status.FAIL:
                    return "FAIL"

        def printStack(stack):
            stkStr = "\n stack len=" + str(len(stack))
            for frame in stack:
                stkStr += "\n  verb=" + frame.verb.__name__ + " status " + WyeCore.utils.printStatus(frame.status) + \
                          " params: " + str(frame.params)
            return stkStr
