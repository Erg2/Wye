# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *

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
        # elements.append(WyeCore.libs.WyeUI._label3d("Stream 0", color=(0, 1, 0, 1), pos=(0, 10, yy), scale=(.2, .2, .2)))
        WyeCore.libs.WyeUI._label3d(txt, color=(0, 1, 0, 1), pos=(txtCoord[0], txtCoord[1], txtCoord[2]),
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
                    #elements.append(WyeCore.libs.WyeUI._label3d("Stream 0", color=(0, 1, 0, 1), pos=(0, 10, yy), scale=(.2, .2, .2)))
                    WyeCore.libs.WyeUI._label3d(txt, color=WyeUI.TEXT_COLOR, pos=(txtCoord[0], txtCoord[1], txtCoord[2]), scale=WyeUI.TEXT_SCALE)
                    txtCoord[2] -= WyeUI.LINE_HEIGHT
                    if hasattr(verb, "codeDescr"):
                        txtCoord[2] = WyeUI._displayVerb(verb, txtCoord)


            
    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class _label3d:
        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.text = None
            self.card = None
            self._label3d = None
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
            self._label3d.setColor(color)

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
            self._label3d.setPos(val)

        def setColor(self, val):
            self._label3d.setColor(val)

        def setScale(self, val):
            self._label3d.setScale(val)

        def setWordWrap(self):
            return self.text.getWordwrap()

        def getText(self):
            return self.text.getText()

        def getPos(self):
            return self._label3d.getPos()

        def getColor(self):
            return self._label3d.getColor()

        def getScale(self):
            return self._label3d.getScale()

        def getWordWrap(self):
            return self.text.setWordwrap()

        def getTag(self):
            return self.text.name

        def getAlign(self):
            return self.text.getAlign()

        def getFrameColor(self):
            return self._label3d.getColor()

        # update the margin spacing
        def getFrameAsMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        # rebuild card and path for updated text object
        def _regen3d(self):
            bg = self._label3d.getColor()
            pos = self._label3d.getPos()
            scale = self._label3d.getScale()
            self._genCardObj()                     # generate new card obj for updated text object
            self._label3d.detachNode()                # detach 3d node path to old card
            self._gen3dTextObj(pos, scale, bg)     # make new 3d node path to new card

        # internal rtn to gen text object with unique wyeTag name
        def _genTextObj(self, text, color=(1,1,1,1)):
            tag = "txt"+str(WyeCore.Utils.getId())
            self.text = TextNode(tag)
            self.text.setText(text)
            self.text.setTextColor(color)

        # internal rtn to gen 3d Card clickable background object
        def _genCardObj(self):
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
        def _gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            global render

            self._label3d = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            self._label3d.attachNewNode(self.text)
            self._label3d.setEffect(DecalEffect.make())        # glue text onto card
            self._label3d.reparentTo(render)
            WyeCore.picker.makePickable(self._label3d)         # make selectable
            self._label3d.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self._label3d.setPos(pos)
            self._label3d.setScale(scale)

            self._label3d.setBillboardPointWorld(0.)           # always face the camera
            self._label3d.setLightOff()                        # unaffected by world lighting
            self._label3d.setColor(bg)

    # text entry verb
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
            ("text", Wye.dType.STRING, "---"),   # 2
           )   # var 4

        # np=loader.loadModel("jack") #load a model
        # #... do something
        # np.removeNode() #unload the model
        # loader.unloadModel(path)


        def __init__(self, text="", color=(1, 1, 1, 1), pos=(0, 0, 0), scale=(1, 1, 1), bg=(0, 0, 0, 1)):
            label = WyeUI._label3d(text, color, pos, scale, bg)

#    class displayDialog:

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
        hasFocus = None                 # frame of input that currently has focus, if any
        focusDialog = None              # frame of dialog that current input belongs to
        _mouseHandler = None

        # Mouse event delivery requires an instantiated class
        class _MouseHandler(DirectObject):
            def __init__(self):
                print("WyeUI FocusManager openDialog set mouse event")
                self.accept('mouse1', self.mouseEvt)

            def mouseEvt(self):
                evt = WyeCore.base.mouseWatcherNode.getMouse()
                print("FocusManager mouseEvt:", evt)

                # todo - deliver event to leaf dialogs

        # find dialogFrame in leaf nodes of dialog hierarchies
        def findDialog(dialogFrame):
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

            # if starting new dialog hierarchy
            if parentFrame is None:
                WyeUI.FocusManager.dialogHierarchies.append([dialogFrame])

            # if has parent then add it to the parent's hierarchy
            else:
                hier = WyeUI.FocusManager.findDialog(parentFrame)
                if not hier is None:
                    hier.append(dialogFrame)

        # Remove the given dialog from the display hierarchy
        def closeDialog(dialogFrame):
            hier = WyeUI.FocusManager.findDialog(dialogFrame)
            del hier[-1]    # remove dialog from hierarchy
            if len(hier) == 0:  # if that was the last dialog, remove hierarchy too
                WyeUI.FocusManager.dialogHierarchies.remove(hier)


        # User clicked on object
        # find it
        # set it as having focus
        # todo - manage hierarchy
        def doSelectEvent(id):
            print("FocusManager doSelectEvent")
            return False


