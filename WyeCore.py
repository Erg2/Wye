# Wye Core
# static single class lib

#
# license: We don't need no stinking license
# This is prototype code.  If it blows up your nuclear reactor, that is your dumb fault.
#

from Wye import Wye
import inspect      # for debugging
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.showbase import Audio3DManager
import sys, os
import math
import pygame.midi
import time
import traceback
from importlib.machinery import SourceFileLoader    # to load library from file

# WyeCore class is a static container for the core Wye Classes that is never instantiated

# Building it this way prevents the editor from accidentally writing over the core because
# editing one of the contained libList will create an external file for just that lib.
# Incorporating the result requires external editing.


'''
Wye Overview

libraries and words in them are static
All refs to a lib or word within a lib or word have to be 3rd person through the core's list of known libraries
(WyeCore.libs.lib.word.xxx) rather than self.  Since there is no instantiated class, there is no self.  
Note that frame.verb.xxx works nicely as shorthand.
All context (local variables, parameters passed in, and PC (which is used by multi-pass word) is on the 
stack frame that is returned by word.start.

Structure of a word:
    The library verb that defines the word has
        Settings: like Wye.mode.SINGLE for a verb that operates in a single display cycle or Wye.mode.MULTI_CYCLE
        for a verb that is run on each cycle until it reaches a termination condition and returns SUCCESS or FAIL, or
        Wye.mode.PARALLEL which has multiple streams of MULTI_CYCLE running in sort-of parallel. (done manually in 
        succession, not in separate parallel threads)
        
        ParamDescr: defines the parameters that are passed to the verb when it is run.  When a verb is called, each 
        parameter value is attached to the verb's instance frame as a parameter attribute.  
        For example, if the verb has a parameter called "passedValue" it would be on the verb instance's frame as 
        frame.parameter.passedValue[0]. Note that the value is in a single element list so it can be passed by 
        reference as a parameter to a lower-level verb.
        
        VarDescr: defines the per-instance variables that are passed to the verb when it is run.  Each variable value
        is attached to the verb's instance frame as a variable attribute, such as frame.vars.myVariable[0].  Again, the 
        value is stored in a single element list so it can be passed by reference to a lower-level verb.
        
        CodeDescr: contains the Wye code description of the verb's runtime code.  This is compiled when the verb's 
        library is loaded into Wye.
        
        Start: Each verb has a start function that creates the verb-specific frame.  One of the critical start functions
        is initializing any list variables in the frame with their unique lists.  The start function is passed the
        stack that the instance of the verb will use if it calls lower-level verbs.  When start returns to the caller, 
        the caller will fill in the values in the parameters section of the frame before calling the verb's run function.
        
        Run: Each verb has a run function that is called when the verb is executed.  The run function is passed the
        frame.  All the verb's runtime context is stored in the frame.  No runtime changes are made to the verb in the
        library.

Basic concept for executing a word in a library:
    wordFrame =  word.start(stack)
        The frame holds the local storage for this exec of word.  The most used attributes are the
        calling params and local variable values.

        if a word uses local variables the word's frame.vars is built automatically from the
        word's varDescr.  

        Pass-by-referene: Each variable is a separate list so it can be passed to another word in that word's 
        stackframe.params and the var can be updated by that word.
        All vars are filled in with initial values by the frame on instantiation.
        example: wordFrame.vars.one[0] = "one", and wordFrame.vars.twoList[0] = [2, 2, 2]
    wordFrame.params.append( [p1], .. )
        If the word being called requires any params passed in, the caller has to set them up.
        Each parameter is wrapped in a list so that its value can be changed
        functions return their value in the first parameter.  For example the caller would init frame.params.p1[0] to "one".
    word.run(wordFrame)
        If the word is a function, the return value is in the first parameter

Compiling 
    Two stages, first translating Wye code to Python code, and then compiling Python code to runtime code.  This is 
    done on library load so the overhead of compiling is done once.  

    If there is a codeDescr = (..wye-code..) then the code will be translated to Python.

    Wye code is in nested tuples in the form ("operator", (..param..), (..param..)) where the param list can be
    zero or more params which are recursively tuples.  Note that a tuple or list with just one entry must end with 
    a comma (entry,) or python will optimize the tuple or list away.
    (..param..) can be either ("Code", a-constant) or ("lib.word", (..param..)) to recurse to a function that will
    supply the parameter.  (gross over-simplification, expand later to cover expressions, if then expressions, loops, 
    etc.)

    The Python output is put in a string under code.

    All code attributes found in classes in the library are compiled to methods under the dynamically created 
    class libName_rt.  Each word's runtime is def'd as wordName_run_rt.  

    The word itself has a run method that calls libName_rt.wordName_run_rt(frame).  Words that have parallel streams 
    have multiple run methods, one per stream.

    Note: there is the risk that the string holding the Python code will get too long (the internal limit is not clearly 
    defined).  If that happens then the compile loop could compile each word's code individually, but that would be much 
    slower.  Or it could process words in chunks that are small enough to fit within the string limit.

    Note: a runtime optimization would be to reparent the rt methods back to each word so there was no indirection
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

    # DEBUG - SHOW COMPILED CODE
    debugListCode = False       # true to list Python code generated from Wye code

    picker = None   # object picker object
    base = None     # panda3d base - set by application
    focusManager = None # dialog input field focus manager

    lastIsNothingToRun = False  # Debug: used to print "nothing to do" only on transition to nothing to do

    versionText = None

    libLoadList = ["WyeLib.py", "WyeUILib.py", "WyeUIUtilsLib.py", "Wye3dObjsLib.py"]  # list of lib files to load on start.  libList on cmd line added to it

    HUD = None      # HUD dialog, if any
    winWidth = 0        # updated on resize
    winHeight = 0

    # interaction recording callbacks
    keyCallbacks = []
    controlKeyCallbacks = []
    mouseMoveCallbacks = []
    mouseWheelCallbacks = []

    class libs:
        pass

    class WyeAudioSound:
        def __init__(self, sound):
            self.sound = sound
        def play(self):
            if Wye.soundOn:
                self.sound.play()

        def set3dAttributes(self, p1, p2, p3, v1, v2, v3):
            self.sound.set3dAttributes(p1, p2, p3, v1, v2, v3)

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
        parallelStreamFlag = True  # flag this as special verb (consider alternative way to encode parallel stream headers)
        paramDescr = ()
        varDescr = ()

        def start(self, stack):
            # print("ParallelStream start: stack ", stack)
            return Wye.codeFrame(WyeCore.ParallelStream, stack)

        def run(frame):
            frame.run(frame)

    # Midi output class
    midiInitialized = False

    # midi
    # pygame.midi.init()
    # player = pygame.midi.Output(0)
    # for ins in range(127):
    #    print("Midi Instrument", ins)
    #    player.set_instrument(ins)
    #    player.note_on(64, 64)
    #    time.sleep(1)
    #    player.note_off(64, 64)
    # del player
    # pygame.midi.quit()
    class WyeMidi(pygame.midi.Output):
        # device_id 0..127, latency, buffer_size
        def __init__(self, *args):
            if not WyeCore.midiInitialized:
                pygame.midi.init()
            super().__init__(*args)

        # instrument_id 0..127, channel
        def setInstrument(self, *args):
            Wye.midiLastIns = args[0]       # risky
            super().set_instrument(*args)

        # note 0..127?, velocity 0..127, channel
        def noteOn(self, *args):
            super().note_on(*args)

        # start note and put frame on queue to stop it after duration
        def playNote(self, instrument, note, velocity, duration):
            Wye.midiLastIns = instrument
            Wye.midi.setInstrument(instrument)
            super().note_on(note, velocity)
            start = time.time()
            end = start + duration
            frm = WyeCore.World.startActiveObject(WyeCore.NoteDone)
            frm.params.stopTime = [end]
            frm.params.note = [note]
            frm.instrument = [instrument]

        # note, velocity 0..127, channel
        def noteOff(self, *args):
            super().note_off(*args)

    class NoteDone:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("stopTime", Wye.dType.INTEGER, Wye.access.REFERENCE),
                      ("note", Wye.dType.INTEGER, Wye.access.REFERENCE),
                      ("instrument", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("stopTime", Wye.dType.INTEGER,0),
                    ("note", Wye.dType.INTEGER, Wye.access.REFERENCE),
                    ("instrument", Wye.dType.INTEGER, Wye.access.REFERENCE))

        def start(stack):
            # print("NoteDone started")
            return Wye.codeFrame(WyeCore.NoteDone, stack)

        def run(frame):
            match(frame.PC):
                case 0:
                    frame.vars.stopTime[0] = frame.params.stopTime[0]
                    frame.vars.note[0] = frame.params.note[0]
                    frame.PC += 1
                case 1:
                    if time.time() > frame.vars.stopTime[0]:
                        oldIns = Wye.midiLastIns
                        Wye.midi.setInstrument(frame.vars.instrument[0])
                        Wye.midi.noteOff(frame.vars.note[0], 64)
                        Wye.midi.setInstrument(oldIns)
                        frame.status = Wye.status.SUCCESS


    class WyeAudio3d(Audio3DManager.Audio3DManager):
        def __init__(self, sfx, camera):
            super().__init__(sfx, camera)

        def loadSfx(self, name):
            sfx = super().loadSfx(name)
            #print("Loaded Sfx", sfx)
            return WyeCore.WyeAudioSound(sfx)

    class World(Wye.staticObj):
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = ()
        codeDescr = ()

        audio3d = None
        keyHandler = None           # keyboard handler slot
        mouseHandler = None         # mouse handler slot
        debugger = None             # no debugger running
        editMenu = None             # no edit menu running
        pasteMenu = None            # no pasteMenu running
        objEditor = None            # editor of Wye objects
        mainMenu = None             # no main menu currently being displayed
        copyPasteManager = None       # cut/paste manager goes here
        mouseCallbacks = []         # any function wanting mouse events
                                    #   Control seems to jam mouse events,
                                    #   (neither mouse nor control-mouse gets called)
                                    #   So do mouse manually.  Sigh

        # used during user compile of verb/lib
        compileErrorTitle = ""
        compileErrorText = ""
        noBuildErrors = True           # only display one error, then stop
        listing = ""

        # universe specific
        dlight = None           # global directional light
        dLightPath = None
        libList = []
        libDict = {}            # lib name -> lib lookup dictionary
        startObjs = []
        objStacks = []          # objects run in parallel so each one gets a stack
        objKillList = []        # frames of objects to be removed from the active list at the end of the current display cycle
        objTags = {}            # map of graphic tags to object frames

        eventCallbackDict = {}              # dictionary of event callbacks
        repeatEventCallbackDict = {}        # dictionary of repeated event frames
        _repEventAddList = []               # can't add event frame from within event callback, so queue here
        _repEventDelList = []               # can't del event frame from within event callback, so queue here

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

                # import libraries
                for libFile in WyeCore.libLoadList:
                    # print("Load lib '", libFile, "'")
                    libName = os.path.splitext(os.path.basename(libFile))[0]
                    # print("Load ", libName)

                    # path = libFile
                    path = WyeCore.Utils.resourcePath(libFile)[2:]
                    # print("Load library '" + path + "'")
                    try:
                        libModule = SourceFileLoader(libName, path).load_module()
                        # print("libModule ", libModule)
                        libClass = getattr(libModule, libName)
                        # print("add libClass", libClass, " to libList")
                        WyeCore.World.libList.append(libClass)
                        # print("Loaded library ", libName, " from file ", path, " into lib class ", libClass)
                    except:
                        #    pass    # if fail to load module, keep going
                        print("Failed to load class ", libName, " From file ", path)
                        ex = sys.exception()
                        traceback.print_exception(ex)

                # Lighting
                WyeCore.World.dlight = DirectionalLight('dlight')
                WyeCore.World.dlight.setColor((1, 1, 1, 1))  # (0.8, 0.8, 0.5, 1))
                WyeCore.World.dlightPath = render.attachNewNode(WyeCore.World.dlight)
                WyeCore.World.dlightPath.setHpr(Wye.startLightAngle[0], Wye.startLightAngle[1], Wye.startLightAngle[2])
                render.setLight(WyeCore.World.dlightPath)

                # Fog

                myFog = Fog("Fog Name")
                myFog.setColor(0, 0, 0)
                myFog.setExpDensity(0.001)
                base.render.setFog(myFog)

                ####### Test 3d text
#
                text = TextNode('node name')
                #text.setWordwrap(7.0)
                text.setText("Welcome to\nWye " + Wye.version)
                text.setTextColor(1, 1, 1, 1)
                text.setAlign(TextNode.ACenter)
                # text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
#
                text.setCardColor(0, 0, 0, 1)
                text.setCardAsMargin(.1, .2, .1, .1)  # extend beyond edge of text (-x, +x, -y, +y)
                text.setCardDecal(True)
                #
                # create 3d text object
                WyeCore.World.versionText = NodePath(text.generate())  # supposed to, but does not, generate pickable node
                # _3dText = NodePath(text)
                WyeCore.World.versionText.reparentTo(render)
                WyeCore.World.versionText.setScale(.2, .2, .2)
                WyeCore.World.versionText.setPos(-.5, 17, 4)
                WyeCore.World.versionText.setTwoSided(True)

                WyeCore.World.versionText.node().setIntoCollideMask(GeomNode.getDefaultCollideMask())

                ####### 3d sound

                #Wye.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                Wye.audio3d = WyeCore.WyeAudio3d(base.sfxManagerList[0], base.camera)

                ######## Midi sound

                Wye.midi = WyeCore.WyeMidi(0)

                # test midi sound
                #Wye.midi.playNote(50, 45,64,.25)
                #time.sleep(.1)
                #Wye.midi.playNote(51, 55,64,.5)
                #time.sleep(.1)
                #Wye.midi.playNote(52, 65, 64, .75)

                # test 3d sound
                snd = Wye.audio3d.loadSfx("WyePop.wav")
                Wye.audio3d.attachSoundToObject(snd, WyeCore.World.versionText)

                ###########

                # set initial cam position
                base.camera.setPos(Wye.startPos[0], Wye.startPos[1], Wye.startPos[2])
                # print("camPos",base.camera.getPos())

                ###########

                # put rep exec obj on obj list
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
                    #print("Build", lib)
                    lib._build()  # build all Wye code segments in code words

                # start focus manager for UI
                if hasattr(WyeCore.libs, "WyeUILib"):
                    #print("Set up focus manager")
                    WyeCore.Utils.setFocusManager(WyeCore.libs.WyeUILib.FocusManager)
                    #print("FocusManager create MouseHandler")
                    WyeCore.libs.WyeUILib.FocusManager._mouseHandler = WyeCore.libs.WyeUILib.FocusManager.MouseHandler()

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

                # started them, clear list
                WyeCore.World.startObjs.clear()

                # set up for text input events
                WyeCore.World.keyHandler = WyeCore.World.KeyHandler()

                #print("start CameraControl")
                WyeCore.World.mouseHandler = WyeCore.libs.WyeUILib.CameraControl()

                # create picker object for object selection events
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

                # set up editor
                WyeCore.World.objEditor = WyeCore.libs.WyeUILib.ObjEditCtl()

                # set up cut/paste manager
                WyeCore.World.copyPasteManager = WyeCore.libs.WyeUILib.CopyPasteManager()

                # WyeCore.picker.makePickable(_3dText)
                # tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
                # _3dText.setTag("wyeTag", tag)

                # start HUD
                WyeCore.HUD = WyeCore.World.startActiveObject(WyeCore.libs.WyeUILib.MainHUDDialog)

                #print("worldRunner done World Init")

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
                    if not Wye.UITest and base.mouseWatcherNode.hasMouse():
                        x = base.mouseWatcherNode.getMouseX()
                        y = base.mouseWatcherNode.getMouseY()
                        mb1 = base.mouseWatcherNode.isButtonDown(MouseButton.one())
                        mb2 = base.mouseWatcherNode.isButtonDown(MouseButton.two())
                        mb3 = base.mouseWatcherNode.isButtonDown(MouseButton.three())
                        shift = base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.shift())
                        ctrl = base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control())
                        alt = base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt())
                        WyeCore.World.mouseHandler.mouseMove(x,y, mb1, mb2, mb3, shift, ctrl, alt)

                # debug
                stackNum = 0
                ranNothing = True  # pessimist
                clearStackList = False      # no empty stacks found so far
                for stack in WyeCore.World.objStacks:
                    sLen = len(stack)
                    if sLen > 0:  # if there's something on the stack
                        ranNothing = False  # found something to execute

                        # run the frame furthest down the stack
                        frame = stack[-1]

                        # if world paused, only run critical code and code being debugged
                        if Wye.breakAll:
                            if not hasattr(stack[0], "systemObject") and stack[0].breakCt == 0:
                                #print("breakAll don't exec stack[0]", stack[0].verb.__name__, " obj", frame.verb.__name__, " stack[0].breakpt", stack[0].breakpt)
                                #if stack[0].verb.__name__ == "Dialog":
                                #    print("  ", stack[0].params.title[0])
                                continue
                        if frame.status == Wye.status.CONTINUE:
                            try:
                                #print("Run ", frame.verb.__name__)
                                if Wye.debugOn:
                                    Wye.debug(frame, "worldRunner run: stack "+ str(stackNum)+ " verb '"+ frame.verb.__name__+ "' PC "+ str(frame.PC))
                                else:
                                    # print("WorldRun: run", frame.verb.__name__, frame.params.title[0] if hasattr(frame.params, "title") else " ", " status", Wye.status.tostring(frame.status))
                                    # run the object frame.  If it throws an error, kill that object stack
                                    frame.verb.run(frame)
                                    # print("WorldRun: after run", frame.verb.__name__, frame.params.title[0] if hasattr(frame.params, "title") else " ", " status", Wye.status.tostring(frame.status))
                            except Exception as e:
                                WyeCore.World.stopActiveObject(frame)
                                if Wye.devPrint:
                                    print("WorldRun: ERROR verb ", frame.verb.__name__, " with error:\n", str(e))
                                    traceback.print_exception(e)
                                title = "Runtime Error a"
                                msg = "Object '"+frame.verb.__name__+", died with error\n"+str(e)+"\n"+traceback.format_exc()
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)

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
                                    # print("WorldRun: child done, run parent", pFrame.verb.__name__, " ", frame.verb.__name__, frame.params.title[0] if hasattr(frame.params, "title") else " ")
                                    # bottom frame done, run its parent
                                    # If it throws an error, kill that object stack
                                    try:
                                        pFrame.verb.run(pFrame)  # parent will remove child frame
                                    except Exception as e:
                                        # print("WorldRun: ERROR verb ", frame.verb.__name__, " with error:\n", str(e))
                                        WyeCore.World.stopActiveObject(frame)
                                        traceback.print_exception(e)
                                        title = "Runtime Error b"
                                        msg = "Object '"+frame.verb.__name__+", died with error\n"+str(e)+"\n"+traceback.format_exc()
                                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)

                            else:  # no parent frame, do the dirty work ourselves
                                # print("worldRunner: done with top frame on stack.  Clean up stack")
                                stack.remove(frame)
                    else:
                        clearStackList = True

                    stackNum += 1

                if clearStackList:
                    ii = 0
                    while ii < len(WyeCore.World.objStacks):
                        if len(WyeCore.World.objStacks[ii]) == 0:
                            WyeCore.World.objStacks.pop(ii)
                        else:
                            ii += 1


                if ranNothing:
                    # print("ranNothing ", ranNothing, " and WyeCore.lastIsNothingToRun", WyeCore.lastIsNothingToRun)
                    if not WyeCore.lastIsNothingToRun:
                        WyeCore.lastIsNothingToRun = True
                        # print("worldRunner stack # ", stackNum, " nothing to run")

                # if active object completed, remove the stack it is on from run list
                if len(WyeCore.World.objKillList) > 0:
                    for frame in WyeCore.World.objKillList:
                        if frame:  # if it still exists
                            #origFrame = frame
                            # if in parallel exec frame, go up to top parent
                            if len(frame.SP) > 0:
                                while frame.SP[0].verb.__name__ == "ParallelStream":
                                    frame = frame.SP[0].parentFrame
                            if frame:  # if it still exists
                                if frame.SP in WyeCore.World.objStacks:
                                    WyeCore.World.objStacks.remove(frame.SP)
                                # DEBUG
                                #else:
                                #    print("StopActiveObject: frame", origFrame.verb.__name__, " not on World exec list")
                    WyeCore.World.objKillList.clear()

            return Task.cont  # tell panda3d we want to run next frame too

        # Start object verb and put it on active list so called every display cycle
        # return its stack frame
        def startActiveObject(obj):
            stk = []            # create stack to run object on
            frame = obj.start(stk)  # start the object and get its stack frame
            if frame.verb.mode == Wye.mode.SINGLE_CYCLE:
                frame.verb.run(frame)
            else:
                stk.append(frame)       # put obj frame on its stack
                # frame.params = [[0], ]  # place to put return param
                WyeCore.World.objStacks.insert(0,stk)  # put obj's stack on list and put obj's frame on the stack
            return frame

        # Put object instance frame on active list
        # caller already created stack and started the object
        # (required when caller needs to pass params to the object)
        def startActiveFrame(frame):
            if frame.verb.mode == Wye.mode.SINGLE_CYCLE:
                frame.verb.run(frame)
            else:
                # make sure frame is on its own stack
                if len(frame.SP) == 0 or not frame.SP[-1] == frame:
                    frame.SP.append(frame)
                WyeCore.World.objStacks.append(frame.SP)  # put obj's stack on exec list
            #print("startActiveFrame: put", frame.verb.__name__, " ", frame.params.title[0] if frame.verb == WyeCore.libs.WyeUILib.Dialog else " ", " ", id(frame), " stack on objStacks")
            #print("startActiveFrame stacks", len(WyeCore.World.objStacks), " ", [stack[0].verb.__name__+" "+str(id(stack[0])) for stack in WyeCore.World.objStacks])
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


        # find frame entry in rep event dict
        # remove it from rep dict and from event dict
        # >> bad to call this from within the repeated event callback
        def clearRepeatEventCallback(frameTag):
            if frameTag in WyeCore.World.repeatEventCallbackDict:
                WyeCore.World._repEventDelList.append(frameTag)
                #print("clrRepEvt: frame ", frame, " evt ", eventName, " tag ", tag, " frmID ", frameID)
                #print("clrRepEvt: callbackDict ", WyeCore.World.eventCallbackDict)
            else:
                print("Error: clearRepeatEventCallback failed to find frameTag '", frameTag,
                      "' in WyeCore.World.repeatEventCallbackDict")

        # key event dispatcher
        # Instantiated class
        # (panda3d key event callback)
        class KeyHandler(DirectObject):
            def __init__(self):
                base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
                self.accept('keystroke', self.keyFunc)
                self.accept('keystroke-repeat', self.keyFunc)
                self.accept('arrow_right', self.controlKeyFunc, [Wye.ctlKeys.RIGHT])
                self.accept('arrow_left', self.controlKeyFunc, [Wye.ctlKeys.LEFT])
                self.accept('arrow_right-repeat', self.controlKeyFunc, [Wye.ctlKeys.RIGHT])
                self.accept('arrow_left-repeat', self.controlKeyFunc, [Wye.ctlKeys.LEFT])
                self.accept('control-arrow_right', self.controlKeyFunc, [Wye.ctlKeys.RIGHT])
                self.accept('control-arrow_left', self.controlKeyFunc, [Wye.ctlKeys.LEFT])
                self.accept('control-arrow_right-repeat', self.controlKeyFunc, [Wye.ctlKeys.RIGHT])
                self.accept('control-arrow_left-repeat', self.controlKeyFunc, [Wye.ctlKeys.LEFT])
                self.accept('arrow_up', self.controlKeyFunc, [Wye.ctlKeys.UP])
                self.accept('arrow_up-repeat', self.controlKeyFunc, [Wye.ctlKeys.UP])
                self.accept('control-arrow_up', self.controlKeyFunc, [Wye.ctlKeys.UP])
                self.accept('control-arrow_up-repeat', self.controlKeyFunc, [Wye.ctlKeys.UP])
                self.accept('arrow_down', self.controlKeyFunc, [Wye.ctlKeys.DOWN])
                self.accept('arrow_down-repeat', self.controlKeyFunc, [Wye.ctlKeys.DOWN])
                self.accept('control-arrow_down', self.controlKeyFunc, [Wye.ctlKeys.DOWN])
                self.accept('control-arrow_down-repeat', self.controlKeyFunc, [Wye.ctlKeys.DOWN])
                self.accept('shift_down', self.controlKeyFunc, [Wye.ctlKeys.SHIFT_DOWN])
                self.accept('shift_up', self.controlKeyFunc, [Wye.ctlKeys.SHIFT_UP])
                self.accept('ctl_down', self.controlKeyFunc, [Wye.ctlKeys.CTL_DOWN])
                self.accept('ctl_up', self.controlKeyFunc, [Wye.ctlKeys.CTL_UP])
                self.accept('delete', self.controlKeyFunc, [Wye.ctlKeys.DELETE])
                self.accept('delete-repeat', self.controlKeyFunc, [Wye.ctlKeys.DELETE])
                self.accept('home', self.controlKeyFunc, [Wye.ctlKeys.HOME])
                self.accept('end', self.controlKeyFunc, [Wye.ctlKeys.END])
                self.accept('escape', self.controlKeyFunc, [Wye.ctlKeys.ESCAPE])
                self.accept('enter', self.controlKeyFunc, [Wye.ctlKeys.ENTER])
                self.accept("f1", self.controlKeyFunc, [Wye.ctlKeys.F1])
                self.accept("f11", self.controlKeyFunc, [Wye.ctlKeys.F11])
                self.accept("window-event", self.resize)
                self.accept("control-w", self.controlKeyFunc, [Wye.ctlKeys.CTL_W])
                self.accept("control-h", self.controlKeyFunc, [Wye.ctlKeys.CTL_H])
                self.accept("control-p", self.controlKeyFunc, [Wye.ctlKeys.CTL_P])


            def resize(self, dummy):
                if WyeCore.HUD and WyeCore.HUD.vars.dlgFrm[0]:
                    width = base.win.getProperties().getXSize()
                    height = base.win.getProperties().getYSize()
                    if width != WyeCore.winWidth or height != WyeCore.winHeight:
                        rat = width/height
                        if rat >= 1:
                            pos = [-6 * rat, Wye.UI.NOTIFICATION_OFFSET, 5.8]
                        else:
                            pos = [-6, Wye.UI.NOTIFICATION_OFFSET, 5.85 * 1/rat]
                        #print("Set HUD pos", pos, " win size", width, height)
                        #print("HUD", WyeCore.HUD.verb.__name__, " params", dir(WyeCore.HUD.params))
                        WyeCore.HUD.vars.dlgFrm[0].params.position[0] = pos
                        WyeCore.winWidth = width
                        WyeCore.winHeight = height

            def controlKeyFunc(self, keyID):
                #print("controlKeyFunc key", Wye.ctlKeys.tostring(keyID))
                # external callbacks
                # If callback(s) return True, don't process any further
                usedCtlKey = False
                if len(WyeCore.controlKeyCallbacks) > 0:
                    for callback in WyeCore.controlKeyCallbacks:
                        usedCtlKey = usedCtlKey or callback(self)
                if usedCtlKey:
                    return

                #print("Control key", keyID)
                if WyeCore.focusManager:
                    WyeCore.focusManager.doKey(keyID)

            def keyFunc(self, keyname):
                # external callbacks
                # If callback(s) return True, don't process any further
                usedKey = False
                if len(WyeCore.keyCallbacks) > 0:
                    for callback in WyeCore.keyCallbacks:
                        usedKey = usedKey or callback(self)
                if usedKey:
                    return

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
            paramDescr = ()
            varDescr = ()

            def start(stack):
                f = Wye.codeFrame(WyeCore.World.repeatEventExecObj, stack)
                f.systemObject = True         # not stopped by debugger or breakAll
                return f

            # run event frames every display frame
            # it is up to the event frames to wait on whatever event they have in mind
            def run(frame):
                delList = []
                #print("repEventObj run: Event dict:", WyeCore.World.repeatEventCallbackDict)

                # if repeat events queued up to be added or removed
                if len(WyeCore.World._repEventAddList) > 0:
                    for repEvt in WyeCore.World._repEventAddList:
                        WyeCore.World.repeatEventCallbackDict[repEvt[3]] = repEvt
                    WyeCore.World._repEventAddList.clear()
                if len(WyeCore.World._repEventDelList) > 0:
                    for repEvt in WyeCore.World._repEventDelList:
                        del WyeCore.World.repeatEventCallbackDict[repEvt]
                    WyeCore.World._repEventDelList.clear()

                evtIx = 0       # debug
                for evtID in WyeCore.World.repeatEventCallbackDict:
                    evt = WyeCore.World.repeatEventCallbackDict[evtID]
                    #print("repeatEventExecObj run: process evtID", evtID, " evt", evt)
                    if len(evt[0]) > 0:
                        #print("repeatEventExecObj run: process evt", evt)
                        evtFrame = evt[0][-1]
                        # if world paused, only run critical code or code being debugged
                        if Wye.breakAll:
                            if not hasattr(evt[0][0], "systemObject") and evt[0][0].breakCt == 0:
                                #print("repEvt breakAll don't exec", evt[0][0].verb.__name__, " evt breakpt", evt[0][0].breakpt)
                                #if evt[0][0].verb.__name__ == "Dialog":
                                #    print("  ", evt[0][0].params.title[0])
                                continue
                            #else:
                            #    print("repEvt breakAll exec sysObj stack", evt[0][0].verb.__name__, " run obj", evtFrame.verb.__name__)

                        #print("repEventObj run: evtFrame=", evtFrame)
                        # run bottom of stack unless done
                        if evtFrame.status == Wye.status.CONTINUE:
                            #print("repEventObj run bot of stack evt: ", evtIx, " verb ", evtFrame.verb.__name__, " PC ", evtFrame.PC)
                            evtFrame.eventData = (evtID, evt[2])        # user data
                            try:
                                if Wye.debugOn:
                                    Wye.debug(evtFrame, "RepeatEvent run:"+ evtFrame.verb.__name__+ " evt data "+ str(evtFrame.eventData))
                                else:
                                    #print("run", evtFrame.verb.__name__)
                                    evtFrame.verb.run(evtFrame)
                            except Exception as e:
                                print("WorldRunrepeatEventExecObj: ERROR verb ", evtFrame.verb.__name__, " with error:\n", str(e))
                                delList.append(evt[3])          # don't run this again
                                traceback.print_exception(e)
                                title = "Runtime Error c"
                                msg = "Object '" + frame.verb.__name__ + ", died with error\n" + str(
                                    e) + "\n" + traceback.format_exc()
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)
                        # bottom of stack done, run next up on stack if any
                        elif len(evt[0]) > 1:
                            dbg = evt[0][-1]
                            #print("Bot of stack", dbg.verb.__name__, " status", Wye.status.tostring(dbg.status))
                            evtFrame = evt[0][-2]
                            evtFrame.eventData = (evtID, evt[2])        # user data
                            try:
                                if Wye.debugOn:
                                    Wye.debug(evtFrame, "RepeatEvent done, run parent:"+ evtFrame.verb.__name__+ " evt data"+ str(evtFrame.eventData))
                                else:
                                    #print("run", evtFrame.verb.__name__)
                                    #print("repEventObj bot of stack done, run caller evt: ", evtIx, " verb ", evtFrame.verb.__name__, " PC ", evtFrame.PC)
                                    evtFrame.verb.run(evtFrame)
                            except Exception as e:
                                print("WorldRunrepeatEventExecObj: ERROR verb ", evtFrame.verb.__name__,
                                      " with error:\n", str(e))
                                WyeCore.World.stopActiveObject(evtFrame)
                                traceback.print_exception(e)
                                title = "Runtime Error d"
                                msg = "Object '" + frame.verb.__name__ + ", died with error\n" + str(
                                    e) + "\n" + traceback.format_exc()
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)
                            # On parent error, bail out - TODO - consider letting its parent handle error
                            if evtFrame.status == Wye.status.FAIL and len(evt[0]) > 1:
                                #print("repEventObj run: -2 evt ", evtIx, " fail, kill event")
                                delList.append(evt[3])  # save this entry's tag to delete when done
                        # if only one evtFrame on stack and it's done, remove event entry
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

            #WyeCore.World.registerMouseCallback(self.objSelectEvent)
            #self.accept('mouse1', self.objSelectEvent)
            #self.accept('control-mouse1', self.objSelectEvent)
            #self.accept('alt-mouse1', self.objSelectEvent)

            self.pickerEnable = True

        # this function is meant to flag an object as being somthing we can pick
        def makePickable(self, obj):
            #print("picker:  set 'pickable' on ", obj)
            obj.setTag('pickable', 'true')

        def makeNotPickable(self, obj):
            obj.setTag('pickable', 'false')

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
        # Note: it does not work with billboard nodes. Fails once the billboard rotates too far.  So we don't use them
        def getObjectHit(self, mpos):  # mpos is the position of the mouse on the screen
            global render

            #print("getObjectHit check mpos", mpos)

            self.pickedObj = None  # don't have an obj yet
            self.pickerRay.setFromLens(WyeCore.base.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(render)
            if self.queue.getNumEntries() > 0:
                #print("getObjectHit: ", self.queue.getNumEntries(), " entries in picker queue")
                self.queue.sortEntries()
                self.pickedObj = None
                for ii in range(self.queue.getNumEntries()):
                    #print("getObjectHit: Queue contains ", self.queue)
                    parent = self.queue.getEntry(ii).getIntoNodePath()
                    #print(" start obj", parent)
                    # go up the path looking for a pickable node
                    while parent != render:
                        # if pickable set false, done with this collision
                        #print(" obj", parent, " has pickable", parent.hasTag('pickable'), " is pickable", "True" if parent.getTag('pickable') else "False")
                        if parent.hasTag('pickable'):
                            if parent.getTag('pickable') == 'true':
                                wyeTag = parent.getTag('wyeTag')
                                #if wyeTag:
                                #    print("Clicked on pickable object", parent, " with wyeTag", wyeTag)
                                #else:
                                #    print("clicked on pickable object", parent)
                                #print(" picked object", parent)
                                self.pickedObj = parent
                                return parent
                            else:
                                #print(" pickable=false, skip obj", parent)
                                break;
                        else:
                            parent = parent.getParent()
            #print(" Nothing picked")
            return None

        def getPickedObj(self):
            return self.pickedObj

        # Wye object selection dispatcher
        # Check for object hit - check hit obj has obj tag - check for event for given obj tag
        def objSelectEvent(self, x, y):
            status = False
            if self.pickerEnable:
                self.getObjectHit(LPoint2f(x,y))
                if self.pickedObj:
                    wyeID = self.pickedObj.getTag('wyeTag')
                    #print("Clicked on ", self.pickedObj, " at ", self.pickedObj.getPos(), " wyeID ", wyeID)
                    if wyeID:
                        #print("Picked object: '", self.pickedObj, "', wyeID ", wyeID)
                        # if there's an object editor
                        if WyeCore.World.objEditor:
                            status = WyeCore.World.objEditor.tagClicked(wyeID)
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
                                #print("objSelectEvent: isPressed", isPressed, " ")
                                tagDict = WyeCore.World.eventCallbackDict["click"]
                                if wyeID in tagDict:
                                    #print(" Found ", len(tagDict[wyeID]), " callbacks for tag ", wyeID)
                                    # run through lists calling callbacks.
                                    #print("objSelectEvent: tagDict=", tagDict)
                                    evtLst = tagDict[wyeID]
                                    for evt in evtLst:
                                        frame = evt[0]
                                        data = evt[1]
                                        #print("objSelectEvent: on mouse 'click' inc frame ", frame.verb.__name__, " PC ", frame.PC)
                                        frame.PC += 1
                                        frame.eventData = (wyeID, data)        # user data
                                    del tagDict[wyeID] # remove tag from dict of active callbacks

                                    #print("objSelectEvent: click callback used tag", wyeID)
                                    #status = True

                                # if there's a callback for 'any' click event, call it
                                if "any" in tagDict:
                                    #print("Found ", len(tagDict[wyeID]), " callbacks for tag 'any'")
                                    for frame, data in tagDict.pop('any'):
                                        #print("ObjSelectEvent: 'any'", frame.verb.__name__)
                                        frame.PC += 1
                                        frame.eventData = (wyeID, data)
                                    #print("objSelectEvent: 'any' callback used tag", wyeID)


                                #else:
                                #    print("No click events waiting")
                #else:
                #    print("No object under mouse")
            #else:
            #    print("Object picking disabled")

            return status

    # General utilities for world building
    class Utils(Wye.staticObj):

        # get unique number
        def getId():
            global _nextId

            _nextId += 1
            if _nextId > 4294967295:        # wrap to pos signed int (ok only sorta unique)
                _nextsId = 1
                
            return _nextId

        def userLibPath():
            if getattr(sys, 'frozen', False):
                path = os.path.dirname(sys.executable) + "/WyeUserLibraries/"
            elif __file__:
                path = os.path.dirname(__file__) + "/WyeUserLibraries/"

            path = path.replace("\\","/")

            return path

        def resourcePath(relative_path):
            try:
                # look for PyInstaller temp folder
                base_path = sys._MEIPASS
            except:
                # nope, guess we're running from python or IDE
                base_path = os.path.abspath(".")

            path = base_path + "/" + relative_path

            path = path.replace("\\","/")

            #print("  return path '"+ path+"'")
            return path

        #def register3dObj(obj, frame):


        def setScreenSize(size):
            Wye.windowSize = size

            # screen size
            xSize = base.pipe.getDisplayWidth()
            ySize = base.pipe.getDisplayHeight()
            props = WindowProperties()

            # set size
            match (size):
                case Wye.winSize.FULL_SCREEN:  # full screen
                    props.setSize(xSize, ySize)
                    props.setOrigin(0, 0)
                case Wye.winSize.MAX_WINDOW:  # max window
                    props.setSize(xSize, ySize - 100)
                    props.setOrigin(1, 50)
                case Wye.winSize.SMALL_WINDOW:  # small window
                    props.setSize(1200, 800)
                    props.setOrigin(1, 50)

            #props.setFixedSize(1)
            base.win.requestProperties(props)


        # slerp between quats. Return q at time t
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

        # nlerp between quats at blend
        #
        # taken from:
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

        # recursively search for tuple in hierarchicaly list
        def findTupleParent(parent, tuple, level=0):
            #indent = "".join(["    " for l in range(level)])
            #print(indent + "findTupleParent: is", tuple, " in", parent)
            if parent is None or isinstance(parent, str):
                #print(indent+"tuple not found")
                return None
            if tuple in parent:
                return parent
            else:
                if len(parent) > 0:
                    for childTuple in parent:
                        #print(indent+"try child", childTuple)
                        foundParent = WyeCore.Utils.findTupleParent(childTuple, tuple, level+1)
                        if foundParent:
                            #print(" Found tuple ", tuple, " parent", foundParent)
                            return foundParent
                #else:
                #    print(indent+"zero len parent", parent)
            # if get here, failed to find tuple
            #print(indent+"tuple not found")
            return None

        # convert hierarchical tree of lists to nicely formatted tuple string
        def listToTupleString(hierList, level):
            tupleStr = ""
            indent = "      " + "".join(["  " for l in range(level)])      # indent by recursion depth
            # recurse for list
            if isinstance(hierList, list) or isinstance(hierList, tuple):
                tupleStr += "\n"+indent+"("
                first = True
                for elem in hierList:
                    if first:
                        tupleStr += WyeCore.Utils.listToTupleString(elem, level+1)
                        first = False
                    else:
                        tupleStr += ","+WyeCore.Utils.listToTupleString(elem, level+1)
                if len(hierList) ==1:
                    tupleStr += ","     # deal with stupid Python "feature" that single element tuples aren't tuples
                tupleStr += ")"
            # output element
            else:
                if hierList is None:
                    tupleStr += "None"
                elif isinstance(hierList, str):
                    if not hierList.isspace():
                        if "\n" in hierList:        # handle multi-line strings
                            tupleStr += "'''"+hierList+"'''"
                        else:
                            tupleStr += "\""+hierList+"\""
                else:
                    tupleStr += str(hierList)
            return tupleStr

        # recursively count nested lists in list
        def countNestedLists(tupleLst):
            count = 0
            if isinstance(tupleLst, list) or isinstance(tupleLst, tuple):
                for elem in tupleLst:
                    if isinstance(elem, list) or isinstance(elem, tuple):
                        count += 1
                        count += WyeCore.Utils.countNestedLists(elem)
            return count

        # search for match [b] in in list of form [[[a]], [[b]], ..]
        #
        # This is array.index(elem) for arrays where each element is wrapped in a list so it can be passed by reference.
        # Because each array element value is wrapped in a list, the elemeent's list can be passed to another function
        # which can update the contained value for the calling function.

        # This kind of array manually implements Pass By Reference for array elements.  But that means we need our own
        # array.index(elem) function.
        def refListFind(lst, tgt):
            # find index to this row's param
            ix = -1
            for ii in range(len(lst)):
                if lst[ii][0] == tgt:
                    ix = ii
                    break
            return ix


        # Take a Wye code description tuple and return compilable Python code
        # Resulting code pushes all the params to the frame, then runs the function
        # Recurses to parse nested param tuples
        #
        # Note: SINGLE_CYCLE and MULTI_CYCLE verb code is a list of verbs to process
        #       PARALLEL verb code is a list of verbs to split into separate parallel
        #       execution streams
        # caseNumList is a list so the number in it can be incremented (i.e. pass by ref)
        # fns is a list that parallel functions are added to
        def parseWyeTuple(wyeTuple, fNum, caseNumList):
            codeText = ""
            parFnText = ""
            retParam = None

            # Wye verb
            if wyeTuple[0] and wyeTuple[0] not in ["Var", "Const", "Var=", "Par=", "Expr", "Code", "CodeBlock"]:     # if there is a verb here
                #print("parseWyeTuple: lib.verb tuple", wyeTuple)
                #Pick it apart to locate lib and verb
                #print("parseWyeTuple parse ", wyeTuple)
                tupleParts = wyeTuple[0].split('.')
                if len(tupleParts) >= 2:
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

                                    # skip empty tuples (list ended in ",") and debug highlighting tuples
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
                                        if True: # paramIx < len(verbClass.paramDescr):
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

                                        if True: # paramIx < len(verbClass.paramDescr):
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
                                codeText += "    if not Wye.debugOn:\n"
                                #codeText += "     print('run',frame." + eff + ".verb.__name__)\n"
                                codeText += "     "+wyeTuple[0] + ".run(frame."+eff+")\n"
                                codeText += "    else:\n"
                                codeText += "     Wye.debug(frame."+eff+",'Exec run:'+frame."+eff+".verb.__name__)\n"
                                codeText += "    if frame."+eff+".status == Wye.status.FAIL:\n"
                                #codeText += "     print('verb ',"+eff+".verb.__name__, ' failed')\n"
                                codeText += "     frame.status = frame."+eff+".status\n     return\n"

                        # multi-cycle verbs create code that pushes a new frame on the stack which will run on the next display cycle and
                        # generates a new case statement in this verb that will pick up when the pushed frame completes
                        # Note that a parallel verb is a multi-cycle verb from the caller's perspective
                        case Wye.mode.MULTI_CYCLE | Wye.mode.PARALLEL:
                            # do not add to caseCodeDict 'cause it will be picked up in the next case
                            #print("WyeCore parseWyeTuple MULTI_CYCLE verb '"+ wyeTuple[0]+"'")
                            eff = "f"+str(fNum)         # eff is the name of the current frame.  fNum keeps frame names unique in nested code
                            # put local frames on the parent frame as attributes to keep local scope across display cycles
                            #codeText += "    if not hasattr(frame,'" + eff + "'):\n"
                            ##codeText += "     print('create frame attr "+eff+"')\n"
                            #codeText += "     setattr(frame,'" + eff + "',None)\n"
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
                                    if tupleKey is None or tupleKey in ["Var", "Const", "Var=", "Par=", "Expr", "Code", "CodeBlock"]:
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


                        # huh, wut?
                        case _:
                            print("INTERNAL ERROR: WyeCore parseWyeTuple verb ",wyeTuple," has unknown mode ",verbClass.mode)


                    retParam = verbClass.paramDescr[0][0] if (hasattr(verbClass, "paramDescr") and len(verbClass.paramDescr) > 0) else "None"
                else:
                    print("parseWyeTuple ERROR: expected lib.verb in", wyeTuple, " tupleParts=", tupleParts)

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

        # build run time code for a sequential verb (single or multiple cycle) or a single parallel stream
        # parse verb's code (list of Wye tuples) into Python code text
        def buildCodeText(name, codeDescr, verb, rowIxRef):
            #print("buildCodeText for", name)
            caseNumList = [0]   # current case stmt number - in list so called fn can increment it.  (pass by reference)
            labelDict = {}
            fwdLabelDict = {}

            if not hasattr(verb, "caseCodeDictLst"):
                #print("buildCodeText: create caseCodeDictList for verb", verb.__name__)
                verb.caseCodeDictLst = []
            caseCodeDict = {}
            verb.caseCodeDictLst.append(caseCodeDict)

            # define runtime method for this function
            codeText = " def " + name + "_run_rt(frame):\n  match frame.PC:\n   case 0:\n"
            parFnText = ""
            firstParam = None
            if len(codeDescr) > 0:
                for wyeTuple in codeDescr:
                    try:
                        caseStr = str(caseNumList[0])
                        if not caseStr in caseCodeDict:
                            caseCodeDict[caseStr] = []
                        caseCodeDict[caseStr].append(rowIxRef[0])
                        # label for branch/loop
                        if wyeTuple[0] == "Label":
                            caseNumList[0] += 1
                            labelDict[wyeTuple[1]] = caseNumList[0]

                            codeText += "    frame.PC += 1\n"
                            codeText += "   case " + str(caseNumList[0]) + ": #Label " + wyeTuple[1] + "\n    pass #2\n"

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
                            codeText += "   case " + str(caseNumList[0]) + ":\n    pass #5\n"
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
                    except Exception as e:
                        print("buildCodeText failed at tuple", wyeTuple, "\n", str(e))
                        traceback.print_exception(e)
                        if WyeCore.worldInitialized:
                            title = "Runtime Error e"
                            msg = "buildCodeText  failed at tuple '" + str(wyeTuple) + "\n" + str(e) + "\n" + traceback.format_exc()
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)
                    rowIxRef[0] += 1

                # stick debug struct on verb
                if not hasattr(verb, "caseCodeDictLst"):
                    verb.caseCodeDictLst = [caseCodeDict]
                else:
                    verb.caseCodeDictLst.append(caseCodeDict)

            # no code, make sure fn compiles
            else:
                codeText += "    pass #4\n"

            #print("buildCodeText complete.  codeText=\n"+codeText[0])
            return (codeText, parFnText)


        # build run time code for parallel function verb (always multi cycle)
        # which includes the inline runtime runction and the separate
        # parallel runtime functions
        def buildParallelText(libName, verbName, streamDescr, verb):
            #print("buildParallelText for", verbName)
            # build the parallel stream functions
            parFnText = ""
            nStreams = len(streamDescr)
            # create run function for each stream
            rowIxRef = [0]
            for ix in range(nStreams):
                #print("  Create ",verbName," stream ", ix)
                # note: streamDescr[ix][0] is user supplied name of this stream.  streamDescr[ix][1] is the codeDescr for the stream
                cd, fn = WyeCore.Utils.buildCodeText(verbName+"_" + streamDescr[ix][0] + "_" + str(ix), streamDescr[ix][1], verb, rowIxRef)
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
                parFnText += "  fs.vars = f.vars\n"
                parFnText += "  fs.params = f.params\n"
                parFnText += "  fs.parentFrame = f\n"
                parFnText += "  fs.run = " + libName + "."  + libName + "_rt." + verbName+"_" + streamDescr[ix][0] + "_" + str(ix)+"_run_rt\n"
                parFnText += "  stk.append(fs)\n"           # put stream frame at top of stream's stack
                parFnText += "  f.stacks.append(stk)\n"     # put stack on our frame's list of stream stacks

            #parFnText +=     "  print('f.stacks', f.stacks)\n"
            #parFnText +=     "  print('f.verb', f.verb)\n"
            parFnText +=     "  return f\n"

            # print("buildParallelText complete.  parFnText=\n"+parFnText[0])
            return (" pass #3\n", parFnText)

        # build a runtime library function for this library
        def buildLib(libClass):
            libName = libClass.__name__
            #print("WyeCore buildLib: libName", libName)
            codeStr = "class "+libName+"_rt:\n"
            parFnStr = ""     # any parallel stream fns to add to end of codeStr

            # for any class in the lib that has a build function, call it to generate class code for the lib runtime
            doBuild = False     # assume nothing to do
            for attr in dir(libClass):
                if attr != "__class__":     # avoid lib's self reference
                    vrb = getattr(libClass, attr)
                    if inspect.isclass(vrb):
                        vrb.library = libClass  # add pointer from verb class to parent library class
                        # if the class has a build function then call it to generate Python source code for its runtime method
                        if hasattr(vrb, "_build"):
                            doBuild = True      # there is code to compile
                            rowRef = [0]
                            cdStr, parStr = vrb._build(rowRef)  # call verb build to get verb's runtime code string(s)
                            codeStr += cdStr
                            parFnStr += parStr

                        # if this class is an object that should be added to the world's active object list
                        if hasattr(vrb, "autoStart") and vrb.autoStart and len(vrb.paramDescr) == 0:
                            classStr = libName + "." + libName + "." + vrb.__name__
                            #print("buildLib autoStart: ", classStr)
                            WyeCore.World.startObjs.append(classStr)

            # if there's code to build for the library, doit
            if doBuild:
                codeStr += parFnStr         # tack parallel code on end of regular code
                codeStr += 'setattr('+libName+', "'+libName+'_rt", '+libName+'_rt)\n'

                # DEBUG PRINT GENERATED CODE
                # If compiled Wye code, print it
                if WyeCore.debugListCode:
                    print("\nlib '"+libClass.__name__+"' code=")
                    lnIx = 1
                    for ln in codeStr.split('\n'):
                        print("%2d "%lnIx, ln)
                        lnIx += 1

                # compile the runtime class containing methods for all the verb runtimes
                try:
                    code = compile(codeStr, "<string>", "exec")
                    # exec the lib method - contains one line to setattr the lib_rt class to the library
                    # so all the verb functions are available at runtime
                    libDict = {
                        libName:libClass,
                        "Wye":Wye,
                        "WyeCore":WyeCore,
                        "WyeLib": WyeCore.libs.WyeLib,
                        "WyeUILib":WyeCore.libs.WyeUILib,
                        "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
                        "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib,
                    }
                    exec(code, libDict)
                except Exception as e:
                    print("Failed to build library:", libClass.__name__, " runtime code\n", str(e))
                    traceback.print_exception(e)
                    print(libClass.__name__, 'code:')
                    lnIx = 1
                    for ln in codeStr.split('\n'):
                        print('%2d ' % lnIx, ln)
                        lnIx += 1
                    print('')

                    if WyeCore.worldInitialized:
                        title = "Runtime Error c"
                        msg = "Failed to build library:"+ libClass.__name__+ " runtime code\n" + str(e) + "\n" + traceback.format_exc()
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR)

        # do we already have a UI input focus manager?
        def haveFocusManager():
            return not WyeCore.focusManager is None

        # set the UI focus manager
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

        # write Python string for lib with this name
        def createLibString(name):

            libTpl = "from Wye import Wye\nfrom WyeCore import WyeCore\n"
            libTpl += "class "+name+":\n  def _build():\n    WyeCore.Utils.buildLib("+name+")\n"
            libTpl += "  canSave = True  # all verbs can be saved with the library\n"
            libTpl += "  modified = False  # no changes\n"
            libTpl += "  class "+name+"_rt:\n   pass #1\n"
            return libTpl


        # Create a new in-memory library
        def createLib(name):

            libTpl = WyeCore.Utils.createLibString(name)
            libTpl += "setattr(WyeCore.libs, "+name+".__name__, "+name+")\n"

        #    print("createLib: Library text:")
        #    lnIx = 1
        #    for ln in libTpl.split('\n'):
        #        print("%2d " % lnIx, ln)
        #        lnIx += 1
        #    print("")

            code = compile(libTpl, "<string>", "exec")

            libDict = {
                name: name,
                "Wye": Wye,
                "WyeCore": WyeCore,
                "WyeLib": WyeCore.libs.WyeLib,
                "WyeUILib": WyeCore.libs.WyeUILib,
                "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
                "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib,
            }
            #print("createLib: exec library", name)
            exec(code, libDict)
            lib = getattr(WyeCore.libs, name)
            #print("Run test from template lib")
            #lib.test()
            #print("Build", name)
            lib._build()
            if name in WyeCore.World.libDict:
                WyeCore.World.libList.remove(WyeCore.World.libDict[name])
            WyeCore.World.libDict[name] = lib
            WyeCore.World.libList.append(lib)
            #print("createLib: Built and installed new library successfully", lib.__name__)
            return lib



        # create the text description of a verb from lib, verb name, settings, param/var/code descrs.
        # If doTest, builds a self-contained Python class that can build itself without having to be in a lib
        def createVerbString(libName, name, verbSettings, paramDescr, varDescr, codeDescr, doTest=False, outDent=True):

            if doTest or outDent:
                vrbStr = "\nclass " + name + ":\n"
            else:
                vrbStr = "\n  class " + name + ":\n"
            if 'mode' in verbSettings:
                vrbStr += "    mode = Wye.mode." + Wye.mode.tostring(verbSettings['mode']) + "\n"
            if 'autoStart' in verbSettings:
                vrbStr += "    autoStart = True\n" if verbSettings['autoStart'] else "    autoStart = False\n"
            if 'dataType' in verbSettings:
                vrbStr += "    dataType = Wye.dType." + Wye.dType.tostring(verbSettings['dataType']) + "\n"
            if 'cType' in verbSettings:
                vrbStr += "    cType = Wye.cType." + Wye.cType.tostring(verbSettings['cType']) + "\n"
            if 'parTermType' in verbSettings:
                vrbStr += "    parTermType = Wye.parTermType." + Wye.parTermType.tostring(
                    verbSettings['parTermType']) + "\n"

            # Convert nested descrs into nicely formatted text so won't create over-long lines and cause trouble.
            # Also looks nice
            #
            # Note: editing requires all tuples be replaced by lists.  This puts lists back to tuples.
            # Note: side effect is that varDescr initial value lists get converted to tuples.
            # That would screw up vars expecting mutable arrays and getting const tuples.  However, the codeFrame does
            # a deep copy of any initial value list/tuple to ensure frames don't share values, and it turns all tuples
            # into lists again.  This could be a surprise somewhere down the road.

            paramStr = WyeCore.Utils.listToTupleString(paramDescr, 0)
            varStr = WyeCore.Utils.listToTupleString(varDescr, 0)
            codeStr = WyeCore.Utils.listToTupleString(codeDescr, 0)

            # note: trim off leading \n from formatted string or compiler fusses
            vrbStr += "    paramDescr =  " + paramStr[1:] + "\n"
            vrbStr += "    varDescr =  " + varStr[1:] + "\n"
            vrbStr += "    codeDescr =  " + codeStr[1:] + "\n"
            vrbStr += '''
    def _build(rowRef):
        # print("Build ",'''
            vrbStr += name + ")\n"
            vrbStr += "        rowIxRef = [0]\n"
            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += "        return WyeCore.Utils.buildParallelText('"
                if doTest:
                    vrbStr += libName + "', '" + name + "', " + name + ".codeDescr" + ", " + name + ")\n\n"
                else:
                    vrbStr += libName + "', '" + name + "', " + libName + "." + name + ".codeDescr" + ", " + libName + "." + name + ")\n\n"
            else:
                vrbStr += "        return WyeCore.Utils.buildCodeText('"
                if doTest:
                    vrbStr += name + "', " + name + ".codeDescr" + ", " + name + ", rowIxRef)\n\n"
                else:
                    vrbStr += name + "', " + libName + "." + name + ".codeDescr" + ", " + libName + "." + name + ", rowIxRef)\n\n"
            vrbStr += "    def start(stack):\n"
            #vrbStr += "        print('" + name + " object start')\n"
            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += "        return " + libName + "." + libName + "_rt." + name + "_start_rt(stack)\n"
            else:
                vrbStr += "        return Wye.codeFrame("
                vrbStr += libName + "." + name + ", stack)\n"

            vrbStr += '''
    def run(frame):
'''
            vrbStr += "        # print('Run '" + name + ")\n"
            #vrbStr += "        try:\n"
            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += "        frame.runParallel()\n"
            else:
                vrbStr += "        " + libName + "." + libName + "_rt." + name + "_run_rt(frame)\n"
            #vrbStr += "        except Exception as e:\n"
            #vrbStr += "          if not hasattr(frame, 'errOnce'):\n"
            #vrbStr += "            import traceback\n"
            #vrbStr += "            if Wye.devPrint:\n"
            #if verbSettings['mode'] == Wye.mode.PARALLEL:
            #    vrbStr += "              print('" + libName + " " + name + " runParallel failed\\n', str(e))\n"
            #else:
            #    vrbStr += "              print('" + libName + "." + libName + "_rt." + name + "_run_rt failed\\n', str(e))\n"
            #vrbStr += "              traceback.print_exception(e)\n"
            #vrbStr += "              frame.errOnce = True\n\n"
            #vrbStr += "            WyeCore.World.compileErrorTitle='Runtime Error'\n"
            #vrbStr += "            WyeCore.World.compileErrorText='Verb \\\""+name+"\\\" died with error\\n'+str(e)+'\\n'+traceback.format_exc()\n"
            #vrbStr += "            WyeCore.Utils.displayError()\n"
            return vrbStr


        def displayError():
            if WyeCore.World.noBuildErrors:                # only put up one error
                WyeCore.World.noBuildErrors = False
                title = WyeCore.World.compileErrorTitle
                msg = WyeCore.World.compileErrorText
                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, Wye.color.WARNING_COLOR, formatLst=["NO_CANCEL", "FORCE_TOP_CTLS"])

        # create a new verb
        # If test, just compile the verb and its runtime code
        # Otherwise attach it to the given library and, if autoStart, start it
        def createVerb(vrbLib, name, verbSettings, paramDescr, varDescr, codeDescr, doTest=False, listCode=False, doAutoStart=True):
            # clear global compile error
            WyeCore.World.noBuildErrors = True
            WyeCore.World.listing = ""

            # build verb
            vrbStr = "from Wye import Wye\nfrom WyeCore import WyeCore\n"
            vrbStr += WyeCore.Utils.createVerbString(vrbLib.__name__, name, verbSettings, paramDescr, varDescr, codeDescr, doTest)

            # put library in verb
            vrbStr += "setattr(" + name + ", 'library', WyeCore.libs." + vrbLib.__name__ + ")\n"

            # put verb in lib
            if not doTest:
                vrbStr += "setattr(WyeCore.libs." + vrbLib.__name__ + ", " + name + ".__name__, " + name + ")\n"

            # build verb's Wye code
            vrbStr += "rowRef = [0]\n"
            vrbStr += "cdStr, parStr = "+name + "._build(rowRef)\n"

            # DEBUG - print out verb's runtime code with line numbers
            if listCode or WyeCore.debugListCode:
                #if not doTest and not verbSettings['mode'] == Wye.mode.PARALLEL:
                if verbSettings['mode'] == Wye.mode.PARALLEL:
                    vrbStr += "if Wye.devPrint:\n"
                    vrbStr += "  print('createVerb: parallel runtime code')\n"
                    vrbStr += "  lnIx = 1\n"
                    vrbStr += "  for ln in parStr.split('\\n'):\n"
                    vrbStr += "    print('%2d ' % lnIx, ln)\n"
                    vrbStr += "    lnIx += 1\n"
                    vrbStr += "  print('')\n"
                    vrbStr += "WyeCore.World.listing += '\\n"+name+": parallel runtime code\\n'\n"
                    vrbStr += "lnIx = 1\n"
                    vrbStr += "for ln in parStr.split('\\n'):\n"
                    vrbStr += '    WyeCore.World.listing += (\"%2d \" % lnIx) + ln + \"\\n\"\n'
                    vrbStr += "    lnIx += 1\n"
                else:
                    vrbStr += "if Wye.devPrint:\n"
                    vrbStr += "  print('createVerb: runtime text')\n"
                    vrbStr += "  lnIx = 1\n"
                    vrbStr += "  for ln in cdStr.split('\\n'):\n"
                    vrbStr += "    print('%2d ' % lnIx, ln)\n"
                    vrbStr += "    lnIx += 1\n"
                    vrbStr += "  print('')\n"
                    vrbStr += "WyeCore.World.listing += '\\n"+name+": runtime code:\\n'\n"
                    vrbStr += "lnIx = 1\n"
                    vrbStr += "for ln in cdStr.split('\\n'):\n"
                    vrbStr += '    WyeCore.World.listing += (\"%2d \" % lnIx) + ln + \"\\n\"\n'
                    vrbStr += "    lnIx += 1\n"
            # when the verb string is executed, the verb's build will be run.
            # The build will return the runtime string for the verb.
            # So the verb's string we're compiling now will need to compile that returned string into code
            # that is put into the verb's lib runtime class. (yes, this code when compiled will run the new verb
            # to generate code that then needs to be compiled...)

            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += '''

# compile verb runtime to tmp class
parStr = "class tmp:\\n" + parStr + "\\n"
'''
            else:
                vrbStr += '''

# compile verb runtime
cdStr = "class tmp:\\n" + cdStr + "\\n"
'''
            # put in code to copy verb runtime code function(s) from tmp class to lib runtime class
            if not doTest:
                if verbSettings['mode'] == Wye.mode.PARALLEL:
                    startName = name + "_start_rt"
                    #vrbStr += "parStr += 'print(\"put "+startName+" on "+ vrbLib.__name__ + "_rt\")\\n'\n"
                    vrbStr += "parStr += 'setattr(WyeCore.libs." + vrbLib.__name__ + "." + vrbLib.__name__ + "_rt, \"" + startName+"\", tmp."+ startName+ ")\\n'\n"
                    ix = 0
                    for stream in codeDescr:
                        streamName = name + "_" + stream[0] + "_" + str(ix)+"_run_rt"
                        ix += 1
                        #vrbStr += "parStr += 'print(\"put " + streamName + " on " + vrbLib.__name__ + "_rt\")\\n'\n"
                        vrbStr += "parStr += 'setattr(WyeCore.libs." + vrbLib.__name__ + "." + vrbLib.__name__ + "_rt, \"" + streamName +"\", tmp."+streamName +")\\n'\n"
                else:
                    vrbStr += "cdStr += 'setattr(WyeCore.libs." + vrbLib.__name__ + "." + vrbLib.__name__ + "_rt, \"" + name + "_run_rt\", tmp." + name + "_run_rt)\\n'\n"

            # compile runtime code function
            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += '''
try:
    # compile the verb's runtime code
    code = compile(parStr, "<string>", "exec")
    print("verb's code contains\\n", dir(code))
    #print("createVerb: Compiled verb runtime successfully")
'''
            else:
                vrbStr += '''
try:
    # compile the verb's runtime code
    code = compile(cdStr, "<string>", "exec")
    #print("createVerb: Compiled verb runtime successfully")
'''
            vrbStr += "    libDict = {\n"

            vrbStr += "        '" + vrbLib.__name__ + "':" + vrbLib.__name__ + ",\n"
            vrbStr += '''
        "Wye": Wye,
        "WyeCore": WyeCore,
        "WyeLib": WyeCore.libs.WyeLib,
        "WyeUILib": WyeCore.libs.WyeUILib,
        "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
        "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib,
    }
    
    #print('createVerb: exec verb " + vrbLib.__name__ + "." + name + "')
    
    # run the compiled code.  This will add the verb's runtime function to the library's runtime class
    try:
        exec(code, libDict)
'''
            #vrbStr += "        print('Created verb "+vrbLib.__name__ + "." + name + "')\n"
            vrbStr += '''
    except Exception as e:
        print("exec verb runtime failed\\n", str(e))    
'''
            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += '''
        if Wye.devPrint:
          print('parStr')
          lnIx = 1
          for ln in parStr.split('\\n'):
            print('%2d ' % lnIx, ln)
            lnIx += 1
          print('')
        lnIx = 1
        WyeCore.World.listing += 'parStr\\n'
        for ln in parStr.split('\\n'):
            WyeCore.World.listing += ('%2d ' % lnIx) + ln + '\\n'
            lnIx += 1
'''
            else:
                vrbStr += '''
        if Wye.devPrint:
          print('cdStr')
          lnIx = 1
          for ln in cdStr.split('\\n'):
            print('%2d ' % lnIx, ln)
            lnIx += 1
          print('')
        WyeCore.World.listing += 'cdStr\\n'
        lnIx = 1
        for ln in cdStr.split('\\n'):
            WyeCore.World.listing += ('%2d ' % lnIx) + ln + '\\n'
            lnIx += 1

'''
            vrbStr += '''
        WyeCore.World.compileErrorTitle = "Build: Exec Verb Runtime Failed"
        WyeCore.World.compileErrorText = "Error\\n" + str(e) + "\\nListing\\n" + WyeCore.World.listing
        WyeCore.Utils.displayError()
        
except Exception as e:
    print("compile verb runtime failed\\n", str(e))
'''

            if verbSettings['mode'] == Wye.mode.PARALLEL:
                vrbStr += '''
    if Wye.devPrint:
      print("compile verb parallel runtime failed\\n", str(e))
      print('parStr')
      lnIx = 1
      for ln in parStr.split('\\n'):
        print('%2d ' % lnIx, ln)
        lnIx += 1
      print('')
    WyeCore.World.listing += 'Parallel Python Stream Runtime Methods:\\n'
    lnIx = 1
    for ln in parStr.split('\\n'):
        WyeCore.World.listing += ('%2d ' % lnIx) + ln + '\\n'
        lnIx += 1
'''
            else:
                vrbStr += '''
    if Wye.devPrint:
      print("compile verb runtime failed\\n", str(e))
      print('cdStr')
      lnIx = 1
      for ln in cdStr.split('\\n'):
          print('%2d ' % lnIx, ln)
          lnIx += 1
      print('')
    WyeCore.World.listing += 'Python Runtime Method:\\n'
    lnIx = 1
    for ln in cdStr.split('\\n'):
        WyeCore.World.listing += ('%2d ' % lnIx) + ln + '\\n'
        lnIx += 1
'''
                vrbStr += "    WyeCore.World.compileErrorTitle = \"Build: Compile '"+name+"' Runtime Python Failed\""
                vrbStr += '''
    WyeCore.World.compileErrorText = "Error\\n" + str(e) + "\\n\\nListing:\\n" + WyeCore.World.listing
    WyeCore.Utils.displayError()

'''

            if not doTest:
                # if verb has autostart, do it, unless blocked by caller
                if doAutoStart:
                    vrbStr += "if hasattr(WyeCore.libs."+vrbLib.__name__+"."+name+", 'autoStart'):\n"
                    vrbStr += "    if WyeCore.libs."+vrbLib.__name__+"."+name+".autoStart and len(WyeCore.libs."+vrbLib.__name__+"."+name+".paramDescr) == 0:\n"
                    #vrbStr += "        print('autoStart "+name+"')\n"
                    vrbStr += "        WyeCore.World.startActiveObject(WyeCore.libs."+vrbLib.__name__+"."+name+")\n"


            # compile verb
            try:
                #print("createVerb: Compile", name)
                code = compile(vrbStr, "<string>", "exec")
                #print("createVerb: Compiled", name, " successfully")

                libDict = {
                    vrbLib.__name__: vrbLib,
                    "Wye": Wye,
                    "WyeCore": WyeCore,
                    "WyeLib": WyeCore.libs.WyeLib,
                    "WyeUILib": WyeCore.libs.WyeUILib,
                    "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
                    "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib,
                }

                #if doTest:
                #    print("createVerb: exec verb", vrbLib.__name__ + "." + name)
                try:
                    exec(code, libDict)
                    if (doTest or Wye.devPrint) and not WyeCore.World.noBuildErrors:
                        print(vrbLib.__name__ + name, " executed successfully")
                except Exception as e:
                    print("exec verb", vrbLib.__name__ + "." + name, " failed\n", str(e))
                    lnIx = 1
                    for ln in vrbStr.split('\n'):
                        WyeCore.World.listing += ("%2d " % lnIx) + ln + "\n"
                        lnIx += 1
                    WyeCore.World.compileErrorTitle = "Build: Execute '"+name+"' Failed"
                    WyeCore.World.compileErrorText = "Verb '" + name+"', died with error\n" + str(e) + "\n" + traceback.format_exc() +"\n\nListing:\n" +WyeCore.World.listing
                    WyeCore.Utils.displayError()

                    if Wye.devPrint:
                        print("exec verb", vrbLib.__name__ + "." + name, " failed\n", str(e))
                        traceback.print_exception(e)
                        print("verb text:")
                        lnIx = 1
                        for ln in vrbStr.split('\n'):
                            print("%2d " % lnIx, ln)
                            lnIx += 1
                        print("")
                    return

            except Exception as e:
                if Wye.devPrint:
                    print("compile verb", vrbLib.__name__ + "." + name, " failed\n", str(e))
                    traceback.print_exception(e)
                    print("verb text:")
                    lnIx = 1
                    for ln in vrbStr.split('\n'):
                        print("%2d " % lnIx, ln)
                        lnIx += 1
                    print("")

                lnIx = 1
                for ln in vrbStr.split('\n'):
                    WyeCore.World.listing += ("%2d " % lnIx) + ln + "\n"
                    lnIx += 1
                WyeCore.World.compileErrorTitle = "Build: Compile '"+name+"' Failed"
                WyeCore.World.compileErrorText = "Compile Verb" + vrbLib.__name__ + "." + name + " failed\n" + str(e) + "\n" + traceback.format_exc() + "\n\nListing:\n" + WyeCore.World.listing
                WyeCore.Utils.displayError()
                return

            # print verb code with line numbers
            if (listCode or WyeCore.debugListCode) and WyeCore.World.noBuildErrors:
                if Wye.devPrint:
                    print("createVerb: verb text:")
                    lnIx = 1
                    for ln in vrbStr.split('\n'):
                        print("%2d " % lnIx, ln)
                        lnIx += 1
                    print("")
                WyeCore.World.listing += "\n"+name+": Verb Python Code:\n"
                lnIx = 1
                for ln in vrbStr.split('\n'):
                    WyeCore.World.listing += ("%2d " % lnIx) + ln + "\n"
                    lnIx += 1
                # only put up listing if haven't thrown an error
                #if WyeCore.World.noBuildErrors:
                #    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Build: "+name+" Python Code:", WyeCore.World.listing, formatLst=["NO_CANCEL", "FORCE_TOP_CTLS"])


            #if it built with no errors
            if WyeCore.World.noBuildErrors:
                if Wye.devPrint:
                    print(name, vrbLib.__name__ + "." + name, " compiled successfully")

                title = "Build Success"
                # if show listing
                if listCode or WyeCore.debugListCode:
                    msg = name + " " + vrbLib.__name__ + "." + name + " built successfully\n" + WyeCore.World.listing
                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg, formatLst=["NO_CANCEL", "FORCE_TOP_CTLS"])
                # if doTest
                elif doTest:
                    msg = name + " " + vrbLib.__name__ + "." + name + " built successfully"
                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, msg)

                # if it built, return pointer to it
                if not doTest:
                    if hasattr(vrbLib, name):
                        return getattr(vrbLib, name)
                    else:
                        return None
