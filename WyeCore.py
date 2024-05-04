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

        eventCallbackDict = {}              # dictionary of event callbacks
        repeatEventCallbackDict = {}      # dictionary of repeated event frames

        displayCycleCount = 0           # DEBUG

        # list of independent frames running until they succeed/fail
        class repeatEventExecObj:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.type.NONE
            paramDescr = ()
            varDescr = ()

            def start(stack):
                return Wye.codeFrame(WyeCore.world.repeatEventExecObj, stack)

            # run event frames every display frame
            # it is up to the event frames to wait on whatever event they have in mind
            def run(frame):
                delList = []
                #print("repEventObj run: Event dict:", WyeCore.world.repeatEventCallbackDict)
                evtIx = 0       # debug
                for evtID in WyeCore.world.repeatEventCallbackDict:
                    evt = WyeCore.world.repeatEventCallbackDict[evtID]
                    frame = evt[0][-1]
                    #print("repEventObj run: frame=", frame)
                    # run bottom of stack unless done
                    if frame.status == Wye.status.CONTINUE:
                        #print("repEventObj run: evt ", evtIx, " verb ", frame.verb.__name__, " PC ", frame.PC)
                        frame.eventData = (evtID, evt[1])        # user data
                        frame.verb.run(frame)
                    # bottom of stack done, run next up on stack if any
                    elif len(evt[0]) > 1:
                        frame = evt[0][-2]
                        print("repEventObj run: bot stack done, run -2 evt ", evtIx, " verb ", frame.verb.__name__, " PC ", frame.PC)
                        frame.eventData = (evtID, evt[1])        # user data
                        frame.verb.run(frame)
                        # On parent error, bail out - TODO - consider letting its parent handle error
                        if frame.status == Wye.status.FAIL and len(evt[0]) > 1:
                            print("repEventObj run: -2 evt ", evtIx, " fail, kill event")
                            delList.append(evt[3])  # save this entry's tag to delete when done
                    # if only one frame on stack and it's done, remove event entry
                    if len(evt[0]) == 1 and evt[0][0].status != Wye.status.CONTINUE:
                        print("repEventObj run: done with evt ", evtIx, ".  Remove from dict")
                        delList.append(evt[3])      # save this entry's tag to delete when done
                    evtIx += 1 # debug

                for tag in delList:
                    #print("repEventObj: done with tag ", tag)
                    WyeCore.world.clearRepeatEventCallback(tag)


        ##########################
        # Per display frame world exec
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

                # put rep exec obj on obj list
                WyeCore.world.objs.append(WyeCore.world.repeatEventExecObj)
                stk = []
                f = WyeCore.world.repeatEventExecObj.start(stk)  # start the object and get its stack frame
                stk.append(f)  # create a stack for it
                f.SP = stk  # put ptr to stack in frame
                f.params = [[0], ]  # place to put return param
                WyeCore.world.objStacks.append(stk)


                # build all libraries - compiles any Wye code words in each lib
                for lib in WyeCore.world.libs:
                    lib.build()         # build all Wye code segments in code words
                    print("build lib ", lib.__name__)
                    libDict[lib.__name__] = lib     # build lib name -> lib lookup dictionary

                # parse starting object names and find the objects in the known libraries
                # print("worldRunner:  start ", len(world.startObjs), " objs")
                for objStr in WyeCore.world.startObjs:
                    namStrs = objStr.split(".")                     # parse name of object
                    obj = getattr(libDict[namStrs[1]], namStrs[2])  # get object from library
                    WyeCore.world.objs.append(obj)                  # add to list of runtime objects
                    stk = []
                    f = obj.start(stk)                                 # start the object and get its stack frame
                    stk.append(f)                                   # create a stack for it
                    #f.SP = stk                                      # put ptr to stack in frame
                    f.params = [[0], ]                              # place to put return param
                    WyeCore.world.objStacks.append(stk)             # put obj's stack on list and put obj's frame on the stack
                # print("worldRunner done World Init")

                # create picker object
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

            # run
            else:
                WyeCore.world.displayCycleCount += 1
                # # DEBUG
                # print("\nworldRunner: cycle ", WyeCore.world.displayCycleCount, " run ", len(WyeCore.world.objStacks), " stacks:")
                # stkNum = 0
                # for stk in WyeCore.world.objStacks:
                #     print("   Stack ", stkNum, " depth ", len(stk))
                #     for frm in stk:
                #         print("     frame for obj ", frm.verb.__name__)
                #     stkNum += 1
                # # END DEBUG

                # debug
                stackNum = 0
                for stack in WyeCore.world.objStacks:
                    sLen = len(stack)
                    if sLen > 0:  # if there's something on the stack
                        # run the frame furthest down the stack
                        frame = stack[-1]
                        #if frame:
                        #    print("worldRunner stack # ", stackNum, " frame ", frame, " status ", WyeCore.utils.statusToString(frame.status),
                        #          " verb", frame.verb.__name__,
                        #          " stackLen ", sLen, " stack ", WyeCore.utils.stackToString(stack))
                        #else:
                        #    print("worldRunner stack # ", stackNum, " frame = None")
                        #    exit(1)
                        if frame.status == Wye.status.CONTINUE:
                            #print("worldRunner run: stack ", stackNum, " verb", frame.verb.__name__, " PC ", frame.PC)
                            frame.verb.run(frame)
                        # print("worldRunner: run ", frame.verb.__name__, " returned status ", WyeCore.utils.statusToString(frame.status),
                        #       " returned param ", frame.params[0])
                        else:
                            # print("worldRunner: status = ", WyeCore.utils.statusToString(frame.status))
                            if sLen > 1:  # if there's a parent frame on the stack list, let them know their called word has exited
                                pFrame = stack[-2]
                                # print("worldRunner: return from call, run frame one back from bottom ", pFrame.verb.__name__)
                                pFrame.verb.run(pFrame)  # parent will remove child frame
                            else:  # no parent frame, do the dirty work ourselves
                                # print("worldRunner: done with top frame on stack.  Clean up stack")
                                stack.remove(frame)
                    stackNum += 1

            return Task.cont    # tell panda3d we want to run next frame too

        ##########################
        # Event Manager
        #
        # A dictionary word waiting for an event is sitting in an empty case statement (case #: pass)
        # The following case is the event processing code.
        # If the event returns data, the event processing code will put any data in frame.eventData
        #
        # The event dictionary has a separate entry for each kind of event
        #
        # Each kind of event has a dictionary of tags
        #   Each tag has a list of (frame, data) pairs
        #
        #   When the event occurs the WyeCore entry point gets the tag associated with the given event
        #       looks for a matching tag in its tag dictionary
        #       If the tag exists, it has a list of frame, data pairs
        #       For each pair it increments the PC in the frame and puts the event data in frame.eventData
        #       Then it clears the tag from the dictionary
        #
        ##########################

        def setEventCallback(eventName, tag, frame, data=None):
            if eventName in WyeCore.world.eventCallbackDict:
                tagDict = WyeCore.world.eventCallbackDict[eventName]
                print("setEventCallback: add frame '", frame.verb.__name__, "' to tag '", tag, "'tagDict ", tagDict)
                if tag in tagDict:
                    tagDict[tag].append((frame, data,))
                    #print("setEventCallback: existing tag '", tag, "', dict now=", WyeCore.world.eventCallbackDict)
                else:
                    tagDict[tag] = [(frame, data,),]
                    #print("setEventCallback: new tag '", tag, "', dict now=", WyeCore.world.eventCallbackDict)
            else:
                WyeCore.world.eventCallbackDict[eventName] = {tag: [(frame, data,),]}
                print("setEventCallback: new event '", eventName, " put frame '", frame.verb.__name__, "' on tag '", tag, "', dict now=", WyeCore.world.eventCallbackDict)

        # frames for repeated events need to be kept globally so they can be called 
        # even if their context has gone away
        # Note that they keep references to any variables up the stack that they need 
        # even if those variable's frames have been GC'd
        def setRepeatEventCallback(eventName, frame, data=None):

            frameID = "frm"+str(WyeCore.utils.getId()) # get unique id for frame list
            # note: list in repEvtCallbackDict acts as global stack frame as well as
            # holding onto the event tags this event is for
            repEvt = [[frame], eventName, data, frameID]
            frame.SP = repEvt[0]        # repeated event runs on its own stack
            WyeCore.world.repeatEventCallbackDict[frameID] = repEvt
            #print("setRepeatEventCallback on event ", eventName, " object ", objTag, " add frameID ", frameID, "\nrepDict now=", WyeCore.world.repeatEventCallbackDict)
            return frameID
            pass

        # find frame entry in rep event dict
        # remove it from rep dict and from event dict
        def clearRepeatEventCallback(frameTag):
            if frameTag in WyeCore.world.repeatEventCallbackDict:
                frame, eventName, tag, frameID = WyeCore.world.repeatEventCallbackDict.pop(frameTag)
                print("clrRepEvt: frame ", frame, " evt ", eventName, " tag ", tag, " frmID ", frameID)
                print("clrRepEvt: callbackDict ", WyeCore.world.eventCallbackDict)
                if eventName in WyeCore.world.eventCallbackDict:
                    tagDict = WyeCore.world.eventCallbackDict[eventName]
                    print("clrRepEvt: found tagDict ", tagDict)
                    if tag in tagDict:
                        print("clrRepEvt: get framelist for tag ", tag)
                        frameList = tagDict[tag]
                        print("clrRepEvt: frameList ", frameList)
                        delList = []
                        for ii in range(len(frameList)):
                            if frame == frameList[ii][0]:
                                print("ClrRepEvt: remove list entry ", ii)
                                delList.insert(0, ii)   # put on del list in reverse order
                        # remove frame from list
                        for ii in delList:
                            del frameList[ii]
                        if len(frameList) == 0:
                            del tagDict[tag]
                    else:
                        print("Error: clearRepeatEventCallback failed to find eventName '", tag,
                              "' in WyeCore.world.eventCallbackDict under event '", eventName,"'")
                else:
                    print("Error: clearRepeatEventCallback failed to find eventName '", eventName,
                          "' in WyeCore.world.eventCallbackDict")
            else:
                print("Error: clearRepeatEventCallback failed to find frameTag '", frameTag,
                      "' in WyeCore.world.repeatEventCallbackDict")

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

            self.accept('mouse1', self.objSelectEvent)

            self.pickerEnable = True

        # this function is meant to flag an object as being somthing we can pick
        def makePickable(self, newObj):
            #print("picker:  set 'pickable' on ", newObj)
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
                #print("getObjectHit: ", self.queue.getNumEntries(), " entries in picker queue")
                self.queue.sortEntries()
                #print("getObjectHit: Queue contains ", self.queue)
                self.pickedObj = self.queue.getEntry(0).getIntoNodePath()
                parent = self.pickedObj
                self.pickedObj = None
                # go up the path looking for a pickable node
                while parent != render:
                    if parent.getTag('pickable') == 'true':
                        self.pickedObj = parent
                        return parent
                    else:
                        parent = parent.getParent()
            return None

        def getPickedObj(self):
            return self.pickedObj

        # get here when mouse clicked
        # Check for object hit - check hit obj has obj tag - check for event for given obj tag
        def objSelectEvent(self):
            if self.pickerEnable:
                self.getObjectHit(WyeCore.base.mouseWatcherNode.getMouse())
                if self.pickedObj:
                    wyeID = self.pickedObj.getTag('wyeTag')
                    print("wyeID ", wyeID)
                    if wyeID:
                        #print("Picked object: '", self.pickedObj, "', wyeID ", wyeID)

                        # if there's a callback for the specific object, call it
                        if "click" in WyeCore.world.eventCallbackDict:
                            tagDict = WyeCore.world.eventCallbackDict["click"]
                            if wyeID in tagDict:
                                print("Found ", len(tagDict[wyeID]), " callbacks for tag ", wyeID)
                                # run through lists calling callbacks.
                                # keep any repeated frames and update the callback entry with just them
                                # if no repeated frames, remove callback entry for this target
                                repEvts = []
                                #print("objSelectEvent: tagDict=", tagDict)
                                evtLst = tagDict[wyeID]
                                for evt in evtLst:
                                    frame = evt[0]
                                    data = evt[1]
                                    print("objSelectEvent: inc frame ", frame.verb.__name__, " PC ", frame.PC)
                                    frame.PC += 1
                                    frame.eventData = (wyeID, data)        # user data
                                    del tagDict[wyeID]

                            # if there's a callback for 'any' click event, call it
                            if "any" in tagDict:
                                #print("Found ", len(tagDict[wyeID]), " callbacks for tag 'any'")
                                for frame, data in tagDict.pop('any'):
                                    frame.PC += 1
                                    frame.eventData = (wyeID, data)

                        #else:
                        #    print("No click events waiting")
            #else:
            #    print("Object picking disabled")

    class utils(Wye.staticObj):

        # get unique number
        def getId():
            global _nextId

            _nextId += 1
            if _nextId > 4294967295:        # wrap to pos signed int (ok only sorta unique)
                _nextsId = 1
                
            return _nextId

        # Take a Wye code description tuple and return compilable Python code
        # Resulting code pushes all the params to the frame, then runs the function
        # Recurses to handle nested param tuples
        def parseWyeTuple(wyeTuple, fNum):
            # Wye verb
            if wyeTuple[0]:
                eff = "f"+str(fNum)         # eff is frame var.  fNum keeps frame var names unique in nested code
                codeText = eff+" = " + wyeTuple[0] + ".start(frame.SP)\n"
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
#                currFrame = inspect.currentframe()
#                callrframe = inspect.getouterframes(currFrame, 2)
#                print('WyeCore buildCodeText caller:', callrframe[1][3])
#                print('WyeCore buildCodeText caller:', callrframe[1][3])
#                print("WyeCore buildCodeText: compile tuple=", wyeTuple)
                # DEBUG end ^^^^
                codeText[0] += WyeCore.utils.parseWyeTuple(wyeTuple, 0)

            #print("buildCodeText complete.  codeText=\n", codeText[0])
            return codeText[0]

        # Take Python code for a Wye word and return compiled code
        def compileCodeText(codeText):
 #           print("WyeCore.compileCodeText: compile ", codeText)
            code = compile(codeText, "<string>", "exec")
 #           if code:
 #               print("WyeCore.compileCodeText: Compiled successfully")
            return code


        def statusToString(stat):
            match stat:
                case Wye.status.CONTINUE:
                    return "CONTINUE"
                case Wye.status.SUCCESS:
                    return "SUCCESS"
                case Wye.status.FAIL:
                    return "FAIL"

        def stackToString(stack):
            stkStr = "\n stack len=" + str(len(stack))
            for frame in stack:
                stkStr += "\n  verb=" + frame.verb.__name__ + " status " + WyeCore.utils.statusToString(frame.status) + \
                          " params: " + str(frame.params)
            return stkStr
