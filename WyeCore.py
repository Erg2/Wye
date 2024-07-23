# Wye Core
# static single class lib
#
# license: We don't need no stinking license
#

from Wye import Wye
import inspect      # for debugging
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.showbase import Audio3DManager
import sys, os

# WyeCore class is a static container for the core Wye Classes that is never instantiated

# Building it this way prevents the editor from accidentally writing over the core because
# editing one of the contained libList will create an external file for just that lib.
# Incorporating the result requires external editing.

# used to make unique ids
_nextId = 0

# minimal object to tack verb param and var offset constants onto
class VerbConst:
    def __init__(self):
        pass

class WyeCore(Wye.staticObj):
    # used to detect first call for initialization
    worldInitialized = False

    debugListCode = True       # true to list Python code generated from Wye code

    picker = None   # object picker object
    base = None     # panda3d base - set by application
    focusManager = None # dialog input field focus manager

    lastIsNothingToRun = False

    class libs:
        placeholder = ""

    class World(Wye.staticObj):
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = ()
        codeDescr = ()

        keyHandler = None

        # universe specific
        libList = []
        libDict = {}  # lib name -> lib lookup dictionary
        startObjs = []
        objs = []  # runnable objects
        objStacks = []  # objects run in parallel so each one gets a stack

        eventCallbackDict = {}              # dictionary of event callbacks
        repeatEventCallbackDict = {}      # dictionary of repeated event frames

        displayCycleCount = 0           # DEBUG

        ##########################
        # Per display frame world exec
        #
        # called once per frame
        # runs all active objects in parallel
        def worldRun(task):
            global render
            global base

            property_names = [p for p in dir(Wye) if isinstance(getattr(Wye, p), property)]
            # print("Wye contains ", property_names)

            # init world on first frame
            if not WyeCore.worldInitialized:
                # print("worldRunner: World Init")
                WyeCore.worldInitialized = True  # Only do this once

                dlight = DirectionalLight('dlight')
                dlight.setColor((1, 1, 1, 1))  # (0.8, 0.8, 0.5, 1))
                dlnp = render.attachNewNode(dlight)
                dlnp.setHpr(45, -60, 0)
                render.setLight(dlnp)

                ####### Test 3d text

                text = TextNode('node name')
                text.setWordwrap(7.0)
                text.setText("Welcome to Wye " + Wye.version)
                text.setTextColor(1, 1, 1, 1)
                text.setAlign(TextNode.ACenter)
                # text.setFrameColor(0, 0, 1, 1)
                # text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

                text.setCardColor(0, 0, 0, 1)
                text.setCardAsMargin(.1, .2, .1, .1)  # extend beyond edge of text (-x, +x, -y, +y)
                text.setCardDecal(True)
                #
                # create 3d text object
                _label3d = NodePath(text.generate())  # supposed to, but does not, generate pickable node
                # _label3d = NodePath(text)
                _label3d.reparentTo(render)
                _label3d.setScale(.2, .2, .2)
                _label3d.setPos(-.5, 17, 4)
                _label3d.setTwoSided(True)

                _label3d.node().setIntoCollideMask(GeomNode.getDefaultCollideMask())

                ####### Test 3d spimd

                audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                snd = audio3d.loadSfx("WyePop.wav")
                audio3d.attachSoundToObject(snd, _label3d)

                ###########

                # base.camera.setPos(10,25,10)        # this does not move camera - something else controlling pos?
                # print("camPos",base.camera.getPos())

                ###########

                # put rep exec obj on obj list
                WyeCore.World.objs.append(WyeCore.World.repeatEventExecObj)
                stk = []
                f = WyeCore.World.repeatEventExecObj.start(stk)  # start the object and get its stack frame
                stk.append(f)  # create a stack for it
                f.SP = stk  # put ptr to stack in frame
                f.params = [[0], ]  # place to put return param
                WyeCore.World.objStacks.append(stk)

                # build list of known libraries (so can ref them during build)
                for lib in WyeCore.World.libList:
                    WyeCore.World.libDict[lib.__name__] = lib  # build lib name -> lib lookup dictionary
                    setattr(WyeCore.libs, lib.__name__, lib)  # put lib on lib dict
                    print("Put '" + lib.__name__ + "' in WyeCore.libs")

                # build all libraries - compiles any Wye code words in each lib
                for lib in WyeCore.World.libList:
                    # print("Build ", lib)
                    lib.build()  # build all Wye code segments in code words

                # parse starting object names and find the objects in the known libraries
                # print("worldRunner:  start ", len(world.startObjs), " objs")
                for objStr in WyeCore.World.startObjs:
                    # print("obj ", objStr," in startObjs")
                    namStrs = objStr.split(".")  # parse name of object
                    if namStrs[1] in WyeCore.World.libDict:
                        obj = getattr(WyeCore.World.libDict[namStrs[1]], namStrs[2])  # get object from library
                        WyeCore.World.objs.append(obj)  # add to list of runtime objects
                        stk = []
                        f = obj.start(stk)  # start the object and get its stack frame
                        stk.append(f)  # create a stack for it
                        f.params = [[0], ]  # place to put return param
                        WyeCore.World.objStacks.append(stk)  # put obj's stack on list and put obj's frame on the stack
                    else:
                        print("Error: Lib '" + namStrs[1] + "' not found for start object ", objStr)

                # set up for text input events
                WyeCore.World.keyHandler = WyeCore.World.KeyHandler()

                # create picker object for object selection events
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

                # WyeCore.picker.makePickable(_label3d)
                # tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
                # _label3d.setTag("wyeTag", tag)

                # print("worldRunner done World Init")

            # run
            else:
                WyeCore.World.displayCycleCount += 1
                # # DEBUG
                # print("\nworldRunner: cycle ", WyeCore.World.displayCycleCount, " run ", len(WyeCore.World.objStacks), " stacks:")
                # stkNum = 0
                # for stk in WyeCore.World.objStacks:
                #     print("   Stack ", stkNum, " depth ", len(stk))
                #     for frm in stk:
                #         print("     frame for obj ", frm.verb.__name__)
                #     stkNum += 1
                # # END DEBUG

                # debug
                stackNum = 0
                ranNothing = True  # pessimist
                for stack in WyeCore.World.objStacks:
                    sLen = len(stack)
                    if sLen > 0:  # if there's something on the stack
                        ranNothing = False
                        # run the frame furthest down the stack
                        frame = stack[-1]
                        # if frame:
                        #    print("worldRunner stack # ", stackNum, " verb", frame.verb.__name__,
                        #          " status ", WyeCore.Utils.statusToString(frame.status),
                        #          " stack:", WyeCore.Utils.stackToString(stack))
                        # else:
                        #    print("worldRunner ERROR: stack # ", stackNum, " depth", len(stack)," stack[-1] frame = None")
                        #    exit(1)
                        if frame.status == Wye.status.CONTINUE:
                            # print("worldRunner run: stack ", stackNum, " verb", frame.verb.__name__, " PC ", frame.PC)
                            frame.verb.run(frame)
                            # if frame.status != Wye.status.CONTINUE:
                            #    print("worldRunner stack ", stackNum, " verb", frame.verb.__name__," status ", WyeCore.Utils.statusToString(frame.status))
                        # print("worldRunner: run ", frame.verb.__name__, " returned status ", WyeCore.Utils.statusToString(frame.status),
                        #       " returned param ", frame.params[0])
                        else:
                            # print("worldRunner: status = ", WyeCore.Utils.statusToString(frame.status))
                            if sLen > 1:  # if there's a parent frame on the stack list, let them know their called word has exited
                                pFrame = stack[-2]
                                # print("worldRunner: return from call, run frame one back from bottom ", pFrame.verb.__name__)
                                pFrame.verb.run(pFrame)  # parent will remove child frame
                            else:  # no parent frame, do the dirty work ourselves
                                # print("worldRunner: done with top frame on stack.  Clean up stack")
                                stack.remove(frame)
                    stackNum += 1
                if ranNothing:
                    # print("ranNothing ", ranNothing, " and WyeCore.lastIsNothingToRun", WyeCore.lastIsNothingToRun)
                    if not WyeCore.lastIsNothingToRun:
                        WyeCore.lastIsNothingToRun = True
                        # print("worldRunner stack # ", stackNum, " nothing to run")

            return Task.cont  # tell panda3d we want to run next frame too

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
            if eventName in WyeCore.World.eventCallbackDict:
                tagDict = WyeCore.World.eventCallbackDict[eventName]
                #print("setEventCallback: add frame '", frame.verb.__name__, "' to tag '", tag, "'tagDict ", tagDict)
                if tag in tagDict:
                    tagDict[tag].append((frame, data,))
                    #print("setEventCallback: existing tag '", tag, "', dict now=", WyeCore.World.eventCallbackDict)
                else:
                    tagDict[tag] = [(frame, data,),]
                    #print("setEventCallback: new tag '", tag, "', dict now=", WyeCore.World.eventCallbackDict)
            else:
                WyeCore.World.eventCallbackDict[eventName] = {tag: [(frame, data,),]}
                #print("setEventCallback: new event '", eventName, " put frame '", frame.verb.__name__, "' on tag '", tag, "', dict now=", WyeCore.World.eventCallbackDict)

        # frames for repeated events need to be kept globally so they can be called
        # even if their context has gone away
        # Note that they keep references to any variables up the stack that they need
        # even if those variable's frames have been GC'd
        def setRepeatEventCallback(eventName, frame, data=None):

            frameID = "frm"+str(WyeCore.Utils.getId()) # get unique id for frame list
            # note: list in repEvtCallbackDict acts as global stack frame as well as
            # holding onto the event tags this event is for
            repEvt = [[frame], eventName, data, frameID]
            frame.SP = repEvt[0]        # repeated event runs on its own stack
            WyeCore.World.repeatEventCallbackDict[frameID] = repEvt
            #print("setRepeatEventCallback on event ", eventName, " object ", objTag, " add frameID ", frameID, "\nrepDict now=", WyeCore.World.repeatEventCallbackDict)
            return frameID
            pass

        # find frame entry in rep event dict
        # remove it from rep dict and from event dict
        def clearRepeatEventCallback(frameTag):
            if frameTag in WyeCore.World.repeatEventCallbackDict:
                del WyeCore.World.repeatEventCallbackDict[frameTag]
                #print("clrRepEvt: frame ", frame, " evt ", eventName, " tag ", tag, " frmID ", frameID)
                #print("clrRepEvt: callbackDict ", WyeCore.World.eventCallbackDict)

            else:
                print("Error: clearRepeatEventCallback failed to find frameTag '", frameTag,
                      "' in WyeCore.World.repeatEventCallbackDict")


        # key event dispatcher
        # (panda3d key event callback)
        class KeyHandler(DirectObject):
            def __init__(self):
                base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
                self.accept('keystroke', self.keyFunc)
                self.accept('arrow_right', self.controlKeyFunc, [Wye.ctlKeys.RIGHT])
                self.accept('arrow_left', self.controlKeyFunc, [Wye.ctlKeys.LEFT])
                self.accept('arrow_up', self.controlKeyFunc, [Wye.ctlKeys.UP])
                self.accept('arrow_down', self.controlKeyFunc, [Wye.ctlKeys.DOWN])
                self.accept('shift_down', self.controlKeyFunc, [Wye.ctlKeys.SHIFT_DOWN])
                self.accept('shift_up', self.controlKeyFunc, [Wye.ctlKeys.SHIFT_UP])
                self.accept('ctl_down', self.controlKeyFunc, [Wye.ctlKeys.CTL_DOWN])
                self.accept('ctl_up', self.controlKeyFunc, [Wye.ctlKeys.CTL_UP])


            def controlKeyFunc(self, keyID):
                #print("Control key ", keyID)
                if WyeCore.focusManager:
                    WyeCore.focusManager.doKey(keyID)

            def keyFunc(self, keyname):
                #print("KeyHandler: key=", keyname, "=", ord(keyname))
                # if there's a dialog focus manager running
                focusStatus = False
                if WyeCore.focusManager:
                    # returns True if it used the event
                    focusStatus = WyeCore.focusManager.doKey(keyname)

                # if there isn't a focusManager or it didn't want that event, check if
                # anyone else wants it
                if not focusStatus:
                    # if there's a callback for the specific object, call itF
                    if "key" in WyeCore.World.eventCallbackDict:
                        tagDict = WyeCore.World.eventCallbackDict["key"]
                        delLst = []
                        for wyeID in tagDict:
                            #print("Found ", len(tagDict[wyeID]), " key callbacks for tag ", wyeID)
                            # run through lists calling callbacks.
                            # print("objSelectEvent: tagDict=", tagDict)
                            evtLst = tagDict[wyeID]
                            for evt in evtLst:
                                frame = evt[0]
                                data = evt[1]
                                #print("KeyHandler event: inc frame ", frame.verb.__name__, " PC ", frame.PC)
                                frame.PC += 1
                                frame.eventData = (wyeID, keyname, data)  # user data
                            delLst.append(wyeID)
                        for tag in delLst:  # remove tag from active callbacks
                            del tagDict[tag]

        # every-frame event dispatcher
        # list of independent frames running until they succeed/fail
        class repeatEventExecObj:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.NONE
            paramDescr = ()
            varDescr = ()

            def start(stack):
                return Wye.codeFrame(WyeCore.World.repeatEventExecObj, stack)

            # run event frames every display frame
            # it is up to the event frames to wait on whatever event they have in mind
            def run(frame):
                delList = []
                #print("repEventObj run: Event dict:", WyeCore.World.repeatEventCallbackDict)
                evtIx = 0       # debug
                for evtID in WyeCore.World.repeatEventCallbackDict:
                    evt = WyeCore.World.repeatEventCallbackDict[evtID]
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
                        #print("repEventObj run: bot stack done, run -2 evt ", evtIx, " verb ", frame.verb.__name__, " PC ", frame.PC)
                        frame.eventData = (evtID, evt[1])        # user data
                        frame.verb.run(frame)
                        # On parent error, bail out - TODO - consider letting its parent handle error
                        if frame.status == Wye.status.FAIL and len(evt[0]) > 1:
                            #print("repEventObj run: -2 evt ", evtIx, " fail, kill event")
                            delList.append(evt[3])  # save this entry's tag to delete when done
                    # if only one frame on stack and it's done, remove event entry
                    if len(evt[0]) == 1 and evt[0][0].status != Wye.status.CONTINUE:
                        #print("repEventObj run: done with evt ", evtIx, ".  Remove from dict")
                        delList.append(evt[3])      # save this entry's tag to delete when done
                    evtIx += 1 # debug

                for tag in delList:
                    #print("repEventObj: done with tag ", tag)
                    WyeCore.World.clearRepeatEventCallback(tag)


    ##########################
    # 3d object Picker
    ##########################

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

            self.pickedObj = None  # don't have an obj yet
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

        # Wye object selection dispatcher
        # (Panda3d mouse click callback)
        # Check for object hit - check hit obj has obj tag - check for event for given obj tag
        def objSelectEvent(self):
            if self.pickerEnable:
                self.getObjectHit(WyeCore.base.mouseWatcherNode.getMouse())
                if self.pickedObj:
                    wyeID = self.pickedObj.getTag('wyeTag')
                    #print("Clicked on ", self.pickedObj, " at ", self.pickedObj.getPos(), " wyeID ", wyeID)
                    if wyeID:
                        #print("Picked object: '", self.pickedObj, "', wyeID ", wyeID)
                        # if there's a user input focus manager, call it
                        focusStatus = False
                        if WyeCore.focusManager:
                            # Returns True if it used the event.
                            focusStatus = WyeCore.focusManager.doSelect(wyeID)

                        # if there isn't a focusManager or it didn't want that event, check if
                        # anyone else wants it
                        if not focusStatus:
                            # if there's a callback for the specific object, call itF
                            if "click" in WyeCore.World.eventCallbackDict:
                                tagDict = WyeCore.World.eventCallbackDict["click"]
                                if wyeID in tagDict:
                                    #print("Found ", len(tagDict[wyeID]), " callbacks for tag ", wyeID)
                                    # run through lists calling callbacks.
                                    #print("objSelectEvent: tagDict=", tagDict)
                                    evtLst = tagDict[wyeID]
                                    for evt in evtLst:
                                        frame = evt[0]
                                        data = evt[1]
                                        #print("objSelectEvent: inc frame ", frame.verb.__name__, " PC ", frame.PC)
                                        frame.PC += 1
                                        frame.eventData = (wyeID, data)        # user data
                                    del tagDict[wyeID] # remove tag from dict of active callbacks

                                # if there's a callback for 'any' click event, call it
                                if "any" in tagDict:
                                    #print("Found ", len(tagDict[wyeID]), " callbacks for tag 'any'")
                                    for frame, data in tagDict.pop('any'):
                                        frame.PC += 1
                                        frame.eventData = (wyeID, data)

                                #else:
                                #    print("No click events waiting")
                #else:
                #    print("No object under mouse")
            #else:
            #    print("Object picking disabled")


    # General utilities for world building
    class Utils(Wye.staticObj):

        # get unique number
        def getId():
            global _nextId

            _nextId += 1
            if _nextId > 4294967295:        # wrap to pos signed int (ok only sorta unique)
                _nextsId = 1
                
            return _nextId

        def resourcePath(relative_path):
            try:
                # look for PyInstaller temp folder
                base_path = sys._MEIPASS
            except:
                # nope, guess we're running from python or IDE
                base_path = os.path.abspath(".")

            path = base_path + "/" + relative_path

            path = path.replace("\\","/")
            #path = path.replace(":","")

            #print("  return path '"+ path+"'")
            return path

        # Take a Wye code description tuple and return compilable Python code
        # Resulting code pushes all the params to the frame, then runs the function
        # Recurses to parse nested param tuples
        #
        # Note: SINGLE_CYCLE and MULTI_CYCLE verb code is a list of verbs to process
        #       PARALLEL verb code is a list of verbs to split into separate parallel
        #       execution streams
        # caseNumList is a list so the number can be incremented
        # fns is a list that parallel functions are added to
        def parseWyeTuple(wyeTuple, fNum, caseNumList):
            codeText = ""
            parFnText = ""
            # Wye verb
            if wyeTuple[0]:     # if there is a verb here
                # find tuple library entry
                #print("parseWyeTuple parse ", wyeTuple)
                tupleParts = wyeTuple[0].split('.')
                libName = tupleParts[-2]
                verbName = tupleParts[-1]
                lib = WyeCore.World.libDict[libName]
                verbClass = getattr(lib, verbName)


                # generate appropriate code for verb mode
                #print("WyeCore parseWyeTuple verb '" + wyeTuple[0] + "' dType "+Wye.mode.tostring(verbClass.mode))
                match(verbClass.mode):
                    # single cycle verbs create code that runs immediately when called
                    case Wye.mode.SINGLE_CYCLE:
                        eff = "f"+str(fNum)         # eff is frame var.  fNum keeps frame var names unique in nested code
                        codeText += "    "+eff+" = " + wyeTuple[0] + ".start(frame.SP)\n"
                        #print("parseWyeTuple: 1 codeText =", codeText[0])
                        if len(wyeTuple) > 1:
                            for paramIx in range(1, len(wyeTuple)):
                                #print("parseWyeTuple: 2a paramIx ", paramIx, " out of ", len(wyeTuple)-1)
                                paramDesc = wyeTuple[paramIx]
                                #print("parseWyeTuple: 2 parse paramDesc ", paramDesc)
                                if paramDesc[0] is None:        # constant/var (leaf node)
                                    #print("parseWyeTuple: 3a add paramDesc[1]=", paramDesc[1])
                                    codeText += "    "+eff+".params.append(" + paramDesc[1] + ")\n"
                                    #print("parseWyeTuple: 3 codeText=", codeText[0])
                                else:                           # recurse to parse nested code tuple
                                    cdTxt, fnTxt = WyeCore.Utils.parseWyeTuple(paramDesc, fNum+1, caseNumList)
                                    # NOTE: Assumes that IDE ensured verb is a function!
                                    cdTxt += "    "+eff+".params.append(f"+str(fNum+1)+".params[0])\n"
                                    codeText += cdTxt
                                    parFnText += fnTxt
                        codeText += "    "+wyeTuple[0] + ".run("+eff+")\n    if "+eff+".status == Wye.status.FAIL:\n"
                        #codeText += "     print('verb ',"+eff+".verb.__name__, ' failed')\n"
                        codeText += "     frame.status = "+eff+".status\n     return\n"

                    # multi-cycle verbs create code that pushes a new frame on the stack which will run on the next display cycle and
                    # generates a new case statement in this verb that will pick up when the pushed frame completes
                    # Note that a parallel verb is a multi-cycle verb from the caller's perspective
                    case Wye.mode.MULTI_CYCLE | Wye.mode.PARALLEL:
                        #print("WyeCore parseWyeTuple MULTI_CYCLE verb '"+ wyeTuple[0]+"'")
                        eff = "f"+str(fNum)         # eff is frame var.  fNum keeps frame var names unique in nested code
                        codeText += "    "+eff+" = " + wyeTuple[0] + ".start(frame.SP)\n"
                        #print("parseWyeTuple: 1 codeText =", codeText[0])
                        if len(wyeTuple) > 1:
                            for paramIx in range(1, len(wyeTuple)):
                                #print("parseWyeTuple: 2a verbIx ", verbIx, " out of ", len(wyeTuple)-1)
                                paramDesc = wyeTuple[paramIx]
                                #print("parseWyeTuple: 2 parse paramDesc ", paramDesc)
                                if paramDesc[0] is None:        # constant/var (leaf node)
                                    #print("parseWyeTuple: 3a add paramDesc[1]=", paramDesc[1])
                                    codeText += "    "+eff+".params.append(" + paramDesc[1] + ")\n"
                                    #print("parseWyeTuple: 3 codeText=", codeText[0])
                                else:                           # recurse to parse nested code tuple
                                    #caseNumList[0] += 1
                                    cdTxt, fnTxt = WyeCore.Utils.parseWyeTuple(paramDesc, fNum+1, caseNumList)
                                    cdTxt += "    "+eff+".params.append(" + "f"+str(fNum+1)+".params[0])\n"
                                    codeText += cdTxt
                                    parFnText += fnTxt
                        codeText += "    frame.SP.append("+eff+")\n    frame.PC += 1\n"
                        caseNumList[0] += 1
                        #codeText += "   case "+str(caseNumList[0])+":\n    pass\n    "+eff+"=frame.SP.pop()\n"
                        codeText += "   case "+str(caseNumList[0])+":\n    "+eff+"=frame.SP.pop()\n"
                        codeText += "    if "+eff+".status == Wye.status.FAIL:\n"
                        #codeText += "     print('verb ',"+eff+".verb.__name__, ' failed')\n"
                        codeText += "     frame.status = "+eff+".status\n     return\n"
                        pass


                    # huh, wut?
                    case _:
                        print("INTERNAL ERROR: WyeCore parseWyeTuple verb ",wyeTuple," has unknown mode ",verbClass.mode)

            # Tuple has no verb, just raw Python code
            else:
                if len(wyeTuple) > 1:
                    codeText += "    "+wyeTuple[1]+"\n"
                else:
                    print("Wye Warning - parseTuple null verb but no raw code supplied")

            return (codeText, parFnText)

        # build run time code for a sequential verb (single or multiple cycle)
        # parse verb's code (list of Wye tuples) into Python code text
        def buildCodeText(name, codeDescr):
            caseNumList = [0]   # list so called fn can increment it.  This is Python pass by reference
            labelDict = {}
            # define runtime method for this function
            codeText = " def " + name + "_run_rt(frame):\n  match(frame.PC):\n   case 0:\n"
            parFnText = ""
            if len(codeDescr) > 0:
                for wyeTuple in codeDescr:
                    # label for branch/loop
                    if wyeTuple[0] == "Label":
                        caseNumList[0] += 1
                        labelDict[wyeTuple[1]] = caseNumList[0]
                        codeText += "    frame.PC += 1\n   case " + str(caseNumList[0]) + ": #Label " + wyeTuple[1] + "\n    pass\n"
                    elif wyeTuple[0] == "IfGoTo":
                        codeText += "    if (" + wyeTuple[1] + "):\n"
                        codeText += "     frame.PC = " + str(labelDict[wyeTuple[2]]) + " #GoToLabel " + wyeTuple[2] + "\n"
                        caseNumList[0] += 1
                        codeText += "    else:\n     frame.PC += 1\n   case " + str(caseNumList[0]) + ":\n    pass\n"
                    elif wyeTuple[0] == "GoTo":     # note: can only go to labels already seen
                        codeText += "    frame.PC = " + str(labelDict[wyeTuple[1]]) + " #GoToLabel " + wyeTuple[1] + "\n"
                        caseNumList[0] += 1
                        # NOTE: This is a wasted case, just to be sure succeeding cmds are not executed
                        codeText += "   case " + str(caseNumList[0]) + ":\n    pass\n"
                    else: # normal tuple
                        # DEBUG start vvv
                        #currFrame = inspect.currentframe()
                        #callrframe = inspect.getouterframes(currFrame, 2)
                        #print('WyeCore buildCodeText caller:', callrframe[1][3])
                        #print('WyeCore buildCodeText caller:', callrframe[1][3])
                        #print("WyeCore buildCodeText: compile tuple=", wyeTuple)
                        # DEBUG end ^^^^
                        cdTxt, parTxt = WyeCore.Utils.parseWyeTuple(wyeTuple, 0, caseNumList)

                        codeText += cdTxt
                        parFnText += parTxt

            # no code, make sure fn compiles
            else:
                codeText += "pass\n"

            #print("buildCodeText complete.  codeText=\n"+codeText[0])
            return (codeText, parFnText)


        # build run time code for parallel function verb (always multi cycle)
        # which includes the inline runtime runction and the separate
        # parallel runtime functions
        def buildParallelText(libName, verbName, streamDescr):

            # build the parallel stream functions
            parFnText = ""
            nStreams = len(streamDescr)
            # create run function for each stream
            for ix in range(nStreams):
                print("Create ",verbName," stream ", ix)
                codeDescr = streamDescr[ix]
                cd, fn = WyeCore.Utils.buildCodeText(verbName+"_stream" + str(ix), codeDescr)
                parFnText += cd + fn

            # define start last since it refs the run routines created above
            # create start routine for this parallel verb
            parFnText +=     " def " + verbName + "_start_rt(stack):\n"
            #parFnText +=     "  print('" + verbName + "_start_rt')\n"
            parFnText +=     "  f = Wye.parallelFrame(" + libName + "." + verbName + ",stack)\n"
            for ix in range(nStreams):
                parFnText += "  stk = []\n"     # stack for parallel stream
                parFnText += "  fs = Wye.codeFrame(WyeCore.ParallelStream, stk)\n" # frame for stream
                parFnText += "  fs.vars = f.vars\n"
                parFnText += "  fs.params = f.params\n"
                parFnText += "  fs.parentFrame = f\n"
                parFnText += "  fs.run = " + libName + "."  + libName + "_rt." + verbName + "_stream"+str(ix)+"_run_rt\n"
                parFnText += "  stk.append(fs)\n"   # put stream frame at top of stream's stack
                parFnText += "  f.stacks.append(stk)\n" # put stack on our frame's list of stream stacks

            #parFnText +=     "  print('f.stacks', f.stacks)\n"
            #parFnText +=     "  print('f.verb', f.verb)\n"
            parFnText +=     "  return f\n"

            # print("buildParallelText complete.  parFnText=\n"+parFnText[0])
            return ("", parFnText)

        def frameToString(frame):
            fStr = ""
            fStr += "frame: "+str(frame)+"\n"
            if hasattr(frame, "verb"):
                if hasattr(frame.verb, "__name__"):
                    fStr += "  verb "+frame.verb.__name__+"\n"
                else:
                    fStr += "  verb has no name"+"\n"
            else:
                fStr += "  frame has no verb"+"\n"
            if hasattr(frame, "PC"):
                fStr += "  PC="+str(frame.PC)+"\n"
            else:
                fStr += "  <no PC>"+"\n"
            if hasattr(frame, "SP"):
                fStr += "  SP="+WyeCore.Utils.frameListSummary(frame.SP)+"\n"
            else:
                fStr += "  <no SP>"+"\n"
            fStr += "  params:" + WyeCore.Utils.paramsToString(frame)+"\n"
            fStr += "  vars:" + WyeCore.Utils.varsToString(frame)

            return fStr

        def frameListSummary(lst):
            pStr = ""
            if len(lst) > 0:
                for ii in range(len(lst)):
                    frm = lst[ii]
                    pStr += str(frm.verb.__name__)
                    if ii < len(lst)-2:
                        pStr += ", "
            else:
                pstr = "<empty>"
            return pStr

        def listToString(lst):
            print("lst", lst)
            pStr = ""
            if len(lst) > 0:
                for ii in range(len(lst)):
                    pStr += str(lst[ii])
                    if ii < len(lst)-2:
                        pStr += ", "
            else:
                pStr = "<empty>"
            return pStr

        # return params concanated
        def paramsToString(frame):
            return WyeCore.Utils.listToString(frame.params)

        # return vars concanated
        def varsToString(frame):
            return WyeCore.Utils.listToString(frame.vars)

        # return status as string
        def statusToString(stat):
            match stat:
                case Wye.status.CONTINUE:
                    return "CONTINUE"
                case Wye.status.SUCCESS:
                    return "SUCCESS"
                case Wye.status.FAIL:
                    return "FAIL"

        # return stack in reverse order
        def stackToString(stack):
            sLen = len(stack)
            stkStr = "\n stack len=" + str(sLen)
            if sLen > 0:
                for ix in range(sLen-1, -1, -1):
                    frame = stack[ix]
                    stkStr += "\n  ["+str(ix)+"] verb=" + frame.verb.__name__ + " status " + WyeCore.Utils.statusToString(frame.status) + \
                              " PC=" + str(frame.PC)+ " params: " + str(frame.params)
            return stkStr

        # build a runtime library function for this library
        def buildLib(libClass):
            libName = libClass.__name__
            #print("WyeCore buildLib: libName", libName)
            codeStr = "class "+libName+"_rt:\n"
            parFnStr = ""     # any parallel stream fns to add to end of codeStr

            # for any class in the lib that has a build function, call it to build class code into the lib runtime
            doBuild = False     # assume nothing to do
            for attr in dir(libClass):
                if attr != "__class__":     # avoid lib's self reference
                    val = getattr(libClass, attr)
                    if inspect.isclass(val):
                        #print("build class ",attr," in lib ",libName)
                        if hasattr(val, "paramDescr"):
                            setattr(val, "pConst", VerbConst())
                            ii = 0
                            for desc in val.paramDescr:
                                if len(desc) > 0:
                                    setattr(val.pConst, desc[0], ii)
                                    ii += 1

                        if hasattr(val, "varDescr"):
                            setattr(val, "vConst", VerbConst())
                            ii = 0
                            for desc in val.varDescr:
                                if len(desc) > 0:
                                    setattr(val.vConst, desc[0], ii)
                                    ii += 1

                        # if the class has a build function then call it to generate Python source code for its runtime method
                        if hasattr(val, "build"):
                            doBuild = True      # there is code to compile
                            # print("class ", attr, " has build method.  attr is ", dType(attr), " val is ", dType(val))
                            build = getattr(val, "build")  # get child's build method
                            # call the build function to get the "run" code string
                            cdStr, parStr = build()  # call it to get child's runtime code string(s)
                            codeStr += cdStr
                            parFnStr += parStr

                        # if this class is an object that should be added to the world's active object list
                        if hasattr(val, "autoStart"):
                            classStr = libName + "." + libName + "." + val.__name__
                            #print("Startobj: ", classStr)
                            WyeCore.World.startObjs.append(classStr)

            # if there's code to build for the library, doit
            if doBuild:
                codeStr += parFnStr         # tack parallel code on end of regular code
                codeStr += 'setattr('+libName+', "'+libName+'_rt", '+libName+'_rt)\n'

                # If debug compiled Wye code
                if WyeCore.debugListCode:
                    print("\nlib '"+libClass.__name__+"' code=")
                    lnIx = 1
                    for ln in codeStr.split('\n'):
                        print("%2d "%lnIx, ln)
                        lnIx += 1

                code = compile(codeStr, "<string>", "exec")
                exec(code, {libName:libClass, "Wye":Wye, "WyeCore":WyeCore, "WyeUI":WyeCore.libs.WyeUI})

        # do we already have a UI input focus manager?
        def haveFocusManager():
            return not WyeCore.focusManager is None

        # set the UI focus manager
        # todo - this really should call a picker method instead of
        # poking a value directly into the picker
        def setFocusManager(focusManager):
            WyeCore.focusManager = focusManager

        def getFocusManager():
            return WyeCore.focusManager

    # Very special verb  used to execute parallel code
    # Each parallel stream needs its own stack and its own parent frame with stack pointer.
    # However all the parent frame params and vars need to be from the actual parent that owns
    # all the parallel streams.
    #
    # This verb is a construct that allows the rest of the compile and run code
    # to charge forward as if there was nothing odd going on.
    #
    # A verb that uses mode=Wye.mode.PARALLEL has codeDescr that is a list of multiple codeDescr blocks
    # that will run in parallel.
    #
    # At compile time each code block is compiled into its own runtime function.  Then a custom start function is
    # defined that creates a separate frame for each code block and fills it in with references to the parent frame
    # plus a custom "run" attribute in each frame that points to its code block runtime function.
    #
    # At runtime the ParallelStream verb "run" function calls through the custom run attribute to the appropriate
    # runtime code.
    #
    # Whether this is elegant or an ugly hack is moot 'cause that's how it works.  So there.
    class ParallelStream:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        parallelStreamFlag = True       # flag this as special verb (consider alternative way to encode parallel stream headers)
        paramDescr = ()
        varDescr = ()

        def start(stack):
            return Wye.codeFrame()
        def run(frame):
            frame.run(frame)
