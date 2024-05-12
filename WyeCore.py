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
# editing one of the contained libs will create an external file for just that lib.
# Incorporating the result requires external editing.

# used to make unique ids
_nextId = 0


class WyeCore(Wye.staticObj):
    # used to detect first call for initialization
    worldInitialized = False

    picker = None   # object picker object
    base = None     # panda3d base - set by application

    lastIsNothingToRun = False

    class World(Wye.staticObj):
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = ()
        codeDescr = ()

        keyHandler = None

        # universe specific
        libs = []
        libDict = {}  # lib name -> lib lookup dictionary
        startObjs = []
        objs = []  # runnable objects
        objStacks = []  # objects run in parallel so each one gets a stack

        eventCallbackDict = {}              # dictionary of event callbacks
        repeatEventCallbackDict = {}      # dictionary of repeated event frames

        displayCycleCount = 0           # DEBUG

        class libObj:
            placeholder = ""

        class KeyHandler(DirectObject):
            def __init__(self):
                base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
                self.accept('keystroke', self.myFunc)

            def myFunc(self, keyname):
                print("KeyHandler: key=",keyname)

        # list of independent frames running until they succeed/fail
        class repeatEventExecObj:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.type.NONE
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
                #print("worldRunner: World Init")
                WyeCore.worldInitialized = True  # Only do this once

                dlight = DirectionalLight('dlight')
                dlight.setColor((1,1,1,1)) #(0.8, 0.8, 0.5, 1))
                dlnp = render.attachNewNode(dlight)
                dlnp.setHpr(45, -60, 0)
                render.setLight(dlnp)

                #######
                WyeCore.World.keyHandler = WyeCore.World.KeyHandler()

                text = TextNode('node name')
                text.setWordwrap(7.0)
                text.setText("Welcome to Wye 0.1")
                text.setTextColor(1, 1, 1, 1)
                text.setAlign(TextNode.ACenter)
                #text.setFrameColor(0, 0, 1, 1)
                #text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

                text.setCardColor(0, 0, 0, 1)
                text.setCardAsMargin(.1, .2, .1, .1)    # extend beyond edge of text (-x, +x, -y, +y)
                text.setCardDecal(True)
#
                # create (unpickable) 3d text object
                text3d = NodePath(text.generate())      # supposed to, but does not, generate pickable node
                #text3d = NodePath(text)
                text3d.reparentTo(render)
                text3d.setScale(.2, .2, .2)
                text3d.setPos(-.5, 17, 4)
                text3d.setTwoSided(True)

                text3d.node().setIntoCollideMask(GeomNode.getDefaultCollideMask())

                #######

                audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                snd = audio3d.loadSfx("WyePop.wav")
                audio3d.attachSoundToObject(snd, text3d)
                #######

            #    cd = CardMaker("a card")
            #    cd.setColor(1,0,0,1)
            #    cd.setFrame(left=-1, right=1, bottom=-.5, top=.5)
            #    card = render.attachNewNode(cd.generate())
            #    #card = NodePath(cd.generate())


                #cd.setFromCollideMask(GeomNode.getDefaultCollideMask())

                #quad = CollisionPolygon(Point3(0, 0, 0), Point3(0, 0, 1),
                #                        Point3(0, 1, 1), Point3(0, 1, 0))

            #    cs = CollisionSphere(0, 0, 0, 1)
            #    cnodePath = card.attachNewNode(CollisionNode('cnode'))
            #    cnodePath.node().addSolid(cs)
            #    cnodePath.node().setFromCollideMask(GeomNode.getDefaultCollideMask())
#
            #    cnodePath.show()
#
            #    #cd = card.attachNewNode(text)
            #    #card.setColor(1,0,0,1)
            #    card.setEffect(DecalEffect.make())
#
                #tnp = NodePath(card)
            #    card.reparentTo(render)
            #    card.setScale(1, .2, .2)
            #    card.setPos(0, 17, 4)
            #    card.setTwoSided(True)

#                text.setScale(scale[0], scale[1], scale[2])
#                text.setPos(pos[0], pos[1], pos[2])
                #textNodePath = aspect2d.attachNewNode(text.generate())
                #textNodePath.setScale(0.07)


                ###########

                #base.camera.setPos(10,25,10)        # this does not move camera - something else controlling pos?
                #print("camPos",base.camera.getPos())

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
                for lib in WyeCore.World.libs:
                    WyeCore.World.libDict[lib.__name__] = lib     # build lib name -> lib lookup dictionary
                    setattr(WyeCore.World.libObj, lib.__name__, lib)

                # build all libraries - compiles any Wye code words in each lib
                for lib in WyeCore.World.libs:
                    #print("Build ", lib)
                    lib.build()         # build all Wye code segments in code words

                # parse starting object names and find the objects in the known libraries
                # print("worldRunner:  start ", len(world.startObjs), " objs")
                for objStr in WyeCore.World.startObjs:
                    #print("obj ", objStr," in startObjs")
                    namStrs = objStr.split(".")                     # parse name of object
                    if namStrs[1] in WyeCore.World.libDict:
                        obj = getattr(WyeCore.World.libDict[namStrs[1]], namStrs[2])  # get object from library
                        WyeCore.World.objs.append(obj)                  # add to list of runtime objects
                        stk = []
                        f = obj.start(stk)                                 # start the object and get its stack frame
                        stk.append(f)                                   # create a stack for it
                        #f.SP = stk                                      # put ptr to stack in frame
                        f.params = [[0], ]                              # place to put return param
                        WyeCore.World.objStacks.append(stk)             # put obj's stack on list and put obj's frame on the stack
                    else:
                        print("Error: Lib '"+namStrs[1]+"' not found for start object ", objStr)
                # print("worldRunner done World Init")

                # create picker object
                WyeCore.picker = WyeCore.Picker(WyeCore.base)

                WyeCore.picker.makePickable(text3d)
                tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
                text3d.setTag("wyeTag", tag)
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
                ranNothing = True   # pessimist
                for stack in WyeCore.World.objStacks:
                    sLen = len(stack)
                    if sLen > 0:  # if there's something on the stack
                        ranNothing = False
                        # run the frame furthest down the stack
                        frame = stack[-1]
                        #if frame:
                        #    print("worldRunner stack # ", stackNum, " frame ", frame, " status ", WyeCore.Utils.statusToString(frame.status),
                        #          " verb", frame.verb.__name__,
                        #          " stackLen ", sLen, " stack ", WyeCore.Utils.stackToString(stack))
                        #else:
                        #    print("worldRunner stack # ", stackNum, " frame = None")
                        #    exit(1)
                        if frame.status == Wye.status.CONTINUE:
                            #print("worldRunner run: stack ", stackNum, " verb", frame.verb.__name__, " PC ", frame.PC)
                            frame.verb.run(frame)
                            #if frame.status != Wye.status.CONTINUE:
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
                if ranNothing:
                    #print("ranNothing ", ranNothing, " and WyeCore.lastIsNothingToRun", WyeCore.lastIsNothingToRun)
                    if not WyeCore.lastIsNothingToRun:
                        WyeCore.lastIsNothingToRun = True
                        #print("worldRunner stack # ", stackNum, " nothing to run")

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
                    print("Clicked on ", self.pickedObj, " at ", self.pickedObj.getPos(), " wyeID ", wyeID)
                    if wyeID:
                        #print("Picked object: '", self.pickedObj, "', wyeID ", wyeID)

                        # if there's a callback for the specific object, call itF
                        if "click" in WyeCore.World.eventCallbackDict:
                            tagDict = WyeCore.World.eventCallbackDict["click"]
                            if wyeID in tagDict:
                                #print("Found ", len(tagDict[wyeID]), " callbacks for tag ", wyeID)
                                # run through lists calling callbacks.
                                # keep any repeated frames and update the callback entry with just them
                                # if no repeated frames, remove callback entry for this target
                                repEvts = []
                                #print("objSelectEvent: tagDict=", tagDict)
                                evtLst = tagDict[wyeID]
                                for evt in evtLst:
                                    frame = evt[0]
                                    data = evt[1]
                                    #print("objSelectEvent: inc frame ", frame.verb.__name__, " PC ", frame.PC)
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
                #    print("No object under mouse")
            #else:
            #    print("Object picking disabled")

    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class Text3d:
        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.__genTextObj(text, color)
            self.__genCardObj()
            self.__gen3dTextObj((-.5, 17, 2), (.2, .2, .2), (0, 0, 0, 1))
            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameColor(0, 0, 1, 1)
            # txtNode.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

        def setAlign(self, ctr):
            self.text.setAlign(ctr)

        # update the frame color
        def setFrameColor(self, color):
            self.text3d.setColor(color)

        # update the margin spacing
        def setFrameAsMargin(self, marginL, marginR, marginB, marginT):
            self.marginL = marginL
            self.marginR = marginR
            self.marginB = marginB
            self.marginT = marginT
            self.__regen3d()

        # changing the text requires regenerating the background card and the 3d node
        def setText(self, text):
            self.text.setText(text)
            self.__regen3d()

        def setPos(self, val):
            self.text3d.setPos(val)

        def setColor(self, val):
            self.text3d.setColor(val)

        def setScale(self, val):
            self.text3d.setScale(val)

        def setWordWrap(self):
            return self.text.getWordwrap()

        def getText(self):
            return self.text.getText()

        def getPos(self):
            return self.text3d.getPos()

        def getColor(self):
            return self.text3d.getColor()

        def getScale(self):
            return self.text3d.getScale()

        def getWordWrap(self):
            return self.text.setWordwrap()

        def getTag(self):
            return self.text.name

        def getAlign(self):
            return self.text.getAlign()

        def getFrameColor(self):
            return self.text3d.getColor()

        # update the margin spacing
        def getFrameAsMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        # rebuild card and path for updated text object
        def __regen3d(self):
            bg = self.text3d.getColor()
            pos = self.text3d.getPos()
            scale = self.text3d.getScale()
            self.__genCardObj()                     # generate new card obj for updated text object
            self.text3d.detachNode()                # detach 3d node path to old card
            self.__gen3dTextObj(pos, scale, bg)     # make new 3d node path to new card

        # internal rtn to gen text object with unique wyeTag name
        def __genTextObj(self, text, color=(1,1,1,1)):
            tag = "txt"+str(WyeCore.Utils.getId())
            self.text = TextNode(tag)
            self.text.setText(text)
            self.text.setTextColor(color)

        # internal rtn to gen 3d Card clickable background object
        def __genCardObj(self):
            #print("initial txtNode frame ", self.text.getFrameActual())
            self.card = CardMaker("My Card")
            frame = self.text.getFrameActual()
            #print("frame", frame)
            frame[0] -= self.marginL
            frame[1] += self.marginR
            frame[2] -= self.marginB
            frame[3] += self.marginT
            #print("initial adjusted frame", frame)
            self.card.setFrame(frame)

        # internal rtn to generate 3d (path) object to position, etc. the text
        def __gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self.text3d = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            self.text3d.attachNewNode(self.text)
            self.text3d.setEffect(DecalEffect.make())        # glue text onto card
            self.text3d.reparentTo(render)
            WyeCore.picker.makePickable(self.text3d)         # make selectable
            self.text3d.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self.text3d.setPos(pos)
            self.text3d.setScale(scale)

            self.text3d.setBillboardPointWorld(0.)           # always face the camera
            self.text3d.setLightOff()                        # unaffected by world lighting
            self.text3d.setColor(bg)



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
    #        #print("WyeCore utils resourcePath: start '"+ relative_path+ "'")
    #        if hasattr(sys, '_MEIPASS'):
    #            pwd = os.path.dirname(sys.executable)
    #            path = str(os.path.join(pwd, relative_path))
    #            #print("executable path", path)
    #        else:
    #            pwd = os.path.abspath(".")
    #            #print("os.path.abspath('.')", pwd)
    #            path = str(os.path.join(pwd, relative_path))
#
    #        path = path.replace("\\","/")
    #        #path = path.replace(":","")

            try:
                # look for PyInstaller temp folder
                base_path = sys._MEIPASS
            except:
                # nope, guess we're running from python or IDE
                base_path = os.path.abspath(".")

            path = base_path + "/" + relative_path

            path = path.replace("\\","/")
            #path = path.replace(":","")

            print("  return path '"+ path+"'")
            return path

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
                            codeText += WyeCore.Utils.parseWyeTuple(paramDesc, fNum+1) + "\n" + \
                                        eff+".params.append(" + "f"+str(fNum+1)+".params[0])\n"
                codeText += wyeTuple[0] + ".run("+eff+")\nif "+eff+".status == Wye.status.FAIL:\n frame.status = "+eff+".status\n return\n"
            # Raw Python code
            else:
                if len(wyeTuple) > 1:
                    codeText = wyeTuple[1]+"\n"
                else:
                    print("Wye Warning - parseTuple null verb but no raw code supplied")

            return codeText

        # parse list of Wye tuples to text
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
                codeText[0] += WyeCore.Utils.parseWyeTuple(wyeTuple, 0)

            #print("buildCodeText complete.  codeText=\n"+codeText[0])
            return codeText[0]

        # return params concanated
        def paramsToString(frame):
            pStr = ""
            for param in frame.params:
                pStr += str(param[0])
            return pStr

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
            stkStr = "\n stack len=" + str(len)
            for ix in range(len-1, -1, -1):
                frame = stack[ix]
                stkStr += "\n  verb=" + frame.verb.__name__ + " status " + WyeCore.Utils.statusToString(frame.status) + \
                          " params: " + str(frame.params)
            return stkStr




        def buildLib(libClass):
            libName = libClass.__name__
            #print("WyeCore buildLib: libNamess", libName)
            codeStr = "class "+libName+"_rt:\n"
            # check all the classes in the lib for build functions.
            doBuild = False     # assume nothing to do
            for attr in dir(libClass):
                val = getattr(libClass, attr)
                if inspect.isclass(val):
                    # if the class has a build function then call it to generate Python source code for its runtime method
                    if hasattr(val, "build"):
                        doBuild = True
                        # print("class ", attr, " has build method.  attr is ", type(attr), " val is ", type(val))
                        build = getattr(val, "build")  # get child's build method
                        # call the build function to get the "run" code string
                        bldStr = build()  # call it to get child's runtime code string(s)
                        lines = bldStr.splitlines(True)  # break the code into lines
                        # start runtime function for class
                        codeStr += " def " + attr + "_run_rt(frame):\n"  # define a runtime method containing the code lines
                        # DEBUG
                        # codeStr += "   print('execute "+attr+"_run_rt(frame) params', frame.params, ' vars', frame.vars)\n"
                        # End DEBUG
                        for line in lines:  # put child's code in rt method at required indent
                            if not line.isspace():
                                codeStr += "   " + line

            # if there's code to build for the library, doit
            if doBuild:
                codeStr += 'setattr('+libName+', "'+libName+'_rt", '+libName+'_rt)\n'
                code = compile(codeStr, "<string>", "exec")
                #print("lib code string\n"+codeStr)  # DEBUG
                exec(code, {"TestLib":libClass, "Wye":Wye, "WyeCore":WyeCore})