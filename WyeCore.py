# Wye Core
# static single class lib
#
# license: We don't need no stinking license
#
from direct.showbase.MessengerGlobal import messenger

from Wye import Wye
import inspect      # for debugging
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.showbase import Audio3DManager
import sys, os
import math


# WyeCore class is a static container for the core Wye Classes that is never instantiated

# Building it this way prevents the editor from accidentally writing over the core because
# editing one of the contained libList will create an external file for just that lib.
# Incorporating the result requires external editing.


'''
Wye Overview

libraries and words in them are static
All refs to a lib or word within a lib or word have to be 3rd person (lib.word.xxx) rather than self.
because there is no instantiated class so there is no self.
All context (local variables, parameters passed in, and PC (which is used by multi-pass word) is in the 
stack frame that is returned by word.start.

Basic concept for executing a word in a library:
    wordFrame =  word.start(stack)
        The frame holds the local storage for this exec of word.  The most used attributes are the
        calling params and local variable values.

        if a word uses local variables the word's frame.vars is built automatically from the
        word's varDescr.  

        Each variable is a separate list so it can be passed to another word in that word's 
        stackframe.params and the var can be updated by that word.
        All vars are filled in with initial values by the frame on instantiation.
        example: wordFrame.vars = [[0],[1],["two"]]
    wordFrame.params.append( [p1], .. )
        If the word being called requires any params passed in, the caller has to set them up.
        Each parameter is wrapped in a list so that its value can be changed
        functions return their value in the first parameter
    word.run(wordFrame)
        If the word is a function, the return value is in the first parameter

Compiling 
    Two stages, first translating Wye code to Python code, and then compiling Python code to runtime code.  This is 
    done on library load so the overhead of compiling is done once.  

    If there is a codeDescr = (..wye-code..) then the code will be translated to Python.

    Wye code is in nested tuples in the form ("lib.word", (..param..), (..param..)) where the param list can be
    zero or more params.  Note that a tuple or list with just one entry must end with a comma (entry,) or python will 
    optimize the tuple or list away.
    (..param..) can be either (None, a-constant) or ("lib.word", (..param..)) to recurse to a function that will
    supply the parameter.

    The Python output is put in a string under code.

    All code attributes found in classes in the library are compiled to methods under the dynamically created 
    class libName_rt.  Each word's runtime is def'd as wordName_run_rt.  

    The word itself has a run method that calls libName_rt.wordName_run_rt(frame)

    Note: there is the risk that the string holding the
    Python code will get too long (the internal limit is not clearly defined).  If that happens then the compile loop
    could compile each word's code individually, but that would be much slower.  Or it could process words in chunks
    that are small enough to fit within the string limit.

    Note: a runtime optimization would be to reparent the rt attributes back to each word so there was no indirection
    on the call.
'''

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
    editor = None   # user editor of registered Wye objects

    lastIsNothingToRun = False

    class libs:
        placeholder = ""

    class World(Wye.staticObj):
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = ()
        codeDescr = ()

        keyHandler = None           # keyboard handler slot
        mouseHandler = None         # mouse handler slot
        debugger = None             # no debugger running
        editor = None               # no editor running
        mouseCallbacks = []         # any function wanting mouse events
                                    #   Control seems to jam mouse events,
                                    #   (neither mouse nor control-mouse gets called)
                                    #   So do mouse manually.  Sigh

        # universe specific
        dlight = None           # global directional light
        dLightPath = None
        libList = []
        libDict = {}  # lib name -> lib lookup dictionary
        startObjs = []
        objs = []  # runnable objects
        objStacks = []  # objects run in parallel so each one gets a stack
        objKillList = []    # frames of objects to be removed from the active list at the end of the current display cycle
        objTags = {}     # map of graphic tags to object frames

        eventCallbackDict = {}              # dictionary of event callbacks
        repeatEventCallbackDict = {}        # dictionary of repeated event frames
        _repEventAddList = []               # can't add event frame from within event callback, so queue here

        displayCycleCount = 0           # DEBUG

        ##########################
        # Per display frame world exec
        #
        # called once per frame
        # runs all active objects in parallel
        def worldRun(task):
            global render
            global base

            # EVENT DEBUG
            #messenger.toggleVerbose()      # Show all events

            property_names = [p for p in dir(Wye) if isinstance(getattr(Wye, p), property)]
            # print("Wye contains ", property_names)

            # init world on first frame
            if not WyeCore.worldInitialized:
                # print("worldRunner: World Init")
                WyeCore.worldInitialized = True  # Only do this once

                # Lighting
                WyeCore.World.dlight = DirectionalLight('dlight')
                WyeCore.World.dlight.setColor((1, 1, 1, 1))  # (0.8, 0.8, 0.5, 1))
                WyeCore.World.dlightPath = render.attachNewNode(WyeCore.World.dlight)
                WyeCore.World.dlightPath.setHpr(45, -65, 0)
                render.setLight(WyeCore.World.dlightPath)

                # Fog

                myFog = Fog("Fog Name")
                myFog.setColor(0, 0, 0)
                myFog.setExpDensity(0.001)
                base.render.setFog(myFog)

                ####### Test 3d text

                text = TextNode('node name')
                #text.setWordwrap(7.0)
                text.setText("Welcome to\nWye " + Wye.version)
                text.setTextColor(1, 1, 1, 1)
                text.setAlign(TextNode.ACenter)
                # text.setFrameColor(0, 0, 1, 1)
                # text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

                text.setCardColor(0, 0, 0, 1)
                text.setCardAsMargin(.1, .2, .1, .1)  # extend beyond edge of text (-x, +x, -y, +y)
                text.setCardDecal(True)
                #
                # create 3d text object
                _3dText = NodePath(text.generate())  # supposed to, but does not, generate pickable node
                # _3dText = NodePath(text)
                _3dText.reparentTo(render)
                _3dText.setScale(.2, .2, .2)
                _3dText.setPos(-.5, 17, 4)
                _3dText.setTwoSided(True)

                _3dText.node().setIntoCollideMask(GeomNode.getDefaultCollideMask())

                ####### Test 3d sound

                audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                snd = audio3d.loadSfx("WyePop.wav")
                audio3d.attachSoundToObject(snd, _3dText)

                ###########

                # set initial cam position
                base.camera.setPos(Wye.startPos[0], Wye.startPos[1], Wye.startPos[2])
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
                    #print("Put '" + lib.__name__ + "' in WyeCore.libs")

                # build all libraries - compiles any Wye code words in each lib
                for lib in WyeCore.World.libList:
                    # print("Build ", lib)
                    lib.build()  # build all Wye code segments in code words

                # parse starting object names and find the objects in the known libraries
                # print("worldRunner:  start ", len(world.startObjs), " objs")
                for objStr in WyeCore.World.startObjs:
                    #print("WorldRun start: obj ", objStr," in startObjs")
                    namStrs = objStr.split(".")  # parse name of object
                    if namStrs[1] in WyeCore.World.libDict:
                        obj = getattr(WyeCore.World.libDict[namStrs[1]], namStrs[2])  # get object from library
                        WyeCore.World.startActiveObject(obj)
                    else:
                        print("Error: Lib '" + namStrs[1] + "' not found for start object ", objStr)

                # set up for text input events
                WyeCore.World.keyHandler = WyeCore.World.KeyHandler()

                #print("start CameraControl")
                WyeCore.World.mouseHandler = WyeCore.libs.WyeUI.CameraControl()

                # create picker object for object selection events
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

                # set up editor
                WyeCore.editor = WyeCore.libs.WyeUI.ObjEditCtl()

                # WyeCore.picker.makePickable(_3dText)
                # tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
                # _3dText.setTag("wyeTag", tag)

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

                if WyeCore.World.mouseHandler:
                    if base.mouseWatcherNode.hasMouse():
                        x = base.mouseWatcherNode.getMouseX()
                        y = base.mouseWatcherNode.getMouseY()
                        WyeCore.World.mouseHandler.mouseMove(x,y)

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
                            #print("worldRunner stack # ", stackNum, " verb", frame.verb.__name__) #,

                            #      " status ", Wye.status.tostring(frame.status),
                            #      " stack:", frame.stackToString(frame.SP))
                        # else:
                        #    print("worldRunner ERROR: stack # ", stackNum, " depth", len(stack)," stack[-1] frame = None")
                        #    exit(1)
                        if frame.status == Wye.status.CONTINUE:
                            #if Wye.debugOn:
                            if Wye.debugOn:
                                Wye.debug(frame, "worldRunner run: stack "+ str(stackNum)+ " verb '"+ frame.verb.__name__+ "' PC "+ str(frame.PC))
                            else:
                                #print("run", frame.verb.__name__)
                                frame.verb.run(frame)
                            # if frame.status != Wye.status.CONTINUE:
                            #    print("worldRunner stack ", stackNum, " verb", frame.verb.__name__," status ", WyeCore.Utils.statusToString(frame.status))
                        # print("worldRunner: run ", frame.verb.__name__, " returned status ", WyeCore.Utils.statusToString(frame.status),
                        #       " returned param ", frame.firstParamVal())
                        else:
                            # print("worldRunner: status = ", WyeCore.Utils.statusToString(frame.status))
                            if sLen > 1:  # if there's a parent frame on the stack list, let them know their called word has exited
                                pFrame = stack[-2]
                                if Wye.debugOn:
                                    Wye.debug(pFrame, "worldRunner: return from call to"+ pFrame.verb.__name__+". Run parent frame "+pFrame.verb.__name__)
                                else:
                                    #print("run", pFrame.verb.__name__)
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

                # if active object completed, remove the stack it is on from run list
                if len(WyeCore.World.objKillList) > 0:
                    for frame in WyeCore.World.objKillList:
                        WyeCore.World.objStacks.remove(frame.SP)
                    WyeCore.World.objKillList.clear()

            return Task.cont  # tell panda3d we want to run next frame too

        # Start object verb and put it on active list so called every display cycle
        # return its stack frame
        def startActiveObject(obj):
            #WyeCore.World.objs.append(obj)  # add to list of runtime objects
            stk = []            # create stack to run object on
            frame = obj.start(stk)  # start the object and get its stack frame
            stk.append(frame)       # put obj frame on its stack
            # frame.params = [[0], ]  # place to put return param
            WyeCore.World.objStacks.append(stk)  # put obj's stack on list and put obj's frame on the stack
            return frame

        # Put object instance frame on active list
        # caller already created stack and started the object
        # (required when caller needs to pass params to the object)
        def startActiveFrame(frame):
            WyeCore.World.objStacks.append(frame.SP)  # put obj's stack on list and put obj's frame on the stack
            return frame

        # Queue frame to be removed from active object list at end of this display cycle
        def stopActiveObject(frame):
            WyeCore.World.objKillList.append(frame)

        # Find first active instance of object with given name
        def findActiveObj(name):
            #print(WyeCore.World.objStacks)
            #stkIx = 0
            for stk in WyeCore.World.objStacks:
                if len(stk) > 0:
                    #print("stack", stkIx)
                    for frm in stk:
                        #print(" frm", frm)
                        if hasattr(frm, "verb"):
                            #print("  verb", frm.verb.__name__)
                            if frm.verb.__name__ == name:
                                #print("   Found", frm.verb, " matching ", name)
                                return frm
                #stkIx += 1
            return None

        def registerMouseCallback(callback):
            if not callback in WyeCore.World.mouseCallbacks:
                WyeCore.World.mouseCallbacks.append(callback)

        def unregisterMouseCallback(callback):
            if callback in WyeCore.World.mouseCallbacks:
                WyeCore.World.mouseCallbacks.append(callback)

        # manage graphic object tag -> object frame list
        def registerObjTag(tag, frame):
            #print("Register tag ", tag, " to object", frame.verb.__name__)
            WyeCore.World.objTags[tag] = frame

        def unregisterObjTag(tag):
            if tag in WyeCore.World.objTags:
                del WyeCore.World.objTags[tag]

        def getRegisteredObj(tag):
            if tag in WyeCore.World.objTags:
                return WyeCore.World.objTags[tag]
            else:
                return None

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
            WyeCore.World._repEventAddList.append(repEvt)
            #print("setRepeatEventCallback on event ", eventName, " object ", frame, " add frameID ", frameID, "\nrepDict now=", WyeCore.World.repeatEventCallbackDict)
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
                self.accept('delete', self.controlKeyFunc, [Wye.ctlKeys.DELETE])

            def controlKeyFunc(self, keyID):
                #print("Control key", keyID)
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
                    # if there's a callback for the specific object, call it
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
                if len(WyeCore.World._repEventAddList) > 0:
                    for repEvt in WyeCore.World._repEventAddList:
                        WyeCore.World.repeatEventCallbackDict[repEvt[3]] = repEvt
                    WyeCore.World._repEventAddList = []

                evtIx = 0       # debug
                for evtID in WyeCore.World.repeatEventCallbackDict:
                    #print("repeatEventExecObj run: process evt", evtID)
                    evt = WyeCore.World.repeatEventCallbackDict[evtID]
                    if len(evt[0]) > 0:
                        #print("repeatEventExecObj run: process evt", evt)
                        frame = evt[0][-1]
                        #print("repEventObj run: frame=", frame)
                        # run bottom of stack unless done
                        if frame.status == Wye.status.CONTINUE:
                            #print("repEventObj run bot of stack evt: ", evtIx, " verb ", frame.verb.__name__, " PC ", frame.PC)
                            frame.eventData = (evtID, evt[2])        # user data
                            if Wye.debugOn:
                                Wye.debug(frame, "RepeatEvent run:"+ frame.verb.__name__+ " evt data "+ str(frame.eventData))
                            else:
                                #print("run", frame.verb.__name__)
                                frame.verb.run(frame)
                        # bottom of stack done, run next up on stack if any
                        elif len(evt[0]) > 1:
                            dbg = evt[0][-1]
                            #print("Bot of stack", dbg.verb.__name__, " status", Wye.status.tostring(dbg.status))
                            frame = evt[0][-2]
                            frame.eventData = (evtID, evt[2])        # user data
                            if Wye.debugOn:
                                Wye.debug(frame, "RepeatEvent done, run parent:"+ frame.verb.__name__+ " evt data"+ str(frame.eventData))
                            else:
                                #print("run", frame.verb.__name__)
                                #print("repEventObj bot of stack done, run caller evt: ", evtIx, " verb ", frame.verb.__name__, " PC ", frame.PC)
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

            WyeCore.World.registerMouseCallback(self.objSelectEvent)
            #self.accept('mouse1', self.objSelectEvent)
            #self.accept('control-mouse1', self.objSelectEvent)
            #self.accept('alt-mouse1', self.objSelectEvent)

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
            wyeTag = obj.getTag('wyeTag')
            if wyeTag:
                print("'", obj, "' has tag wyeTag =",wyeTag)
                hasTag = True
            if not hasTag:
                print("'", obj, "' has no known tags")

        # this function finds the closest object to the camera that has been hit by our ray
        # TODO it does not work with billboard nodes. Fails once the billboard rotates too far
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
                        #wyeTag = parent.getTag('wyeTag')
                        #if wyeTag:
                        #    print("Clicked on pickable object", parent, " with wyeTag", wyeTag)
                        #else:
                        #    print("clicked on pickable object", parent)
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
                        status = False
                        if WyeCore.editor:
                            status = WyeCore.editor.tagClicked(wyeID, self.pickedObj.getPos())
                            #if status:
                            #    print("objSelectEvent: Editor used tag", wyeID)

                        # if editor didn't use the tag, try the dialog focus manager
                        if WyeCore.focusManager and not status:
                            # Returns True if it used the event.
                            status = WyeCore.focusManager.doSelect(wyeID)
                            #if status:
                            #    print("objSelectEvent: Focus manager used tag", wyeID)

                        # if there isn't a focusManager or it didn't want that event, check if
                        # anyone else wants it
                        if not status:
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

                                    #print("objSelectEvent: click callback used tag", wyeID)

                                # if there's a callback for 'any' click event, call it
                                if "any" in tagDict:
                                    #print("Found ", len(tagDict[wyeID]), " callbacks for tag 'any'")
                                    for frame, data in tagDict.pop('any'):
                                        frame.PC += 1
                                        frame.eventData = (wyeID, data)
                                    #print("objSelectEvent: 'any' callback used tag", wyeID)


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

        def slerp(q1, q2, t):
            costheta = q1.dot(q2)
            if costheta < 0.0:
                costheta = -costheta
                q1 = q1.conjugate()
            elif costheta > 1.0:
                costheta = 1.0

            theta = math.acos(costheta)
            if abs(theta) < 0.01:
                return q2

            sintheta = math.sqrt(1.0 - costheta * costheta)
            if abs(sintheta) < 0.01:
                return (q1 + q2) * 0.5

            r1 = math.sin((1.0 - t) * theta) / sintheta
            r2 = math.sin(t * theta) / sintheta
            return (q1 * r1) + (q2 * r2)


        #https://physicsforgames.blogspot.com/2010/02/quaternions.html
        #Quat nlerp(const Quat& i, const Quat& f, float blend)
        #{
        #     Quat result;
        #     float dot = i.w*f.w + i.x*f.x + i.y*f.y + i.z*f.z;
        #     float blendI = 1.0f - blend;
        #     if(dot < 0.0f)
        #     {
        #          Quat tmpF;
        #          tmpF.w = -f.w;
        #          tmpF.x = -f.x;
        #          tmpF.y = -f.y;
        #          tmpF.z = -f.z;
        #          result.w = blendI*i.w + blend*tmpF.w;
        #          result.x = blendI*i.x + blend*tmpF.x;
        #          result.y = blendI*i.y + blend*tmpF.y;
        #          result.z = blendI*i.z + blend*tmpF.z;
        #     }
        #     else
        #     {
        #          result.w = blendI*i.w + blend*f.w;
        #          result.x = blendI*i.x + blend*f.x;
        #          result.y = blendI*i.y + blend*f.y;
        #          result.z = blendI*i.z + blend*f.z;
        #     }
        #     result = QuatNormalize(result);
        #     return result;
        #}
        def nlerp(q1, q2, tt):
            result = Quat()
            ttInv = 1.0 - tt
            dotp = q1.getR()*q2.getR() + q1.getI()*q2.getI() + q1.getJ()*q2.getJ() + q1.getK()*q2.getK();
            if dotp < 0.0:
                tmpF = Quat()
                tmpF.setR(-q2.getR())
                tmpF.setI(-q2.getI())
                tmpF.setJ(-q2.getJ())
                tmpF.setK(-q2.getK())
                result.setR(ttInv * q1.getR() + tt * tmpF.getR())
                result.setI(ttInv * q1.getI() + tt * tmpF.getI())
                result.setJ(ttInv * q1.getJ() + tt * tmpF.getJ())
                result.setK(ttInv * q1.getK() + tt * tmpF.getK())
            else:
                result.setR(ttInv * q1.getR() + tt * q2.getR())
                result.setI(ttInv * q1.getI() + tt * q2.getI())
                result.setJ(ttInv * q1.getJ() + tt * q2.getJ())
                result.setK(ttInv * q1.getK() + tt * q2.getK())

            return result.normalized()


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
            if wyeTuple[0] and wyeTuple[0] not in ["Var", "Const", "Var=", "Expr", "Code", "CodeBlock"]:     # if there is a verb here
                #Pick it apart to locate lib and verb
                #print("parseWyeTuple parse ", wyeTuple)
                tupleParts = wyeTuple[0].split('.')
                libName = tupleParts[-2]
                verbName = tupleParts[-1]
                lib = WyeCore.World.libDict[libName]
                verbClass = getattr(lib, verbName)

                # generate appropriate code for verb mode
                #print("\nWyeCore parseWyeTuple verb '" + wyeTuple[0] + "' dType "+Wye.mode.tostring(verbClass.mode))
                match verbClass.mode:
                    # single cycle verbs create code that runs immediately when called
                    # parse Wye code tuples in the form
                    #  (verb, [(optional), (params)]) - where each opt param is a recursive code tuple
                    # or
                    #  (None, "python code to inline")
                    case Wye.mode.SINGLE_CYCLE:
                        eff = "f"+str(fNum)         # eff is the name of the current frame.  fNum keeps frame names unique in nested code
                        # put local frames on the parent frame as attributes to keep local scope
                        codeText += "    if not hasattr(frame,'"+eff+"'):\n     setattr(frame,'"+eff+"',None)\n"
                        codeText += "    frame."+eff+" = " + wyeTuple[0] + ".start(frame.SP)\n"
                        #print("parseWyeTuple: verbClass", verbClass.__name__, " paramDescr", verbClass.paramDescr)
                        #print("parseWyeTuple SINGLE: 1 codeText =", codeText[0], " wyeTuple", wyeTuple)
                        #print("   len(verbClass.paramDescr)", len(verbClass.paramDescr))
                        #print("   verbClass.paramDescr", verbClass.paramDescr)
                        #print("   eff", eff)
                        # for all the params in the tuple
                        if len(wyeTuple) > 1:
                            #print("*** parseWyeTuple: parse params")
                            paramIx = 0
                            for paramTuple in wyeTuple:
                                #print(" parseWyeTuple: 2a paramIx ", paramIx, " out of ", len(wyeTuple) - 1)
                                # first tuple element is not a param
                                if paramIx == 0:
                                    paramIx += 1
                                    if paramIx > len(wyeTuple):
                                        print("parseWyeTuple SOURCE CODE ERROR: wyeTyple has ", len(wyeTuple), " params:", wyeTuple)
                                        print("  but verb", verbClass.__name__, " has only", len(verbClass.paramDescr), " params:", verbClass.paramDescr)

                                    #print(" parseWyeTuple: skip 0th entry in wyeTuple")
                                    continue        # skip processing any more of this tuple parameter

                                # skip empty tuples (list ended in ",")
                                if len(paramTuple) == 0:
                                    continue

                                tupleKey = paramTuple[0]
                                #print(" parseWyeTuple: 2 parse paramTuple ", paramTuple)
                                # if tuple is code to compile
                                #print("tupleKey", tupleKey)
                                if tupleKey is None or tupleKey in ["Var", "Const", "Expr", "Code", "CodeBlock"]:        # constant/var (leaf node)
                                    #print(" parseWyeTuple: paramTuple[0] is None/Const/Expr/Code")
                                    #print("  parseWyeTuple: 3a add paramTuple[1]=", paramTuple[1])
                                    #print("   verbClass.paramDescr", verbClass.paramDescr)
                                    #print("   verbClass.paramDescr[paramIx-1]", verbClass.paramDescr[paramIx-1][0])

                                    # if this is a variable param then recurse to parse list of wyetuples
                                    if verbClass.paramDescr[paramIx-1][1] == Wye.dType.VARIABLE:
                                        codeText += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "[0].append(" + paramTuple[1] + ")\n"
                                    else:
                                        codeText += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "=" + paramTuple[1] + "\n"

                                    #print("parseWyeTuple: 3 codeText=", codeText[0])
                                else:                           # recurse to parse nested code tuple
                                    #print(" parseWyeTuple: paramTuple[0] is", paramTuple[0], " >>>> Recurse <<<<")
                                    # Recurse to generate code to call verb and return its value
                                    cdTxt, fnTxt, firstParam = WyeCore.Utils.parseWyeTuple(paramTuple, fNum+1, caseNumList)

                                    # NOTE: Assumes that IDE ensured verb is a function!
                                    #print("  popped back to parsing verb", verbClass.__name__, " wyeTuple", wyeTuple)
                                    #print("   verbClass.paramDescr[paramIx-1]", verbClass.paramDescr[paramIx-1][0])

                                    if verbClass.paramDescr[paramIx-1][1] == Wye.dType.VARIABLE:
                                        cdTxt += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1] + "[0].append(frame.f"+str(fNum+1)+".params."+firstParam+")\n"
                                    else:
                                        cdTxt += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "=frame.f"+str(fNum+1)+".params."+firstParam+"\n"

                                    codeText += cdTxt
                                    parFnText += fnTxt

                                # if we get a VARIABLE param, all succeeding params belong to it
                                if verbClass.paramDescr[paramIx-1][1] != Wye.dType.VARIABLE:
                                    paramIx += 1
                                    if paramIx > len(wyeTuple):
                                        print("parseWyeTuple SOURCE CODE ERROR: wyeTyple has ", len(wyeTuple), " params:", wyeTuple)
                                        print("  but verb", verbClass.__name__, " has only", len(verbClass.paramDescr), " params:", verbClass.paramDescr)


                            #print("*** parseWyeTuple: finished params")
                            
                            # debug hook placeholder
                            codeText += "    if Wye.debugOn:\n"
                            codeText += "     Wye.debug(frame."+eff+",'Exec run:'+frame."+eff+".verb.__name__)\n"
                            codeText += "    else:\n"
                            #codeText += "     print('run',frame." + eff + ".verb.__name__)\n"
                            codeText += "     "+wyeTuple[0] + ".run(frame."+eff+")\n"
                            codeText += "    if frame."+eff+".status == Wye.status.FAIL:\n"
                            codeText += "     print('verb ',"+eff+".verb.__name__, ' failed')\n"
                            codeText += "     frame.status = frame."+eff+".status\n     return\n"

                    # multi-cycle verbs create code that pushes a new frame on the stack which will run on the next display cycle and
                    # generates a new case statement in this verb that will pick up when the pushed frame completes
                    # Note that a parallel verb is a multi-cycle verb from the caller's perspective
                    case Wye.mode.MULTI_CYCLE | Wye.mode.PARALLEL:
                        #print("WyeCore parseWyeTuple MULTI_CYCLE verb '"+ wyeTuple[0]+"'")
                        eff = "f"+str(fNum)         # eff is the name of the current frame.  fNum keeps frame names unique in nested code
                        # put local frames on the parent frame as attributes to keep local scope across display cycles
                        codeText += "    if not hasattr(frame,'" + eff + "'):\n"
                        #codeText += "     print('create frame attr "+eff+"')\n"
                        codeText += "     setattr(frame,'" + eff + "',None)\n"
                        codeText += "    frame."+eff+" = " + wyeTuple[0] + ".start(frame.SP)\n"
                        #print("parseWyeTuple MULTI|PARA: 1 codeText =", codeText[0], " wyeTuple", wyeTuple)
                        if len(wyeTuple) > 1:
                            paramIx = 0
                            for paramTuple in wyeTuple:
                                #print("parseWyeTuple: 2a verbIx ", verbIx, " out of ", len(wyeTuple)-1)
                                #print("parseWyeTuple: 2 parse paramTuple ", paramTuple)
                                if paramIx == 0:
                                    paramIx += 1
                                    if paramIx > len(wyeTuple):
                                        print("parseWyeTuple SOURCE CODE ERROR: wyeTyple has ", len(wyeTuple), " params:", wyeTuple)
                                        print("  but verb", verbClass.__name__, " has only", len(verbClass.paramDescr), " params:", verbClass.paramDescr)
                                    #print(" parseWyeTuple: skip 0th entry in wyeTuple")
                                    continue

                                # param starts with None, is a python code snippet returning a value
                                # (const, frame var ref, other expression)
                                tupleKey = paramTuple[0]
                                #print("tupleKey", tupleKey)
                                if tupleKey is None or tupleKey in ["Var", "Const", "Var=", "Expr", "Code", "CodeBlock"]:
                                    #print("parseWyeTuple: 3a add paramTuple[1]=", paramTuple[1])

                                    # debug
                                    #print("parseWyeTuple paramIx", paramIx, " verb", verbClass.__name__, " paramDescr ", verbClass.paramDescr)

                                    if verbClass.paramDescr[paramIx-1][1] == Wye.dType.VARIABLE:
                                        codeText += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "[0].append(" + paramTuple[1] + ")\n"
                                    else:
                                        codeText += "    frame." + eff + ".params." + verbClass.paramDescr[paramIx - 1][0] + "=" + paramTuple[1] + "\n"
                                    #print("parseWyeTuple: 3 codeText=", codeText[0])

                                # param tuple starts with library word
                                else: # recurse to parse nested code tuple
                                    #caseNumList[0] += 1
                                    cdTxt, fnTxt, firstParam = WyeCore.Utils.parseWyeTuple(paramTuple, fNum+1, caseNumList)

                                    # debug
                                    #print("parseWyeTuple paramIx", paramIx, " verb", verbClass.__name__, " paramDescr ", verbClass.paramDescr)

                                    # variable params
                                    if verbClass.paramDescr[paramIx-1][1] == Wye.dType.VARIABLE:
                                        cdTxt += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "[0].append(frame.f"+str(fNum+1)+".params."+firstParam+")\n"
                                    else:
                                        cdTxt += "    frame."+eff+".params." + verbClass.paramDescr[paramIx-1][0] + "=frame.f"+str(fNum+1)+".params."+firstParam+"\n"

                                    codeText += cdTxt
                                    parFnText += fnTxt

                                # if we get a VARIABLE param, all succeeding params belong to it
                                if verbClass.paramDescr[paramIx - 1][1] != Wye.dType.VARIABLE:
                                    paramIx += 1
                                    if paramIx > len(wyeTuple):
                                        print("parseWyeTuple SOURCE CODE ERROR: wyeTyple has ", len(wyeTuple), " params:", wyeTuple)
                                        print("  but verb", verbClass.__name__, " has only", len(verbClass.paramDescr), " params:", verbClass.paramDescr)

                        codeText += "    frame.SP.append(frame."+eff+")\n    frame.PC += 1\n"
                        caseNumList[0] += 1
                        #codeText += "   case "+str(caseNumList[0])+":\n    pass\n    frame."+eff+"=frame.SP.pop()\n"
                        codeText += "   case "+str(caseNumList[0])+":\n    frame."+eff+"=frame.SP.pop()\n"
                        codeText += "    if frame."+eff+".status == Wye.status.FAIL:\n"
                        #codeText += "     print('verb ',frame."+eff+".verb.__name__, ' failed')\n"
                        codeText += "     frame.status = frame."+eff+".status\n     return\n"
                        pass


                    # huh, wut?
                    case _:
                        print("INTERNAL ERROR: WyeCore parseWyeTuple verb ",wyeTuple," has unknown mode ",verbClass.mode)


                retParam = verbClass.paramDescr[0][0] if (hasattr(verbClass, "paramDescr") and len(verbClass.paramDescr) > 0) else "None"

            # Tuple has no verb, just raw Python code
            else:
                if len(wyeTuple) > 1:
                    # if multi-line block of code, offset it all correctly
                    codeLines = wyeTuple[1].split('\n')
                    for line in codeLines:
                        codeText += "    "+line+"\n"
                else:
                    print("Wye Warning - parseWyeTuple null verb but no raw code supplied")

                retParam = None

            # return parsed code, any parallel function defs, and the first param name (in case this is a function def)
            # (prolly should check for return value type def in verb def, but that's for fancier future parsing)

            # todo - figure out how to catch the None cases  softly
            return (codeText, parFnText, retParam)

        # build run time code for a sequential verb (single or multiple cycle)
        # parse verb's code (list of Wye tuples) into Python code text
        def buildCodeText(name, codeDescr):
            caseNumList = [0]   # list so called fn can increment it.  This is Python pass by reference
            labelDict = {}
            fwdLabelDict = {}
            # define runtime method for this function
            codeText = " def " + name + "_run_rt(frame):\n  match frame.PC:\n   case 0:\n"
            parFnText = ""
            firstParam = None
            if len(codeDescr) > 0:
                for wyeTuple in codeDescr:
                    # label for branch/loop
                    if wyeTuple[0] == "Label":
                        caseNumList[0] += 1
                        labelDict[wyeTuple[1]] = caseNumList[0]

                        codeText += "    frame.PC += 1\n"
                        codeText += "   case " + str(caseNumList[0]) + ": #Label " + wyeTuple[1] + "\n    pass\n"

                        # if this is the resolution of any forward label references
                        lblStr = wyeTuple[1]
                        if lblStr in fwdLabelDict:
                            fwdLabelDict.pop(lblStr)        # remove label from fwd ref dict
                            codeText = codeText.replace(">>>FWDLABEL_"+lblStr+"<<<", str(caseNumList[0]))
                            #print(">>>>Found forward ref", lblStr, " and replaced it with", caseNumList[0])

                    elif wyeTuple[0] == "IfGoTo":
                        # if label is behind this position (we've seen it already), it's easy
                        if wyeTuple[2] in labelDict:
                            codeText += "    if (" + wyeTuple[1] + "):\n"
                            codeText += "     frame.PC = " + str(labelDict[wyeTuple[2]]) + " #GoToLabel " + wyeTuple[2] + "\n"
                            codeText += "     return\n"     # skips any code following a successful If
                        # else this is a forward ref to a label we've not seen yet.
                        # Put a placeholder in the code and make a note to fix it later
                        else:
                            # print(">>> ifgoto found fwd ref to label", wyeTuple[1])
                            if not wyeTuple[2] in fwdLabelDict:
                                fwdLabelDict[wyeTuple[2]] = 1  # count positions that need fixing when we know the label location
                            else:
                                fwdLabelDict[wyeTuple[2]] += 1
                            # mark label location that needs fixing
                            codeText += "    if (" + wyeTuple[1] + "):\n"
                            codeText += "     frame.PC = >>>FWDLABEL_" + wyeTuple[2] + "<<< #GoToLabel " + wyeTuple[2] + "\n"
                            codeText += "     return\n"     # skips any code following a successful If
                        glideThruLabel = False      # don't auto inc PC when get to next label
                        #caseNumList[0] += 1
                        #codeText += "    else:\n     frame.PC += 1\n   case " + str(caseNumList[0]) + ":\n    pass\n"


                    elif wyeTuple[0] == "GoTo":
                        # if label is behind this position (we've seen it already), it's easy
                        if wyeTuple[1] in labelDict:
                            codeText += "    frame.PC = " + str(labelDict[wyeTuple[1]]) + " #GoToLabel " + wyeTuple[1] + "\n"
                        # else this is a forward ref to a label we've not seen yet.
                        # Put a placeholder in the code and make a note to fix it later
                        else:
                            #print(">>> goto found fwd ref to label", wyeTuple[1])
                            if not wyeTuple[1] in fwdLabelDict:
                                fwdLabelDict[wyeTuple[1]] = 1       # count positions that need fixing when we know the label location
                            else:
                                fwdLabelDict[wyeTuple[1]] += 1
                            # mark label location that needs fixing
                            codeText += "    frame.PC = >>>FWDLABEL_" + wyeTuple[1] + "<<< #GoToLabel " + wyeTuple[1] + "\n"

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
                        cdTxt, parTxt, firstParam = WyeCore.Utils.parseWyeTuple(wyeTuple, 0, caseNumList)

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
                #print("Create ",verbName," stream ", ix)
                codeDescr = streamDescr[ix]
                cd, fn = WyeCore.Utils.buildCodeText(verbName+"_stream" + str(ix), codeDescr)
                parFnText += cd + fn

            # create start routine for this parallel verb
            # define start last since it refs the run routines created above
            parFnText +=     " def " + verbName + "_start_rt(stack):\n"
            #parFnText +=     "  print('" + verbName + "_start_rt')\n"
            parFnText +=     "  f = Wye.parallelFrame(" + libName + "." + verbName + ",stack)\n"
            for ix in range(nStreams):
                parFnText += "  stk = []\n"                 # stack for parallel stream
                parFnText += "  fs = Wye.codeFrame(WyeCore.ParallelStream, stk)\n" # frame for stream
                #parFnText += "  print('gen parallel frame.  Old frame var: ', dir(f.vars))\n  print('   new frame var: ', dir(fs.vars))\n"
                parFnText += "  fs.vars = f.vars\n"
                parFnText += "  fs.params = f.params\n"
                parFnText += "  fs.parentFrame = f\n"
                parFnText += "  fs.run = " + libName + "."  + libName + "_rt." + verbName + "_stream"+str(ix)+"_run_rt\n"
                parFnText += "  stk.append(fs)\n"           # put stream frame at top of stream's stack
                parFnText += "  f.stacks.append(stk)\n"     # put stack on our frame's list of stream stacks

            #parFnText +=     "  print('f.stacks', f.stacks)\n"
            #parFnText +=     "  print('f.verb', f.verb)\n"
            parFnText +=     "  return f\n"

            # print("buildParallelText complete.  parFnText=\n"+parFnText[0])
            return ("", parFnText)

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
                            if val.autoStart:
                                classStr = libName + "." + libName + "." + val.__name__
                                #print("buildLib Startobj: ", classStr)
                                WyeCore.World.startObjs.append(classStr)

                        # add pointer from verb class to parent library class
                        setattr(val, "library", libClass)

            # if there's code to build for the library, doit
            if doBuild:
                codeStr += parFnStr         # tack parallel code on end of regular code
                codeStr += 'setattr('+libName+', "'+libName+'_rt", '+libName+'_rt)\n'

                # DEBUG PRINT GENERATED CODE
                # If compiled Wye code, print it
                #if WyeCore.debugListCode:
                #    print("\nlib '"+libClass.__name__+"' code=")
                #    lnIx = 1
                #    for ln in codeStr.split('\n'):
                #        print("%2d "%lnIx, ln)
                #        lnIx += 1

                # compile the runtime class containing methods for all the verb runtimes
                code = compile(codeStr, "<string>", "exec")
                # exec the lib method - contains one line to setattr the lib_rt class to the library
                # so all the verb functions are available at runtime
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

        # return all the verbs in a library
        def getLibEntries(lib):
            retLst = []
            for attr in dir(lib):
                if attr != "__class__":
                    verb = getattr(lib, attr)
                    if inspect.isclass(verb) and hasattr(verb, "mode"):
                        retLst.append(verb)
            return retLst


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
    # At compile time each code block is compiled into its own runtime stream function.
    # Then a custom start function is defined for the main verb that creates a separate code frame for each
    # code block with ParallelStream as a verb.  The start function fills the stream's frame vars and params
    # tuples with references to the parent frame vars and params.
    # It also puts a custom "run" attribute in each stream frame that points to that code block's runtime stream
    # function.
    #
    # At runtime the ParallelStream verb "run" function calls through the frame's custom run attribute to the
    # appropriate runtime code.
    #
    # Whether this is an elegant or an ugly hack is moot 'cause that's how it works.  So there.
    class ParallelStream:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        parallelStreamFlag = True       # flag this as special verb (consider alternative way to encode parallel stream headers)
        paramDescr = ()
        varDescr = ()

        def start(self, stack):
            #print("ParallelStream start: stack ", stack)
            return Wye.codeFrame(WyeCore.ParallelStream, stack)

        def run(frame):
            frame.run(frame)
