# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *
#from functools import partial
#import traceback
#import sys
#from sys import exit
#from direct.showbase import Audio3DManager

#for 3d geometry (input cursor)
#from direct.showbase.ShowBase import ShowBase

from functools import partial

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import MouseButton

# 3d UI element library
class WyeUI(Wye.staticObj):
    LINE_HEIGHT = 1.25
    TEXT_SCALE = (.2,.2,.2)

    TEXT_COLOR = (.2,.2,.2,1)
    SELECTED_COLOR = (0,.4,0,1)
    LABEL_COLOR = (1, 0, 0, 1)
    BACKGROUND_COLOR = (0, 0, 0, 1)
    HEADER_COLOR = (1,1,1,1)
    CURSOR_COLOR = (0,1,0,1)

    # create a piece of geometry
    # this is a real class that gets instantiated
    class _geom3d:

        def __init__(self, size, pos=[0,0,0]):
            # Instantiate a vertex buffer
            # https://stackoverflow.com/questions/75774821/how-to-create-three-dimensional-geometric-shapes-in-panda3d-in-python
            # https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-vertex-data
            format = GeomVertexFormat.getV3c4()
            format = GeomVertexFormat.registerFormat(format)
            vdata = GeomVertexData("name", format, Geom.UHStatic)
            vertex = GeomVertexWriter(vdata, "vertex")
            color = GeomVertexWriter(vdata, "color")

            # Add vertices and colors
            vertex.addData3f(-1*size[0], -1*size[1], -1*size[2])
            color.addData4f(0, 0, 0, 1)

            vertex.addData3f(-1*size[0], -1*size[1], 1*size[2])
            color.addData4f(0, 0, 1, 1)

            vertex.addData3f(-1*size[0], 1*size[1], -1*size[2])
            color.addData4f(0, 1, 0, 1)

            vertex.addData3f(-1*size[0], 1*size[1], 1*size[2])
            color.addData4f(0, 1, 1, 1)

            vertex.addData3f(1*size[0], -1*size[1], -1*size[2])
            color.addData4f(1, 0, 0, 1)

            vertex.addData3f(1*size[0], -1*size[1], 1*size[2])
            color.addData4f(1, 0, 1, 1)

            vertex.addData3f(1*size[0], 1*size[1], -1*size[2])
            color.addData4f(1, 1, 0, 1)

            vertex.addData3f(1*size[0], 1*size[1], 1*size[2])
            color.addData4f(1, 1, 1, 1)

            # Create the triangles (2 per face)
            # https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-primitives
            prim = GeomTriangles(Geom.UHStatic)
            prim.addVertices(0, 1, 2)
            prim.addVertices(2, 1, 3)
            prim.addVertices(2, 3, 6)
            prim.addVertices(6, 3, 7)
            prim.addVertices(6, 7, 4)
            prim.addVertices(4, 7, 5)
            prim.addVertices(4, 5, 0)
            prim.addVertices(0, 5, 1)
            prim.addVertices(1, 5, 3)
            prim.addVertices(3, 5, 7)
            prim.addVertices(6, 4, 2)
            prim.addVertices(2, 4, 0)

            geom = Geom(vdata)
            geom.addPrimitive(prim)
            node = GeomNode("node")
            node.addGeom(geom)

            self.node = node

            self.path = render.attachNewNode(self.node)
            self.path.setPos(pos[0], pos[1], pos[2])

    # Build run_rt methods on each class
    def build():
        WyeCore.Utils.buildLib(WyeUI)

#    # utility functions for building 3d objects
#    def _displayCommand(cmd, coord):
#        txt = str([str(e) for e in cmd])
#        txtCoord = list(coord)
#        # elements.append(WyeUI._label3d("Stream 0", color=(0, 1, 0, 1), pos=(0, 10, yy), scale=(.2, .2, .2)))
#        WyeUI._label3d(txt, color=(0, 1, 0, 1), pos=(txtCoord[0], txtCoord[1], txtCoord[2]),
#                                   scale=(.2, .2, .2))
#        txtCoord[2] -= WyeUI.LINE_HEIGHT
#        return txtCoord[2]
#
#    def _displayVerb(verb, coord):
#        cd = verb.codeDescr
#        xyz = list(coord)
#        xyz[0] += WyeUI.LINE_HEIGHT
#        if verb.mode == Wye.mode.PARALLEL:
#            for codeBlock in cd:
#                for cmd in codeBlock:
#                    xyz[2] = WyeUI._displayCommand(cmd, xyz)
#                xyz[2] -= WyeUI.LINE_HEIGHT
#        else:
#            for cmd in cd:
#                xyz[2] = WyeUI._displayCommand(cmd, xyz)
#
#        xyz[2] -= WyeUI.LINE_HEIGHT
#        return xyz[2]
#
#    def _displayLibOld(lib, coord, elements=None):
#        txtCoord = list(coord)
#        verbLst = WyeCore.Utils.getLibEntries(lib)
#        for verb in verbLst:
#            #print("lib", lib.__name__, " verb", verb.__name__)
#            txt = lib.__name__ + "." +verb.__name__
#            txtCoord[2] -= WyeUI.LINE_HEIGHT
#            WyeUI._label3d(txt, color=WyeUI.TEXT_COLOR, pos=(txtCoord[0], txtCoord[1], txtCoord[2]), scale=WyeUI.TEXT_SCALE)
#            txtCoord[2] -= WyeUI.LINE_HEIGHT
#            if hasattr(verb, "codeDescr"):
#                txtCoord[2] = WyeUI._displayVerb(verb, txtCoord)
#
#    class _displayLibCallback():
#        mode = Wye.mode.SINGLE_CYCLE
#        dataType = Wye.dType.STRING
#        paramDescr = ()
#        varDescr = (("count", Wye.dType.INTEGER, 0),)
#
#        def start(stack):
#            return Wye.codeFrame(WyeUI._displayLibCallback, stack)
#
#        def run(frame):
#            print("Display Lib Callback event data", frame.eventData)
#            rowIx = frame.eventData[1]
#            # return (dropdown index, verb) tuple in dropdown dialog's first param
#            setattr(frame.params, frame.firstParamName(), (rowIx, WyeCore.Utils.getLibEntries()[rowIx]))
#            pass
#            #print("_displayLibCallback data=", frame.eventData, " index = ", frame.eventData[1])
#
#            # really bad coding / wizardry required here
#            # Get the text widget of the
#       #     inFrm = frame.eventData[1][0]
#       #     var = frame.eventData[1][1]
#       #     #print("data [1]", frame.eventData[1][1], " var", var)
#       #     dlgFrm = inFrm.parentFrame
#       #     #print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
##
#       #     var[0] += 1
##
#       #     # get label input's frame from parent dialog
#       # TODO fix dialog inputs
#       #     lblFrame = dlgFrm.params.inputs+3][0]
##
#       #     # supreme hackery - look up the display label in the label's graphic widget list
#       #     inWidg = lblFrame.vars.frame[0][0]
#       #     txt = "Count " + str(var[0])
#       #     # print("  set text", txt," ix", ix, " txtWidget", inWidg)
#       #     inWidg.setText(txt)
##
#       #     if var[0] >= 10:
#       #         var[0] = 0
#
#
#    def _displayLib(frame, dlgPos, lib, coord, elements=None):
#        txtCoord = list(coord)
#
#        # how good is Python's GC.  Will this temp list stay as long as it's used or will it go away, crashing everything?
#        dlgFrm = WyeUI.Dialog.start([])
#
#        dlgFrm.params.retVal =[0]
#        dlgFrm.params.title = [lib.__name__]
#        dlgFrm.params.position=coord
#        dlgFrm.params.parent = [None]
#
#        # build dialog frame params list of input frames
#        attrIx = 0
#        #print("_displayLib: process library", lib.__name__)
#        for attr in dir(lib):
#            if attr != "__class__":
#                verb = getattr(lib, attr)
#                if inspect.isclass(verb):
#                    #print("lib", lib.__name__, " verb", verb.__name__)
#                    btnFrm = WyeUI.InputButton.start(dlgFrm.SP)
#                    dlgFrm.params.inputs[0].append([btnFrm])
#
#                    txt = lib.__name__ + "." +verb.__name__
#                    btnFrm.params.frame = [None]
#                    btnFrm.params.parent = [None]        # return value
#                    btnFrm.params.label = [txt]     # button label is verb name
#                    btnFrm.params.verb = [WyeUI._displayLibCallback]   # button callback
#                    btnFrm.params.optData = [attrIx]       # button data - offset to button
#                    WyeUI.InputButton.run(btnFrm)
#
#                    attrIx += 1
#
#        #WyeUI.Dialog.run(dlgFrm)
#        frame.SP.append(dlgFrm)

            
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
            self._nodePath.setBillboardAxis()
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

    class CameraControl(DirectObject):
        def __init__(self):
            self.m1Down = False
            self.m2Down = False
            self.m3Down = False

            self.accept('mouse1', self.mouseEvt)
            self.accept('mouse2', self.mouseEvt)
            self.accept('mouse3', self.mouseEvt)
            self.accept('mouse1-up', self.mouseEvt)
            self.accept('mouse2-up', self.mouseEvt)
            self.accept('mouse3-up', self.mouseEvt)



        def mouseEvt(self):
            global base
            evt = WyeCore.base.mouseWatcherNode.getMouse()
            self.m1Down = base.mouseWatcherNode.isButtonDown(MouseButton.one())
            self.m2Down = base.mouseWatcherNode.isButtonDown(MouseButton.two())
            self.m3Down = base.mouseWatcherNode.isButtonDown(MouseButton.three())
            #print("CameraControl mouseEvt: m1Down", self.m1Down, " m2Down", self.m2Down, " m3Down", self.m3Down)

        def mouseMove(self, x, y):
            #print("CameraControl mousemove:", x, ",", y)
            if self.m1Down:
                # rotate viewpoing
                pass
            elif self.m2Down:
                # move viewpoint
                pass


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

        _dialogHierarchies = []          # list of open dialog hierarchies (dialog frame lists)
        #_mouseHandler = None

        _shiftDown = False
        _ctlDown = False

        _activeDialog = None
        _mouseHandler = None

        class MouseHandler(DirectObject):
            def __init__(self):
                #print("FocusManager create MouseHandler")
                self.accept('wheel_up', partial(self.mouseWheel, 1))
                self.accept('wheel_down', partial(self.mouseWheel, -1))

                ## reference - events
                # "escape", "f" + "1-12"(e.g.
                # "f1", "f2", ...
                # "f12"), "print_screen",
                # "scroll_lock", "backspace", "insert", "home", "page_up", "num_lock",
                # "tab", "delete", "end", "page_down", "caps_lock", "enter", "arrow_left",
                # "arrow_up", "arrow_down", "arrow_right", "shift", "lshift", "rshift",
                # "control", "alt", "lcontrol", "lalt", "space", "ralt", "rcontrol"
                ## end reference

            # if there's an active dialog, pass it mousewheel events
            def mouseWheel(self, dir):
                #print("mouseWheel", dir)
                if WyeUI.FocusManager._activeDialog:
                    #print("MouseHandler: mouseWheel", dir)
                    WyeUI.FocusManager._activeDialog.verb.doWheel(dir)


        # find dialogFrame in leaf nodes of dialog hierarchies
        def findDialogHier(dialogFrame):
            retHier = None
            for hier in WyeUI.FocusManager._dialogHierarchies:
                # if found it, add to hierarchy list
                if len(hier) > 0 and hier[-1] == dialogFrame:
                    retHier = hier
                    break  # found it, break out of loop

            if retHier is None:
                print("Error: WyeUI FocusManager findDialogHier - dialog not found")
                print("  dialog title", dialogFrame.params.title[0])
            return retHier


        # User is adding a dialog to the display
        # If it has a parent dialog, it is now the leaf of the hierarchy and
        # its inputs get any incoming events
        def openDialog(dialogFrame, parentFrame):
            # if no focus manager set to catch selected objects, fix that
            if WyeCore.Utils.getFocusManager() is None:
                WyeCore.Utils.setFocusManager(WyeUI.FocusManager)
                
            if WyeUI.FocusManager._mouseHandler is None:
                WyeUI.FocusManager._mouseHandler = WyeUI.FocusManager.MouseHandler()

            # connect to parent frame
            dialogFrame.parentFrame = parentFrame

            # if starting new dialog hierarchy
            if parentFrame is None:
                WyeUI.FocusManager._dialogHierarchies.append([dialogFrame])
                #print("Wye UI FocusManager openDialog: no parent, add dialog", dialogFrame," to hierarchy list", WyeUI.FocusManager._dialogHierarchies)

            # if has parent then add it to the parent's hierarchy
            else:
                #print("WyeUI FocusManager openDialog find parentFrame ", parentFrame)
                hier = WyeUI.FocusManager.findDialogHier(parentFrame)
                if not hier is None:
                    hier.append(dialogFrame)
                else:
                    print("Error: WyeUI FocusManager openDialog - did not find parent dialog", parentFrame, " in", WyeUI.FocusManager._dialogHierarchies)

            #print("FocusManager openDialog", WyeUI.FocusManager._dialogHierarchies)


        # Remove the given dialog from the display hierarchy
        def closeDialog(dialogFrame):
            #print("FocusManager closeDialog", dialogFrame)
            hier = WyeUI.FocusManager.findDialogHier(dialogFrame)
            #print("FocusManager closeDialog remove", dialogFrame, " from len", len(hier), ", hier", hier)
            del hier[-1]    # remove dialog from hierarchy
            if len(hier) == 0:  # if that was the last dialog, remove hierarchy too
                #print(" hier now empty, remove it")
                WyeUI.FocusManager._dialogHierarchies.remove(hier)
            #print("FocusManager closeDialog complete: hierarchies", WyeUI.FocusManager._dialogHierarchies)
            if dialogFrame == WyeUI.FocusManager._activeDialog:
                WyeUI.FocusManager._activeDialog = None

            # User clicked on object
        # call each leaf dialog to see if obj belongs to it.
        # If so, return True (we used it)
        # else return False (someone else can use it)
        def doSelect(id):
            status = False
            WyeUI.Dialog.hideCursor()
            WyeUI.FocusManager._activeDialog = None
            for hier in WyeUI.FocusManager._dialogHierarchies:       # loop through them all to be sure only one dialog has field selected
                #print("FocusManager doSelect hier=", hier)
                if len(hier) > 0:
                    frm = hier[-1]
                    #print("FocusManager doSelect", frm, ",", frm.params.title[0], ",", id)
                    if not frm.parentFrame is None:
                        if frm.parentFrame.verb.doSelect(frm, id):
                            WyeUI.FocusManager._activeDialog = frm.parentFrame
                            #print("doSelect: Active dialog", WyeUI.FocusManager._activeDialog.params.title)
                            status = True
                    else:
                        if frm.verb.doSelect(frm, id):
                            WyeUI.FocusManager._activeDialog = frm
                            #print("doSelect: Active dialog", WyeUI.FocusManager._activeDialog.params.title)
                            status = True
            return status

        def doKey(key):
            # handle control codes.
            # if key, apply case
            match key:
                # check for control codes
                case Wye.ctlKeys.CTL_DOWN:
                    WyeUI.FocusManager._ctlDown = True
                    return True
                case Wye.ctlKeys.CTL_UP:
                    WyeUI.FocusManager._ctlDown = False
                    return True
                case Wye.ctlKeys.SHIFT_DOWN:
                    WyeUI.FocusManager._shiftDown = True
                    return True
                case Wye.ctlKeys.SHIFT_UP:
                    WyeUI.FocusManager._shiftDown = True
                    return True
                # any other key
                case _:
                    if isinstance(key, str) and 'a' <= key and key <= 'z' and WyeUI.FocusManager._shiftDown:
                        key = key.upper()
                    # pass key to next lowest (?) in every dialog hierarchy
                    # key will be handled by the one that currently has focus
                    for hier in WyeUI.FocusManager._dialogHierarchies:
                        if len(hier) > 0:
                            frm = hier[-1]
                            #print("FocusManager doKey", frm, " ,", key)
                            if hasattr(frm, "parentFrame") and not frm.parentFrame is None:
                                if frm.parentFrame.verb.doKey(frm, key):
                                    return True
                            else:
                                if frm.verb.doKey(frm, key):
                                    return True

                    return False # if get this far, didn't use the character



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
    class InputLabel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE))  # 1 user supplied label for field
        varDescr = (("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("currPos", Wye.dType.INTEGER, 0),
                   )  # 0

        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputLabel, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def run(frame):
            frame.params.frame[0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgHeader, pos):

            pos[2] -= WyeUI.LINE_HEIGHT

            lbl = WyeUI._label3d(frame.params.label[0], WyeUI.LABEL_COLOR, pos=tuple(pos),
                                 scale=(1, 1, 1), parent=dlgHeader.getNodePath())
            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            return []       # no clickable object tags

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)


    # text input field
    class InputText:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))  # user supplied var to return value in
        varDescr = (("gWidgetStack", Wye.dType.OBJECT_LIST, 0),           # list of objects to delete on exit
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None)                    # input cursor graphic widget
                    )
        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputText, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def run(frame):
            frame.vars.currVal[0] = frame.params.value[0]
            frame.params.frame[0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgHeader, pos):

            pos[2] -= WyeUI.LINE_HEIGHT       # update position for next widget

            gTags = []      # clickable graphic object tags assoc with this input
            lbl = WyeUI._label3d(frame.params.label[0], WyeUI.LABEL_COLOR, pos=tuple(pos),
                                 scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            #tmp = WyeUI._geom3d([.1,.1,1])
            #render.attachNewNode(tmp.node)

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + .5
            txt = WyeUI._label3d(frame.vars.currVal[0], WyeUI.LABEL_COLOR,
                                 pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath())
            txt.setColor(WyeUI.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            gTags.append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            return gTags

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.frame[0][0].setText(text)

        def setText(frame, text):
            frame.vars.frame[0][1].setText(text)

    class InputInteger(InputText):

        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))  # user supplied var to return value in
        varDescr = (("gWidgetStack", Wye.dType.OBJECT_LIST, 0),           # list of objects to delete on exit
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None)                    # input cursor graphic widget
                    )

        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputInteger, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def display(frame, dlgHeader, pos):

            pos[2] -= WyeUI.LINE_HEIGHT       # update position for next widget

            gTags = []      # clickable graphic object tags assoc with this input
            lbl = WyeUI._label3d(frame.params.label[0], WyeUI.LABEL_COLOR, pos=tuple(pos),
                                 scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            #tmp = WyeUI._geom3d([.1,.1,1])
            #render.attachNewNode(tmp.node)

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + .5
            txt = WyeUI._label3d(str(frame.vars.currVal[0]), WyeUI.LABEL_COLOR,
                                 pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath())
            txt.setColor(WyeUI.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            gTags.append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            return gTags

        def setLabel(frame, text):
            frame.vars.frame[0][0].setText(text)

        def setText(frame, text):
            frame.vars.frame[0][1].setText(str(text))


    # text input field
    class InputButton:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("verb", Wye.dType.STRING, Wye.access.REFERENCE),   # 2 verb to call when button clicked
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),   # 3 optional data
                      )
        varDescr = (("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("gWidget", Wye.dType.OBJECT, None),                  # 1 associated graphic widget
                    ("verb", Wye.dType.OBJECT, None),                     # 2 verb to call
                    ("clickCount", Wye.dType.INTEGER, 0),                 # 3 button depressed count
                    ("verbStack", Wye.dType.OBJECT_LIST, None),           # 4 verb callback stack
                    )

        def start(stack):
            frm = Wye.codeFrame(WyeUI.InputButton, stack)
            frm.vars.gWidgetStack[0] = []
            frm.vars.verbStack[0] = []
            return frm

        def run(frame):
            #print("InputButton frame", frame.tostring())
            #print("  frame.params.frame=",frame.params.frame)
            frame.vars.verb[0] = frame.params.verb[0]       # save verb to call
            frame.params.frame[0] = frame  # self referential!
            #print("InputButton params.frame=", frame.params.frame)
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgHeader, pos):
            #print("InputButton display: pos", pos)
            pos[2] -= WyeUI.LINE_HEIGHT       # update position for next widget
            btn = WyeUI._label3d(frame.params.label[0], WyeUI.LABEL_COLOR, pos=tuple(pos),
                                 scale=(1, 1, 1), parent=dlgHeader.getNodePath())
            frame.vars.gWidgetStack[0].append(btn)  # save for deleting on dialog close
            frame.vars.gWidget[0] = btn  # stash graphic obj in input's frame

            return [btn.getTag()]

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.frame[0][0].setText(text)

    # Dialog object.
    # Display dialog and fields
    # Update fields on events
    class Dialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("retVal", Wye.dType.INTEGER, Wye.access.REFERENCE),    # 0 ok/cancel or other status (if dropdown)
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog frame, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE)) # 5+ variable length list of input control frames
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

        _cursor = None      # 3d TextInput cursor
        _activeInputInteger = None  # used for wheel up/down events

        def start(stack):
            frame = Wye.codeFrame(WyeUI.Dialog, stack)
            # give frame unique lists
            frame.vars.dlgWidgets[0] = []      # standard widgets common to all Dialogs
            frame.vars.dlgTags[0] = []         # tags for OK, Cancel buttons
            frame.vars.inpTags[0] = {}         # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []     # clicked button(s) being "flashed" (so user sees they were clicked)

            # If we don't have a text input cursor, make one
            if WyeUI.Dialog._cursor is None:
                WyeUI.Dialog._cursor = WyeCore.libs.WyeUI._geom3d([.05, .05, .6], [0,0,0])
            return frame

        # first time, draw dialog and all its fields
        # after that, process any buttons being flashed to show user they were clicked on
        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    frame.params.retVal[0] = Wye.status.CONTINUE      # return value: 0 running, 1 OK, 2 Cancel
                    parent = frame.params.parent[0]
                    WyeUI.FocusManager.openDialog(frame, parent)  # pass parent, if any
                    #print("Dialog put frame in param[0][0]", frame)
                    frame.vars.position = (frame.params.position)        # save display position
                    # return frame

                    #print("Dialog display: pos=frame.params.position", frame.params.position)
                    if parent is None:
                        #print("Dialog title", frame.params.title[0]," pos", frame.params.position)
                        #print("  params.inputs", frame.params.inputs)
                        dlgHeader = WyeUI._label3d(text=frame.params.title[0], color=(WyeUI.HEADER_COLOR), pos=frame.params.position, scale=(.2, .2, .2))
                    else:
                        dlgHeader = WyeUI._label3d(text=frame.params.title[0], color=(WyeUI.HEADER_COLOR), pos=frame.params.position,
                                                   scale=(1,1,1), parent=parent.vars.topGObj[0].getNodePath())

                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.topGObj[0] = dlgHeader        # save graphic for parenting sub dialogs

                    pos = [0, 0, 0] # [x for x in frame.params.position]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = len(frame.params.inputs[0])
                    # draw user- supplied label and text inputs
                    for ii in range(nInputs):
                        #pos[2] -= 1.5

                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]
                        #print("    inFrm", inFrm)
                        #print("    Dialog input ", ii, " inFrm", inFrm)
                        #print("       inFrm.params.title", inFrm.params.title)
                        #print("")

                        setattr(inFrm, "parentFrame", frame)

                        if inFrm.verb in [WyeUI.InputLabel, WyeUI.InputText, WyeUI.InputInteger, WyeUI.InputButton]:
                            for lbl in inFrm.verb.display(inFrm, dlgHeader, pos):  # displays label, updates pos, returns selection tags
                                frame.vars.inpTags[0][lbl] = ii

                        else:
                            print("Dialog: Error. Unknown input verb", inFrm.verb.__name__)

                    #print("Dialog has input widgets", frame.vars.inpTags[0])

                    # display OK, Cancel buttons
                    pos[2] -= 1.5
                    txt = WyeUI._label3d("OK", color=(WyeUI.HEADER_COLOR), pos=tuple(pos), scale=(1,1,1),
                                         parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())
                    pos[0] += 2.5       # shove Cancel to the right of OK
                    #print("Dialog Cancel btn at", pos)
                    txt = WyeUI._label3d("Cancel", color=(WyeUI.HEADER_COLOR), pos=tuple(pos), scale=(1,1,1),
                                        parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())
                    # done setup, go to next case to process events
                    frame.PC += 1

                    # make a background for entire dialog
                    if parent is None:
                        scMult = 5
                    else:
                        scMult = 1
                    dlgNodePath = frame.vars.topGObj[0].getNodePath()
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
                    # do click-flash count down and end-flash color reset for buttons user clicked
                    delLst = []
                    # decrement flash count.  if zero, turn off button highlight
                    for btnFrm in frame.vars.clickedBtns[0]:
                        #print("button ", btnFrm.verb.__name__, " count ", btnFrm.vars.clickCount[0])
                        btnFrm.vars.clickCount[0] -= 1
                        if btnFrm.vars.clickCount[0] <= 0:
                            #print("Dialog run: Done click flash for button ", btnFrm.verb.__name__)
                            delLst.append(btnFrm)
                            btnFrm.vars.gWidget[0].setColor(WyeUI.BACKGROUND_COLOR)
                    # remove any buttons whose count is finished
                    for btnFrm in delLst:
                        #print("Dialog run: Remove clicked btn frame", btnFrm.verb.__name__)
                        frame.vars.clickedBtns[0].remove(btnFrm)

        # process field selection event (user clicked on a tag, figure out which field and do its thing)
        def doSelect(frame, tag):
            #print("Dialog doSelect: ", frame.verb, " tag", tag)
            prevSel = frame.vars.currInp[0]      # get current selection
            # if tag is input field in this dialog, select it
            closing = False
            WyeUI.Dialog._activeInputInteger = None
            retStat = False     # haven't used the tag (yet)

            # if clicked on input field
            if tag in frame.vars.inpTags[0]:        # do we have a matching tag?
                #print("Dialog header bounds", frame.vars[6][0].getNodePath().getTightBounds())

                ix = frame.vars.inpTags[0][tag]     # Yes
                retStat = True

                # process dialog inputs
                if frame.verb is WyeUI.Dialog:
                    inFrm = frame.params.inputs[0][ix][0]

                    # if is text input make it selected
                    if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputInteger:
                        inWidg = inFrm.vars.gWidget[0]
                        #print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                        inWidg.setColor(WyeUI.SELECTED_COLOR)        # set input background to "has focus" color
                        WyeUI.Dialog.drawCursor(inFrm)
                        frame.vars.currInp[0] = ix           # save as current input focus

                        if inFrm.verb is WyeUI.InputInteger:
                            WyeUI.Dialog._activeInputInteger = inFrm

                    # button callback
                    elif inFrm.verb is WyeUI.InputButton:
                        callVerb = inFrm.vars.verb[0]
                        inFrm.vars.gWidget[0].setColor(WyeUI.SELECTED_COLOR) # set button color pressed
                        if inFrm.vars.clickCount[0] <= 0:     # if not in an upclick count, process click
                            #print("Dialog doSelect: Start clicked countdown for", inFrm.verb.__name__)
                            inFrm.vars.clickCount[0] = 10       # start flash countdown (in display frames)
                            frame.vars.clickedBtns[0].append(inFrm)  # stash button for flash countdown

                            # if something to call
                            if not callVerb is None:
                                #print("Dialog doSelect: clicked btn, verb ", callVerb.__name__)
                                # start the verb
                                verbFrm = callVerb.start(frame.SP)
                                # handle user data
                                if len(inFrm.params.optData) > 0:
                                    #print("Button callback", callVerb.__name__, " user data", inFrm.params[3][0])
                                    data = inFrm.params.optData[0]
                                else:
                                    data = None
                                # if not single cycle, then put up as parallel path
                                if callVerb.mode != Wye.mode.SINGLE_CYCLE:
                                    # call every display cycle
                                    WyeCore.World.setRepeatEventCallback("Display", verbFrm, data)
                                else:
                                    # call once
                                    #print("doSelect call single cycle verb ", verbFrm.verb.__name__)
                                    verbFrm.eventData = (tag, data, inFrm)  # pass along user supplied event data, if any
                                    verbFrm.verb.run(verbFrm)

                        frame.vars.currInp[0] = -1       # no input has focus

                # if dropdown, currInp is dropdown index
                elif frame.verb is WyeUI.DropDown:
                    #print("Dropdown selected line ", ix)
                    frame.vars.currInp[0] = ix


            # if clicked on OK or Cancel
            elif tag in frame.vars.dlgTags[0]:
                # if is OK button
                if tag == frame.vars.dlgTags[0][-1]:    # if cancel button
                    frame.params.retVal[0] = Wye.status.FAIL
                    print("Dialog", frame.params.title[0], " Cancel Button pressed, return status", frame.params.retVal)
                    retStat = True

                # else is OK button
                else:
                    #print("Dialog", frame.params[1][0], " OK Button pressed")
                    nInputs = (len(frame.params.inputs[0]))
                    #print("dialog ok: nInputs",nInputs," inputs",frame.params.inputs[0])
                    for ii in range(nInputs):
                        inFrm = frame.params.inputs[0][ii][0]
                        # for any text inputs, copy working string to return string
                        if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputInteger:
                            #print("input", ii, " frame", inFrm, "\n", WyeCore.Utils.frameToString(inFrm))
                            #print("input old val '"+ inFrm.params[2][0]+ "' replaced with '"+ inFrm.vars[1][0]+"'")
                            inFrm.params.value[0] = inFrm.vars.currVal[0]
                    frame.params.retVal[0] = Wye.status.SUCCESS
                    #print("doSelect OK button, return status", frame.params.retVal)
                    retStat = True

                # Done with dialog
                frame.status = Wye.status.SUCCESS

                # remove dialog from active dialog list
                WyeUI.FocusManager.closeDialog(frame)

                # delete any graphic objects associated with the inputs
                nInputs = (len(frame.params.inputs[0]))
                for ii in range(nInputs):
                    inFrm = frame.params.inputs[0][ii][0]
                    inFrm.verb.close(inFrm)

                # delete the graphic widgets associated with the dialog
                for wdg in frame.vars.dlgWidgets[0]:
                    #print("del ctl ", wdg.text.name)
                    wdg.removeNode()

                closing = True
                #print("Closing dialog.  Status", frame.status)

            # selected graphic tag not recognized as a control in this dialog
            else:
                frame.vars.currInp[0] = -1   # no currInp

            # If there was a diff selection before, fix that
            # (if closing dialog, nevermind)
            if prevSel > -1 and prevSel != frame.vars.currInp[0] and not closing:
                inFrm =frame.params.inputs[0][prevSel][0]
                if inFrm.verb in [WyeUI.InputText, WyeUI.InputInteger, WyeUI.InputButton]:
                    inWidg = inFrm.vars.gWidget[0]
                    inWidg.setColor(WyeUI.TEXT_COLOR)

            return retStat      # return true if we used the tag

        # inc/dec InputInteger on wheel event
        def doWheel(dir):
            #print("doWheel")
            if not WyeUI.Dialog._activeInputInteger is None:
                #print("doWheel update input")
                inFrm = WyeUI.Dialog._activeInputInteger
                inFrm.vars.currVal[0] += dir
                txt = str(inFrm.vars.currVal[0])
                inWidg = inFrm.vars.gWidget[0]
                inWidg.setText(txt)
                WyeUI.Dialog.drawCursor(inFrm)

        # update InputText/InputInteger on key event
        def doKey(frame, key):
            # if we have an input with focus
            ix = frame.vars.currInp[0]
            if ix >= 0:
                inFrm = frame.params.inputs[0][ix][0]
                if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputInteger:

                    txt = str(inFrm.vars.currVal[0])    # handle either text or integer
                    insPt = inFrm.vars.currInsPt[0]
                    preTxt = txt[:insPt]
                    postTxt = txt[insPt:]
                    # delete key
                    if key == '\x08':         # delete key
                        if insPt > 0:
                            preTxt = preTxt[:-1]
                            insPt -= 1
                            inFrm.vars.currInsPt[0] = insPt
                        txt = preTxt + postTxt
                    # arrow keys
                    elif key == Wye.ctlKeys.LEFT:   # arrow keys
                        if insPt > 0:
                            insPt -= 1
                            inFrm.vars.currInsPt[0] = insPt
                        # place insert cursor
                        WyeUI.Dialog.drawCursor(inFrm)
                        return
                    elif key == Wye.ctlKeys.RIGHT:
                        if insPt < len(txt):
                            insPt += 1
                            inFrm.vars.currInsPt[0] = insPt
                        # place insert cursor
                        WyeUI.Dialog.drawCursor(inFrm)
                        return
                    # not special control, if printable insert it in the string
                    else:
                        print("verb is", inFrm.verb.__name__)
                        if inFrm.verb is WyeUI.InputInteger:
                            if key in "-0123456789":
                                if key != '-' or insPt == 0:
                                    txt = preTxt + key + postTxt
                                    insPt += 1
                                    inFrm.vars.currInsPt[0] = insPt  # set text insert point after new char

                        elif key.isalnum() or key == ' ':  # ignore unprintble keys
                            txt = preTxt + key + postTxt
                            insPt += 1
                            inFrm.vars.currInsPt[0] = insPt        # set text insert point after new char

                    inFrm.vars.currVal[0] = txt
                    inWidg = inFrm.vars.gWidget[0]
                    #print("  set text", txt," ix", ix, " txtWidget", inWidg)
                    inWidg.setText(txt)
                    # place insert cursor
                    WyeUI.Dialog.drawCursor(inFrm)

        # draw text cursor at InputText frame's currInsPt
        def drawCursor(inFrm):
            insPt = inFrm.vars.currInsPt[0]

            inWidg = inFrm.vars.gWidget[0]
            #wPos = inWidg.getPos()
            xOff = 0
            WyeUI.Dialog._cursor.path.reparentTo(inWidg._nodePath)
            WyeUI.Dialog._cursor.path.setColor(WyeUI.CURSOR_COLOR)
            # If cursor not at beginning of text in widget,
            # get length of text before insert pt by generating temp text obj
            # with just pre-insert chars and getting its width
            if insPt > 0:
                txt = inWidg.getText()
                tmp = TextNode("tempNode")
                tmp.setText(txt[0:insPt]+'.')  # '.' - hack to force trailing spaces to be included
                tFrm = tmp.getFrameActual()
                xOff = tFrm[1] - tFrm[0] - .2  # get width of text. Subtract off trailing period hack
            # put cursor after current character
            WyeUI.Dialog._cursor.path.setPos(xOff + .01, -.1, .3)
            WyeUI.Dialog._cursor.path.show()

        def hideCursor():
            WyeUI.Dialog._cursor.path.hide()

    # dropdown menu
    # subclass of Dialog so FocusManager can handle focus properly
    # Returns index of selected line or -1
    class DropDown(Dialog):
        def start(stack):
            frame = Wye.codeFrame(WyeUI.DropDown, stack)
            frame.vars.dlgWidgets[0] = []      # standard widgets common to all Dialogs
            frame.vars.dlgTags[0] = []         # not used
            frame.vars.inpTags[0] = {}         # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []     # clicked button(s) being "flashed"
            if WyeUI.Dialog._cursor is None:
                WyeUI.Dialog._cursor = WyeCore.libs.WyeUI._geom3d([.05, .05, .6], [0, 0, 0])
            return frame

        def run(frame):
            match frame.PC:
                case 0:  # Start up case - set up all the fields
                    #print("DropDown frame ", frame.tostring())
                    frame.params.retVal[0] = -1           # set default return value
                    parent = frame.params.parent[0]
                    WyeUI.FocusManager.openDialog(frame, parent)  # pass parent, if any
                    # print("DropDown put frame in param[0][0]", frame)
                    frame.vars.position = (frame.params.position)  # save display position
                    # return frame

                    # handle scale and parent obj, if any
                    if parent is None:
                        dlgHeader = WyeUI._label3d(text=frame.params.title[0], color=(WyeUI.HEADER_COLOR), pos=frame.params.position, scale=(.2, .2, .2))
                    else:
                        dlgHeader = WyeUI._label3d(text=frame.params.title[0], color=(WyeUI.HEADER_COLOR), pos=frame.params.position,
                                                   scale=(1,1,1), parent=parent.vars.topGObj[0].getNodePath())

                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.topGObj[0] = dlgHeader        # save graphic for parenting sub dialogs

                    pos = [0, 0, 0]  # [x for x in frame.params[2]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = len(frame.params.inputs[0])
                    # draw user- supplied label and text inputs
                    for ii in range(nInputs):
                        #pos[2] -= 1.5

                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]
                        #print("    inFrm", inFrm)
                        #print("    Dialog input ", ii, " inFrm", inFrm)
                        #print("       inFrm.params.title", inFrm.params.title)
                        #print("")

                        setattr(inFrm, "parentFrame", frame)

                        # tell input to display itself.  Collect returned objects to close when dlg closes
                        if inFrm.verb in [WyeUI.InputLabel, WyeUI.InputButton]:
                            for lbl in inFrm.verb.display(inFrm, dlgHeader, pos):  # displays label, updates pos, returns selection tags
                                frame.vars.inpTags[0][lbl] = ii

                        else:
                            print("Dialog: Error. Only Label and Button allowed in dropdown", inFrm.verb.__class__)

                    # Cancel button
                    pos[2] -= 1.5
                    #print("Dialog Cancel btn at", pos)
                    txt = WyeUI._label3d("Cancel", color=(WyeUI.HEADER_COLOR), pos=tuple(pos),
                                                      scale=(1,1,1), parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())

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


                    frame.PC += 1

                case 1:
                    #print("DropDown case 1")
                    # if click event, callback set status to selected row, clean up dialog
                    if frame.vars.currInp[0] > -1:
                        #print("DropDown got click event.  CurrInp", frame.vars.currInp[0], " ")
                        frame.params.retVal[0] = frame.vars.currInp[0]
                        # remove dialog from active dialog list
                        WyeUI.FocusManager.closeDialog(frame)
                        # delete the graphic widgets associated with the dialog
                        for wdg in frame.vars.dlgWidgets[0]:
                            # print("del ctl ", wdg.text.name)
                            wdg.removeNode()
                        frame.status = Wye.status.SUCCESS

    # Put in as button callback for each dropdown row
    class DropdownCallback():
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            print("DropdownCallback start")
            return Wye.codeFrame(WyeUI.DropdownCallback, stack)

        def run(frame):
            print("DropdownCallback run: event data", frame.eventData)
            rowIx = frame.eventData[1][0]
            dlgFrm = frame.eventData[1][1]
            # return dropdown index in dropdown dialog's first param
            lst = getattr(dlgFrm.params, dlgFrm.firstParamName())
            lst[0] = rowIx
            # print("DropdownCallback data=", frame.eventData, " index = ", frame.eventData[1])


    # called when user clicks on a graphic object that has a WyeID tag
    class ObjEditCtl(DirectObject):
        def __init__(self):
            pass

        # User clicked on object.  It alt key down and it's editable, open the editor
        def tagClicked(self, wyeID):
            #print("tagClicked")
            # if alt key down
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt()):
                #print("Alt held down, is wyeID registered?")
                frm = WyeCore.World.getRegisteredObj(wyeID)
                if not frm is None:
                    #print("wyeID", wyeID, " Is registered")
                    print("Edit object", frm.verb.__name__)
                    return True

            # Get this far and we didn't use the tag so let someone else have it
            return False

    # put up object dialog for given object
    class ObjEditor:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),)  # gotta have a ret param
        varDescr = (("TBD", Wye.dType.INTEGER, -1),
                    )

        def start(stack):
            return Wye.codeFrame(WyeUI.ObjEditor, stack)

        def run(frame):
            pass