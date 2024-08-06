# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *
from functools import partial

#import partial
import traceback
import sys
from sys import exit
from direct.showbase import Audio3DManager

from direct.showbase.DirectObject import DirectObject

# 3d UI element library
class WyeUI(Wye.staticObj):
    LINE_HEIGHT = .25
    TEXT_SCALE = (.2,.2,.2)
    TEXT_COLOR = (1,1,1,1)


    # Build run_rt methods on each class
    def build():
        WyeCore.Utils.buildLib(WyeUI)

    # utility functions for building 3d objects
    def _displayCommand(cmd, coord):
        txt = str([str(e) for e in cmd])
        txtCoord = list(coord)
        # elements.append(WyeUI._label3d("Stream 0", color=(0, 1, 0, 1), pos=(0, 10, yy), scale=(.2, .2, .2)))
        WyeUI._label3d(txt, color=(0, 1, 0, 1), pos=(txtCoord[0], txtCoord[1], txtCoord[2]),
                                   scale=(.2, .2, .2))
        txtCoord[2] -= WyeUI.LINE_HEIGHT
        return txtCoord[2]

    def _displayVerb(verb, coord):
        cd = verb.codeDescr
        xyz = list(coord)
        xyz[0] += WyeUI.LINE_HEIGHT
        if verb.mode == Wye.mode.PARALLEL:
            for codeBlock in cd:
                for cmd in codeBlock:
                    xyz[2] = WyeUI._displayCommand(cmd, xyz)
                xyz[2] -= WyeUI.LINE_HEIGHT
        else:
            for cmd in cd:
                xyz[2] = WyeUI._displayCommand(cmd, xyz)

        xyz[2] -= WyeUI.LINE_HEIGHT
        return xyz[2]

    def _displayLib(lib, coord, elements=None):
        txtCoord = list(coord)
        for attr in dir(lib):
            if attr != "__class__":
                verb = getattr(lib, attr)
                if inspect.isclass(verb) and hasattr(verb, "mode"):
                    print("lib", lib.__name__, " verb", verb.__name__)
                    txt = lib.__name__ + "." +verb.__name__
                    txtCoord[2] -= WyeUI.LINE_HEIGHT
                    WyeUI._label3d(txt, color=WyeUI.TEXT_COLOR, pos=(txtCoord[0], txtCoord[1], txtCoord[2]), scale=WyeUI.TEXT_SCALE)
                    txtCoord[2] -= WyeUI.LINE_HEIGHT
                    if hasattr(verb, "codeDescr"):
                        txtCoord[2] = WyeUI._displayVerb(verb, txtCoord)


            
    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class _label3d:
        global render

        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1), parent=None):
            if parent is None:
                self.parent = render
            else:
                self.parent = parent
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.text = None
            self.card = None
            self._nodePath = None
            #
            self._genTextObj(text, color)
            self._genCardObj()
            self._gen3dTextObj(pos, scale, bg)

            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameColor(0, 0, 1, 1)
            # txtNode.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

        def setAlign(self, ctr):
            self.text.setAlign(ctr)

        # update the frame color
        def setFrameColor(self, color):
            self._nodePath.setColor(color)

        # update the margin spacing
        def setFrameAsMargin(self, marginL, marginR, marginB, marginT):
            self.marginL = marginL
            self.marginR = marginR
            self.marginB = marginB
            self.marginT = marginT
            self._regen3d()

        # changing the text requires regenerating the background card and the 3d node
        def setText(self, text):
            self.text.setText(text)
            self._regen3d()

        def setPos(self, val):
            self._nodePath.setPos(val)

        def setColor(self, val):
            self._nodePath.setColor(val)

        def setScale(self, val):
            self._nodePath.setScale(val)

        def setWordWrap(self):
            return self.text.getWordwrap()

        def getText(self):
            return self.text.getText()

        def getPos(self):
            return self._nodePath.getPos()

        def getColor(self):
            return self._nodePath.getColor()

        def getScale(self):
            return self._nodePath.getScale()

        def getWordWrap(self):
            return self.text.setWordwrap()

        def getTag(self):
            return self.text.name

        def getAlign(self):
            return self.text.getAlign()

        def getFrameColor(self):
            return self._nodePath.getColor()

        def getNodePath(self):
            return self._nodePath

        # update the margin spacing
        def getFrameAsMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        # rebuild card and path for updated text object
        def _regen3d(self):
            bg = self._nodePath.getColor()
            pos = self._nodePath.getPos()
            scale = self._nodePath.getScale()
            self._genCardObj()                     # generate new card obj for updated text object
            self._nodePath.detachNode()            # detach 3d node path from old card
            self._gen3dTextObj(pos, scale, bg)     # make new 3d node path to new card

        # internal rtn to gen text object with unique wyeTag name
        def _genTextObj(self, text, color=(1,1,1,1)):
            tag = "txt"+str(WyeCore.Utils.getId())
            self.text = TextNode(tag)
            if len(text) == 0:
                text = ' '
            self.text.setText(text)
            self.text.setTextColor(color)

        # internal rtn to gen 3d Card clickable background object
        def _genCardObj(self):
            #print("initial txtNode frame ", self.text.getFrameActual())
            self.card = CardMaker("Txt Card")
            gFrame = self.text.getFrameActual()
            if gFrame[1] == 0:      # if empty frame
                gFrame[1] = 1
                gFrame[3] = 1
            #print("gFrame", gFrame)
            gFrame[0] -= self.marginL
            gFrame[1] += self.marginR
            gFrame[2] -= self.marginB
            gFrame[3] += self.marginT
            #print("initial adjusted gFrame", gFrame)
            self.card.setFrame(gFrame)

        # internal rtn to generate 3d (path) object to position, etc. the text
        def _gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self._nodePath = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            self._nodePath.attachNewNode(self.text)
            self._nodePath.setEffect(DecalEffect.make())        # glue text onto card
            self._nodePath.reparentTo(self.parent)
            WyeCore.picker.makePickable(self._nodePath)         # make selectable
            self._nodePath.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self._nodePath.setPos(pos)
            self._nodePath.setScale(scale)

            self._nodePath.setBillboardPointWorld(0.)           # always face the camera
            self._nodePath.setLightOff()                        # unaffected by world lighting
            self._nodePath.setColor(bg)

        def removeNode(self):
            self._nodePath.removeNode()


    # text entry verb
    # todo - finish this
    class text3d:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NUMBER
        paramDescr = (
            ("text", Wye.dType.STRING, Wye.access.REFERENCE),       # 0 - caller var updated with curr text
            ("pos", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),  # 1 - position to put text3d at
            ("color", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 - color
            ("scale", Wye.dType.NUMBER_LIST, Wye.access.REFERENCE)  # 3 - scale
        )
        varDescr = (
            ("label", Wye.dType.OBJECT, None),          # 0 - label showing text
            ("labelID", Wye.dType.STRING, None),        # 1 - id of label for setting selected
            ("pos", Wye.dType.INTEGER_LIST, [0,0,0]),   # 2 - pos?
            ("text", Wye.dType.STRING, "---"),          # 3
            ("graphicID", Wye.dType.OBJECT, None)       # 4
           )   # var 4

        # np=loader.loadModel("jack") #load a model
        # #... do something
        # np.removeNode() #unload the model
        # loader.unloadModel(path)


        #def __init__(self, text="", color=(1, 1, 1, 1), pos=(0, 0, 0), scale=(1, 1, 1), bg=(0, 0, 0, 1)):
        #    label = WyeUI._label3d(text, color, pos, scale, bg)



    # Widget focus manager singleton
    # Maintains a list of dialog hierarchies where the most recently added member of each hierarchy is the only one
    # whose widgets can accept focus
    # Only one widget in all of them can have focus (if any have)
    #
    # Note: in theory this should turn on event handling when there's a dialog up and
    # shut it off when
    #
    # Note: event management is rudimentary.
    # Optimization might be to switch off key and drag events when an input doesn't have
    # focus.  For now, simplicity wins over optimization
    #
    class FocusManager:
        dialogHierarchies = []          # list of open dialog hierarchies (dialog frame lists)
        _mouseHandler = None

        shiftDown = False
        ctlDown = False

        # Mouse event delivery requires an instantiated class
        class _MouseHandler(DirectObject):
            def __init__(self):
                #print("WyeUI FocusManager openDialog set mouse event")
                self.accept('mouse1', self.mouseEvt)

                ## reference
                # "escape", "f" + "1-12"(e.g.
                # "f1", "f2", ...
                # "f12"), "print_screen",
                # "scroll_lock", "backspace", "insert", "home", "page_up", "num_lock",
                # "tab", "delete", "end", "page_down", "caps_lock", "enter", "arrow_left",
                # "arrow_up", "arrow_down", "arrow_right", "shift", "lshift", "rshift",
                # "control", "alt", "lcontrol", "lalt", "space", "ralt", "rcontrol"
                ## end reference

            def mouseEvt(self):
                evt = WyeCore.base.mouseWatcherNode.getMouse()
                #print("FocusManager mouseEvt:", evt)


        # find dialogFrame in leaf nodes of dialog hierarchies
        def findDialogHier(dialogFrame):
            retHier = None
            for hier in WyeUI.FocusManager.dialogHierarchies:
                # if found it, add to hierarchy list
                if len(hier) > 0 and hier[-1] == dialogFrame:
                    retHier = hier
                    break;  # found it, break out of loop

                if retHier is None:
                    print("Error: WyeUI FocusManager openDialog - dialog not found")
                    print("  dialog ", dialogFrame.params[1][0])
            return retHier


        # User is adding a dialog to the display
        # If it has a parent dialog, it is now the leaf of the hierarchy and
        # its inputs get any incoming events
        def openDialog(dialogFrame, parentFrame):
            # if no focus manager set to catch selected objects, fix that
            if WyeCore.Utils.getFocusManager() is None:
                WyeCore.Utils.setFocusManager(WyeUI.FocusManager)
                #WyeUI.FocusManager._mouseHandler = WyeUI.FocusManager._MouseHandler()

                # sign up for events

            # connect to parent frame
            dialogFrame.parentFrame = parentFrame

            # if starting new dialog hierarchy
            if parentFrame is None:
                WyeUI.FocusManager.dialogHierarchies.append([dialogFrame])

            # if has parent then add it to the parent's hierarchy
            else:
                print("openDialog find parentFrame ", parentFrame)
                hier = WyeUI.FocusManager.findDialogHier(parentFrame)
                if not hier is None:
                    hier.append(dialogFrame)

            #print("FocusManager openDialog", WyeUI.FocusManager.dialogHierarchies)


        # Remove the given dialog from the display hierarchy
        def closeDialog(dialogFrame):
            hier = WyeUI.FocusManager.findDialogHier(dialogFrame)
            #print("FocusManager closeDialog remove ", dialogFrame, " from len ", len(hier), ", ", hier)
            del hier[-1]    # remove dialog from hierarchy
            if len(hier) == 0:  # if that was the last dialog, remove hierarchy too
                #print(" hier empty, remove it")
                WyeUI.FocusManager.dialogHierarchies.remove(hier)
            #print("FocusManager closeDialog", WyeUI.FocusManager.dialogHierarchies)

        # User clicked on object
        # call each leaf dialog to see if obj belongs to it.
        # If so, return True (we used it)
        # else return False (someone else can use it)
        def doSelect(id):
            status = False
            for hier in WyeUI.FocusManager.dialogHierarchies:       # loop through them all to be sure only one dialog has field selected
                #print("FocusManager doSelect hier=", hier)
                if len(hier) > 0:
                    frm = hier[-1]
                    #print("FocusManager doSelect", frm, ",", frm.params[1][0], ",", id)
                    if not frm.parentFrame is None:
                        if frm.parentFrame.verb.doSelect(frm, id):
                            status = True
                    else:
                        if frm.verb.doSelect(frm, id):
                            status = True
            return status

        def doKey(key):
            # handle control codes.
            # if key, apply case
            match key:
                case Wye.ctlKeys.CTL_DOWN:
                    WyeUI.FocusManager.ctlDown = True
                    return True
                case Wye.ctlKeys.CTL_UP:
                    WyeUI.FocusManager.ctlDown = False
                    return True
                case Wye.ctlKeys.SHIFT_DOWN:
                    WyeUI.FocusManager.shiftDown = True
                    return True
                case Wye.ctlKeys.SHIFT_UP:
                    WyeUI.FocusManager.shiftDown = True
                    return True
                case _:
                    if isinstance(key, str) and 'a' <= key and key <= 'z' and WyeUI.FocusManager.shiftDown:
                        key = key.upper()
                    for hier in WyeUI.FocusManager.dialogHierarchies:
                        if len(hier) > 0:
                            frm = hier[-1]
                            #print("FocusManager doKey", frm, " ,", key)
                            # todo - figure out how to get rid of parentFrame hack
                            if hasattr(frm, "parentFrame"):
                                if frm.parentFrame.verb.doKey(frm, key):
                                    return True
                            else:
                                if frm.verb.doKey(frm, key):
                                    return True
                    return False



    # Input field classes
    # Each input run method just returns its frame as p0
    #
    # Dialog sets up input graphics when it runs
    # Since the input has run before the dialog does, it cannot do any graphic setup
    # because it doesn't know where it's going to be.  The Dialog manages that.
    # Therefore, all it can do is set up its info in its frame and return the frame for the
    # dialog to use.
    #
    # Effectively each is a factory generating an input object frame for dialog to use

    # label field
    # Technically not an input, but is treated as one for space
    class LabelInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE))  # 1 user supplied label for field
        varDescr = (("currPos", Wye.dType.INTEGER, 0),)  # 0

        def start(stack):
            return Wye.codeFrame(WyeUI.LabelInput, stack)

        def run(frame):
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

    # text input field
    class TextInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))  # 2 user supplied var to return value in
        varDescr = (("currPos", Wye.dType.INTEGER, 0),      # 0 3d pos
                    ("currVal", Wye.dType.STRING, ""),      # 1 current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),    # 2 text insertion point
                    ("gWidget", Wye.dType.OBJECT, None)     # 3 stashed graphic widget
                    )
        def start(stack):
            frm = Wye.codeFrame(WyeUI.TextInput, stack)
            return frm

        def run(frame):
            frame.vars[1][0] = frame.params[2][0]
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS


    # text input field
    class ButtonInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("verb", Wye.dType.STRING, Wye.access.REFERENCE),   # 2 verb to call when button clicked
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),   # 3 optional data
                      )
        varDescr = (("currPos", Wye.dType.INTEGER, 0),      # 0
                    ("gWidget", Wye.dType.OBJECT, None),    # 1 associated graphic widget
                    ("verb", Wye.dType.OBJECT, None),       # 2 verb to call
                    ("clickCount", Wye.dType.INTEGER, 0),   # 3 button depressed count
                    ("verbStack", Wye.dType.OBJECT_LIST, None), # 4 verb callback stack
                    )

        def start(stack):
            frm = Wye.codeFrame(WyeUI.ButtonInput, stack)
            frm.vars[WyeUI.ButtonInput.vConst.verbStack][0] = []
            return frm

        def run(frame):
            frame.vars[2][0] = frame.params[2][0]       # save verb to call
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS


    # Dialog object.
    # Display and run input fields
    class Dialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.OBJECT, Wye.access.REFERENCE),    # 0 return own frame
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog frame, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE)) # 4+ variable length list of input control frames
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),          # 0 pos copy
                    ("dlgWidgets", Wye.dType.OBJECT_LIST, None),            # 1 standard dialog widgets
                    ("dlgTags", Wye.dType.STRING_LIST, None),               # 2 OK, Cancel widget tags
                    ("inpTags", Wye.dType.OBJECT, None),                    # 3 dictionary return param ix of input by graphic tag
                    ("currInp", Wye.dType.INTEGER, -1),                     # 4 index to current focus widget, if any
                    ("clickedBtns", Wye.dType.OBJECT_LIST, None),           # 5 list of buttons that need to be unclicked
                    ("topGObj", Wye.dType.OBJECT, None),                    # 6 path to top graphic obj (to hang sub dlgs off)
                    ("bgndGObj", Wye.dType.OBJECT, None),                   # 7 background card
                    )
        def start(stack):
            #print("Dialog start")

            frame = Wye.codeFrame(WyeUI.Dialog, stack)
            # give frame unique lists
            frame.vars[1][0] = []   # standard widgets common to all Dialogs
            frame.vars[2][0] = []   # Ok, Cancel widgets
            frame.vars[3][0] = {}   # map input widget to input sequence number
            frame.vars[5][0] = []   # clicked button(s) being "blinked"
            return frame

        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    frame.params[0][0] = frame      # return own frame as p0
                    parent = frame.params[3][0]
                    WyeUI.FocusManager.openDialog(frame, parent)  # pass parent, if any
                    frame.params[WyeUI.Dialog.pConst.frame][0] = frame  # self referential!
                    #print("Dialog put frame in param[0][0]", frame)
                    frame.vars[WyeUI.Dialog.vConst.position] = (frame.params[2])        # save display position
                    # return frame

                    #print("Dialog display: pos=frame.params[2]", frame.params[2])
                    if parent is None:
                        dlgHeader = WyeUI._label3d(text=frame.params[1][0], color=(1, 1, 1, 1), pos=frame.params[2], scale=(.2, .2, .2))
                    else:
                        dlgHeader = WyeUI._label3d(text=frame.params[1][0], color=(1, 1, 1, 1), pos=frame.params[2],
                                                   scale=(1,1,1), parent=parent.vars[6][0].getNodePath())

                    frame.vars[1][0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars[6][0] = dlgHeader        # save graphic for parenting sub dialogs

                    pos = [0, 0, 0] # [x for x in frame.params[2]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = (len(frame.params) - 4)
                    #print("Dialog ", nInputs, " user widgets. nParams=", len(frame.params))
                    # draw user- supplied label and text inputs
                    for ii in range(nInputs):
                        pos[2] -= 1.5

                        #print("Dialog input", ii, " param ", 4+(ii*2))
                        inFrm = frame.params[4+ii][0]
                        #print("    Dialog input ", ii, " inFrm", inFrm)
                        #print("       inFrm.params[1]", inFrm.params[1])
                        #print("")

                        inFrm.parentFrame = frame

                        if inFrm.verb is WyeUI.LabelInput:
                            lbl = WyeUI._label3d(inFrm.params[1][0], (1, 0, 0, 1), pos=tuple(pos),
                                                              scale=(1,1,1), parent=dlgHeader.getNodePath())
                            frame.vars[1][0].append(lbl)  # save graphic widget for deleting on dialog close

                        elif inFrm.verb is WyeUI.TextInput:
                            lbl = WyeUI._label3d(inFrm.params[1][0], (1, 0, 0, 1), pos=tuple(pos),
                                                          scale=(1,1,1), parent=dlgHeader.getNodePath())
                            frame.vars[1][0].append(lbl)    # save graphic widget for deleting on dialog close

                            # add tag, input index to dictionary
                            frame.vars[3][0][lbl.getTag()] = ii     # tag => inp index dictionary (both label and entry fields point to inp frm)
                            # offset 3d input field past end of 3d label
                            lblGFrm = lbl.text.getFrameActual()
                            width = (lblGFrm[1] - lblGFrm[0]) * 1 + .5
                            txt = WyeUI._label3d(inFrm.vars[1][0], (1, 0, 0, 1),
                                                              pos=(pos[0] + width, pos[1], pos[2]), scale=(1,1,1), parent=dlgHeader.getNodePath())
                            #print("    Dialog inWdg", txt)
                            frame.vars[1][0].append(txt)    # save graphic widget for deleting on dialog close
                            inFrm.vars[3][0] = txt          # stash graphic obj in input's frame
                            frame.vars[3][0][txt.getTag()] = ii     # add tag and inp param index to dict (so evt can find inp frame)
                        elif inFrm.verb is WyeUI.ButtonInput:

                            btn = WyeUI._label3d(inFrm.params[1][0], (1, 0, 0, 1), pos=tuple(pos),
                                                              scale=(1,1,1), parent=dlgHeader.getNodePath())
                            frame.vars[1][0].append(btn)  # save for deleting on dialog close
                            frame.vars[3][0][btn.getTag()] = ii  # add tag and inp param index to dict (so evt can find inp frame)
                            inFrm.vars[1][0] = btn  # stash graphic obj in input's frame
                        else:
                            print("Dialog: Error. Unknown input verb", inFrm.verb.__class__)

                    #print("Dialog has input widgets", frame.vars[3])

                    # display OK, Cancel buttons
                    pos[2] -= 1.5
                    txt = WyeUI._label3d("OK", color=(1, 1, 1, 1), pos=tuple(pos), scale=(1,1,1), parent=dlgHeader.getNodePath())
                    frame.vars[1][0].append(txt)
                    frame.vars[2][0].append(txt.getTag())
                    pos[0] += 2.5
                    txt = WyeUI._label3d("Cancel", color=(1, 1, 1, 1), pos=tuple(pos),
                                                      scale=(1,1,1), parent=dlgHeader.getNodePath())
                    frame.vars[1][0].append(txt)
                    frame.vars[2][0].append(txt.getTag())
                    # done setup, go to next case to process events
                    frame.PC += 1

                    # make a background for entire dialog
                    if parent is None:
                        scMult = 5
                    else:
                        scMult = 1
                    dlgNodePath = frame.vars[6][0].getNodePath()
                    dlgBounds = dlgNodePath.getTightBounds()
                    card = CardMaker("Dlg Bgnd")
                    gFrame = LVecBase4f(0, 0, 0, 0)
                    # print("gFrame", gFrame)
                    ht = (dlgBounds[1][2] - dlgBounds[0][2]) * scMult + 1
                    wd = (dlgBounds[1][0] - dlgBounds[0][0]) * scMult + 1
                    gFrame[0] = 0                                  # marginL
                    gFrame[1] = wd  # marginR
                    gFrame[2] = 0  # marginB
                    gFrame[3] = ht # marginT
                    # print("initial adjusted gFrame", gFrame)
                    card.setFrame(gFrame)
                    cardPath = NodePath(card.generate())
                    cardPath.reparentTo(dlgNodePath)
                    cardPath.setPos((-.5, .1, 1.2 - ht))

                case 1:
                    # do end of click-blink for buttons
                    delLst = []
                    # decrement blink count.  if zero, turn off button highlight
                    for btnFrm in frame.vars[WyeUI.Dialog.vConst.clickedBtns][0]:
                        #print("button ", btnFrm.verb.__name__, " count ", btnFrm.vars[WyeUI.ButtonInput.vConst.clickCount][0])
                        btnFrm.vars[WyeUI.ButtonInput.vConst.clickCount][0] -= 1
                        if btnFrm.vars[WyeUI.ButtonInput.vConst.clickCount][0] <= 0:
                            #print("Dialog run: Done click flash for button ", btnFrm.verb.__name__)
                            delLst.append(btnFrm)
                            btnFrm.vars[1][0].setColor((0, 0, 0, 1))
                    # remove any buttons whose count is finished
                    for btnFrm in delLst:
                        #print("Dialog run: Remove clicked btn frame", btnFrm.verb.__name__)
                        frame.vars[WyeUI.Dialog.vConst.clickedBtns][0].remove(btnFrm)

        def doSelect(frame, tag):
            #print("Dialog doSelect: ", frame.verb, " tag", tag)
            prevSel = frame.vars[4][0]      # get current selection
            # if tag is input field in this dialog, select it
            closing = False

            # if clicked on input field
            if tag in frame.vars[3][0]:        # do we have a matching tag?
                print("Dialog header bounds", frame.vars[6][0].getNodePath().getTightBounds())

                ix = frame.vars[3][0][tag]     # Yes
                # process dialog inputs
                if frame.verb is WyeUI.Dialog:
                    inFrm = frame.params[4+ix][0]
                    # if is text input make it selected
                    if inFrm.verb is WyeUI.TextInput:
                        inWidg = inFrm.vars[3][0]
                        #print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                        inWidg.setColor((0,.25,0,1))        # set input background to "has focus" color
                        frame.vars[WyeUI.Dialog.vConst.currInp][0] = ix           # save as current input focus
                    # button callback
                    elif inFrm.verb is WyeUI.ButtonInput:
                        callVerb = inFrm.vars[2][0]
                        inFrm.vars[1][0].setColor((0, .25, 0, 1)) # set button color pressed
                        if inFrm.vars[WyeUI.ButtonInput.vConst.clickCount][0] <= 0:     # if not in an upclick count, process click
                            #print("Dialog doSelect: Start clicked countdown for", inFrm.verb.__name__)
                            inFrm.vars[WyeUI.ButtonInput.vConst.clickCount][0] = 10       # start flash countdown (in display frames)
                            frame.vars[WyeUI.Dialog.vConst.clickedBtns][0].append(inFrm)  # stash button for flash countdown

                            # if something to call
                            if not callVerb is None:
                                #print("Dialog doSelect: clicked btn, verb ", callVerb.__name__)
                                # start the verb
                                verbFrm = callVerb.start(frame.SP)
                                # handle user data
                                if len(inFrm.params) > 3:
                                    print("Button callback", callVerb.__name__, " user data", inFrm.params[3][0])
                                    data = inFrm.params[3][0]
                                else:
                                    data = None
                                # if not single cycle, then put up as parallel path
                                if callVerb.mode != Wye.mode.SINGLE_CYCLE:
                                    # call every display cycle
                                    WyeCore.World.setRepeatEventCallback("Display", verbFrm, data)
                                else:
                                    # call once
                                    #print("doSelect call single cycle verb ", verbFrm.verb.__name__)
                                    verbFrm.eventData = (tag, data)  # pass along user supplied event data, if any
                                    verbFrm.verb.run(verbFrm)

                        frame.vars[WyeUI.Dialog.vConst.currInp][0] = -1       # no input has focus

                # if dropdown, currInp is dropdown index
                elif frame.verb is WyeUI.DropDown:
                    print("Dropdown selected line ", ix)
                    frame.vars[WyeUI.Dialog.vConst.currInp][0] = ix


            # if clicked on OK or Cancel
            elif tag in frame.vars[2][0]:
                # if is OK button
                if tag == frame.vars[2][0][0]:
                    #print("Dialog", frame.params[1][0], " OK Button pressed")
                    nInputs = (len(frame.params) - 4)
                    for ii in range(nInputs):
                        inFrm = frame.params[4+ii][0]
                        # for any text inputs, copy working string to return string
                        if inFrm.verb is WyeUI.TextInput:
                            #print("input", ii, " frame", inFrm, "\n", WyeCore.Utils.frameToString(inFrm))
                            #print("input old val '"+ inFrm.params[2][0]+ "' replaced with '"+ inFrm.vars[1][0]+"'")
                            inFrm.params[2][0] = inFrm.vars[1][0]
                    frame.status = Wye.status.SUCCESS

                # else is Cancel button
                else:
                    #print("Dialog", frame.params[1][0], " Cancel Button pressed")
                    frame.status = Wye.status.FAIL
                # clean up dialog
                #print("Close dialog")
                # remove dialog from active dialog list
                WyeUI.FocusManager.closeDialog(frame)
                # delete the graphic widgets associated with the dialog
                for wdg in frame.vars[1][0]:
                    #print("del ctl ", wdg.text.name)
                    wdg.removeNode()
                closing = True

            # selected graphic tag not recognized as a control in this dialog
            else:
                frame.vars[4][0] = -1   # no currInp

            # If there was a diff selection before, fix that
            # (if closing dialog, nevermind)
            if prevSel > -1 and prevSel != frame.vars[4][0] and not closing:
                inFrm =frame.params[4+prevSel][0]
                if inFrm.verb is WyeUI.TextInput:
                    inWidg = inFrm.vars[3][0]
                    inWidg.setColor((0,0,0, 1))

        def doKey(frame, key):
            # if we have an input with focus
            ix = frame.vars[4][0]
            if ix >= 0:
                inFrm = frame.params[4 + ix][0]
                txt = inFrm.vars[1][0]
                insPt = inFrm.vars[2][0]
                preTxt = txt[:insPt]
                postTxt = txt[insPt:]
                # delete key
                if key == '\u0008':         # delete key
                    if insPt > 0:
                        preTxt = preTxt[:-1]
                        insPt -= 1
                        inFrm.vars[2][0] = insPt
                    txt = preTxt + postTxt
                # arrow keys
                elif key == Wye.ctlKeys.LEFT:   # arrow keys
                    if insPt > 0:
                        insPt -= 1
                        inFrm.vars[2][0] = insPt
                    return
                elif key == Wye.ctlKeys.RIGHT:
                    if insPt < len(txt):
                        insPt += 1
                        inFrm.vars[2][0] = insPt
                    return
                # printable key, insert it in the string
                else:
                    txt = preTxt + key + postTxt
                    insPt += 1
                    inFrm.vars[2][0] = insPt        # set text insert point after new char
                inFrm.vars[1][0] = txt
                inWidg = inFrm.vars[3][0]
                #print("  set text", txt," ix", ix, " txtWidget", inWidg)
                inWidg.setText(txt)


    # dropdown menu
    # subclass of Dialog so FocusManager can handle focus properly
    class DropDown(Dialog):
        def start(stack):
            frame = Wye.codeFrame(WyeUI.DropDown, stack)
            frame.vars[1][0] = []   # standard widgets common to all Dialogs
            frame.vars[2][0] = []   # not used
            frame.vars[3][0] = {}   # map input widget to input sequence number
            frame.vars[5][0] = []   # clicked button(s) being "blinked"
            return frame

        def run(frame):
            match(frame.PC):
                case 0:  # Start up case - set up all the fields
                    print("DropDown frame ", WyeCore.Utils.frameToString(frame))
                    frame.params[0][0] = frame  # return own frame as p0
                    parent = frame.params[3][0]
                    WyeUI.FocusManager.openDialog(frame, parent)  # pass parent, if any
                    frame.params[WyeUI.Dialog.pConst.frame][0] = frame  # self referential!
                    # print("DropDown put frame in param[0][0]", frame)
                    frame.vars[WyeUI.Dialog.vConst.position] = (frame.params[2])  # save display position
                    # return frame

                    lines = frame.params[WyeUI.Dialog.pConst.inputs]
                    print("DropDown lines ", len(lines), ":", lines)
                    # first line becomes header that rest hang off of
                    if parent is None:
                        dlgHeader = WyeUI._label3d(text=lines[0], color=(1, 1, 0, 1), pos=frame.params[2],
                                                   scale=(.2, .2, .2))
                    else:
                        dlgHeader = WyeUI._label3d(text=lines[0], color=(1, 1, 0, 1), pos=frame.params[2],
                                                   scale=(1, 1, 1), parent=parent.vars[6][0].getNodePath())

                    frame.vars[1][0].append(dlgHeader)  # save graphic for DropDown delete
                    frame.vars[6][0] = dlgHeader  # save graphic for parenting sub dialogs
                    frame.vars[3][0][dlgHeader.getTag()] = 0  # tag => inp index dictionary (both label and entry fields point to inp frm)

                    pos = [0, 0, 0]  # [x for x in frame.params[2]]    # copy position

                    nLines = len(lines)
                    if nLines > 1:
                        for ii in range(1, nLines):
                            pos[2] -= 1.5
                            lbl = WyeUI._label3d(lines[ii], (1, 1, 0, 1), pos=tuple(pos),
                                                 scale=(1, 1, 1), parent=dlgHeader.getNodePath())
                            frame.vars[1][0].append(lbl)  # save graphic widget for deleting on DropDown close
                            frame.vars[3][0][lbl.getTag()] = ii  # tag => inp index dictionary (both label and entry fields point to inp frm)

                    # done setup, go to next case to process events
                    frame.PC += 1

                    # make a background for entire DropDown
                    if parent is None:
                        scMult = 5  # no parent, everything has been scaled by .2
                    else:
                        scMult = 1  # have parent, already scaled by parent
                    dlgNodePath = dlgHeader.getNodePath()
                    dlgBounds = dlgNodePath.getTightBounds()
                    card = CardMaker("Dlg Bgnd")
                    gFrame = LVecBase4f(0, 0, 0, 0)
                    # print("gFrame", gFrame)
                    ht = (dlgBounds[1][2] - dlgBounds[0][2]) * scMult + 1
                    wd = (dlgBounds[1][0] - dlgBounds[0][0]) * scMult + 1
                    gFrame[0] = 0  # marginL
                    gFrame[1] = wd  # marginR
                    gFrame[2] = 0  # marginB
                    gFrame[3] = ht  # marginT
                    # print("initial adjusted gFrame", gFrame)
                    card.setFrame(gFrame)
                    cardPath = NodePath(card.generate())
                    cardPath.reparentTo(dlgNodePath)
                    cardPath.setPos((-.5, .1, 1.2 - ht))

                case 1:
                    # if click event set status, we're done, clean up
                    if frame.vars[WyeUI.Dialog.vConst.currInp][0] > -1:
                        # remove dialog from active dialog list
                        WyeUI.FocusManager.closeDialog(frame)
                        # delete the graphic widgets associated with the dialog
                        for wdg in frame.vars[1][0]:
                            # print("del ctl ", wdg.text.name)
                            wdg.removeNode()
                        frame.status = Wye.status.SUCCESS
