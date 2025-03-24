# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *
from panda3d.core import LVector3f
#from functools import partial
import traceback
import sys
#from sys import exit
import math
import sys, os
#for 3d geometry (input cursor)
#from direct.showbase.ShowBase import ShowBase
from importlib.machinery import SourceFileLoader    # to load library from file

from functools import partial

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MouseButton

# from https://github.com/Epihaius/procedural_panda3d_model_primitives
from sphere import SphereMaker

import inspect

#import pygame.midi
#import time


# 3d UI element library
class WyeUILib(Wye.staticObj):
    systemLib = True        # prevent overwriting

    dragFrame = None    # not currently dragging anything

    # Build run_rt methods on each class in library
    def _build():
        WyeCore.Utils.buildLib(WyeUILib)

    # instantiated class to manage cut-paste list
    # todo - rethink this as std Wye object
    class CutPasteManager:
        def __init__(self):
            self.cutList = []   # cut data goes here
            self.maxLen = 10    # max number of cutList entries
            self.selectedRow = None   # nothing on list yet
            self.displayObj = None

        def add(self, rec):
            # keep cutList reasonable size
            if len(self.cutList) >= self.maxLen:
                self.cutList.pop(0)
            self.cutList.append(rec)

            #print("CutPasteManager: added", rec, "\n  to", self.cutList)
            self.show()
            # There are sequencing issues setting background of row first time - do this way, or do some debugging...
            if len(self.cutList) > 1:
                self.setSelected(rec)
            else:
                self.selectedRow = rec

        def setSelected(self, row):
            if row in self.cutList:
                #print("CutPasteManager set selected row", row)
                self.selectedRow = row

                if self.displayObj:
                    ix = self.cutList.index(row)
                    print("CutPasteManager setSelected: highlight row", ix, " out of ", len(self.cutList), " cutList rows")
                    print("   display rows:", len(self.displayObj.vars.dlgFrm[0].params.inputs[0]))
                    self.displayObj.verb.highlightRow(self.displayObj, ix)

            else:
                print("CutPasteManager setSelected ERROR: selected row not in cutList")


        def getSelected(self):
            return self.selectedRow

        def show(self):
            if self.displayObj:
                #print("CutPasteManager dialog already showing, bring to front and update")
                self.displayObj.verb.redisplay(self.displayObj)
                self.displayObj.vars.dlgFrm[0].vars.dragObj[0].setPos(base.camera, (2, 7, 0))
                self.displayObj.vars.dlgFrm[0].vars.dragObj[0].setHpr(base.camera, 0, 1, 0)
            else:
                #print("CutPasteManager: open dialog")
                self.displayObj = WyeCore.World.startActiveObject(WyeUILib.CutPasteManager.CutPasteDisplay)
                # todo - rethink this when cvt cut/paste to Wye obj
                # Need object graphics to exist 'cause need to set highlight
                self.displayObj.verb.run(self.displayObj)

        class CutPasteDisplay:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.NONE
            autoStart = False
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.OBJECT, None),
                        ("rows", Wye.dType.OBJECT_LIST, None),  # list of refreshable objects
                        ("currRowIx", Wye.dType.INTEGER, 0),
                        )

            # global list of frames being edited
            activeFrames = {}

            def start(stack):
                #print("CutPasteDisplay: Start")
                f = Wye.codeFrame(WyeUILib.CutPasteManager.CutPasteDisplay, stack)  # not stopped by breakAll or debugger debugger
                f.systemObject = True
                f.vars.rows[0] = []
                return f

            def run(frame):
                #print("CutPasteDisplay: run")
                match (frame.PC):
                    case 0:
                        #print("CutPasteDiaplay: run case 0:")
                        # position in front of other dialogs
                        point = NodePath("point")
                        point.reparentTo(render)
                        point.setPos(base.camera, (2, 7, 0))
                        pos = point.getPos()
                        point.removeNode()
                        dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog("Copy/Paste List", position=pos, formatLst=["NO_CANCEL"])
                        WyeUILib.CutPasteManager.CutPasteDisplay.displayRows(frame, dlgFrm)

                        frame.vars.dlgFrm[0] = dlgFrm

                        frame.SP.append(dlgFrm)  # push dialog so it runs next cycle
                        frame.PC += 1  # on return from dialog, run next case

                    # done, remove self from everywhere
                    case 1:
                        #print("CutPasteDiaplay: run case 1: stop self")
                        dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                        frame.status = Wye.status.SUCCESS  # done
                        WyeCore.World.stopActiveObject(frame)
                        WyeCore.World.cutPasteManager.displayObj = None

            def highlightRow(frame, ix):
                #print("CutPastDisplay highlightRow: old row", frame.vars.currRowIx[0])

                if ix != frame.vars.currRowIx[0]:
                    #print("CutPastDisplay highlightRow: unhighlight", frame.vars.currRowIx[0])
                    oldRowFrm = frame.vars.dlgFrm[0].params.inputs[0][frame.vars.currRowIx[0]][0]
                    oldRowFrm.verb.setBackgroundColor(oldRowFrm, Wye.color.TRANSPARENT)
                #print("CutPastDisplay highlightRow: highlight", ix)
                if ix >=  0 and ix < len(frame.vars.dlgFrm[0].params.inputs[0]):
                    newRowFrm = frame.vars.dlgFrm[0].params.inputs[0][ix][0]
                    #print("  row", newRowFrm.params.label[0])
                    newRowFrm.verb.setBackgroundColor(newRowFrm, Wye.color.SELECTED_BG_COLOR)
                    frame.vars.currRowIx[0] = ix
                else:
                    print("CutPasteDisplay highlightRow", ix," out of range 0.."+str(len(frame.vars.dlgFrm[0].params.inputs[0])))

            def displayRows(frame, dlgFrm):
                #print("CutPasteDisplay displayRows: display", len(WyeCore.World.cutPasteManager.cutList), " rows")
                ix = 0
                for row in WyeCore.World.cutPasteManager.cutList:
                    # todo - pretty print text
                    if ix == frame.vars.currRowIx[0]:
                        btn = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, row[0]+": "+str(row[1]),
                                                                       WyeUILib.CutPasteManager.CutPasteDisplay.RowCallback,
                                                                       [row], backgroundColor=Wye.color.SELECTED_BG_COLOR)
                        #print("CutPastDisplay displayRows: highlight", ix)
                    else:
                        btn = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, row[0]+": "+str(row[1]),
                                                                   WyeUILib.CutPasteManager.CutPasteDisplay.RowCallback,
                                                                   [row], backgroundColor=Wye.color.TRANSPARENT)
                    frame.vars.rows[0].append(btn)
                    ix += 1

            # cut/paste list changed, update display
            def redisplay(frame):
                dlgFrm = frame.vars.dlgFrm[0]

                # remove current rows
                #print("CutPasteDisplay redisplay: remove", len(frame.vars.rows[0]), " rows")
                for frmRef in frame.vars.rows[0]:
                    inpIx = WyeCore.Utils.nestedIndexFind(dlgFrm.params.inputs[0], frmRef)
                    #print(" remove row", inpIx)
                    oldFrm = dlgFrm.params.inputs[0].pop(inpIx)[0]
                    if oldFrm in dlgFrm.vars.clickedBtns[0]:
                        dlgFrm.vars.clickedBtns[0].remove(oldFrm)
                    #print(" remove", oldFrm.verb.__name__, " ", oldFrm.params.label[0])
                    oldFrm.verb.close(oldFrm)   # remove graphic content
                frame.vars.rows[0].clear()

                # make new rows
                WyeUILib.CutPasteManager.CutPasteDisplay.displayRows(frame, dlgFrm)

                # generate display elements for rows (correct pos calc by redisplay, below)
                pos = [0, 0, 0]
                for frm in frame.vars.rows[0]:
                    frm.verb.display(frm, dlgFrm, pos)

                # update dialog display
                dlgFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                dlgFrm.verb.redisplay(dlgFrm)  # redisplay the dialog

            # make this the current cut/paste selection
            class RowCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = ()

                def start(stack):
                    # print("RowCallback started")
                    return Wye.codeFrame(WyeUILib.CutPasteManager.CutPasteDisplay.RowCallback, stack)

                def run(frame):
                    data = frame.eventData
                    #print("CutPasteDisplay RowCallback: data=", data)
                    row = data[1][0]
                    #parentFrm = data[1][1]
                    #editFrm = data[1][2]

                    WyeCore.World.cutPasteManager.setSelected(row)

    # note: this is an instantiated class
    # This does more than camera control, it also triggers debugger and editor
    class CameraControl(DirectObject):
        def __init__(self):
            self.m1Down = False     # state
            self.m2Down = False
            self.m3Down = False

            self.shift = False
            self.ctl = False
            self.alt = False

            self.m1Pressed = False  # edge
            self.m2Pressed = False
            self.m3Pressed = False

            self.shiftPressed = False
            self.ctlPressed = False
            self.altPressed = False

            self.walk = False       # start off flying [not currently implemented]
            self.viewDir = (0, 1, 0)
            self.shift = False

            self.speed = .25
            self.rotRate = .5


        def mouseMove(self, x, y):
            global base
            global render

            self.m1Pressed = False  # edge
            self.m2Pressed = False
            self.m3Pressed = False

            self.shiftPressed = False
            self.ctlPressed = False
            self.altPressed = False

            self.shiftReleased = False
            self.ctlReleased = False
            self.alttReleased = False

            # get mouse buttons and mouse-down start pos
            if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                if not self.m1Down:
                    self.m1Down = True
                    self.m1DownPos = [x, y]     # use list to allow modification while zooming dialog
                    self.m1DownRot = base.camera.getHpr()
                    self.m1Pressed = True
            else:
                self.m1Down = False
            if base.mouseWatcherNode.isButtonDown(MouseButton.two()):
                if not self.m2Down:
                    self.m2Down = True
                    self.m2DownPos = (x, y)
                    self.m2DownRot = base.camera.getHpr()
                    self.m2Pressed = True
            else:
                self.m2Down = False
            if base.mouseWatcherNode.isButtonDown(MouseButton.three()):
                if not self.m3Down:
                    self.m3Down = True
                    self.m3DownPos = (x, y)
                    self.m3DownRot = base.camera.getHpr()
                    self.m3Pressed = True
            else:
                self.m3Down = False

            # if anyone wants to know a mouse button was pressed
            if (self.m1Pressed or self.m2Pressed or self.m3Pressed) and len(WyeCore.World.mouseCallbacks) > 0:
                for callback in WyeCore.World.mouseCallbacks:
                    callback()

            # get shift key
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.shift()):
                if not self.shift:
                    self.shift = True
                    self.shiftPressed = True
            else:
                if self.shift:
                    self.shiftReleased = True
                self.shift = False
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt()):
                if not self.alt:
                    self.alt = True
                    self.altPressed = True
            else:
                if self.alt:
                    self.altReleased = True
                self.alt = False
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                if not self.ctl:
                    self.ctl = True
                    self.ctlPressed = True
            else:
                if self.ctl:
                    self.ctlReleased = True
                self.ctl = False

            if self.m1Pressed and self.ctl and self.alt:
                if not WyeCore.World.mainMenu:
                    WyeCore.World.mainMenu = WyeCore.World.startActiveObject(WyeUILib.MainMenuDialog)
                else:
                    #print("Already have Wye Main Menu", WyeCore.World.mainMenu.verb.__name__)
                    WyeCore.World.mainMenu.vars.dlgFrm[0].vars.dragObj[0].setPos(base.camera, 0,Wye.UI.DIALOG_OFFSET,0)
                    WyeCore.World.mainMenu.vars.dlgFrm[0].vars.dragObj[0].setHpr(base.camera, 0, 1, 0)

            # if don't have the main edit menu and the user wants it, start it
            elif self.m1Pressed and self.shift and self.ctl:
                if not WyeCore.World.editMenu:
                    WyeCore.World.editMenu = WyeCore.World.startActiveObject(WyeUILib.EditMainDialog)
                    WyeCore.World.editMenu.eventData = ("", (0))
                else:
                    #print("Already have editor")
                    WyeCore.World.editMenu.vars.dlgFrm[0].vars.dragObj[0].setPos(base.camera, 0,Wye.UI.DIALOG_OFFSET,0)
                    WyeCore.World.editMenu.vars.dlgFrm[0].vars.dragObj[0].setHpr(base.camera, 0, 1, 0)

            # if don't have the main debug menu and the user wants it, start it
            elif self.m1Pressed and self.shift and self.alt:
                if not WyeCore.World.debugger:
                    WyeCore.World.debugger = WyeCore.World.startActiveObject(WyeUILib.DebugMain)
                else:
                    #print("Already have debugger")
                    WyeCore.World.debugger.vars.dlgFrm[0].vars.dragObj[0].setPos(base.camera, 0,Wye.UI.DIALOG_OFFSET,0)
                    WyeCore.World.debugger.vars.dlgFrm[0].vars.dragObj[0].setHpr(base.camera, 0, 1, 0)

            elif self.m1Pressed and WyeCore.picker.objSelectEvent():
                # if picker used event then everything already done in picker, nothing more to do here
                pass

            # if not dragging then moving
            # mouseY is fwd/back
            # mouseX is rotate left/right
            # shift mouseY is up/down
            # shift mouseX is slide left/right
            elif not Wye.dragging:

                # motion
                if self.m1Down:
                    # regular motion
                    if not self.shift:
                        # walk fwd/back (mouseY), turning l/r (mouseX)
                        camRot = base.camera.getHpr()
                        dx = -(x - self.m1DownPos[0]) * self.rotRate
                        base.camera.setHpr(camRot[0] + dx, camRot[1], camRot[2])

                        quaternion = base.camera.getQuat()
                        fwd = quaternion.getForward()

                        #fwd = LVector3f(fwd[0], fwd[1], 0)
                        quat = Quat()
                        quat.setFromAxisAngle(-90, LVector3f.up())
                        right = quat.xform(fwd)

                        base.camera.setPos(base.camera.getPos() + fwd * (y - self.m1DownPos[1]) * self.speed) # + right * (x - self.m1DownPos[0]) * self.speed)

                    else:
                        # tilt up/down (mouseY), slide left/right (mouseX)
                        camRot = base.camera.getHpr()
                        dy = (y - self.m1DownPos[1]) * self.rotRate
                        base.camera.setHpr(camRot[0], camRot[1] + dy, camRot[2])

                        quaternion = base.camera.getQuat()
                        fwd = quaternion.getForward()
                        fwd = LVector3f(fwd[0], fwd[1], 0)      # no roll
                        quat = Quat()
                        quat.setFromAxisAngle(-90, LVector3f.up())
                        right = quat.xform(fwd)

                        #up = LVector3f(0, 0, 1)
                        #base.camera.setPos(base.camera.getPos() + up * (y - self.m1DownPos[1]) * self.speed + right * (x - self.m1DownPos[0]) * self.speed)
                        base.camera.setPos(base.camera.getPos() + right * (x - self.m1DownPos[0]) * self.speed)


                # reset viewpoint
                elif self.m2Down:
                    if not self.shift:
                        base.camera.setPos(Wye.startPos[0], Wye.startPos[1], Wye.startPos[2])
                    base.camera.setHpr(0,0,0)


                # slide sideways and up
                elif self.m3Down:
                    #quaternion = base.camera.getQuat()
                    #fwd = quaternion.getForward()
                    #fwd = LVector3f(fwd[0], fwd[1], 0)  # no roll
                    #quat = Quat()
                    #quat.setFromAxisAngle(-90, LVector3f.up())
                    #right = quat.xform(fwd)
                    right = LVector3f(1,0,0)

                    up = LVector3f(0, 0, 1)
                    #base.camera.setPos(base.camera.getPos() + up * (y - self.m3DownPos[1]) * self.speed + right * (x - self.m3DownPos[0]) * self.speed)
                    base.camera.setPos(base.camera, up * (y - self.m3DownPos[1]) * self.speed + right * (x - self.m3DownPos[0]) * self.speed)

            # dragging dialog
            else:
                if self.m1Pressed or (self.m1Down and self.shiftReleased) or (self.m1Down and self.ctlReleased):
                    # calc drag plane once per downclick
                    self.m1DownPos = [x,y]       # only needed for shift released

                    # camera forward vec - old way, keep for ref
                    #quaternion = base.camera.getQuat()
                    #fwd = quaternion.getForward()

                    # make plane at same orientation and pos as dialog
                    frm = WyeUILib.dragFrame
                    while frm.params.parent[0]:
                        frm = frm.params.parent[0]  # find top dialog to get wld HPR

                    self.topDragFrame = frm
                    if self.ctl:        # hold control to drag only selected dialog
                        dragFrame = WyeUILib.dragFrame
                    else:               # otherwise, drag whole dialog stack
                        dragFrame = self.topDragFrame

                    objPath = dragFrame.vars.dragObj[0]._path
                    fwd = render.getRelativeVector(objPath, (0, -1, 0))
                    pos = objPath.getPos(render)    # sub dialogs pos rel to parent.  Get pos rel to world
                    if not self.ctl:    # don't change angle if dragging just lowest level dialog
                        objPath.setHpr(base.camera, 0, 1, 0)
                    self.objPlane = LPlanef(fwd, pos)
                    self.dragStartPos = pos

                    #frame.vars.dragObj[0]._path.wrtReparentTo(base.camera)

                    mpos = base.mouseWatcherNode.getMouse()
                    newPos = Point3(0,0,0)
                    nearPoint = Point3()
                    farPoint = Point3()
                    base.camLens.extrude(mpos, nearPoint, farPoint)
                    if self.objPlane.intersectsLine(newPos,
                                                 render.getRelativePoint(base.camera, nearPoint),
                                                 render.getRelativePoint(base.camera, farPoint)):
                        objPosInPlane = self.objPlane.project(objPath.getPos(render))
                        self.dragOffset = newPos - objPosInPlane
                    else:
                        pass # todo - this can't happen?

                # do dragging
                if self.m1Down:
                    if self.ctl:        # hold control to drag only selected dialog
                        dragFrame = WyeUILib.dragFrame
                    else:               # otherwise, drag whole dialog stack
                        dragFrame = self.topDragFrame

                    objPath = dragFrame.vars.dragObj[0]._path
                    # get mouse pos
                    mpos = base.mouseWatcherNode.getMouse()

                    # on shift, mouse up/down moves plane far/near
                    # don't allow moving just selected dialog or risk losing behind others in dlg stack
                    if self.shiftPressed:
                        # if shift pressed while moving dialog, reset starting ht so don't jump up/down
                        self.m1DownPos[1] = mpos[1]

                    if self.shift and not self.ctl:
                        zoom = (mpos[1] - self.m1DownPos[1]) * 30
                        mpos = LVecBase2f(mpos[0], self.m1DownPos[1])

                        frm = dragFrame
                        while frm.params.parent[0]:
                            frm = frm.params.parent[0]  # find top dialog to get wld HPR
                        fwd = render.getRelativeVector(objPath, (0, 1, 0))
                        mov = fwd * zoom
                        pos = self.dragStartPos + mov
                        self.objPlane = LPlanef(fwd, pos)

                    # calc mouse position on drag plane
                    newPos = Point3(0,0,0)
                    nearPoint = Point3()
                    farPoint = Point3()
                    # generate ray from camera through mouse xy
                    base.camLens.extrude(mpos, nearPoint, farPoint)
                    # get intersection of mouse point ray with object plane
                    if self.objPlane.intersectsLine(newPos,
                                                 render.getRelativePoint(base.camera, nearPoint),
                                                 render.getRelativePoint(base.camera, farPoint)):
                        # Move dialog to that location, taking into account offset
                        # from where user clicked rel to position of dialog

                        # Note, subdialog position rel to parent dialog.
                        # So put point at world pos, then set dialog pos at zero rel to that point
                        # (panda3d does all the recalc based on parent pos) I'm sure there's a better way, but this works
                        point = NodePath("point")
                        point.reparentTo(render)
                        dlgPos = newPos - self.dragOffset
                        point.setPos(dlgPos)
                        objPath.setPos(point, LVector3f(0,0,0))
                        point.removeNode()

                        # update dialog's stored position
                        if hasattr(dragFrame.params, "position"):
                            dragFrame.params.position[0] = objPath.getPos()

                else:
                    Wye.dragging = False
                    WyeUILib.dragFrame = None

        # stub
        def setFly(self, doFly):
            self.fly = doFly

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

        # note: this is an instantiated class
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
                if WyeUILib.FocusManager._activeDialog:
                    #print("MouseHandler: mouseWheel", dir)
                    WyeUILib.FocusManager._activeDialog.verb.doWheel(dir)


        # find dialogFrame in leaf nodes of dialog hierarchies
        def findDialogHier(dialogFrame):
            retHier = None
            for hier in WyeUILib.FocusManager._dialogHierarchies:
                # if found it, add to hierarchy list
                if len(hier) > 0 and hier[-1] == dialogFrame:
                    retHier = hier
                    break  # found it, break out of loop

            if retHier is None:
                print("Error: WyeUILib FocusManager findDialogHier - dialog not found")
                print("  dialog title", dialogFrame.params.title[0])
            return retHier


        # User is adding a dialog to the display
        # If it has a parent dialog, it is now the leaf of the hierarchy and
        # its inputs get any incoming events
        def openDialog(dialogFrame, parentDlg):
            # if no focus manager set to catch selected objects, fix that
            if WyeCore.Utils.getFocusManager() is None:
                WyeCore.Utils.setFocusManager(WyeUILib.FocusManager)

            # also set up to handle mouse events
            if WyeUILib.FocusManager._mouseHandler is None:
                WyeUILib.FocusManager._mouseHandler = WyeUILib.FocusManager.MouseHandler()

            # connect to parent frame
            dialogFrame.parentDlg = parentDlg

            # if starting new dialog hierarchy
            if parentDlg is None:
                WyeUILib.FocusManager._dialogHierarchies.append([dialogFrame])
                #print("Wye UI FocusManager openDialog: no parent, add dialog", dialogFrame," to hierarchy list", WyeUILib.FocusManager._dialogHierarchies)

            # if has parent then add it to the parent's hierarchy
            else:
                #print("WyeUILib FocusManager openDialog find parentDlg ", parentDlg)
                hier = WyeUILib.FocusManager.findDialogHier(parentDlg)
                if not hier is None:
                    hier.append(dialogFrame)
                else:
                    print("Error: WyeUILib FocusManager openDialog - did not find parent dialog", parentDlg, " in", WyeUILib.FocusManager._dialogHierarchies)

            # if there's an active dialog, deactivate it and activate this one
            if not WyeUILib.FocusManager._activeDialog is None:
                WyeUILib.Dialog.activateDialog(WyeUILib.FocusManager._activeDialog, False)

            WyeUILib.Dialog.activateDialog(dialogFrame, True)
            #print("FocusManager openDialog", WyeUILib.FocusManager._dialogHierarchies)


        # Remove the given dialog from the display hierarchy
        def closeDialog(dialogFrame):
            #print("FocusManager closeDialog", dialogFrame)
            hier = WyeUILib.FocusManager.findDialogHier(dialogFrame)
            #print("FocusManager closeDialog remove", dialogFrame, " from len", len(hier), ", hier", hier)
            del hier[-1]    # remove dialog from hierarchy
            if len(hier) == 0:  # if that was the last dialog, remove hierarchy too
                #print(" hier now empty, remove it")
                WyeUILib.FocusManager._dialogHierarchies.remove(hier)
            #print("FocusManager closeDialog complete: hierarchies", WyeUILib.FocusManager._dialogHierarchies)
            if dialogFrame == WyeUILib.FocusManager._activeDialog:
                if len(hier) > 0:
                    WyeUILib.Dialog.activateDialog(hier[-1], True)
                else:
                    WyeUILib.FocusManager._activeDialog = None

        # User clicked on object, it might be a dialog field.
        # call each leaf dialog to see if tag belongs to it.
        # If so, return True (we used it)
        # else return False (not ours, someone else can use it)
        def doSelect(id):
            status = False
            WyeUILib.Dialog.hideCursor()
            for hier in WyeUILib.FocusManager._dialogHierarchies:       # loop through them all to be sure only one dialog has field selected
                if len(hier) > 0:
                    frm = hier[-1]
                    # if dialog uses the tag, mark it active
                    if frm.verb.doSelect(frm, id):
                        WyeUILib.Dialog.postSelect(frm)
                        break   # Found user of tag. Done with loop
            return status

        # process keys and controls (shift, ctl)
        def doKey(key):
            # handle control codes.
            # if key, apply case
            match key:
                # check for control codes
                case Wye.ctlKeys.CTL_DOWN:
                    WyeUILib.FocusManager._ctlDown = True
                    return True
                case Wye.ctlKeys.CTL_UP:
                    WyeUILib.FocusManager._ctlDown = False
                    return True
                case Wye.ctlKeys.SHIFT_DOWN:
                    WyeUILib.FocusManager._shiftDown = True
                    return True
                case Wye.ctlKeys.SHIFT_UP:
                    WyeUILib.FocusManager._shiftDown = True
                    return True
                # any other key
                case _:
                    if isinstance(key, str) and 'a' <= key and key <= 'z' and WyeUILib.FocusManager._shiftDown:
                        key = key.upper()
                    # pass key to next lowest (?) in every dialog hierarchy
                    # key will be handled by the one that currently has focus
                    for hier in WyeUILib.FocusManager._dialogHierarchies:
                        if len(hier) > 0:
                            frm = hier[-1]
                            #print("FocusManager doKey", frm, " ,", key)
                            if hasattr(frm, "parentDlg") and not frm.parentDlg is None:
                                if frm.parentDlg.verb.doKey(frm, key):
                                    return True
                            else:
                                if frm.verb.doKey(frm, key):
                                    return True

                    return False # if get this far, didn't use the character



    # Input field classes
    # Each input run method just returns its frame as p0.
    # Since the input is a parameter and is run before the dialog runs, the input's run cannot do any graphic setup
    #
    # When the dialog runs it calls the input's display method to do the actual graphical layout.
    #
    # Effectively each input is a factory generating an input object frame for dialog to use

    # label field
    # Technically not an input, but is treated as one for layout
    class InputLabel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),                 # parent dialog/dropdown
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),
                   )  # 0

        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputLabel, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []     # no clickable tags
            return frame

        def run(frame):
            frame.params.frame[0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]
            lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=(pos[0], pos[1], pos[2]),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])
            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # update dialog pos to next free space downward

            pos[2] -= lbl.getHeight()           # update to next position
            frame.vars.size[0] = (lbl.getWidth(), 0, lbl.getHeight())

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()

        # update value means nothing to us
        def update(frame):
            pass

        # return false 'cause we do not respond to user clicks
        def doSelect(frame, dlgFrame, tag):
            return False        # label never accepts a hit

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)

        def setBackgroundColor(frame, color):
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setBackgroundColor(color)


    # text input field
    class InputText:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL)
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None),                    # input cursor graphic widget
                    )
        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputText, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []  # create local stack
            return frame

        def run(frame):
            #print("InputText label", frame.params.label, " value=", frame.params.value)
            frame.vars.currVal[0] = frame.params.value[0]
            frame.params.frame[0] = frame  # self referential!

            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]

            lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            frame.vars.tags[0].append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label

            width = lbl.getWidth() + .5
            txt = WyeCore.libs.Wye3dObjsLib._3dText(frame.vars.currVal[0], Wye.color.TEXT_COLOR,
                                pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath(), bg=frame.params.backgroundColor[0])
            #txt.setColor(WyeUILib.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            frame.vars.tags[0].append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            # update dialog pos to next free space downward
            pos[2] -= max(lbl.getHeight(), txt.getHeight())           # update to next position
            frame.vars.size[0] = (width + txt.getWidth(), 0, max(lbl.getHeight(), txt.getHeight()))

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos[0], pos[1], pos[2])
            width = lbl.getWidth() + .5
            pos[0] += width
            txt = frame.vars.gWidgetStack[0][1]
            txt.setPos(width, 0, 0)
            pos[2] -= max(lbl.getHeight(), txt.getHeight())
            frame.vars.size[0] = (width + txt.getWidth(), 0, max(lbl.getHeight(), txt.getHeight()))

        # update value
        def update(inFrm):
            inWidg = inFrm.vars.gWidget[0]
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(str(inFrm.vars.currVal[0]))

        # return true if this is one of our tags (got clicked by user)
        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                inWidg = frame.vars.gWidget[0]
                # print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                inWidg.setColor(Wye.color.SELECTED_COLOR)  # set input background to "has focus" color
                WyeUILib.Dialog.drawCursor(frame)
                return True
            else:
                return False

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, text):
            frame.vars.gWidget[0].setText(text)
            frame.vars.currVal[0] = text
            # relayout to fit everything
            frame.parentDlg.verb.redisplay(frame.parentDlg)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setCurrentPos(frame, index):
            frame.vars.currPos[0] = index       # TODO needs validating!

        def setBackgroundColor(frame, color):
            frame.vars.gWidgetStack[0][0].setBackgroundColor(color)
            frame.vars.gWidget[0].setBackgroundColor(color)


    class InputInteger(InputText):

        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.INTEGER, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL)
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),                  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None),                    # input cursor graphic widget
                    )

        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputInteger, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []  # create local stack
            return frame

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]

            lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            frame.vars.tags[0].append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)

            width = lbl.getWidth() + .5
            txt = WyeCore.libs.Wye3dObjsLib._3dText(str(frame.vars.currVal[0]), Wye.color.LABEL_COLOR,
                                pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath(), bg=frame.params.backgroundColor[0])
            txt.setColor(Wye.color.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            frame.vars.tags[0].append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            # update dialog pos to next free space downward
            pos[2] -= txt.getHeight()  # update to next position
            frame.vars.size[0] = (width + txt.getWidth(), 0, max(lbl.getHeight(), txt.getHeight()))

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()
            lbl = frame.vars.gWidgetStack[0][1]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()

        # update value
        def update(inFrm):
            inWidg = inFrm.vars.gWidget[0]
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(str(inFrm.vars.currVal[0]))

        # return true if this is one of our tags (got clicked by user)
        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                inWidg = frame.vars.gWidget[0]
                # print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                inWidg.setColor(Wye.color.SELECTED_COLOR)  # set input background to "has focus" color
                WyeUILib.Dialog.drawCursor(frame)
                WyeUILib.Dialog._activeInputInteger = frame
                return True
            else:
                return False

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, int):
            frame.vars.gWidget[1].setText(str(int))
            frame.vars.currVal[0] = str(int)
            # relayout to fit everything
            frame.parentDlg.verb.redisplay(frame.parentDlg)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setBackgroundColor(frame, color):
            frame.vars.gWidgetStack[0][0].setBackgroundColor(color)
            frame.vars.gWidget[0].setBackgroundColor(color)


    class InputFloat(InputText):

        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.INTEGER, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL)
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),                  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None),                    # input cursor graphic widget
                    )

        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputFloat, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []  # create local stack
            return frame

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]

            lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            frame.vars.tags[0].append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)

            width = lbl.getWidth() + .5
            txt = WyeCore.libs.Wye3dObjsLib._3dText(str(frame.vars.currVal[0]), Wye.color.LABEL_COLOR,
                                pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath(), bg=frame.params.backgroundColor[0])
            txt.setColor(Wye.color.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            frame.vars.tags[0].append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            # update dialog pos to next free space downward
            pos[2] -= txt.getHeight()  # update to next position
            frame.vars.size[0] = (width + txt.getWidth(), 0, max(lbl.getHeight(), txt.getHeight()))

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()
            lbl = frame.vars.gWidgetStack[0][1]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()

        # update value
        def update(inFrm):
            inWidg = inFrm.vars.gWidget[0]
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(str(inFrm.vars.currVal[0]))

        # return true if this is one of our tags (got clicked by user)
        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                inWidg = frame.vars.gWidget[0]
                # print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                inWidg.setColor(Wye.color.SELECTED_COLOR)  # set input background to "has focus" color
                WyeUILib.Dialog.drawCursor(frame)
                WyeUILib.Dialog._activeInputFloat = frame
                return True
            else:
                return False

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, val):
            frame.vars.gWidget[1].setText(str(val))
            frame.vars.currVal[0] = str(val)
            # relayout to fit everything
            frame.parentDlg.verb.redisplay(frame.parentDlg)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setBackgroundColor(frame, color):
            frame.vars.gWidgetStack[0][0].setBackgroundColor(color)
            frame.vars.gWidget[0].setBackgroundColor(color)

    # text input field
    class InputButton:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE),   # 2 verb to call when button clicked
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),   # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL)
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("gWidget", Wye.dType.OBJECT, None),                  # 1 associated graphic widget
                    ("clickCount", Wye.dType.INTEGER, 0),                 # 3 button depressed count
                    )

        def start(stack):
            frm = Wye.codeFrame(WyeUILib.InputButton, stack)
            frm.vars.gWidgetStack[0] = []   # create local stack
            frm.vars.tags[0] = []           # create local stack
            return frm

        def run(frame):
            #print("InputButton frame", frame.tostring())
            frame.params.frame[0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]
            #print("InputButton display: label", frame.params.label)
            btn = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0],
                    bg=frame.params.backgroundColor[0], pos=(pos[0], pos[1], pos[2]), scale=(1, 1, 1),
                    parent=dlgHeader.getNodePath())
            frame.vars.gWidgetStack[0].append(btn)  # save for deleting on dialog close
            frame.vars.gWidget[0] = btn  # stash graphic obj in input's frame
            frame.vars.tags[0].append(btn.getTag())

            # update dialog pos to next free space downward
            pos[2] -= btn.getHeight()  # update to next position
            frame.vars.size[0] = (btn.getWidth(), 0, btn.getHeight())

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()

        # update value means nothing to us
        def update(frame):
            pass

        # return true if this is one of our tags (got clicked by user)
        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                frame.vars.gWidget[0].setColor(Wye.color.SELECTED_COLOR)  # set button color pressed
                if frame.vars.clickCount[0] <= 0:  # if not in an upclick count, process click
                    frame.vars.clickCount[0] = 10  # start flash countdown (in display frames)
                    dlgFrame.vars.clickedBtns[0].append(frame)  # stash button for flash countdown

                    WyeUILib.Dialog.doCallback(dlgFrame, frame, tag)
                return True
            else:
                return False

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidget[0].setText(text)
            frame.params.label[0] = text

        def setColor(frame, color):
            frame.vars.gWidget[0].setColor(color)

        def setBackgroundColor(frame, color):
            frame.vars.gWidget[0].setBackgroundColor(color)

    # checkbox
    # if radioGroup is a list, then will act as part of a group of radio buttons
    class InputCheckbox:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.OBJECT, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.BOOL, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.OBJECT, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL),
                      ("radioGroup", Wye.dType.STRING, Wye.access.REFERENCE, None),    # name of checkbox radio group, if any
                      ("selectedRadio", Wye.dType.INTEGER, Wye.access.REFERENCE, 0),  # if radio button, ix of currently selected one
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("localCallback", Wye.dType.OBJECT, None),            # local verb to call to toggle check value
                    ("localOptData", Wye.dType.ANY, None),
                    ("radioGroupList", Wye.dType.OBJECT, None),
                    )
        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputCheckbox, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []  # create local stack
            return frame

        def run(frame):
            #print("InputText label", frame.params.label, " value=", frame.params.value)
            frame.vars.currVal[0] = frame.params.value[0]
            frame.params.frame[0] = frame  # self referential!
            frame.vars.localCallback[0] = WyeUILib.InputCheckbox.InputCheckboxCallback       # save verb to call
            frame.vars.localOptData[0] = (frame)       # don't know position yet

            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm

            dlgHeader = dlgFrm.vars.dragObj[0]

            # label
            lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])
            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close
            # add tag, input index to dictionary
            frame.vars.tags[0].append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + 1

            # check box
            check = WyeCore.libs.Wye3dObjsLib._box(size=[.5, .05, .5], pos=[width, 0, .25], parent=lbl.getNodePath())
            check.setColor(Wye.color.FALSE_COLOR)
            tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
            check.setTag(tag)
            frame.vars.tags[0].append(tag)  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(check)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = check

            # are we part of a radio group?
            radNm = frame.params.radioGroup[0]
            if radNm:
                if radNm in frame.parentDlg.vars.radBtnDict[0]:
                    #print("InputCheckbox: found rad grp", radNm)
                    frame.vars.radioGroupList[0] = frame.parentDlg.vars.radBtnDict[0][radNm]
                    frame.vars.radioGroupList[0].append(frame)
                else:
                    #print("InputCheckbox: new rad grp", radNm)
                    radGrp = [frame]
                    frame.parentDlg.vars.radBtnDict[0][radNm] = radGrp
                    frame.vars.radioGroupList[0] = radGrp

            # set checkbox color to match data
            #print("InputCheckbox display: init value to", frame.params.value[0])
            frame.verb.setValue(frame, frame.params.value[0])

            # update dialog pos to next free space downward
            pos[2] -= max(lbl.getHeight(), check.getHeight())           # update to next position
            frame.vars.size[0] = (width + .75, 0, lbl.getHeight())

        # reposition in dialog
        def redisplay(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            lbl = frame.vars.gWidgetStack[0][0]
            lbl.setPos(pos)
            pos[2] -= lbl.getHeight()

        # update value
        def update(frame):
            frame.verb.setValue(frame, frame.params.value[0])

        # return true if this is one of our tags (got clicked by user)
        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                WyeUILib.Dialog.doCallback(dlgFrame, frame, tag)
                return True
            else:
                return False

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        # for checkbox, set on/off
        # for checkbox part of radioGroup, only do on
        def setValue(frame, isOn):
            if frame.vars.radioGroupList[0]:
                if isOn:
                    for frm in frame.vars.radioGroupList[0]:
                        if frm != frame:
                            frm.vars.currVal[0] = False
                            frm.vars.gWidget[0].setColor(Wye.color.FALSE_COLOR)
                    frame.vars.currVal[0] = True
                    frame.params.value[0] = True
                    frame.vars.gWidget[0].setColor(Wye.color.TRUE_COLOR)
                    ix = frame.vars.radioGroupList[0].index(frame)
                    for frm in frame.vars.radioGroupList[0]:
                        frm.params.selectedRadio[0] = ix
            else:
                frame.vars.currVal[0] = isOn
                frame.params.value[0] = isOn
                frame.vars.gWidget[0].setColor(Wye.color.TRUE_COLOR if isOn else Wye.color.FALSE_COLOR)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setBackgroundColor(frame, color):
            frame.vars.gWidget[0].setBackgroundColor(color)

        def setCurrentPos(frame, index):
            frame.vars.currPos[0] = index       # TODO needs validating!


        # User clicked input, generate the DropDown
        class InputCheckboxCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("retStat", Wye.dType.INTEGER, -1),
                        ("rowFrm", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                # print("InputCheckboxCallback started")
                return Wye.codeFrame(WyeUILib.InputCheckbox.InputCheckboxCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("InputCheckboxCallback run: data", data)
                rowFrm = data[1]
                dlgFrm = rowFrm.parentDlg

                #print("InputCheckboxCallback run: rowFrm", rowFrm.params.label[0], " ", rowFrm.verb.__name__)

                # toggle value
                rowFrm.vars.currVal[0] = not rowFrm.vars.currVal[0]     # toggle value
                rowFrm.verb.setValue(rowFrm, rowFrm.vars.currVal[0])    # make graphic match value state

                # if the user supplied a callback, call it
                WyeUILib.Dialog.doCallback(dlgFrm, rowFrm, "", doUserCallback=True)


    # dropdown input field
    class InputDropdown:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),    # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),    # user supplied label for field
                      ("list", Wye.dType.STRING, Wye.access.REFERENCE),     # text list of entries
                      ("selectionIx", Wye.dType.INTEGER, Wye.access.REFERENCE), # current selection index
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("backgroundColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.TRANSPARENT),
                      ("callback", Wye.dType.OBJECT, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),
                      ("layout", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.layout.VERTICAL),
                      ("showText", Wye.dType.BOOL, Wye.access.REFERENCE, True),
                      ("showLabel", Wye.dType.BOOL, Wye.access.REFERENCE, True)
                      )
        varDescr = (("retStat", Wye.dType.INTEGER, 0),                  # Dropdown returned index
                    ("position", Wye.dType.INTEGER_LIST, (0, 0, 0)),  # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),        # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("lWidget", Wye.dType.OBJECT, None),                  # associated graphic widget
                    ("bWidget", Wye.dType.OBJECT, None),                  # associated graphic widget
                    ("callback", Wye.dType.OBJECT, None),                 # internal verb to call when done
                    ("optData", Wye.dType.ANY, None),
                    ("localCallback", Wye.dType.OBJECT, None),             # internal verb to call when clicked - brings up dropdown
                    ("localOptData", Wye.dType.ANY, None),
                    ("clickCount", Wye.dType.INTEGER, 0),                 # button depressed count
                    ("list", Wye.dType.OBJECT_LIST, None),                # local copy of dropdown values
                    )

        def start(stack):
            frame = Wye.codeFrame(WyeUILib.InputDropdown, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.list[0] = []
            frame.vars.tags[0] = []  # create local stack
            return frame

        def run(frame):
            #print("  frame.params.frame=",frame.params.frame)
            frame.vars.localOptData[0] = (frame,)       # don't know position yet
            frame.vars.localCallback[0] = WyeUILib.InputDropdown.InputDropdownCallback
            frame.params.frame[0] = frame  # self referential!
            #print("InputDropdown optData", frame.params.optData, " manufactured optData", frame.vars.optData)

            #print("InputDropdown run: callback=", frame.vars.callback)

            # copy the list over for later
            frame.vars.list[0] = frame.params.list[0][:]
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position
            frame.parentDlg = dlgFrm
            dlgHeader = dlgFrm.vars.dragObj[0]
            width = 0
            height = 0
            if frame.params.showLabel[0]:
                lbl = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.label[0], frame.params.color[0], pos=(pos[0], pos[1], pos[2]),
                                    scale=(1, 1, 1), parent=dlgHeader.getNodePath(), bg=frame.params.backgroundColor[0])
                frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close
                frame.vars.lWidget[0] = lbl
                # add tag, input index to dictionary
                frame.vars.tags[0].append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
                width += lbl.getWidth()
                height = lbl.getHeight()

            # if show text
            if frame.params.showText[0] or not frame.params.showLabel[0]:       # have to show something, force text if user wants nothing
                width += .5
                # offset 3d input field right past end of 3d label
                if frame.vars.lWidget[0]:
                    txtParent = frame.vars.lWidget[0]
                    txtPos = (width, 0, 0)
                else:
                    txtParent = dlgHeader
                    txtPos = (pos[0], pos[1], pos[2])
                btn = WyeCore.libs.Wye3dObjsLib._3dText(frame.params.list[0][frame.params.selectionIx[0]], Wye.color.TEXT_COLOR,
                                    pos=txtPos, scale=(1, 1, 1), parent=txtParent.getNodePath(), bg=frame.params.backgroundColor[0])
                #btn.setColor(Wye.color.TEXT_COLOR)
                # print("    Dialog inWdg", btn)
                frame.vars.tags[0].append(btn.getTag())  # save tag for doSelect
                frame.vars.gWidgetStack[0].append(btn)  # save graphic widget for deleting on close
                frame.vars.bWidget[0] = btn
                width += btn.getWidth()
                if not height:
                    height = btn.getHeight()

            # update dialog pos to next free space downward
            pos[2] -= height  # update to next position
            frame.vars.size[0] = (width + .5, 0, height)       # TODO - width + .5 is hack to space lines nicely, add border spacing to layout
            #print("InputDropdown", frame.params.label[0], " size", frame.vars.size[0])
            #print("InputDropdown", frame.params.label[0], " redisplay size", frame.vars.size[0], " pos", pos, " width", width)


        def redisplay(frame, dlgFrm, pos):
            frame.verb.update(frame)
            frame.vars.position[0] = (pos[0], pos[1], pos[2])
            width = 0
            height = 0
            if frame.vars.lWidget[0]:
                lbl = frame.vars.lWidget[0]
                lbl.setPos(pos)
                width += lbl.getWidth()
                height = lbl.getHeight()
            #print("lbl '"+lbl.dbgTxt+"' width", width)
            if frame.vars.bWidget[0]:
                width += .5
                btn = frame.vars.bWidget[0]
                #print("btn'"+btn.dbgTxt+"' width", btn.getWidth())
                if frame.vars.lWidget[0]:
                    btn.setPos((width, 0,0))
                else:
                    btn.setPos((pos[0], pos[1], pos[2]))
                width += btn.getWidth()
                if not height:
                    height = btn.getHeight()
            pos[2] -= height
            frame.vars.size[0] = (width + .5, 0, height)      # TODO - width + .5 is hack to space lines nicely, add border spacing to layout
            #print("InputDropdown", frame.params.label[0], " redisplay size", frame.vars.size[0], " pos", pos, " width", width)

        def update(frame):
            frame.verb.setValue(frame, frame.params.selectionIx[0])

        def doSelect(frame, dlgFrame, tag):
            if tag in frame.vars.tags[0]:
                dlgFrame.params.retVal[0] = Wye.status.SUCCESS
                # call user callback
                WyeUILib.Dialog.doCallback(dlgFrame, frame, tag)
                return True
            else:
                return False

        def setList(frame, newList, newIndex):
            #print("frame", frame.verb.__name__, " setList: newList", newList, " newIndex", newIndex)
            frame.vars.list[0] = newList
            frame.verb.setValue(frame, newIndex)
            frame.params.selectionIx[0] = newIndex

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            if frame.vars.lWidget[0]:
                frame.vars.lWidget[0].setText(text)

        def setValue(frame, index):
            # todo Range check index!
            if frame.vars.bWidget[0]:
                frame.vars.bWidget[0].setText(frame.vars.list[0][index])
            frame.params.selectionIx[0] = index
            # relayout dialog to fit everything
            frame.parentDlg.verb.redisplay(frame.parentDlg)

        def setColor(frame, color):
            if frame.vars.lWidget[0]:
                frame.vars.lWidget[0].setColor(color)
            if frame.vars.bWidget[0]:
                frame.vars.bWidget[0].setColor(color)

        def setBackgroundColor(frame, color):
            if frame.vars.lWidget[0]:
                frame.vars.lWidget[0].setBackgroundColor(color)
            if frame.vars.bWidget[0]:
                frame.vars.bWidget[0].setBackgroundColor(color)


        # User clicked input, generate the DropDown and return selected row /
        class InputDropdownCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("retStat", Wye.dType.INTEGER, -1),
                        ("rowFrm", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                # print("InputDropdownCallback started")
                return Wye.codeFrame(WyeUILib.InputDropdown.InputDropdownCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("InputDropdownCallback run: data", data)
                rowFrm = data[1][0]
                parentFrm = rowFrm.parentDlg

                match (frame.PC):
                    case 0:
                        pos = [rowFrm.vars.position[0][0], rowFrm.vars.position[0][1], rowFrm.vars.position[0][2]]
                        pos[1] -= .5 # move in front of parent

                        dlgFrm = WyeUILib.DropDown.start(frame.SP)
                        dlgFrm.params.retVal = frame.vars.retStat
                        dlgFrm.params.title = [rowFrm.params.label[0].strip()]
                        dlgFrm.params.position = [[pos[0], pos[1], pos[2]],]
                        dlgFrm.params.parent = [parentFrm]

                        # build dialog frame params list of input frames
                        attrIx = 0
                        for rowTxt in rowFrm.vars.list[0]:
                            # print("lib", lib.__name__, " verb", verb.__name__)
                            btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [rowFrm]  # return value
                            btnFrm.params.parent = [dlgFrm]
                            btnFrm.params.label = [rowTxt]  # button label is currently selected value
                            # note: dropdown doesn't do per-row callbacks
                            WyeUILib.InputButton.run(btnFrm)

                            attrIx += 1

                        # WyeUILib.Dialog.run(dlgFrm)
                        frame.SP.append(dlgFrm)     # push dialog so it runs next cycle
                        frame.PC += 1               # on return from dialog, run next case

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = dlgFrm.status
                        if frame.vars.retStat[0] >=0:
                            #print("InputDropdown set value to", dlgFrm.params.retVal[0])
                            rowFrm.verb.setValue(rowFrm, frame.vars.retStat[0])

                            #print("parentFrm", rowFrm.verb.__name__, " callback", rowFrm.params.callback)
                            WyeUILib.Dialog.doCallback(dlgFrm, rowFrm, "none", doUserCallback=True)
                        #else:
                        #    print("InputDropdownCallback: user cancelled")



    # Dialog object.
    # Display dialog and fields
    # Update fields on events
    class Dialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("retVal", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.status.CONTINUE),    # 0 ok/cancel or other status (if dropdown)
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog frame, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE),
                      ("format", Wye.dType.STRING_LIST, Wye.access.REFERENCE, ""), # valid entries: "NO_OK", "NO_CANCEL", "
                      ("headerColor", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.HEADER_COLOR),
                      ("callback", Wye.dType.OBJECT, Wye.access.REFERENCE, None),   # exit callback
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE)
                      ) # 5+ variable length list of input control frames
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = (("position", Wye.dType.FLOAT_LIST, (0,0,0)),            # pos copy  *** REQUIRED ***
                    ("dlgWidgets", Wye.dType.OBJECT_LIST, None),            # standard dialog widgets
                    ("okTags", Wye.dType.STRING_LIST, None),                # OK widget tags
                    ("canTags", Wye.dType.STRING_LIST, None),               # Cancel widget tags
                    ("inpTags", Wye.dType.OBJECT, None),                    # dictionary return param ix of input by graphic tag
                    ("currInp", Wye.dType.OBJECT, None),                    # current focus widget, if any
                    ("radBtnDict", Wye.dType.OBJECT_LIST, None),  # radio button group dictionary
                    ("clickedBtns", Wye.dType.OBJECT_LIST, None),           # list of buttons that need to be unclicked
                    ("dragObj", Wye.dType.OBJECT, None),                    # path to top graphic obj *** REF'D BY CHILDREN ***
                    ("topTag", Wye.dType.STRING, ""),                       # Wye tag for top object (used for dragging)
                    ("bgndGObj", Wye.dType.OBJECT, None),                   # background card
                    ("outlineGObj", Wye.dType.OBJECT, None),                # background outline card
                    )

        _cursor = None      # 3d TextInput cursor
        _activeInputInteger = None  # used for wheel up/down events
        _activeInputFloat = None  # used for wheel up/down events

        def start(stack):
            frame = Wye.codeFrame(WyeUILib.Dialog, stack)
            # give frame unique lists
            frame.vars.dlgWidgets[0] = []       # standard widgets common to all Dialogs
            frame.vars.okTags[0] = []           # tags for OK buttons
            frame.vars.canTags[0] = []          # tags for Cancel buttons
            frame.vars.inpTags[0] = {}          # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []      # clicked button(s) being "flashed" (so user sees they were clicked)
            frame.vars.radBtnDict[0] = {}  # dictionary of radio button groups in this dialog

            # If there isn't a text input cursor, make it
            if WyeUILib.Dialog._cursor is None:
                WyeUILib.Dialog._cursor = WyeCore.libs.Wye3dObjsLib._box([.05, .05, .6], [0, 0, 0])
                WyeUILib.Dialog._cursor.hide()
            return frame

        # first time through run, draw dialog and all its fields
        # after that, process any buttons being flashed to show user they were clicked on
        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    #print("Dialog run: frame", frame.verb.__name__, " params", frame.paramsToStringV())
                    frame.params.retVal[0] = Wye.status.CONTINUE        # return value: 0 running, 1 OK, 2 Cancel
                    parent = frame.params.parent[0]

                    #print("Dialog put frame in param[0][0]", frame)
                    # make a copy of the position value
                    frame.vars.position[0] = (frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2])      # save display position
                    # return frame

                    #print("Dialog display: pos=frame.params.position", frame.params.position)

                    # top ok/cancel
                    if parent is None:
                        #print("  params.inputs", frame.params.inputs)
                        dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(frame.params.headerColor[0]), pos=frame.params.position[0], scale=(.2, .2, .2))
                        #dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0], scale=(1,1,1))
                        dlgHeader.setHpr(base.camera, 0,1,0)
                    else:
                        dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(frame.params.headerColor[0]), pos=frame.params.position[0],
                                                  scale=(1,1,1), parent=parent.vars.dragObj[0].getNodePath())
                    frame.vars.topTag[0] = dlgHeader.getTag()   # save tag for drag checking
                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.dragObj[0] = dlgHeader        # save graphic for parenting sub dialogs

                    # if big dialog, put ok/can at top too
                    nInputs = len(frame.params.inputs[0])
                    if nInputs > 4 or ("FORCE_TOP_CTLS" in frame.params.format[0]):
                        pos = [dlgHeader.getWidth() + 2, 0, 0]
                        haveOk = False
                        if not(frame.params.format[0] and "NO_OK" in frame.params.format[0]):
                            txt = WyeCore.libs.Wye3dObjsLib._3dText("[ OK ]", color=(Wye.color.CONTROL_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                                parent=dlgHeader.getNodePath())
                            frame.vars.dlgWidgets[0].append(txt)
                            frame.vars.okTags[0].append(txt.getTag())
                            pos[0] += txt.getWidth()       # shove Cancel to the right of OK
                            haveOk = True

                        if not (frame.params.format[0] and "NO_CANCEL" in frame.params.format[0]):
                            #print("Dialog Cancel btn at", pos)
                            txt = WyeCore.libs.Wye3dObjsLib._3dText("[ Cancel ]", color=(Wye.color.CONTROL_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                                parent=dlgHeader.getNodePath())
                            frame.vars.dlgWidgets[0].append(txt)
                            frame.vars.canTags[0].append(txt.getTag())

                    #print("Dialog run: params.position",frame.params.position[0])
                    # row position rel to parent, not global
                    pos = [0,0,0-dlgHeader.getHeight()] #[x for x in frame.params.position[0]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value

                    # draw user- supplied label and text inputs
                    #print("Dialog run: display %i inputs" % nInputs)
                    newX = pos[0]
                    prevZ = pos[2]
                    frame.doingDisplay = True
                    for ii in range(nInputs):
                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]

                        #print("  Dialog input", ii, " frame", inFrm.verb.__name__, inFrm.params.label if hasattr(inFrm.params, "label") else "<no label>")

                        # display inputs
                        # Note: each Input's display function updates draw "pos" downward
                        # stash returned display obj tags in lookup dict to detect what user clicked on
                        #print("Build dialog", frame.params.title[0])

                        # make sure this verb can display itself
                        if hasattr(inFrm.verb, "display"):
                            # if layout to the right instead of down
                            if inFrm.params.layout[0] == Wye.layout.ADD_RIGHT:
                                pos[0] = newX
                                pos[2] = prevZ
                                #print("Dialog Display:", inFrm.verb.__name__, " ", inFrm.params.label[0], " ADD_RIGHT X=", newX)
                                inFrm.verb.display(inFrm, frame, pos)  # displays label, updates pos
                            else:
                                prevZ = pos[2]
                                pos[0] = 0
                                #print("Dialog Display:", inFrm.verb.__name__, " ", inFrm.params.label[0], " VERTICAL X= 0")
                                inFrm.verb.display(inFrm, frame, pos)  # displays label, updates pos
                            # position the input on the dialog
                            newX = inFrm.vars.position[0][0] + inFrm.vars.size[0][0]
                            #print("Display", inFrm.verb.__name__, " ", inFrm.params.label[0], " pos"inFrm.)
                        else:
                            print("Dialog: Error. Unknown input verb", inFrm.verb.__name__)
                    frame.doingDisplay = False

                    # display bottom OK, Cancel buttons
                    pos[0] = 0
                    haveOk = False
                    if not (frame.params.format[0] and "NO_OK" in frame.params.format[0]):
                        txt = WyeCore.libs.Wye3dObjsLib._3dText("[ OK ]", color=(Wye.color.CONTROL_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                            parent=dlgHeader.getNodePath())
                        frame.vars.dlgWidgets[0].append(txt)
                        frame.vars.okTags[0].append(txt.getTag())
                        pos[0] += txt.getWidth()       # shove Cancel to the right of OK
                        haveOk = True

                    if not (haveOk and frame.params.format[0] and "NO_CANCEL" in frame.params.format[0]):
                        txt = WyeCore.libs.Wye3dObjsLib._3dText("[ Cancel ]", color=(Wye.color.CONTROL_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                            parent=dlgHeader.getNodePath())
                        frame.vars.dlgWidgets[0].append(txt)
                        frame.vars.canTags[0].append(txt.getTag())
                        
                    # done setup, go to next case to process events
                    frame.PC += 1

                    # make a background for entire dialog
                    WyeUILib.Dialog.genBackground(frame)

                    # Add dialog to known dialogs
                    WyeUILib.FocusManager.openDialog(frame, parent)        # pass parent, if any

                case 1:
                    # do click-flash count down and end-flash color reset for buttons user clicked
                    delLst = []
                    # decrement flash count.  if zero, turn off button highlight
                    for btnFrm in frame.vars.clickedBtns[0]:
                        #print("button", btnFrm.verb.__name__, " count ", btnFrm.vars.clickCount[0])
                        btnFrm.vars.clickCount[0] -= 1
                        if btnFrm.vars.clickCount[0] <= 0:
                            delLst.append(btnFrm)
                            btnFrm.vars.gWidget[0].setColor(btnFrm.params.color[0])
                    # remove any buttons whose count is finished
                    for btnFrm in delLst:
                        #print("Dialog run: Remove clicked btn frame", btnFrm.verb.__name__)
                        frame.vars.clickedBtns[0].remove(btnFrm)


        def genBackground(frame):
            if frame.params.parent[0] is None:
                scMult = 5
            else:
                scMult = 1
            dlgNodePath = frame.vars.dragObj[0].getNodePath()
            # dlgNodePath.setPos(frame.vars.position[0][0], frame.vars.position[0][1], frame.vars.position[0][2])
            dlgBounds = dlgNodePath.getTightBounds()
            card = CardMaker("Dlg Bgnd")
            gFrame = LVecBase4f(0, 0, 0, 0)
            # print("gFrame", gFrame)
            ht = (dlgBounds[1][2] - dlgBounds[0][2]) * scMult + 1
            dx = dlgBounds[1][0] - dlgBounds[0][0]
            dy = dlgBounds[1][1] - dlgBounds[0][1]
            wd = (math.sqrt(dx * dx + dy * dy)) * scMult + 1
            gFrame[0] = 0  # marginL
            gFrame[1] = wd  # marginR
            gFrame[2] = 0  # marginB
            gFrame[3] = ht  # marginT
            # print("initial adjusted gFrame", gFrame)
            card.setFrame(gFrame)
            cardPath = NodePath(card.generate())
            cardPath.reparentTo(dlgNodePath)
            cardPath.setPos((-.5, .1, 1.2 - ht))
            cardPath.setColor(Wye.color.BACKGROUND_COLOR)
            frame.vars.bgndGObj[0] = cardPath

            # background outline
            oCard = CardMaker("Dlg Bgnd Outline")
            # print("gFrame", gFrame)
            gFrame[0] = -.1  # marginL
            gFrame[1] = wd + .3  # marginR
            gFrame[2] = -.1  # marginB
            gFrame[3] = ht + .3  # marginT
            # print("initial adjusted gFrame", gFrame)
            oCard.setFrame(gFrame)
            oCardPath = NodePath(oCard.generate())
            oCardPath.reparentTo(dlgNodePath)
            oCardPath.setPos((-.6, .2, 1.1 - ht))
            oCardPath.setColor(Wye.color.OUTLINE_COLOR)
            frame.vars.outlineGObj[0] = oCardPath

        # dialog's input list changed, update all row positions
        def redisplay(frame):
            if hasattr(frame, "doingDisplay") and frame.doingDisplay:
                return
            #print("Dialog '"+frame.params.title[0]+"' redisplay")
            frame.doingDisplay = True
            # readjust the position for all the inputs
            pos = LVecBase3f(0, 0, 0 - frame.vars.dragObj[0].getHeight())
            nInputs = len(frame.params.inputs[0])
            #print("redisplay", nInputs, " lines of dialog")

            # draw user-supplied label and text inputs
            newX = pos[0]
            prevZ = pos[2]
            #print("Dialog", frame.params.title[0]," redisplay: start pos", pos)
            for ii in range(nInputs):
                inFrm = frame.params.inputs[0][ii][0]
                #print("  Dialog input", ii, " frame", inFrm.verb.__name__, inFrm.params.label if hasattr(inFrm.params, "label") else "<no label>")
                # print("    inFrm", inFrm)
                # print("    Dialog input ", ii, " inFrm", inFrm)
                # print("       inFrm.params.title", inFrm.params.title)
                # print("")

                # update position of all inputs
                # Note: each Input's display function updates draw position "pos" downward
                if hasattr(inFrm.verb, "redisplay"):
                    # if stack to the right of prev input
                    if inFrm.params.layout[0] == Wye.layout.ADD_RIGHT:
                        pos[0] = newX
                        pos[2] = prevZ

                        # DEBUG
                        #if hasattr(inFrm.params, "label"):
                        #    print("  ", inFrm.params.label[0], " at", pos)
                        #else:
                        #    print("   ", inFrm.verb.__name__, " at", pos)
                        #print("Dialog Display:", inFrm.verb.__name__, " ", inFrm.params.label[0], " ADD_RIGHT X=", newX)
                        inFrm.verb.redisplay(inFrm, frame, pos)  # displays label, updates pos

                    # else stack below prev input
                    else:
                        prevZ = pos[2]
                        pos[0] = 0

                        # DEBUG
                        #if hasattr(inFrm.params, "label"):
                        #    print("  ", inFrm.params.label[0], " at rel", pos)
                        #else:
                        #    print("   ", inFrm.verb.__name__, " at rel", pos)
                        #print("Dialog Display:", inFrm.verb.__name__, " ", inFrm.params.label[0], " VERTICAL X= 0")
                        inFrm.verb.redisplay(inFrm, frame, pos)  # displays label, updates pos

                    # calc the pos plus width in case next is ADD_RIGHT
                    newX = inFrm.vars.position[0][0] + inFrm.vars.size[0][0]

                else:
                    print("Dialog redisplay: Error. No redisplay function on input verb", inFrm.verb.__name__)
                #print("pos", pos)

            # update Ok/Cancel positions
            pos[0] = 0
            pos[1] -= .1
            #print("ok pos", pos)
            # if have cancel button, then ok (if any) will be 2nd from end
            if (frame.params.format[0] and "NO_CANCEL" in frame.params.format[0]):
                okIx = -1
            else:
                okIx = -2
            # if have ok button, position it
            if not (frame.params.format[0] and "NO_OK" in frame.params.format[0]):
                #print("Dialog redisplay: okIx", okIx, " put", frame.vars.dlgWidgets[0][okIx].dbgTxt, " at", pos)
                frame.vars.dlgWidgets[0][okIx].setPos(pos)        # Ok
                pos[0] += 2.5  # shove Cancel to the right of OK
                haveOk = True
            if not (haveOk and frame.params.format[0] and "NO_CANCEL" in frame.params.format[0]):
                frame.vars.dlgWidgets[0][-1].setPos(pos)

            # update background
            frame.vars.bgndGObj[0].removeNode()
            frame.vars.outlineGObj[0].removeNode()
            frame.verb.genBackground(frame)
            frame.doingDisplay = False

        def doCallback(frame, inFrm, tag, doUserCallback=False):
            # Unless caller overrides with doUserCallback, look for vars.localCallback first
            # to run control's internal callback
            if not doUserCallback and hasattr(inFrm.vars, "localCallback") and inFrm.vars.localCallback[0]:
                callVerb = inFrm.vars.localCallback[0]
                #print("Dialog doCallback: verb", inFrm.verb.__name__, " local callback", callVerb.__name__)
                if callVerb and hasattr(inFrm.vars, "localOptData"):      # check vars copy first to handle InputXxxx classes
                    if len(inFrm.vars.localOptData) > 0:
                        data = inFrm.vars.localOptData[0]
                    else:
                        data = None
            # either no internal callback, or we're called from the internal callback with "doUserCallback"
            # If there's a user supplied callback, call it
            elif hasattr(inFrm.params, "callback") and isinstance(inFrm.params.callback, list) \
                    and len(inFrm.params.callback) > 0 and inFrm.params.callback[0]:
                callVerb = inFrm.params.callback[0]
                #print("Dialog doCallback: ", inFrm.verb.__name__, "params callback", callVerb.__name__)
                if callVerb and hasattr(inFrm.params, "optData") and isinstance(inFrm.params.optData, list) \
                    and len(inFrm.params.optData) > 0 and inFrm.params.optData[0]:
                    data = inFrm.params.optData[0]
                else:
                    data = None
            else:
                #print("Dialog doCallback: No callback for input", inFrm.verb.__name__, " '"+ inFrm.params.label[0]+"'")
                callVerb = None
            if callVerb:
                # start the verb
                try:
                    verbFrm = callVerb.start(frame.SP)

                    # if not single cycle, then put up as parallel path
                    if callVerb.mode != Wye.mode.SINGLE_CYCLE:
                        # queue to be called every display cycle
                        WyeCore.World.setRepeatEventCallback("Display", verbFrm, data)
                    else:
                        # call this once
                        verbFrm.eventData = (tag, data, inFrm)  # pass along user supplied event data, if any
                        if Wye.debugOn:
                            Wye.debug(verbFrm, "Dialog doSelect: call single cycle verb " + verbFrm.verb.__name__ + " data" + str(verbFrm.eventData))
                        else:
                            # print("Dialog doSelect run", verbFrm.verb.__name__)
                            verbFrm.verb.run(verbFrm)
                except Exception as e:
                    if Wye.devPrint:
                        print("Dialog doCallback: Error running callback verb", callVerb.__name__, "\n", str(e))
                        traceback.print_exception(e)
                    title = "Callback Error"
                    text = "Error running callback verb "+ callVerb.__name__+ "\n"+ str(e) + "\n" + traceback.format_exc()
                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog(title, text, color=Wye.color.WARNING_COLOR)

        # User clicked on a tag. It might belong to a field in our dialog.
        # Figure out what dialog field it belongs to, if any, and do the appropriate thing
        def doSelect(frame, tag):
            # print("Dialog doSelect: ", frame.verb, " tag", tag)
            prevSel = frame.vars.currInp[0]      # get current selection
            # if tag is input field in this dialog, select it
            closing = False
            WyeUILib.Dialog._activeInputFloat = None
            WyeUILib.Dialog._activeInputInteger = None
            retStat = False     # haven't used the tag (yet)

            # if clicked header for dragging
            if tag == frame.vars.topTag[0]:
                if not Wye.dragging:
                    Wye.dragging = True
                    WyeUILib.dragFrame = frame

                    retStat = True  # used up the tag

            # for all inputs check to see if they want the tag
            else:
                for inp in frame.params.inputs[0]:
                    inFrm = inp[0]
                    if inFrm.verb.doSelect(inFrm, frame, tag):
                        # print("Dialog doSelect set currInp", inFrm.verb.__name__)
                        frame.vars.currInp[0] = inFrm
                        retStat = True


            # if clicked on OK or Cancel
            if not retStat:
                # if is Cancel button
                if tag in frame.vars.canTags[0]:    # if cancel button
                    frame.params.retVal[0] = Wye.status.FAIL
                    #print("Dialog", frame.params.title[0], " Cancel Button pressed, return status", frame.params.retVal)
                    retStat = True

                # else if OK button
                elif tag in frame.vars.okTags[0]:
                    #print("Dialog", frame.params.title[0], " OK Button pressed")
                    nInputs = (len(frame.params.inputs[0]))
                    #print("dialog ok: nInputs",nInputs," inputs",frame.params.inputs[0])
                    for ii in range(nInputs):
                        inFrm = frame.params.inputs[0][ii][0]
                        # for any text inputs, copy working string to return string
                        if inFrm.verb is WyeUILib.InputText or inFrm.verb is WyeUILib.InputCheckbox:
                            #print("input", ii, " frame", inFrm, "\n", WyeCore.Utils.frameToString(inFrm))
                            #print("input old val '"+ inFrm.params[2][0]+ "' replaced with '"+ inFrm.vars[1][0]+"'")
                            inFrm.params.value[0] = inFrm.vars.currVal[0]
                        elif inFrm.verb is WyeUILib.InputInteger:
                            inFrm.params.value[0] = int(inFrm.vars.currVal[0])
                        elif inFrm.verb is WyeUILib.InputFloat:
                            inFrm.params.value[0] = float(inFrm.vars.currVal[0])

                    frame.params.retVal[0] = Wye.status.SUCCESS
                    #print("doSelect OK button, return status", frame.params.retVal)
                    retStat = True

                if retStat:
                    # Done with dialog
                    WyeUILib.Dialog.closeDialog(frame)
                    WyeUILib.Dialog.doCallback(frame, frame, tag)

                    closing = True
                    #print("Closing dialog.  Status", frame.status)

            # selected graphic tag not recognized as a control in this dialog
            if not retStat:
                frame.vars.currInp[0] = None   # no currInp

            # If there was a diff selection before, fix that
            # (if closing dialog, nevermind)
            if not prevSel is None and prevSel != frame.vars.currInp[0] and not closing:
                inFrm =prevSel
                if inFrm.verb in [WyeUILib.InputText, WyeUILib.InputInteger, WyeUILib.InputFloat]:
                    inWidg = inFrm.vars.gWidget[0]
                    inWidg.setColor(Wye.color.TEXT_COLOR)

            #print("Dialog retStat", retStat)
            return retStat      # return true if we used the tag

        def closeDialog(frame):
            frame.status = Wye.status.SUCCESS

            # remove dialog from active dialog list
            WyeUILib.FocusManager.closeDialog(frame)

            # delete any graphic objects associated with the inputs
            nInputs = (len(frame.params.inputs[0]))
            for ii in range(nInputs):
                inFrm = frame.params.inputs[0][ii][0]
                inFrm.verb.close(inFrm)

            # delete the graphic widgets associated with the dialog
            for wdg in frame.vars.dlgWidgets[0]:
                # print("del ctl ", wdg.text.name)
                wdg.removeNode()

        # do select-related operations that cannot be done when elements of dialog are executing
        # (i.e. if a line gets deleted, do it after the line has finished execting its callback
        # so we don't crash)
        # setOn - true if something in dialog used the
        def postSelect(frame):
            # Something in dialog used the tag, highlight the dialog
            WyeUILib.Dialog.activateDialog(frame, True)


        # manage selected/unselected look of dialog
        def activateDialog(frame, setOn):
            if setOn:
                # if there's already an active dialog, deactivate it
                if WyeUILib.FocusManager._activeDialog:
                    WyeUILib.Dialog.activateDialog(WyeUILib.FocusManager._activeDialog, False)
                # make this the currently active dialog
                WyeUILib.FocusManager._activeDialog = frame
                frame.vars.bgndGObj[0].setColor(Wye.color.BACKGROUND_COLOR_SEL)
                frame.vars.outlineGObj[0].setColor(Wye.color.OUTLINE_COLOR_SEL)
                #print("Dialog '"+frame.params.title[0]+ "' Selected")

            else:
                pass
                frame.vars.bgndGObj[0].setColor(Wye.color.BACKGROUND_COLOR)
                frame.vars.outlineGObj[0].setColor(Wye.color.OUTLINE_COLOR)
                #print("Dialog '"+frame.params.title[0]+ "' Unselected")

        # inc/dec InputInteger on wheel event
        def doWheel(dir):
            #print("doWheel")
            if WyeUILib.Dialog._activeInputInteger:
                #print("doWheel update input")
                inFrm = WyeUILib.Dialog._activeInputInteger
                if isinstance(inFrm.vars.currVal[0], str):
                    inFrm.vars.currVal[0] = str(int(inFrm.vars.currVal[0]) + dir)
                else:
                    inFrm.vars.currVal[0] += dir

                txt = str(inFrm.vars.currVal[0])
                inWidg = inFrm.vars.gWidget[0]
                inWidg.setText(txt)
                WyeUILib.Dialog.drawCursor(inFrm)

                # if the user supplied a callback
                if inFrm.vars.callback[0]:
                    WyeUILib.Dialog.doCallback(inFrm.parentDlg, inFrm, "none")

            elif WyeUILib.Dialog._activeInputFloat:
                #print("doWheel update input")
                inFrm = WyeUILib.Dialog._activeInputFloat
                if isinstance(inFrm.vars.currVal[0], str):
                    try:
                        f = float(inFrm.vars.currVal[0])
                    except:
                        f = 0
                    inFrm.vars.currVal[0] = str(f + dir)
                else:
                    inFrm.vars.currVal[0] += dir

                txt = str(inFrm.vars.currVal[0])
                inWidg = inFrm.vars.gWidget[0]
                inWidg.setText(txt)
                WyeUILib.Dialog.drawCursor(inFrm)

                # if the user supplied a callback
                WyeUILib.Dialog.doCallback(inFrm.parentDlg, inFrm, "none")

        # update InputText/InputInteger on key event
        def doKey(frame, key):
            #print("Dialog doKey: key", key)
            # if we have an input with focus
            inFrm = frame.vars.currInp[0]
            if not inFrm is None:
                if inFrm.verb in [WyeUILib.InputText, WyeUILib.InputInteger, WyeUILib.InputFloat]:

                    txt = str(inFrm.vars.currVal[0])    # handle either text or integer
                    insPt = inFrm.vars.currInsPt[0]
                    preTxt = txt[:insPt]
                    postTxt = txt[insPt:]
                    # delete key
                    if key == '\x08':  # backspace delete key
                        if insPt > 0:
                            preTxt = preTxt[:-1]
                            insPt -= 1
                            inFrm.vars.currInsPt[0] = insPt
                        txt = preTxt + postTxt
                        if not txt.strip() and inFrm.verb in [WyeUILib.InputInteger, WyeUILib.InputFloat]:     # if blank and numeric
                            txt = "0"

                    if key == -9:  # delete (forward) key
                        if insPt < len(txt):
                            postTxt = postTxt[1:]
                        txt = preTxt + postTxt
                        if not txt.strip() and inFrm.verb in [WyeUILib.InputInteger, WyeUILib.InputFloat]:     # if blank and numeric
                            txt = "0"

                    # arrow keys
                    elif key == Wye.ctlKeys.LEFT:   # arrow keys
                        # if ctl down, skip whole alphanum word, or at least 1 ch
                        if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                            startPt = insPt
                            txtLen = len(txt)
                            while insPt > 0 and txt[insPt-1].isalnum():
                                insPt -= 1
                            # if not alphanum so didn't move, move 1
                            if insPt == startPt and insPt > 0:
                                insPt -= 1
                        # else move 1 ch
                        elif insPt > 0:
                            insPt -= 1
                        # place insert cursor
                        inFrm.vars.currInsPt[0] = insPt
                        WyeUILib.Dialog.drawCursor(inFrm)
                        return

                    elif key == Wye.ctlKeys.RIGHT:
                        # if ctl down, skip whole alphanum word, or at least 1 ch
                        txtLen = len(txt)
                        if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                            startPt = insPt
                            while insPt < txtLen and (txt[insPt].isalnum() if insPt < txtLen else True):
                                insPt += 1
                            # if not alphanum so didn't move, move 1
                            if startPt == insPt and insPt < txtLen:
                                insPt += 1
                        # else move 1 ch
                        elif insPt < txtLen:
                            insPt += 1
                        # place insert cursor
                        inFrm.vars.currInsPt[0] = insPt
                        WyeUILib.Dialog.drawCursor(inFrm)
                        return

                    elif key == Wye.ctlKeys.END:
                        txtLen = len(txt)
                        insPt = txtLen
                        inFrm.vars.currInsPt[0] = insPt
                        WyeUILib.Dialog.drawCursor(inFrm)

                    elif key == Wye.ctlKeys.HOME:
                        inFrm.vars.currInsPt[0] = 0
                        WyeUILib.Dialog.drawCursor(inFrm)


                    # not special control, if printable char, insert it in the string
                    else:
                        if isinstance(key,str):
                            #print("verb is", inFrm.verb.__name__)
                            # For int input, only allow ints
                            if inFrm.verb is WyeUILib.InputInteger:
                                if key in "-0123456789":
                                    if key != '-' or insPt == 0:
                                        txt = preTxt + key + postTxt
                                        insPt += 1
                                        inFrm.vars.currInsPt[0] = insPt  # set text insert point after new char

                            # For float input, only allow floats
                            if inFrm.verb is WyeUILib.InputFloat:
                                if key in "-0123456789.":
                                    # only allow "-" as first char
                                    # #only allow "." if don't have one
                                    if (key != '-' or insPt == 0) and (key != '.' or txt.find('.') == -1):
                                        txt = preTxt + key + postTxt
                                        insPt += 1
                                        inFrm.vars.currInsPt[0] = insPt  # set text insert point after new char


                            # else general text
                            elif key.isprintable():
                                txt = preTxt + key + postTxt
                                insPt += 1
                                inFrm.vars.currInsPt[0] = insPt        # set text insert point after new char

                    if inFrm.verb is WyeUILib.InputInteger and len(txt) == 0 or txt == "-":
                        txt = '0'
                    inFrm.vars.currVal[0] = txt

                    # if the user supplied a callback
                    # note: callback can change currVal and result will be displayed
                    WyeUILib.Dialog.doCallback(inFrm.parentDlg, inFrm, "none")

                    inWidg = inFrm.vars.gWidget[0]
                    #print("  set text", txt," ix", ix, " txtWidget", inWidg)
                    inWidg.setText(txt)
                    # place insert cursor
                    WyeUILib.Dialog.drawCursor(inFrm)

        # draw text cursor at InputText frame's currInsPt
        def drawCursor(inFrm):
            insPt = inFrm.vars.currInsPt[0]

            inWidg = inFrm.vars.gWidget[0]
            #wPos = inWidg.getPos()
            xOff = 0
            WyeUILib.Dialog._cursor._path.reparentTo(inWidg._path)
            WyeUILib.Dialog._cursor.setColor(Wye.color.CURSOR_COLOR)
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
            WyeUILib.Dialog._cursor.setPos(xOff + .01, -.1, .3)
            WyeUILib.Dialog._cursor.show()

        def hideCursor():
            WyeUILib.Dialog._cursor.hide()

        def setPos(frame, pos):
            frame.vars.dragObj[0]._path.setPos(pos[0], pos[1], pos[2])

    # dropdown menu
    # subclass of Dialog so FocusManager can handle focus properly
    # Returns index of selected line or -1
    class DropDown(Dialog):
        def start(stack):
            frame = Wye.codeFrame(WyeUILib.DropDown, stack)
            frame.vars.dlgWidgets[0] = []      # standard widgets common to all Dialogs
            frame.vars.okTags[0] = []         # tags for OK buttons
            frame.vars.canTags[0] = []         # tags for Cancel buttons
            frame.vars.inpTags[0] = {}         # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []     # clicked button(s) being "flashed" (so user sees they were clicked)

            return frame

        def run(frame):
            match frame.PC:
                case 0:  # Start up case - set up all the fields
                    frame.params.retVal[0] = -1           # set default return value
                    parent = frame.params.parent[0]

                    frame.vars.position[0] = (frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2])  # save display position

                    # handle scale and parent obj, if any
                    if parent is None:
                        dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0], scale=(.2, .2, .2))
                        #dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0], scale=(1,1,1))
                    else:
                        #print("dropdown parent", parent.verb.__name__)
                        dlgHeader = WyeCore.libs.Wye3dObjsLib._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0],
                                                  scale=(1,1,1), parent=parent.vars.dragObj[0].getNodePath())

                    frame.vars.topTag[0] = dlgHeader.getTag()   # save tag for drag checking
                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.dragObj[0] = dlgHeader        # save graphic for parenting sub dialogs

                    # if big dialog, put ok/can at top too
                    nInputs = len(frame.params.inputs[0])
                    if nInputs > 6:
                        pos = [dlgHeader.getWidth() + 2, 0, 0]
                        txt = WyeCore.libs.Wye3dObjsLib._3dText("[ Cancel ]", color=(Wye.color.CONTROL_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                            parent=dlgHeader.getNodePath())
                        frame.vars.dlgWidgets[0].append(txt)
                        frame.vars.canTags[0].append(txt.getTag())


                    pos = [0, 0, -dlgHeader.getHeight()]  # [x for x in frame.params.position[0]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value

                    # draw user-supplied label and text inputs
                    for ii in range(nInputs):
                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]

                        # tell input to display itself.  Collect returned objects to close when dlg closes
                        # Note: each Input's display function updates pos downward
                        if inFrm.verb in [WyeUILib.InputLabel, WyeUILib.InputButton]:
                            inFrm.verb.display(inFrm, frame, pos)  # displays label, updates pos
                        else:
                            print("Dialog: ERROR. Only Label and Button allowed in dropdown", inFrm.verb.__class__)

                    # Cancel button

                    #print("Dialog Cancel btn at", pos)
                    txt = WyeCore.libs.Wye3dObjsLib._3dText("[ Cancel ]", color=(Wye.color.HEADER_COLOR), pos=tuple(pos),
                                        scale=(1,1,1), parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.canTags[0].append(txt.getTag())

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
                    cardPath.setColor(Wye.color.BACKGROUND_COLOR)
                    frame.vars.bgndGObj[0] = cardPath
                    # background outline
                    oCard = CardMaker("Dlg Bgnd Outline")
                    # print("gFrame", gFrame)
                    gFrame[0] = -.1    # marginL
                    gFrame[1] = wd+.3  # marginR
                    gFrame[2] = -.1    # marginB
                    gFrame[3] = ht+.3  # marginT
                    # print("initial adjusted gFrame", gFrame)
                    oCard.setFrame(gFrame)
                    oCardPath = NodePath(oCard.generate())
                    oCardPath.reparentTo(dlgNodePath)
                    oCardPath.setPos((-.6, .2, 1.1 - ht))
                    oCardPath.setColor(Wye.color.OUTLINE_COLOR)
                    frame.vars.outlineGObj[0] = oCardPath
                    WyeUILib.FocusManager.openDialog(frame, parent)  # pass parent, if any

                    frame.params.retVal[0] = -1     # default to cancelled
                    frame.PC += 1

                case 1:
                    # spin waiting for click event to set currInp
                    if frame.vars.currInp[0]:
                        # On click event, callback set status to selected row, clean up dialog
                        ix = 0
                        for inLst in frame.params.inputs[0]:
                            if inLst[0] == frame.vars.currInp[0]:
                                frame.params.retVal[0] = ix
                                break
                            ix += 1

                        # remove dialog from active dialog list
                        WyeUILib.FocusManager.closeDialog(frame)
                        # delete the graphic widgets associated with the dialog
                        for wdg in frame.vars.dlgWidgets[0]:
                            # print("del ctl ", wdg.text.name)
                            wdg.removeNode()
                        # and we're done!
                        frame.status = Wye.status.SUCCESS


    class AskSaveAsFile:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("retVal", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.status.CONTINUE),
                      ("fileName", Wye.dType.STRING, Wye.access.REFERENCE, ""),
                      ("fileType", Wye.dType.STRING, Wye.access.REFERENCE, ".py"),
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE, "Save As"),
                      ("parent", Wye.dType.OBJECT, Wye.access.REFERENCE, None),
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, (0,0,0))
                      )
        varDescr = (("fileName", Wye.dType.OBJECT, None),
                    ("newFile", Wye.dType.BOOL, True),
                    ("overWriteQuery", Wye.dType.BOOL, False)
                    )

        # global list of libs being edited
        activeFrames = {}

        def start(stack):
            f = Wye.codeFrame(WyeUILib.AskSaveAsFile, stack)
            f.systemObject = True         # not stopped by breakAll or debugger
            return f

        def run(frame):
            match(frame.PC):
                case 0:
                    #print("AskSaveAsFile run case 0: fileName", frame.params.fileName[0])
                    filePath = frame.params.fileName[0].strip()
                    fileName, ext = os.path.splitext(os.path.basename(filePath))
                    #print("AskSaveAsFile: fileName", fileName, " ext", ext)

                    # generate unique name
                    ii = 1
                    while os.path.exists(fileName + "_" + str(ii)+ frame.params.fileType[0]):
                        ii += 1
                    frame.vars.fileName[0] = fileName + "_" + str(ii) + frame.params.fileType[0]

                    if not frame.params.parent[0]:
                        # position in front of other dialogs
                        point = NodePath("point")
                        point.reparentTo(render)
                        point.setPos(base.camera, (0, Wye.UI.NOTIFICATION_OFFSET, 0))
                        pos = point.getPos()
                        point.removeNode()

                    else:
                        pos = frame.params.position[0]

                    dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog(frame.params.title[0], parent=frame.params.parent[0], position=pos)
                    WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Save  New", frame.vars.newFile, radioGroup="newRad")
                    WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "File Name:", frame.vars.fileName, layout=Wye.layout.ADD_RIGHT)
                    WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Overwrite ", [False], radioGroup="newRad")
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, frame.params.fileName[0], layout=Wye.layout.ADD_RIGHT)
                    frame.SP.append(dlgFrm)     # push dialog so it runs next cycle

                    frame.PC += 1               # on return from dialog, run next case
                    #print("AskSaveAsFile: case 0: push dialog frame. Stack:")
                    #for ii in range(len(frame.SP)):
                    #    print("  ",ii," ",frame.SP[ii].params.title[0] if hasattr(frame.SP[ii].params, "title") else frame.SP[ii].verb.__name__)

                case 1:
                    dlgFrm = frame.SP.pop()
                    frame.status = Wye.status.SUCCESS       # we always succeed
                    #print("AskSaveAsFile: case 1: dlg done with status", Wye.status.tostring(dlgFrm.status), ", dlg retVal", Wye.status.tostring(dlgFrm.params.retVal[0]))
                    frame.params.retVal[0] = dlgFrm.params.retVal[0]    # return dialog's status
                    if frame.params.retVal[0] == Wye.status.SUCCESS:
                        if frame.vars.newFile[0]:   # if user chose new file name
                            filePath = frame.vars.fileName[0].strip()

                        else:
                            filePath = frame.params.fileName[0].strip()
                        # ensure has correct extension
                        fileName = os.path.splitext(os.path.basename(filePath))[0]
                        #print("AskSaveAs ", filePath," base name:", fileName)
                        frame.params.fileName[0] = fileName + frame.params.fileType[0]
                    #print("AskSaveAs final fileName", fileName)

    # Wye main menu - user settings n stuff
    class MainMenuDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("dlgFrm", Wye.dType.OBJECT, None),
                    ("listCode", Wye.dType.BOOL, False)
                    )

        # global list of libs being edited
        activeFrames = {}

        def start(stack):
            f = Wye.codeFrame(WyeUILib.MainMenuDialog, stack)
            f.systemObject = True         # not stopped by breakAll or debugger
            return f

        def run(frame):
            match(frame.PC):
                case 0:

                    # create top level edit dialog
                    dlgFrm = WyeUILib.Dialog.start(frame.SP)
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Wye Main Menu"]
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,Wye.UI.DIALOG_OFFSET,0))
                    pos = point.getPos()
                    point.removeNode()
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]
                    dlgFrm.params.format = [["NO_CANCEL"]]
                    frame.vars.dlgFrm[0] = dlgFrm

                    # Settings
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Settings", Wye.color.SUBHD_COLOR)

                    sndChkFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  3D Sound On", [Wye.soundOn], WyeUILib.MainMenuDialog.SoundCheckCallback)
                    sndChkFrm.params.optData = [sndChkFrm]

                    codeChkFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  List Compiled Code", [WyeCore.debugListCode],
                                        WyeUILib.MainMenuDialog.ListCodeCallback)
                    codeChkFrm.params.optData = [codeChkFrm]


                    devChkFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  Dev prints in IDE", [Wye.devPrint],
                                        WyeUILib.MainMenuDialog.ListDevCodeCallback)
                    devChkFrm.params.optData = [devChkFrm]

                    verChkFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  Show Wye Version", [True],
                                        WyeUILib.MainMenuDialog.VerCheckCallback)
                    verChkFrm.params.optData = [verChkFrm]

                    copyBtnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Show Copy Paste List",
                                        WyeUILib.MainMenuDialog.CopyPasteCallback)
                    copyBtnFrm.params.optData = [copyBtnFrm]

                    #
                    # system debug
                    #
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Diagnostics")

                    verboseChkFrm = WyeUILib.InputCheckbox.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([verboseChkFrm])
                    verboseChkFrm.params.frame = [None]
                    verboseChkFrm.params.parent = [None]
                    verboseChkFrm.params.value = [False]
                    verboseChkFrm.params.label = ["  Toggle verbose message display"]
                    verboseChkFrm.params.callback = [WyeUILib.MainMenuDialog.VerboseCheckCallback]  # button callback
                    verboseChkFrm.params.optData = [verboseChkFrm]
                    verboseChkFrm.verb.run(verboseChkFrm)

                    #
                    # Test
                    #

                    testLblFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                    testLblFrm.params.frame = [None]  # return value
                    testLblFrm.params.parent = [None]
                    testLblFrm.params.label = ["Test"]
                    testLblFrm.params.color = [Wye.color.SUBHD_COLOR]
                    WyeUILib.InputLabel.run(testLblFrm)
                    dlgFrm.params.inputs[0].append([testLblFrm])

                    obj2ChkFrm = WyeUILib.InputCheckbox.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([obj2ChkFrm])
                    obj2ChkFrm.params.frame = [None]
                    obj2ChkFrm.params.parent = [None]
                    obj2ChkFrm.params.value = [True]
                    obj2ChkFrm.params.label = ["  Show Test Fish"]
                    obj2ChkFrm.params.callback = [WyeUILib.MainMenuDialog.AngleFishCheckCallback]  # button callback
                    obj2ChkFrm.params.optData = [obj2ChkFrm]
                    obj2ChkFrm.verb.run(obj2ChkFrm)

                    btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([btnFrm])
                    btnFrm.params.frame = [None]
                    btnFrm.params.parent = [None]
                    btnFrm.params.label = ["  Test Button"]
                    btnFrm.params.callback = [WyeUILib.MainMenuDialog.TestButtonCallback]  # button callback
                    #btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb)]  # button row, dialog frame
                    WyeUILib.InputButton.run(btnFrm)

                    btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([btnFrm])
                    btnFrm.params.frame = [None]
                    btnFrm.params.parent = [None]
                    btnFrm.params.label = ["  Test Create Lib"]
                    btnFrm.params.callback = [WyeUILib.MainMenuDialog.TestCreateLibCallback]  # button callback
                    btnFrm.params.optData = [(frame,)]  # button row, dialog frame
                    WyeUILib.InputButton.run(btnFrm)

                    WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "   Display Code", frame.vars.listCode, layout=Wye.layout.ADD_RIGHT)

                    # midi test
                    midFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                    midFrm.params.frame = [None]
                    midFrm.params.parent = [None]
                    midFrm.params.label = ["  Test Midi: "]
                    midFrm.params.callback = [WyeUILib.MainMenuDialog.TestMidiCallback]  # button callback
                    # opt data and run below, after ins and note frames created
                    dlgFrm.params.inputs[0].append([midFrm])

                    midInsFrm = WyeCore.libs.WyeUIUtilsLib.doInputInteger(dlgFrm, "Instrument:", [64], layout=Wye.layout.ADD_RIGHT)
                    midNoteFrm = WyeCore.libs.WyeUIUtilsLib.doInputInteger(dlgFrm, "Note:", [64], layout=Wye.layout.ADD_RIGHT)
                    midVolFrm = WyeCore.libs.WyeUIUtilsLib.doInputInteger(dlgFrm, "Vol:", [64], layout=Wye.layout.ADD_RIGHT)
                    midLenFrm = WyeCore.libs.WyeUIUtilsLib.doInputFloat(dlgFrm, "Len(s)", [1.0], layout=Wye.layout.ADD_RIGHT)

                    # fill in midFrm callback data now that ins, note frames created
                    midFrm.params.optData = [(midInsFrm, midNoteFrm, midVolFrm, midLenFrm)]  # button row, dialog frame
                    midFrm.verb.run(midFrm)

                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.mainMenu)
                    WyeCore.World.mainMenu = None



        # turn sound on/off
        class SoundCheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("SoundCheckCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.SoundCheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                Wye.soundOn = rowFrm.vars.currVal[0]
                #print("3D Sound On", Wye.soundOn)


        # turn compile code listing
        class ListCodeCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("ListCodeCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.ListCodeCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                WyeCore.debugListCode = rowFrm.vars.currVal[0]
                #("List Code On", WyeCore.debugListCode)

        # turn compile code listing
        class ListDevCodeCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("ListDevCodeCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.ListDevCodeCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                Wye.devPrint = rowFrm.vars.currVal[0]
                #("List Code On", WyeCore.debugListCode)

        # show/hide version in world
        class VerCheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("VerCheckCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.VerCheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                showObj = rowFrm.vars.currVal[0]
                if showObj:
                    WyeCore.World.versionText.show()
                else:
                    WyeCore.World.versionText.hide()

        # show/hide version in world
        class CopyPasteCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("CopyPasteCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.CopyPasteCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                WyeCore.World.cutPasteManager.show()

        #
        # diagnostic callbacks
        #

        # turn on/off display of every event Panda3d processes
        class VerboseCheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("VerboseCheckCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.VerboseCheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                verbose = rowFrm.vars.currVal[0]

                from direct.showbase.MessengerGlobal import messenger
                messenger.toggleVerbose()      # Show all events



        #
        # test callbacks
        #

        # show/hide obj2 (sun angle fish & button)
        class AngleFishCheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("AngleFishCheckCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.AngleFishCheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                showObj = rowFrm.vars.currVal[0]
                angleFish = WyeCore.World.findActiveObj('angleFish')
                testText = WyeCore.World.findActiveObj('showFishDialog')
                if showObj:
                    angleFish.vars.gObj[0].show()
                    testText.vars.dlgButton[0].show()
                else:
                    angleFish.vars.gObj[0].hide()
                    testText.vars.dlgButton[0].hide()

        # test whatever needs testing now
        class TestButtonCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("TestButtonCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.TestButtonCallback, stack)

            def run(frame):
                #("Test Button")
                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Test Callback", "Pop Up Dialog Test default color")
                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Test Callback", "Pop Up Dialog Test normal", Wye.color.NORMAL_COLOR)
                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Test Callback", "Pop Up Dialog Test warning", Wye.color.WARNING_COLOR)
                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Test Callback", "Pop Up Dialog Test error", Wye.color.ERROR_COLOR)


        # test create lib and verb from data
        class TestCreateLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("TestCreatLibCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.TestCreateLibCallback, stack)

            def run(frame):
                data = frame.eventData
                editVerbFrm = data[1][0]
                #print("createLibrary test")
                lib = WyeCore.Utils.createLib("MyTestLibrary")


                # libTpl += "    def test():\n        print('Hi from "+name+" " + str(WyeCore.Utils.getId())+"')\n"
                vertSettings = {
                    'mode': Wye.mode.MULTI_CYCLE,
                    'autoStart': True,
                    'dataType': Wye.dType.NONE
                }

                paramDescr = ()

                varDescr = (
("gObj", Wye.dType.OBJECT, None),
("objTag", Wye.dType.STRING, "objTag"),
("sound", Wye.dType.OBJECT, None),
("position", Wye.dType.FLOAT_LIST, [0, 15, 0]),
("dPos", Wye.dType.FLOAT_LIST, [0., 0., .1]),
("dAngle", Wye.dType.FLOAT_LIST, [0., 0., 0.]),
("colorWk", Wye.dType.FLOAT_LIST, [1, 1, 1]),
("colorInc", Wye.dType.FLOAT_LIST, [1, 5, 10]),
("color", Wye.dType.FLOAT_LIST, [.5, .5, .5, 1]),
("skew", Wye.dType.FLOAT, 0),
("delta", Wye.dType.FLOAT, 0),
("cleanUpObjs", Wye.dType.OBJECT_LIST, None),  # list of graphic elements to delete on Stop
)

                codeDescr = (
# (None, ("print('MyTestVerb case 0: start - set up object')")),
("Var=", "frame.vars.cleanUpObjs[0] = []"),
("WyeCore.libs.WyeLib.loadObject",
 (None, "[frame]"),
 (None, "frame.vars.gObj"),
 (None, "['fish.glb']"),
 (None, "frame.vars.position"),  # posVec
 (None, "[[0, 90, 0]]"),  # rotVec
 (None, "[[.25,.25,.25]]"),  # scaleVec
 (None, "frame.vars.objTag"),
 (None, "frame.vars.color"),
 ("Var", "frame.vars.cleanUpObjs"),
 ),
# ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
# ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
(None, "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
("Label", "Repeat"),
# set angle
#("Code", "print('MyTestVerb run')"),
("Code", "from random import random"),
("Code", "frame.vars.skew[0] = .25 if abs(frame.vars.dAngle[0][2]) > .8 else .5"),
("Code", "frame.vars.skew[0] = 1-frame.vars.skew[0] if frame.vars.dAngle[0][2] > .0 else frame.vars.skew[0]"),
("Code", "frame.vars.delta[0] = (random()-frame.vars.skew[0])/10"),
#("Code", "print('dAngle', frame.vars.dAngle[0][2], ' skew', frame.vars.skew[0], ' delta', frame.vars.delta[0])"),
("Code", "frame.vars.dAngle[0][2] += frame.vars.delta[0]"),
("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngle")),
# Step forward
("Code", "frame.vars.dPos[0][2] += (random()-.5)/100"),
("Code", "frame.vars.dPos[0][2] = max(min(frame.vars.dPos[0][2], .3), .05)"),
("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
("WyeCore.libs.WyeLib.getObjPos", (None, "frame.vars.position"), (None, "frame.vars.gObj")),
# set color
("Var=", "frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
("Var=", "frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
("Var=", "frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
("Code", "if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
("Code", " frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
("Code", "if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
("Code", " frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
("Code", "if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
("Code", " frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
("Var=",
 "frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
(
"WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.vars.gObj"), ("Var", "frame.vars.color")),

("GoTo", "Repeat")
)
                WyeCore.Utils.createVerb(lib, "MyTestFish", vertSettings, paramDescr, varDescr, codeDescr,
                                         listCode=editVerbFrm.vars.listCode[0])

        # test midi player
        class TestMidiCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("TestMidiCallback started")
                return Wye.codeFrame(WyeUILib.MainMenuDialog.TestMidiCallback, stack)

            def run(frame):
                data = frame.eventData
                insFrm = data[1][0]
                noteFrm = data[1][1]
                volFrm = data[1][2]
                lenFrm = data[1][3]

                ins = int(insFrm.vars.currVal[0])
                note = int(noteFrm.vars.currVal[0])
                vol = int(volFrm.vars.currVal[0])
                len = float(lenFrm.vars.currVal[0])

                if ins > 127:
                    ins = 127
                    insFrm.vars.currVal[0] = ins
                    insFrm.verb.update(insFrm)
                if ins < 0:
                    ins = 0
                    insFrm.vars.currVal[0] = ins
                    insFrm.verb.update(insFrm)
                if note > 127:
                    note = 127
                    noteFrm.vars.currVal[0] = note
                    noteFrm.verb.update(noteFrm)
                if note < 0:
                    note = 0
                    noteFrm.vars.currVal[0] = note
                    noteFrm.verb.update(noteFrm)
                if vol > 127:
                    vol = 127
                    volFrm.vars.currVal[0] = vol
                    volFrm.verb.update(volFrm)
                if len < .1:
                    len = .1
                    lenFrm.vars.currVal[0] = len
                    lenFrm.verb.update(lenFrm)
                Wye.midi.playNote(ins, note, vol, len)


    # Create dialog showing loaded libraries so user can edit them
    class EditMainDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("dlgFrm", Wye.dType.OBJECT, None),
                    ("fileName", Wye.dType.STRING, "MyWyeLib.py"),  # file name to save to
                    ("libFileNameFrm", Wye.dType.OBJECT, "MyWyeLib"),  # new lib name input, if user wants to create one
                    ("libNameFrm", Wye.dType.OBJECT, "MyWyeLib"),  # new lib name input, if user wants to create one
                    ("libRows", Wye.dType.OBJECT_LIST, None),
                    )

        activeLibs = {}

        def start(stack):
            f = Wye.codeFrame(WyeUILib.EditMainDialog, stack)
            f.vars.libRows[0] = []
            return f

        def run(frame):
            match(frame.PC):
                case 0:
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0, Wye.UI.DIALOG_OFFSET, 0))
                    pos = point.getPos()
                    point.removeNode()

                    # create top level edit dialog
                    dlgFrm = WyeUILib.Dialog.start(frame.SP)
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Wye Libraries"]
                    dlgFrm.params.format = [["NO_CANCEL"]]
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]
                    frame.vars.dlgFrm[0] = dlgFrm

                    # build dialog

                    # Load lib from file
                    loadLibFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, " Load Library From:", WyeUILib.EditMainDialog.LoadLibCallback)
                    loadLibFrm.params.optData = [(loadLibFrm, dlgFrm, frame)]
                    libFileNameFrm = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "  File Name", frame.vars.fileName, layout=Wye.layout.ADD_RIGHT)
                    frame.vars.libFileNameFrm[0] = libFileNameFrm

                    # New lib
                    newLibFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, " Create New Library:", WyeUILib.EditMainDialog.NewLibCallback)
                    newLibFrm.params.optData = [(newLibFrm, dlgFrm, frame)]
                    libNameFrm = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "  Lib Name:", ["MyWyeLib"], layout=Wye.layout.ADD_RIGHT)
                    frame.vars.libNameFrm[0] = libNameFrm


                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Select Library to Edit", color=Wye.color.SUBHD_COLOR)

                    # list all the known libs
                    for lib in WyeCore.World.libList:
                        WyeUILib.EditMainDialog.listLib(frame, dlgFrm, lib)

                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle
                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done
                    #print("EditMainDialog: Done")

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.editMenu)
                    WyeCore.World.editMenu = None

        def listLib(frame, dlgFrm, lib):
            if hasattr(lib, "systemLib"):
                editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "      .")
                frame.vars.libRows[0].append(editLnFrm)
            else:
                editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [["Save To File", "Delete Library"]], [0],
                                                                       WyeUILib.EditMainDialog.EditLibLineCallback,
                                                                       showText=False)
                frame.vars.libRows[0].append(editLnFrm)

            # make the dialog row
            btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, " " + lib.__name__, WyeUILib.EditMainDialog.EditLibCallback,
                                                              layout=Wye.layout.ADD_RIGHT)
            frame.vars.libRows[0].append(btnFrm)
            btnFrm.params.optData = [[btnFrm, dlgFrm, lib]]  # button row, row frame, dialog frame, obj frame

            editLnFrm.params.optData = [(editLnFrm, dlgFrm, frame, btnFrm, lib)]
            
        def update(editVerbFrm, dlgFrm):
            # update the dialog

            # remove rows from dialog
            firstIx = WyeCore.Utils.nestedIndexFind(dlgFrm.params.inputs[0], editVerbFrm.vars.libRows[0][0])
            for ii in range(len(editVerbFrm.vars.libRows[0])):
                frm = dlgFrm.params.inputs[0].pop(firstIx)[0]
                frm.verb.close(frm)

            # generate new rows
            editVerbFrm.vars.libRows[0].clear()
            # list all the known libs
            for lib in WyeCore.World.libList:
                WyeUILib.EditMainDialog.listLib(editVerbFrm, dlgFrm, lib)

            # display new rows
            pos = [0, 0, 0]
            for frm in editVerbFrm.vars.libRows[0]:
                frm.verb.display(frm, dlgFrm, pos)

            # relayout display
            dlgFrm.verb.redisplay(dlgFrm)

        class CloseLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("retStat", Wye.dType.INTEGER, -1),
                        ("rowFrm", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                # print("CloseLibCallback started")
                return Wye.codeFrame(WyeUILib.EditMainDialog.CloseLibCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("CloseLibCallback run: data", data)
                lib = data[1]
                #print("CloseLibCallback remove", lib.__name__)
                #print(" from ", WyeUILib.EditMainDialog.activeLibs)
                WyeUILib.EditMainDialog.activeLibs.pop(lib.__name__)


        # load library / save library
        class EditLibLineCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.NONE
            paramDescr = ()
            varDescr = (("fileName", Wye.dType.STRING, ""),
                        ("doExistsQuery", Wye.dType.BOOL, False),
                        )

            def start(stack):
                #print("EditLibLineCallback started")
                return Wye.codeFrame(WyeUILib.EditMainDialog.EditLibLineCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditLibLineCallback data", data)
                editLnFrm = data[1][0]  # add/del/copy button frame
                parentFrm = data[1][1]  # parent dialog
                editVerbFrm = data[1][2] # EditVerb frame
                btnFrm = data[1][3]     # param line
                lib = data[1][4]      # the library we're messing with

                # make sure we have the latest version of this library (stored links can ref old copies of lib)
                lib = WyeCore.World.libDict[lib.__name__]

                # get selectionIx
                opIx = editLnFrm.params.selectionIx[0]

                match(frame.PC):
                    case 0:
                        match(opIx):
                            case 0:     # Save library op
                                if hasattr(lib, "systemLib"):
                                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Library", "System libraries cannot be saved", Wye.color.WARNING_COLOR)
                                    frame.status = Wye.status.SUCCESS
                                    return

                                fileName = lib.__name__+".py"
                                frame.vars.fileName[0] = fileName
                                # if the file alredy exists, as the user what they want to do
                                fileExists = os.path.exists(fileName)
                                frame.vars.doExistsQuery[0] = fileExists
                                if frame.vars.doExistsQuery[0]:
                                    title = fileName + " Already Exists"
                                    pos = editLnFrm.vars.position[0]
                                    pos = [pos[0] + .5, pos[1] - .5, pos[2] - .5]
                                    askSaveFrm = WyeCore.libs.WyeUIUtilsLib.doAskSaveAsFileAsync(frame, parentFrm,
                                                                fileName, position=pos, title=title)
                                    frame.SP.append(askSaveFrm)  # push dialog so it runs next cycle

                                frame.PC = 1  # on return from dialog, run save lib case
                                # print("EditLibLineCallback: case 0: save library")

                            case 1:     # Delete library op
                                if hasattr(lib, "systemLib"):
                                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Library", "System libraries cannot be deleted", Wye.color.WARNING_COLOR)
                                    frame.status = Wye.status.SUCCESS
                                    return

                                # delete lib ok?
                                #print("EditLibLineCallback: case 0: delete library")
                                delOkFrm = WyeCore.libs.WyeUIUtilsLib.doPopUpDialogAsync(frame, "Delete Library", "Delete Library "+lib.__name__+"?", formatLst=[""])
                                frame.SP.append(delOkFrm)  # push dialog so it runs next cycle
                                frame.PC = 2  # on return from dialog, run del ok case

                    case 1: # continue saving library
                        frame.status = Wye.status.SUCCESS
                        # if we asked the user about overwrite, get the final filename
                        if frame.vars.doExistsQuery[0]:
                            askSaveFrm = frame.SP.pop()
                            #print("EditLibLineCallback: case 1: askSaveFrm", askSaveFrm.verb.__name__,
                            #      " user status", Wye.status.tostring(askSaveFrm.params.retVal[0]))

                            # if the user cancelled, don't save the lib
                            if askSaveFrm.params.retVal[0] != Wye.status.SUCCESS:
                                #print("User cancelled saving library")
                                return

                            # get the filename
                            fileName = askSaveFrm.params.fileName[0].strip()
                            if not fileName:
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Invalid File Name", "'"+fileName+"' is not a valid library file name",
                                                       Wye.color.WARNING_COLOR)
                                frame.status = Wye.status.SUCCESS
                                return
                            frame.vars.fileName[0] = fileName

                        else:
                            fileName = frame.vars.fileName[0]

                        # force lib name to match file name
                        libName = os.path.splitext(os.path.basename(fileName))[0]
                        #print("EditLibLineCallback base file name:", libName)

                        # create library header text and add text for all its verbs
                        fileTxt = WyeCore.Utils.createLibString(libName)
                        for attr in dir(lib):
                            if attr != "__class__":
                                verb = getattr(lib, attr)
                                if inspect.isclass(verb):
                                    # can only export verbs that have the required data
                                    if hasattr(verb, "paramDescr") and hasattr(verb, "varDescr") and hasattr(verb, "codeDescr"):
                                        # capture the flags
                                        verbSettings = {}
                                        if hasattr(verb, 'mode'):
                                            verbSettings['mode'] = verb.mode
                                        if hasattr(verb, 'cType'):
                                            verbSettings['cType'] = verb.cType
                                        if hasattr(verb, 'parTermType'):
                                            verbSettings['parTermType'] = verb.parTermType
                                        if hasattr(verb, 'autoStart'):
                                            verbSettings['autoStart'] = verb.autoStart
                                        if hasattr(verb, 'dataType'):
                                            verbSettings['dataType'] = verb.dataType

                                        # gen verb code
                                        vrbStr = WyeCore.Utils.createVerbString(libName, verb.__name__,
                                                    verbSettings,  verb.paramDescr,  verb.varDescr,
                                                    verb.codeDescr, doTest=False, outDent=False)

                                        fileTxt += vrbStr
                                    else:
                                        # ignoring generated runtime code is good.  Anything else is a problem
                                        if not verb.__name__[-3:] == "_rt":
                                            print("WARNING: Verb", verb.__name__,
                                              " not saved to file because it does not have all required attributes")
                        try:
                            # write the file
                            f = open(fileName, "w")
                            f.write(fileTxt)
                            f.close()
                        except Exception as e:
                            #print("Failed to write library '" + libName + "' to file '" + fileName + "'\n", str(e))
                            traceback.print_exception(e)
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Failed to write library", "Failed to write library '"+libName+"' to file '"+fileName+"'",
                                                   Wye.color.WARNING_COLOR)
                            frame.status = Wye.status.SUCCESS
                            return
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Saved Library", "Wrote "+libName+" to "+fileName)
                        #print("EditLibLineCallback case 1: Wrote lib '" + libName + "' to '" + fileName + "'")


                    case 2: # return from Del Ok? dialog
                        delOkFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS
                        if delOkFrm.params.retVal[0] == Wye.status.SUCCESS:
                            #print("EditLibLineCallback case 2: del lib "+lib.__name__)

                            # delete the library
                            libName = lib.__name__
                            WyeCore.World.libDict.pop(libName)
                            WyeCore.World.libList.remove(lib)

                            editVerbFrm.update(editVerbFrm, parentFrm)
                        #else:
                        #    print("User cancelled delete library")

        # load library from file and start any autoStart verbs in it
        class LoadLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("LoadLibCallback started")
                return Wye.codeFrame(WyeUILib.EditMainDialog.LoadLibCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("LoadLibCallback data=", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                # get lib name
                libFilePath = editFrm.vars.libFileNameFrm[0].vars.currVal[0].strip()
                if libFilePath:
                    # extract libName from file name and make sure there's an extension
                    libName, ext = os.path.splitext(os.path.basename(libFilePath))
                    if not ext:
                        #print("Add .py to ", libFilePath)
                        libFilePath += ".py"

                    # see if file exists
                    if not os.path.exists(libFilePath):
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("File Not Found", "File not found "+libFilePath, Wye.color.ERROR_COLOR)
                        return

                    # path = libFile
                    path = WyeCore.Utils.resourcePath(libFilePath)[2:]
                    #print("Load library '" + path + "'")
                    try:
                        #print("Load lib", libName, " from", path)
                        libModule = SourceFileLoader(libName, path).load_module()

                        #print("LoadLibCallback: libModule ", libModule, " libName", libName)
                        #print(" libModule", dir(libModule))
                        lib = getattr(libModule, libName)
                        #print("Read library", lib.__name__, " from file")
                        # print("add libClass", libClass, " to libList")
                        newLib = True   # assume this is a new lib
                        oldLibIx = -1
                        if libName in WyeCore.World.libDict:
                            #print("Lib", libName, " already loaded.  Delete old and add new")
                            oldLib = WyeCore.World.libDict[libName]
                            if not hasattr(oldLib, "systemLib"):
                                oldLibIx = WyeCore.World.libList.index(oldLib)
                                WyeCore.World.libList.remove(oldLib)
                                newLib = False
                            # don't allow overwrite of system lib
                            # todo - read text file, if invalid name give user option to have us generate a versioned one and load that
                            else:
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Library", libName + " is a system library.  Overwriting not allowed",
                                                    Wye.color.ERROR_COLOR)
                                return

                        WyeCore.World.libList.append(lib)
                        # print("Loaded library ", libName, " from file ", path, " into lib class ", libClass)

                        # add to known libraries
                        WyeCore.World.libDict[lib.__name__] = lib  # build lib name -> lib lookup dictionary
                        setattr(WyeCore.libs, libName, lib)  # put lib on lib dict
                        lib._build()  # build all Wye code segments in code words.
                                     # Any verbs with autoStart are added to startObjs

                        # parse starting object names and find the objects in the known libraries
                        # print("worldRunner:  start ", len(world.startObjs), " objs")
                        for objStr in WyeCore.World.startObjs:
                            # print("WorldRun start: obj ", objStr," in startObjs")
                            namStrs = objStr.split(".")  # parse name of object
                            if namStrs[1] in WyeCore.World.libDict:
                                obj = getattr(WyeCore.World.libDict[namStrs[1]], namStrs[2])  # get object from library
                                WyeCore.World.startActiveObject(obj)
                            else:
                                err = "Lib '" + namStrs[1] + "' not found for start object "+ objStr
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Failed to start object", err, Wye.color.WARNING_COLOR)
                        # started them, clear list
                        WyeCore.World.startObjs.clear()

                        # show new library
                        if newLib:
                            # puts two inputs in dialog (todo - find better way to get just-added rows)
                            WyeUILib.EditMainDialog.listLib(editFrm, parentFrm, lib)
                            b1 = editFrm.vars.libRows[0][-2]
                            b2 = editFrm.vars.libRows[0][-1]

                            # display new buttons
                            pos = [0, 0, 0]
                            b1.verb.display(b1, parentFrm, pos)
                            b2.verb.display(b2, parentFrm, pos)
                            # redisplay dialog
                            parentFrm.verb.redisplay(parentFrm)
                        else:
                            # ugh, hacky, find index of lib button to update with updated lib
                            backIx = 0 - (len(WyeCore.World.libList) - oldLibIx)
                            oldBtn = parentFrm.params.inputs[0][backIx][0]
                            oldBtn.params.optData[0][2] = lib

                    except Exception as e:
                        err = "Failed to read file " + path +"\n"+str(e)
                        traceback.print_exception(e)
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("File Read Failed", err, Wye.color.ERROR_COLOR)
                        return

                else:
                    err = "Invalid library file name '"+ libFilePath +"'.  Library not saved"
                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("File Read Failed", err, Wye.color.ERROR_COLOR)
                    return



        # load library from file and start any autoStart verbs in it
        class NewLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                #print("NewLibCallback started")
                return Wye.codeFrame(WyeUILib.EditMainDialog.NewLibCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("NewLibCallback data=", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                libName = editFrm.vars.libNameFrm[0].vars.currVal[0].strip()
                #print("NewLibCallback: libName", libName)

                if not libName:
                    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Name Required", "Please enter a name for the new library",
                                        Wye.color.WARNING_COLOR)
                    return

                newLib = True   # assume this is a new lib
                oldLibIx = -1
                if libName in WyeCore.World.libDict:
                    # print("Lib", libName, " already loaded.  Delete old and add new")
                    oldLib = WyeCore.World.libDict[libName]
                    if not hasattr(oldLib, "systemLib"):
                        oldLibIx = WyeCore.World.libList.index(oldLib)
                        WyeCore.World.libList.remove(oldLib)
                        mewlib = False
                        # don't allow overwrite of system lib
                    else:
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Library", libName + " is a system library.  Overwriting not allowed",
                                            Wye.color.ERROR_COLOR)
                        return

                # if we got here, finally we can create the lib
                lib = WyeCore.Utils.createLib(libName)

                # show new library
                if newLib:
                    # puts two inputs in dialog (todo - find better way to get just-added rows)
                    WyeUILib.EditMainDialog.listLib(editFrm, parentFrm, lib)
                    b1 = editFrm.vars.libRows[0][-2]
                    b2 = editFrm.vars.libRows[0][-1]

                    # display new buttons
                    pos = [0, 0, 0]
                    b1.verb.display(b1, parentFrm, pos)
                    b2.verb.display(b2, parentFrm, pos)
                    # redisplay dialog
                    parentFrm.verb.redisplay(parentFrm)
                else:
                    # ugh, hacky, find index of lib button to update with updated lib
                    backIx = 0 - (len(WyeCore.World.libList) - oldLibIx)
                    oldBtn = parentFrm.params.inputs[0][backIx][0]
                    oldBtn.params.optData[0][2] = lib

        # put up dialog showing verbs in given library
        # NOTE, ALSO CALLED FROM EditVerb.  POTENTIAL FOR SUBTLE DISASTER
        class EditLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.OBJECT, None),
                        ("selVerb", Wye.dType.OBJECT, None),
                        ("vrbStat", Wye.dType.INTEGER, -1),
                        ("newVerbName", Wye.dType.STRING, "NewVerb"),
                        ("rows", Wye.dType.OBJECT_LIST, None),
                        ("lib", Wye.dType.OBJECT, None)
                        )

            def start(stack):
                # print("EditLibCallback started")
                f = Wye.codeFrame(WyeUILib.EditMainDialog.EditLibCallback, stack)
                f.vars.rows[0] = []
                return f

            def run(frame):
                data = frame.eventData
                #print("EditLibCallback data=", data)
                btnFrm = data[1][0]
                parentDlgFrm = data[1][1]
                lib = data[1][2]

                # make sure we have the latest version
                lib = WyeCore.World.libDict[lib.__name__]
                frame.vars.lib[0] = lib

                if lib.__name__ in WyeUILib.EditMainDialog.activeLibs:
                    #print("Already editing this object", lib.__name__)

                    # bring lib to front
                    dlgFrm = WyeUILib.EditMainDialog.activeLibs[lib.__name__]
                    #print("bring dlg", dlgFrm.params.title, " to front")
                    path = dlgFrm.vars.dragObj[0]._path
                    path.setPos(base.camera, (0, Wye.UI.DIALOG_OFFSET - .5, 0))
                    path.setHpr(base.camera, 0, 1, 0)
                    return

                #print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)

                #print("EditLibCallback called, library row", libRow, " name", lib.__name__)
                #print("parentDlg '"+ parentDlgFrm.params.title[0] +"'")
                #print("parentDlgFrm", parentDlgFrm)

                # get the world position of the relative location of the dialog row the user clicked on
                #print("editLibCallback btnFrm.vars.position", btnFrm.vars.position[0])
                objOffset = -.5 + btnFrm.vars.position[0][2]
                objPos = (2, -.5, objOffset)
                point = NodePath("point")
                point.reparentTo(render)
                point.setPos(parentDlgFrm.vars.dragObj[0]._path, objPos)
                pos = point.getPos()
                point.removeNode()

                stk = []
                dlgFrm = WyeUILib.Dialog.start(stk)

                dlgFrm.params.retVal = frame.vars.vrbStat
                dlgFrm.params.title = ["Library '" + lib.__name__ +"'"]
                dlgFrm.params.position = [[pos[0], pos[1], pos[2]],]
                dlgFrm.params.parent = [None]
                dlgFrm.params.format = [["NO_CANCEL",]]
                dlgFrm.params.callback = [WyeUILib.EditMainDialog.CloseLibCallback]
                dlgFrm.params.optData = [(lib),]

                # add lib to actively edited objs
                #print("put lib", lib.__name__, "in", WyeUILib.EditMainDialog.activeLibs)
                WyeUILib.EditMainDialog.activeLibs[lib.__name__] = dlgFrm

                createFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  New Verb:", WyeUILib.EditMainDialog.EditLibCallback.CreateVerbCallback)
                newVerbNameFrm = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "  Name:", frame.vars.newVerbName, layout=Wye.layout.ADD_RIGHT)
                createFrm.params.optData = [(createFrm, newVerbNameFrm, dlgFrm, lib, frame),]

                WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  New Verb:", WyeUILib.EditMainDialog.EditLibCallback.CreateVerbCallback)

                # todo - add
                WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Select Verb to Edit", color=Wye.color.SUBHD_COLOR)

                # create a row for each verb in the library
                WyeUILib.EditMainDialog.EditLibCallback.listVerbs(frame, dlgFrm)

                # launch lib as stand alone dlg so can have multiple libs open at once
                stk.append(dlgFrm)
                dlgFrm.verb.run(dlgFrm)
                WyeCore.World.startActiveFrame(dlgFrm)

                # Hack to point back to this frame for updating
                dlgFrm.motherFrame = frame


            def listVerbs(frame, dlgFrm):
                lib = frame.vars.lib[0]
                # print("_displayLib: process library", lib.__name__)
                for attr in dir(lib):
                    if attr != "__class__":
                        verb = getattr(lib, attr)
                        if inspect.isclass(verb) and not verb.__name__.endswith("_rt"):
                            # can only start verbs that don't require data
                            if hasattr(verb, "paramDescr") and len(verb.paramDescr) == 0:
                                prefFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "Start",
                                          WyeUILib.EditMainDialog.EditLibCallback.StartLibVerbCallback, (verb,))
                            else:
                                prefFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "        .")
                            frame.vars.rows[0].append(prefFrm)

                            # can only delete verbs if not a system library
                            if not hasattr(lib, "systemLib"):
                                delFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, " Del",
                                          WyeUILib.EditMainDialog.EditLibCallback.DelLibVerbCallback, (verb,),
                                                    layout=Wye.layout.ADD_RIGHT)
                                frame.vars.rows[0].append(delFrm)


                            if hasattr(verb, "codeDescr"):
                                # print("lib", lib.__name__, " verb", verb.__name__)
                                btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  " + verb.__name__,
                                                             WyeUILib.EditMainDialog.EditLibCallback.EditlibraryVerbCallback,
                                                             layout=Wye.layout.ADD_RIGHT)
                                btnFrm.params.optData = [(btnFrm, dlgFrm, verb)]  # button data - offset to button
                                frame.vars.rows[0].append(btnFrm)
                            else:
                                # gray out verbs that don't have editable code
                                btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  " + verb.__name__,
                                                            layout=Wye.layout.ADD_RIGHT,
                                                            color=Wye.color.DISABLED_COLOR)
                                frame.vars.rows[0].append(btnFrm)


            # delete all verb rows and redo them
            def update(frame, dlgFrm):
                # delete all dialog lib verb inputs
                delCt = 0
                for bFrmRef in frame.vars.rows[0]:
                    inpIx = WyeCore.Utils.nestedIndexFind(dlgFrm.params.inputs[0], bFrmRef)
                    oldFrm = dlgFrm.params.inputs[0].pop(inpIx)[0]
                    oldFrm.verb.close(oldFrm)  # remove graphic content
                    delCt += 1
                # print("after delete", delCt," dialog rows, inputs len", len(dlgFrm.params.inputs[0]))
                frame.vars.rows[0].clear()  # old inputs gone

                # rebuild dialog lib verb list
                WyeUILib.EditMainDialog.EditLibCallback.listVerbs(frame, dlgFrm)
                # update display
                for frm in frame.vars.rows[0]:
                    pos = [0, 0, 0]
                    frm.verb.display(frm, dlgFrm, pos)
                dlgFrm.verb.redisplay(dlgFrm)

            # edit verb in lib
            class EditlibraryVerbCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = (("count", Wye.dType.INTEGER, 0),)

                def start(stack):
                    #print("EditlibraryVerbCallback start")
                    return Wye.codeFrame(WyeUILib.EditMainDialog.EditLibCallback.EditlibraryVerbCallback, stack)

                def run(frame):
                    data = frame.eventData
                    btnFrm = data[1][0]
                    dlgFrm = data[1][1]
                    verb = data[1][2]

                    #print("EditlibraryVerbCallback run: event data", frame.eventData)
                    #print("EditlibraryVerbCallback data=", frame.eventData, " index = ", frame.eventData[1][0])

                    # get the world position of the relative location of the dialog row the user clicked on
                    objOffset = -.5 + btnFrm.vars.position[0][2]
                    objPos = (2, -.5, objOffset)
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(dlgFrm.vars.dragObj[0]._path, objPos)
                    pos = point.getPos()
                    point.removeNode()

                    # open object editor as stand alone dialog
                    stk = []
                    edFrm = WyeUILib.EditVerb.start(stk)
                    edFrm.params.verb = [verb]
                    edFrm.params.parent = [None]
                    edFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    stk.append(edFrm)
                    edFrm.verb.run(edFrm)
                    WyeCore.World.startActiveFrame(edFrm)

            # Delete verb
            class DelLibVerbCallback:
                mode = Wye.mode.MULTI_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = (("count", Wye.dType.INTEGER, 0),)

                def start(stack):
                    #print("DelLibVerbCallback start")
                    return Wye.codeFrame(WyeUILib.EditMainDialog.EditLibCallback.DelLibVerbCallback, stack)

                def run(frame):
                    data = frame.eventData
                    #print("DelLibVerbCallback: data", data)
                    verb = data[1][0]
                    lib = verb.library

                    # make sure we have latest version
                    lib = WyeCore.World.libDict[lib.__name__]
                    match(frame.PC):
                        case 0:  # Delete library op
                            # delete verb ok?
                            #print("EditLibLineCallback: case 0: delete verb", verb.__name__, " from", lib.__name__)
                            delOkFrm = WyeCore.libs.WyeUIUtilsLib.doPopUpDialogAsync(frame, "Delete Verb",
                                               "Delete Verb " + verb.__name__ + "?", formatLst=[""])
                            frame.SP.append(delOkFrm)  # push dialog so it runs next cycle
                            frame.PC += 1   # on return from dialog, run del ok case


                        case 1: # return from Del Ok? dialog
                            delOkFrm = frame.SP.pop()
                            frame.status = Wye.status.SUCCESS
                            if delOkFrm.params.retVal[0] == Wye.status.SUCCESS:
                                #print("DelLibVerbCallback case 2: del verb", verb.__name__, " from ", lib.__name__)

                                # delete the verb
                                verbName = verb.__name__
                                delattr(lib, verbName)

                                # push updated lib back to system
                                WyeCore.World.libDict[lib.__name__] = lib
                                setattr(WyeCore.libs, lib.__name__, lib)

                                # if there's an edit dialog showing this library, refresh it
                                if lib.__name__ in WyeUILib.EditMainDialog.activeLibs:
                                    dlgFrm = WyeUILib.EditMainDialog.activeLibs[lib.__name__]
                                    dlgFrm.motherFrame.verb.update(dlgFrm.motherFrame, dlgFrm)
                            #else:
                            #    print("User cancelled delete verb")

            # Start verb
            class StartLibVerbCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = (("count", Wye.dType.INTEGER, 0),)

                def start(stack):
                    #print("StartLibVerbCallback start")
                    return Wye.codeFrame(WyeUILib.EditMainDialog.EditLibCallback.StartLibVerbCallback, stack)

                def run(frame):
                    data = frame.eventData
                    verb = data[1][0]

                    print("StartLibVerbCallback: start", verb.__name__)
                    WyeCore.World.startActiveObject(verb)


            # edit verb in lib
            # May create new verb in same or new lib
            class CreateVerbCallback:
                mode = Wye.mode.MULTI_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = (("verbName", Wye.dType.INTEGER, 0),)

                def start(stack):
                    #print("CreateVerbCallback start")
                    return Wye.codeFrame(WyeUILib.EditMainDialog.EditLibCallback.CreateVerbCallback, stack)

                def run(frame):
                    data = frame.eventData
                    #print("CreateVerbCallback data:", data)
                    btnFrm = data[1][0]
                    verbNmFrm = data[1][1]
                    dlgFrm = data[1][2]
                    lib = data[1][3]
                    editLibFrm = data[1][4]

                    editLibFrm = data[1][4]

                    match(frame.PC):
                        case 0:

                            # build a default verb
                            vertSettings = {
                                'mode': Wye.mode.MULTI_CYCLE,
                                'autoStart': True,
                                'dataType': Wye.dType.NONE
                            }

                            paramDescr = (("newParam", Wye.dType.ANY, Wye.access.REFERENCE),)

                            varDescr = (("newVar", Wye.dType.ANY, None),)

                            codeDescr = (("WyeLib.noop", ("Code", "0")),)

                            frame.vars.verbName[0] = verbNmFrm.vars.currVal[0].strip()

                            if not frame.vars.verbName[0]:
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Name Required", "Please enter a name for the new verb",
                                                    Wye.color.WARNING_COLOR)
                                frame.status = Wye.status.SUCCESS
                                return

                            if hasattr(lib, frame.vars.verbName[0]):
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Unique Name Required", "'"+frame.vars.verbName[0]+"' already in library. Please enter a unique name",
                                                    Wye.color.WARNING_COLOR)
                                frame.status = Wye.status.SUCCESS
                                return

                            WyeCore.Utils.createVerb(lib, frame.vars.verbName[0], vertSettings, paramDescr, varDescr, codeDescr)

                            verb = getattr(lib, frame.vars.verbName[0])

                            # open object editor
                            edFrm = WyeUILib.EditVerb.start(frame.SP)
                            edFrm.params.verb = [verb]
                            edFrm.params.parent = [dlgFrm]
                            edFrm.params.position = [(.5, -1.3, -.5 + btnFrm.vars.position[0][2]),]

                            frame.SP.append(edFrm)
                            frame.PC += 1

                        case 1:
                            edFrm = frame.SP.pop()  # remove dialog frame from stack
                            frame.status = Wye.status.SUCCESS  # done

                            # if we should throw out the verb created above
                            # a) user cancelled b) user changed verb name and created that c) user put verb in diff lib
                            if edFrm.params.retVal[0] != Wye.status.SUCCESS or \
                                edFrm.vars.nameFrm[0].vars.currVal[0] != verbNmFrm.vars.currVal[0] or \
                                    (edFrm.params.retLib[0] and (edFrm.params.retLib[0].__name__ != lib.__name__)):

                                # delete the verb created above from the lib
                                delattr(lib, frame.vars.verbName[0])

                            # on success, redisplay lib
                            if edFrm.params.retVal[0] == Wye.status.SUCCESS:
                                editLibFrm.verb.update(editLibFrm, dlgFrm)

                            #print("EditlibraryVerbCallback case 1: popped frame", edFrm.verb.__name__)




    # note: this is an instantiated class
    # class instance is called when user clicks on a graphic object that has a WyeID tag
    # fires up Wye's ObjEditor object with the given object to edit
    class ObjEditCtl(DirectObject):
        def __init__(self):
            self.currObj = None

        # User clicked on object.  If alt key down and it's editable, open the editor
        # note: all object frames must have a "position" variable with the object's position in it
        # for edit and debug dialog's to be positioned near
        def tagClicked(self, wyeID):
            status = False      # assume we won't use this tag
            #print("ObjEditCtl tagClicked", wyeID)
            # if ctl key, edit
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                frm = WyeCore.World.getRegisteredObj(wyeID)
                if frm:
                    #print("wyeID", wyeID, " Is registered")
                    #print("ObjEditCtl: Edit object", frm.verb.__name__)

                    # fire up object editor with given frame
                    #print("ObjEditorCtl: Create ObjEditor")
                    edFrm = WyeCore.World.startActiveObject(WyeUILib.EditVerb)
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,Wye.UI.DIALOG_OFFSET,0))
                    pos = point.getPos()
                    point.removeNode()
                    edFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    #edFrm.params.position = [(frm.vars.position[0][0], frm.vars.position[0][1], frm.vars.position[0][2]),]
                    edFrm.params.parent = [None]
                    #print("ObjEditorCtl: Fill in ObjEditor objFrm param")

                    # if this is one subframe of a parallel stream, edit the parent
                    if frm.verb is WyeCore.ParallelStream:
                        #print(frm.verb.__name__, " is parallel stream, get parent", frm.parentDlg.verb.__name__)
                        frm = frm.parentFrame
                    edFrm.params.verb = [frm.verb]

                    status = True     # tell caller we used the tag

            # if alt key down then debug
            elif base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt()):
                #print("ObjEditCtl tag Clicked: Alt held down, is wyeID registered?")
                frm = WyeCore.World.getRegisteredObj(wyeID)
                if not frm is None:
                    #print("wyeID", wyeID, " Is registered")
                    #print("ObjEditCtl: Edit object", frm.verb.__name__)

                    # set up object to be put on active list
                    #print("ObjEditorCtl: Create ObjDebugger")
                    stk = []            # create stack to run object on
                    dbgFrm = WyeUILib.ObjectDebugger.start(stk)  # start obj debugger and get its stack frame
                    dbgFrm.params.objFrm = [frm]  # object to debug
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0, Wye.UI.DIALOG_OFFSET, 0))
                    pos = point.getPos()
                    point.removeNode()
                    dbgFrm.params.position = [[pos[0], pos[1], pos[2]],]

                    # put object frame on active list
                    stk.append(dbgFrm)
                    dbgFrm.verb.run(dbgFrm)
                    WyeCore.World.startActiveFrame(dbgFrm)
                    #print("ObjEditorCtl: Fill in ObjEditor objFrm param")

                    status = True     # tell caller we used the tag

            # return status true if used tag, false if someone else can have it
            return status

    # put up object dialog for given object
    class EditVerb:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.INTEGER
        autoStart = False
        paramDescr = (("retVal", Wye.dType.INTEGER, Wye.access.REFERENCE, Wye.status.FAIL), # if doesn't get replaced, is fail
                      ("verb", Wye.dType.OBJECT, Wye.access.REFERENCE),     # library verb to edit
                      ("parent", Wye.dType.OBJECT, Wye.access.REFERENCE),   # parent dialog, if any
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE),  # object frame to edit
                      ("retLib", Wye.dType.OBJECT, Wye.access.REFERENCE, None))
        varDescr = (("paramInpLst", Wye.dType.OBJECT_LIST, None),   # Inputs showing params
                    ("varInpLst", Wye.dType.OBJECT_LIST, None),     # Inputs showing vars
                    ("oldVerb", Wye.dType.OBJECT, None),            # verb used as a source
                    ("nameFrm", Wye.dType.OBJECT, None),            # new verb name
                    ("existingLibFrm", Wye.dType.OBJECT, None),     # existing lib name input
                    ("disaAutoFrm", Wye.dType.OBJECT, None),        # disable auto for testing (updates running object instead of create new)
                    ("listCodeFrm", Wye.dType.OBJECT, None),        # new lib name input, if user wants to create one
                    ("settingsFrms", Wye.dType.OBJECT_LIST, None),  # new verb settings
                    ("newVerbSettings", Wye.dType.OBJECT, None),    # verb used as a source
                    ("newParamDescr", Wye.dType.OBJECT_LIST, None), # Build new verb params here
                    ("newVarDescr", Wye.dType.OBJECT_LIST, None),   # Build new verb vars here
                    ("newCodeDescr", Wye.dType.OBJECT_LIST, None),  # Build new verb code here
                    ("fileName", Wye.dType.STRING, "MyWyeLib.py"),             # file name to save to
                    )

        # global list of frames being edited
        activeVerbs = {}

        modParamOpList = [
            "Move Line Up",
            "Add Line Before",
            "Copy This Line",
            "Cut This Line",
            "Paste Parameter Before",
            "Delete This Line",
            "Add Line After",
            "Move Line Down",
        ]

        modVarOpList = [
            "Move Line Up",
            "Add Line Before",
            "Copy This Line",
            "Cut This Line",
            "Paste Variable Before",
            "Delete This Line",
            "Add Line After",
            "Move Line Down",
        ]

        modCodeOpList = [
            "Move This Code Up",
            "Add Line Before",
            "Copy This",
            "Cut This",
            "Paste Code Before",
            "Delete This",
            "Add Line After",
            "Move This Code Down",
        ]

        modStreamOpList = [
            "Move Stream Up",
            "Add New Stream Before",
            "Copy This Stream",
            "Cut This Stream",
            "Paste Stream Before",
            "Delete This Stream",
            "Add New Stream After",
            "Move Stream Down",
        ]

        # Note: order MUST BE SAME as order in EditCodeCallback
        opList = [
            "Verb",
            "Var=",
            "Par=",
            "Const",
            "Var",
            "Expr",
            "Code",
            "CodeBlock",
            "Label",
            "GoTo",
            "IfGoTo"
        ]

        eqList = ["=", "+=", "-="]  # for =, +=, -=

        def start(stack):
            #print("EditVerb start")
            f = Wye.codeFrame(WyeUILib.EditVerb, stack)
            # fill in local copies of lists
            f.vars.paramInpLst[0] = []
            f.vars.varInpLst[0] = []
            f.vars.newParamDescr[0] = []
            f.vars.newVarDescr[0] = []
            f.vars.newCodeDescr[0] = []
            f.vars.newVerbSettings[0] = {
                'mode': Wye.mode.SINGLE_CYCLE,
                'cType': Wye.cType.VERB,
                'parTermType': Wye.parTermType.FIRST_FAIL,
                'autoStart': False,
                'dataType': Wye.dType.NONE,
            }
            f.vars.settingsFrms[0] = {}
            return f

        def run(frame):
            verb = frame.params.verb[0]  # shorthand
            # re-get verb from lib in case it's been updated
            libName = verb.library.__name__
            verbName = verb.__name__
            lib = WyeCore.World.libDict[libName]
            if lib != verb.library:
                print("EditVerb lib", lib.__name__, " has been updated.  Using most recent")
            verb = getattr(lib, verbName)
            if verb != frame.params.verb[0]:
                print("EditVerb verb", verbName, " has been updated. using most recent")
                frame.params.verb[0] = verb
            match(frame.PC):
                case 0:
                    #print("EditVerb run case 0: edit", verb.__name__)

                    # only edit frame once
                    if verb in WyeUILib.EditVerb.activeVerbs:
                        #print("Already editing this library", verb.library.__name__, " verb", verb.__name__)
                        # take self off active object list
                        WyeCore.World.stopActiveObject(frame)

                        # bring lib in front of user
                        frm = WyeUILib.EditVerb.activeVerbs[verb]
                        frm.vars.dragObj[0].setPos(base.camera, 0, Wye.UI.DIALOG_OFFSET, 0)
                        frm.vars.dragObj[0].setHpr(base.camera, 0, 1, 0)

                        frame.status = Wye.status.FAIL
                        return

                    if not hasattr(verb, "codeDescr"):
                        #print("Cannot edit hard-coded verb")
                        # take self off active object list
                        WyeCore.World.stopActiveObject(frame)
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Editable", "Cannot edit hard-coded verb", Wye.color.WARNING_COLOR)

                    frame.vars.oldVerb[0] = verb

                    # copy verb's data into work spaces
                    if hasattr(verb, 'mode'):
                        frame.vars.newVerbSettings[0]['mode'] = verb.mode
                    if hasattr(verb, 'cType'):
                        frame.vars.newVerbSettings[0]['cType'] = verb.cType
                    if hasattr(verb, 'parTermType'):
                        frame.vars.newVerbSettings[0]['parTermType'] = verb.parTermType
                    if hasattr(verb, 'autoStart'):
                        frame.vars.newVerbSettings[0]['autoStart'] = verb.autoStart
                    if hasattr(verb, 'dataType'):
                        frame.vars.newVerbSettings[0]['dataType'] = verb.dataType

                    # copy all the descrs from immutable tuples to mutable lists
                    for param in verb.paramDescr:
                        newP = []
                        frame.vars.newParamDescr[0].append(newP)
                        for p in param:
                            newP.append(p)

                    for var in verb.varDescr:
                        newV = []
                        frame.vars.newVarDescr[0].append(newV)
                        for v in var:
                            newV.append(v)

                    frame.vars.newCodeDescr[0] = Wye.listCopy(verb.codeDescr)

                    #print("newParamDescr", frame.vars.newParamDescr)
                    #print("newVarDescr", frame.vars.newVarDescr)

                    # create object dialog
                    # print("Edit ", verb.__name__)

                    # build dialog
                    dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog("Edit '" + verb.__name__ + "'", frame.params.parent[0], (frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2]))
                    # object name

                    verbNameFrm = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "  Name:", [verb.__name__])
                    frame.vars.nameFrm[0] = verbNameFrm

                    # Choose from existing Library list
                    libList = [lib.__name__ for lib in WyeCore.World.libList]
                    libFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "    Update/Add to Library", [libList],
                                     [libList.index(verb.library.__name__)], layout=Wye.layout.ADD_RIGHT)
                    frame.vars.existingLibFrm[0] = libFrm

                    # save to library
                    saveCodeFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Write to library", WyeUILib.EditVerb.EditCodeSaveLibCallback)
                    saveCodeFrm.params.optData = [(saveCodeFrm, dlgFrm, frame)]

                    saveCodeFileFrm = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "    Library File Name", frame.vars.fileName,
                                WyeUILib.EditVerb.EditCodeSaveLibNameCallback, layout=Wye.layout.ADD_RIGHT)
                    saveCodeFileFrm.params.optData = [(saveCodeFileFrm, dlgFrm, frame)]

                    # edit library
                    # NOTE: WE ARE CALLING EditMainDialog's CALLBACK, THIS IS RISKY!!!!
                    editLibFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Open Library "+verb.library.__name__, WyeUILib.EditMainDialog.EditLibCallback)
                    editLibFrm.params.optData = [(editLibFrm, dlgFrm, verb.library)]


                    # Test edited code
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Test:", color=Wye.color.SUBHD_COLOR)

                    tstBtnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Check Code", WyeUILib.EditVerb.TestCodeCallback)
                    tstBtnFrm.params.optData = [(tstBtnFrm, dlgFrm, frame)]  # button row, dialog frame

                    # if want to see code
                    lstCodeFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "   Display Code", [False], layout=Wye.layout.ADD_RIGHT)
                    frame.vars.listCodeFrm[0] = lstCodeFrm

                    updBtnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Update Verb", WyeUILib.EditVerb.UpdateCodeCallback)
                    updBtnFrm.params.optData = [(updBtnFrm, dlgFrm, frame)]  # button row, dialog frame


                    # settings
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Settings:", color=Wye.color.SUBHD_COLOR)

                    modeNames = [Wye.mode.stringLookup[val] for val in Wye.mode.valList]
                    modeFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  Mode", [modeNames], [Wye.mode.valList.index(frame.vars.newVerbSettings[0]['mode'])])
                    frame.vars.settingsFrms[0]['mode'] = modeFrm

                    autoFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  Auto Start", [frame.vars.newVerbSettings[0]['autoStart']])
                    frame.vars.settingsFrms[0]['autoStart'] = autoFrm

                    disaAutoFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  disable for testing", [False], layout=Wye.layout.ADD_RIGHT)
                    frame.vars.disaAutoFrm[0] = disaAutoFrm

                    dTypeNames = [Wye.dType.stringLookup[val] for val in Wye.dType.valList]
                    selectionIx = Wye.dType.valList.index(frame.vars.newVerbSettings[0]['dataType'])
                    dTypeFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  Data Type", [dTypeNames], [selectionIx])
                    frame.vars.settingsFrms[0]['dataType'] = dTypeFrm

                    cTypeNames = [Wye.cType.stringLookup[val] for val in Wye.cType.valList]
                    cTypeFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  Object Type", [cTypeNames],
                                                     [Wye.cType.valList.index(frame.vars.newVerbSettings[0]['cType'])])
                    frame.vars.settingsFrms[0]['cType'] = cTypeFrm

                    pTypeNames = [Wye.parTermType.stringLookup[val] for val in Wye.parTermType.valList]
                    parTermTypeFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  Parallel Exec Termination", [pTypeNames],
                                                    [Wye.parTermType.valList.index(frame.vars.newVerbSettings[0]['parTermType'])])
                    frame.vars.settingsFrms[0]['parTermType'] = parTermTypeFrm


                    # params
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Parameters:", color=Wye.color.SUBHD_COLOR)

                    if len(verb.paramDescr) > 0:     # if we have params, list them
                        attrIx = 0

                        for param in frame.vars.newParamDescr[0]:
                            # make the dialog row
                            editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [WyeUILib.EditVerb.modParamOpList], [0],
                                                              WyeUILib.EditVerb.EditParamLineCallback, showText=False)
                            label = "'"+param[0] + "' "+Wye.dType.tostring(param[1]) + " call by:"+Wye.access.tostring(param[2])
                            if len(param) > 3:
                                label += " default:"+param[3]
                            btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, label, WyeUILib.EditVerb.EditParamCallback, layout=Wye.layout.ADD_RIGHT)
                            btnFrm.params.optData = [(btnFrm, dlgFrm, frame, editLnFrm, param)]  # button row, dialog frame

                            editLnFrm.params.optData = [(editLnFrm, dlgFrm, frame, btnFrm, param)]

                            attrIx += 1

                    # else no params to edit
                    else:
                        # todo fix this so it will work
                        editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  +/-")
                        #editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [WyeUILib.EditVerb.modOpLst], [0], WyeUILib.EditVerb.EditParamLineCallback, showText=False)
                        lblFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  todo <no parameters>", layout=Wye.layout.ADD_RIGHT)
                        editLnFrm.params.optData = [(editLnFrm, dlgFrm, lblFrm, None)]

                    # vars
                    lblFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Variables:"]
                    lblFrm.params.color = [Wye.color.SUBHD_COLOR]
                    WyeUILib.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if len(frame.vars.newVarDescr[0]) > 0:
                        attrIx = 0

                        for var in frame.vars.newVarDescr[0]:
                            # make the dialog row
                            editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [WyeUILib.EditVerb.modVarOpList], [0],
                                                              WyeUILib.EditVerb.EditVarLineCallback, showText=False)

                            label = "'"+var[0] + "' "+Wye.dType.tostring(var[1]) + " = "+str(var[2])
                            btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, label, WyeUILib.EditVerb.EditVarCallback, layout=Wye.layout.ADD_RIGHT)
                            btnFrm.params.optData = [(btnFrm, dlgFrm, frame, editLnFrm, var)]  # button row, dialog frame

                            editLnFrm.params.optData = [(editLnFrm, dlgFrm, frame, btnFrm, var)]

                            attrIx += 1

                    # else no vars to edit
                    else:
                        WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  <no variables>")


                    # code
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Wye Code:", color=Wye.color.SUBHD_COLOR)

                    if hasattr(verb, "codeDescr"):
                        if len(verb.codeDescr) > 0:
                            # If it's parallel code blocks
                            if verb.mode == Wye.mode.PARALLEL:
                                rowLst = []  # add rows here
                                for streamTuple in frame.vars.newCodeDescr[0]:
                                    WyeUILib.EditVerb.bldStreamCodeLine(streamTuple, frame, dlgFrm, rowLst)

                                dlgFrm.params.inputs[0].extend(rowLst)
                                #print("Stream added", len(rowLst), " rows to dialog")

                            # regular boring normal single stream code
                            else:
                                level = 0       # starting indent for nesting tuple data
                                rowLst = []     # build rows here
                                for tuple in frame.vars.newCodeDescr[0]:
                                    WyeUILib.EditVerb.bldEditCodeLine(tuple, level, frame, dlgFrm, rowLst)
                                dlgFrm.params.inputs[0].extend(rowLst)
                                #print("added", len(rowLst), " rows to dialog")

                        # no code, put <add code here>
                        # todo handle this on OK exit!!!!
                        else:
                            # line edit button
                            editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  +/-")

                            lblFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  todo <add code here>", layout=Wye.layout.ADD_RIGHT)

                            editLnFrm.params.optData = [(editLnFrm, dlgFrm, frame, None, lblFrm, 0)]  # button row, dialog frame
                            editLnFrm.verb.run(editLnFrm)

                    # no code to edit
                    else:
                        WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  <no editable code>")


                    # mark this frame actively being edited
                    WyeUILib.EditVerb.activeVerbs[verb] = dlgFrm

                    # WyeUILib.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = dlgFrm.status
                    WyeUILib.EditVerb.activeVerbs.pop(verb)
                    #print("ObjEditor: returned status", frame.vars.dlgStat[0])  # Wye.status.tostring(frame.))

                    # pass dlg status back to our caller
                    frame.params.retVal = dlgFrm.params.retVal

                    # if success, update verb
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        frame.verb.updateVerb(frame, dlgFrm)


        # build and save the verb to the library
        def updateVerb(frame, dlgFrm):
            modeFrm = frame.vars.settingsFrms[0]['mode']
            modeIx = modeFrm.params.selectionIx[0]
            if modeIx >= 0:
                mode = Wye.mode.valList[modeIx]
            else:
                mode = frame.vars.newVerbSettings[0]['mode']
            frame.vars.newVerbSettings[0]['mode'] = mode

            autoFrm = frame.vars.settingsFrms[0]['autoStart']
            autoStart = autoFrm.params.value[0]
            frame.vars.newVerbSettings[0]['autoStart'] = autoStart

            dTypeFrm = frame.vars.settingsFrms[0]['dataType']
            dTypeIx = dTypeFrm.params.selectionIx[0]
            dataType = Wye.dType.valList[dTypeIx]
            frame.vars.newVerbSettings[0]['dataType'] = dataType

            # get verb name
            name = frame.vars.nameFrm[0].params.value[0]
            if name:
                name = name.strip()
            if not name:
                name = "TestVerb"

            # find library
            libList = [lib for lib in WyeCore.World.libList]
            lib = libList[frame.vars.existingLibFrm[0].params.selectionIx[0]]

            frame.params.retLib[0] = lib  # tell caller where verb went

            disableAuto = frame.vars.disaAutoFrm[0].params.value[0]

            WyeCore.Utils.createVerb(lib, name,
                                     frame.vars.newVerbSettings[0],
                                     frame.vars.newParamDescr[0],
                                     frame.vars.newVarDescr[0],
                                     frame.vars.newCodeDescr[0], False, False, not disableAuto)

            # push updated lib back to system
            WyeCore.World.libDict[lib.__name__] = lib
            setattr(WyeCore.libs, lib.__name__, lib)

            # if there's an edit dialog showing this library, refresh it
            if lib.__name__ in WyeUILib.EditMainDialog.activeLibs:
                dlgFrm = WyeUILib.EditMainDialog.activeLibs[lib.__name__]
                dlgFrm.motherFrame.verb.update(dlgFrm.motherFrame, dlgFrm)



        # build a parallel stream code entry
        # stream header plus recursively displayed code
        def bldStreamCodeLine(streamTuple, frame, dlgFrm, rowLst):

            level = 0  # start at left, no indent

            # line edit dropdown
            #print("bldStreamCodeLine: Build stream", streamTuple[0])
            editLnFrm = WyeUILib.InputDropdown.start(dlgFrm.SP)
            editLnFrm.params.frame = [None]
            editLnFrm.params.parent = [None]
            editLnFrm.params.showText = [False]
            editLnFrm.params.label = ["  +/-"]
            editLnFrm.params.list = [WyeUILib.EditVerb.modStreamOpList]
            editLnFrm.params.callback = [WyeUILib.EditVerb.EditStreamLineCallback]  # button callback
            editLnFrm.params.selectionIx = [0]
            editLnFrm.verb.run(editLnFrm)
            rowLst.append([editLnFrm])
            #print("bldStreamCodeLine create modCode button", editLnFrm.params.label)

            # convert level number into indent space
            indent = "".join(["   " for l in range(level)])      # indent by recursion depth

            # code button
            btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
            rowLst.append([btnFrm])
            btnFrm.params.layout = [Wye.layout.ADD_RIGHT]       # put after the line edit button
            btnFrm.params.frame = [None]
            btnFrm.params.parent = [None]
            btnFrm.params.label = ["Stream: " + str(streamTuple[0])]
            btnFrm.params.callback = [WyeUILib.EditVerb.EditStreamCallback]  # button callback

            # fill in opt data including ptr to these ctls
            editLnFrm.params.optData = [(editLnFrm, dlgFrm, frame, streamTuple, btnFrm, level)]  # button frame, dialog frame
            btnFrm.params.optData = [(btnFrm, dlgFrm, frame, streamTuple, level, editLnFrm)]  # button frame, dialog frame

            # build code rows for stream
            for tuple in streamTuple[1]:
                level = 1  # starting indent for nesting tuple data
                WyeUILib.EditVerb.bldEditCodeLine(tuple, level, frame, dlgFrm, rowLst)


        # recursively build dialog code rows
        # level is the recursion level
        # verb is the verb being edited
        # return the results in rowLst so this can be used by both Dialog and EditLineCallback
        def bldEditCodeLine(tuple, level, editVerbFrm, dlgFrm, rowLst, prefix=""):
            #print("level", level, " indent '"+indent+"' tuple", tuple)

            # note: can't use utility rtns to build inputs 'cause they are added to rowList, not dlgFrm

            # line edit dropdown
            editLnFrm = WyeUILib.InputDropdown.start(dlgFrm.SP)
            editLnFrm.params.frame = [None]
            editLnFrm.params.parent = [None]
            editLnFrm.params.showText = [False]
            editLnFrm.params.label = ["  +/-"]
            editLnFrm.params.list = [WyeUILib.EditVerb.modCodeOpList]
            editLnFrm.params.callback = [WyeUILib.EditVerb.EditCodeLineCallback]  # button callback
            editLnFrm.params.selectionIx = [0]
            editLnFrm.verb.run(editLnFrm)
            rowLst.append([editLnFrm])
            #print("bldEditCodeLine create modCode button", editLnFrm.params.label)

            # convert level number into indent space
            indent = "".join(["   " for l in range(level)])      # indent by recursion depth

            # code button
            btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
            rowLst.append([btnFrm])
            btnFrm.params.layout = [Wye.layout.ADD_RIGHT]       # put after the line edit button
            btnFrm.params.frame = [None]
            btnFrm.params.parent = [None]
            btnFrm.params.callback = [WyeUILib.EditVerb.EditCodeCallback]  # button callback

            # fill in editLnFrm opt data including ptr to code button
            editLnFrm.params.optData = [(editLnFrm, dlgFrm, editVerbFrm, tuple, btnFrm, level)]  # button frame, dialog frame


            # fill in text and callback based on code row type

            # if lib.verb
            if not tuple[0] is None and "." in tuple[0]:
                op = "Verb"  # which code operator does the line currently have
                vStr = str(tuple[0])
                if vStr.startswith("WyeCore.libs."):        # trim off the prefix
                    vStr = vStr[13:]
                # parse out the lib and verb names
                libStr,verbStr = vStr.split(".")
                lib = WyeCore.World.libDict[libStr]
                # find the actual verb from the lib
                verb = getattr(lib, verbStr)
                btnFrm.params.label = [indent + prefix + "Verb: " + vStr]

                # display verb's params (if any)
                if len(tuple) > 1:
                    paramIx = 0
                    for paramTuple in tuple[1:]:
                        prefix = "(param:" + verb.paramDescr[paramIx][0] + ") "
                        WyeUILib.EditVerb.bldEditCodeLine(paramTuple, level + 1, editVerbFrm, dlgFrm, rowLst, prefix)
                        if verb.paramDescr[paramIx][1] != Wye.dType.VARIABLE:
                            paramIx += 1
            # else Code, etc.
            else:
                match tuple[0]:
                    case "Code" | None:  # raw Python
                        btnFrm.params.label = [indent + prefix + "Code: " + str(tuple[1])]
                        op = "Code"
                    case "CodeBlock":  # multi-line raw Python
                        btnFrm.params.label = [indent + prefix + "CodeBLock: " + str(tuple[1])]
                        op = "CodeBlock"
                    case "Expr":
                        btnFrm.params.label = [indent + prefix + "Expression: " + str(tuple[1])]
                        op = "Expr"
                    case "Const":
                        btnFrm.params.label = [indent + prefix + "Constant: " + str(tuple[1])]
                        op = "Const"
                    case "Var":
                        btnFrm.params.label = [indent + prefix + "Variable: " + str(tuple[1])]
                        op = "Var"
                    case "Var=":
                        btnFrm.params.label = [indent + prefix + "Variable=: " + str(tuple[1])]
                        op = "Var="
                    case "Par=":
                        btnFrm.params.label = [indent + prefix + "Parameter=: " + str(tuple[1])]
                        op = "Par="
                    case "GoTo":
                        btnFrm.params.label = [indent + prefix + "GoTo: " + str(tuple[1])]
                        op = "GoTo"
                    case "Label":
                        op = "Label"
                        btnFrm.params.label = [indent + prefix + "Label: " + str(tuple[1])]
                    case "IfGoTo":
                        op = "IfGoTO"
                        btnFrm.params.label = [indent + prefix + "If: " + str(tuple[1]) + " GoTo: " + str(tuple[2])]

            btnFrm.params.optData = [(btnFrm, dlgFrm, editVerbFrm, tuple, level, editLnFrm, op)]  # button frame, dialog frame

        # single-row insert into paramDescr/varDescr and add row to dialog
        def insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, currDesc, descrList, label, prefixCallback, rowCallback, newData, insertBefore, isParam=True):
            # print("insertParamOrVar: Add up")

            # find index to this row's param in EditVerb's newParamDescr
            dIx = descrList.index(currDesc)
            if dIx < 0:
                print("insertParamOrVar ERROR: Failed to find", currDesc, " in ", descrList)
                return

            # create new dialog row for this param

            # find index to dialog row to insert before/after
            rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
            # Debug: if the unthinkable happens, give us a hint
            if rIx < 0:
                print("insertParamOrVar ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ", editLnFrm.params.label[0], " not in input list")
                return

            # build dialog row
            # Note: have to do it out by hand 'cause helper rtns add to end of input list and we need to insert in middle
            newEdLnFrm = WyeUILib.InputDropdown.start(parentFrm.SP)
            newEdLnFrm.params.frame = [None]
            newEdLnFrm.params.parent = [None]
            newEdLnFrm.params.label = ["  +/-"]
            if isParam:
                newEdLnFrm.params.list = [WyeUILib.EditVerb.modParamOpList]
            else:
                newEdLnFrm.params.list = [WyeUILib.EditVerb.modVarOpList]
            newEdLnFrm.params.showText = [False]
            newEdLnFrm.params.callback = [prefixCallback]
            # callback data below, after create param button
            newEdLnFrm.params.selectionIx = [0]
            newEdLnFrm.verb.run(newEdLnFrm)

            newBtnFrm = WyeUILib.InputButton.start(parentFrm.SP)
            newBtnFrm.params.layout = [Wye.layout.ADD_RIGHT]  # put after the line edit button
            newBtnFrm.params.frame = [None]
            newBtnFrm.params.parent = [None]
            newBtnFrm.params.label = [label]
            newBtnFrm.params.callback = [rowCallback]  # button callback
            newBtnFrm.params.optData = [(newBtnFrm, parentFrm, editVerbFrm, newEdLnFrm, newData)]  # button row, dialog frame
            newBtnFrm.verb.run(newBtnFrm)

            # now we can fill in the editline opt data with the new button frame
            newEdLnFrm.params.optData = [(newEdLnFrm, parentFrm, editVerbFrm, newBtnFrm, newData)]

            # print("params before insert", WyeCore.Utils.listToTupleString(editVerbFrm.vars.newParamDescr, 0))

            # Insert placeholder param after the current param
            if insertBefore:
                descrList.insert(dIx, newData)
            else:
                descrList.insert(dIx+1, newData)


            #for desc in descrList:
            #    print("  ", desc)

            # print("params after insert", WyeCore.Utils.listToTupleString(editVerbFrm.vars.newParamDescr, 0))

            # DEBUG
            # print("Before Insert")
            # for ii in range(rIx - 1, rIx + 6):
            #    print("  ", ii, " ", parentFrm.params.inputs[0][ii][0].params.label[0])

            # insert new dialog rows into dialog
            if insertBefore:
                parentFrm.params.inputs[0].insert(rIx, [newEdLnFrm])
                parentFrm.params.inputs[0].insert(rIx + 1, [newBtnFrm])
            else:
                parentFrm.params.inputs[0].insert(rIx + 2, [newEdLnFrm])
                parentFrm.params.inputs[0].insert(rIx + 3, [newBtnFrm])

            # DEBUG
            # print("After Insert")
            # for ii in range(rIx - 1, rIx + 6):
            #    print("  ", ii, " ", parentFrm.params.inputs[0][ii][0].params.label[0])

            # display new dialog rows (don't sweat the position, they will be correctly
            # placed by dialog redisplay, below)
            pos = [0, 0, 0]
            newEdLnFrm.verb.display(newEdLnFrm, parentFrm, pos)
            newBtnFrm.verb.display(newBtnFrm, parentFrm, pos)

            # update position of all Dialog fields
            parentFrm.verb.redisplay(parentFrm)

        ######################
        # VerbEditor Callback classes
        # Callback gets passed eventData = (buttonTag, optUserData, buttonFrm)
        ######################

        # Modify lib.verb
        class EditVerbCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            autoStart = False
            paramDescr = (("verb", Wye.dType.OBJECT, Wye.access.REFERENCE),)  # object frame to edit
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),  # object dialog frame
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        ("libName", Wye.dType.STRING, ""),
                        ("libNames", Wye.dType.STRING_LIST, []),
                        ("verbName", Wye.dType.STRING, ""),
                        ("verbNames", Wye.dType.STRING_LIST, []),
                        ("prefix", Wye.dType.STRING, ""),
                        )

            # global list of frames being edited
            activeVerbs = {}

            tempLib = None      # lib holding new version of verb

            noneSelected = "<none selected>"

            def start(stack):
                return Wye.codeFrame(WyeUILib.EditVerb.EditVerbCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("EditVerbCallback data='" + str(data) + "'")
                btnFrm = data[1][0]
                parentDlg = data[1][1]
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                level = data[1][4]

                match (frame.PC):
                    case 0:
                        # if there is a prefix, save it
                        labelStr = btnFrm.params.label[0].strip()
                        if labelStr[0] == "(":      # if there's a prefix
                            endPrefIx = labelStr.find(")")
                            frame.vars.prefix[0] = labelStr[:endPrefIx+2]

                        # build verb select/edit dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.position = [(.5, -.5, -.5 + btnFrm.vars.position[0][2]),]
                        dlgFrm.params.parent = [parentDlg]
                        dlgFrm.params.title = ["Select Library and Verb"]

                        WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Op:", [WyeUILib.EditVerb.opList], [0])

                        # split verb into lib, verb dropowns

                        # build lib list for dropdown
                        libName, verbName = btnFrm.params.label[0].split(".")
                        libName = libName.split(":")[1].strip()
                        verbName = verbName.strip()
                        frame.vars.libName[0] = libName

                        #print("lib", libName, " verb", verbName, " from ", btnFrm.params.label[0])

                        # do this here so can ref it in lib callback data
                        verbFrm = WyeUILib.InputDropdown.start(dlgFrm.SP)


                        libFrm = WyeUILib.InputDropdown.start(dlgFrm.SP)
                        libFrm.params.frame = [None]
                        libFrm.params.parent = [None]
                        libFrm.params.label = ["Library"]
                        frame.vars.libNames[0] = [lib.__name__ for lib in WyeCore.World.libList]
                        frame.vars.libName[0] = libName
                        libFrm.params.list = frame.vars.libNames
                        libFrm.params.selectionIx = [frame.vars.libNames[0].index(libName)]
                        libFrm.params.callback = [WyeUILib.EditVerb.EditCodeCallback.EditCodeOpCallback]
                        libFrm.params.optData = [(libFrm, dlgFrm, editVerbFrm, frame.vars.libName, verbFrm),]
                        libFrm.verb.run(libFrm)
                        dlgFrm.params.inputs[0].append([libFrm])


                        # build verb list for 2nd dropdown

                        frame.vars.verbNames[0] = frame.verb.buildVerbList(libName)

                        # fill in rest of verb drop down
                        verbFrm.params.frame = [None]
                        btnFrm.params.parent = [None]
                        verbFrm.params.label = ["Verb"]
                        verbFrm.params.list = frame.vars.verbNames
                        frame.vars.verbName[0] = verbName
                        #print("find verName", verbName, " in ", frame.vars.verbNames)
                        try:
                            verbFrm.params.selectionIx = [frame.vars.verbNames[0].index(verbName)]
                        except:
                            # todo - figure out how to flag that this is not a good value
                            print("ERROR invalid verbName", verbName, " not found in library", libName)
                            verbFrm.params.selectionIx = [0]
                        verbFrm.params.callback = [WyeUILib.EditVerb.EditVerbCallback.SelectVerbCallback]
                        verbFrm.params.optData = [(verbFrm, dlgFrm, editVerbFrm, frame.vars.verbName),]
                        verbFrm.verb.run(verbFrm)
                        dlgFrm.params.inputs[0].append([verbFrm])


                        frame.SP.append(dlgFrm)
                        # (if change lib, then have to rebuild verb dropdown)

                        frame.PC += 1
                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = dlgFrm.status
                        if frame.vars.dlgStat[0] == Wye.status.SUCCESS:
                            # print("EditVerbCallback done, success, set row label to", dlgFrm.vars.currInp[0])
                            if frame.vars.verbName[0] == WyeUILib.EditVerb.EditVerbCallback.noneSelected:
                                print("no valid verb")

                            # get old values in case we need them for fallback
                            oldLib, oldVerb = btnFrm.params.label[0].split(".")
                            oldLib = oldLib.split(":")[1].strip()
                            oldVerb = oldVerb.strip()

                            libFrm = dlgFrm.params.inputs[0][-2][0]
                            if libFrm.params.selectionIx[0] >= 0:
                                newLib = libFrm.params.list[0][libFrm.params.selectionIx[0]]
                            else:
                                newLib = oldLib

                            vrbFrm = dlgFrm.params.inputs[0][-1][0]
                            #print("vrbFrm ix", vrbFrm.params.selectionIx[0], " in list", vrbFrm.params.list[0])
                            if vrbFrm.params.selectionIx[0] >= 0:
                                newVerb = vrbFrm.vars.list[0][vrbFrm.params.selectionIx[0]]
                            else:
                                # fall back to original value - this will be bad if library changed
                                # todo - figure out how to flag user that this is invalid
                                newVerb = oldVerb

                            #print("EditVerbCallback done: newOp", newLib, "newTxt", newVerb)
                            # save back to code
                            tuple[0] = newLib + "." + newVerb


                            # update display
                            prefix = frame.vars.prefix[0]
                            indent = "".join(["   " for l in range(level)])  # indent by recursion depth
                            btnFrm.verb.setLabel(btnFrm, indent + prefix + "Verb: " + str(tuple[0]))


            # given the name of a library, get the list of verb names in the library
            def buildVerbList(libName):
                #print("libName", libName)
                verbLst = []
                lib = WyeCore.World.libDict[libName]
                for attr in dir(lib):
                    if attr != "__class__":
                        libVerb = getattr(lib, attr)
                        if inspect.isclass(libVerb):
                            verbLst.append(libVerb.__name__)
                return verbLst

            class SelectLibCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = ()

                def start(stack):
                    #print("SelectLibCallback started")
                    return Wye.codeFrame(WyeUILib.EditVerb.EditVerbCallback.SelectLibCallback, stack)

                def run(frame):
                    data = frame.eventData
                    print("SelectLibCallback data", data)
                    btnFrm = data[1][0]
                    parentDlg = data[1][1]
                    editVerbFrm = data[1][2]
                    libNameLst = data[1][3]
                    verbFrm = data[1][4]

                    # if lib changed, invalidate verb dropdown
                    newLib = btnFrm.vars.list[0][btnFrm.params.selectionIx[0]]
                    #print("SelectLibCallback old lib", libNameLst[0], " new lib", newLib)
                    if libNameLst[0] != newLib:
                        libNameLst[0] = newLib
                        verbLst = WyeUILib.EditVerb.EditVerbCallback.buildVerbList(libNameLst[0])
                        verbLst.append(WyeUILib.EditVerb.EditVerbCallback.noneSelected)
                        verbFrm.verb.setList(verbFrm,verbLst, len(verbLst)-1)

                        # jam <none selected> into current verb"
                        # todo - using dropdown value is uggly - better to just use the index everywhere
                        verbFrm.params.optData[0][3][0] = verbFrm.vars.list[0][len(verbLst)-1]


            class SelectVerbCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = ()

                def start(stack):
                    #print("SelectVerbCallback started")
                    return Wye.codeFrame(WyeUILib.EditVerb.EditVerbCallback.SelectVerbCallback, stack)

                def run(frame):
                    data = frame.eventData
                    btnFrm = data[1][0]
                    parentDlg = data[1][1]
                    editVerbFrm = data[1][2]
                    verbNameLst = data[1][3]

                    #print("SelectVerbCallback data='" + str(frame.eventData) + "'")
                    newVerb = btnFrm.vars.list[0][btnFrm.params.selectionIx[0]]
                    #print("SelectVerbCallback old verb", verbNameLst[0], " new verb", newVerb)
                    verbNameLst[0] = newVerb

        # add/move/remove parameter
        class EditParamLineCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                # print("EditParamLineCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditParamLineCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditParamLineCallback data", data)
                editLnFrm = data[1][0]  # add/del/copy button frame
                parentFrm = data[1][1]  # parent dialog
                editVerbFrm = data[1][2] # EditVerb frame
                btnFrm = data[1][3]     # param line
                param = data[1][4]      # the param we're messing with

                # get selectionIx
                opIx = editLnFrm.params.selectionIx[0]

                #print("EditParamLineCallback: operator ix", opIx, " paramDescr", param)

                newData = ["newParam", Wye.dType.ANY, Wye.access.REFERENCE]  # placeholder param to insert

                # "0 Move line up",
                # "1 Add line before",
                # "2 Copy line",
                # "3 Delete Line",
                # "4 Add line after",
                # "5 Move line down",
                match (opIx):
                    # move line up
                    case 0:
                        # .index(param) not working, dunno why
                        # dIx = editVerbFrm.vars.newParamDescr[0].index(param)
                        dIx = -1
                        for p in editVerbFrm.vars.newParamDescr[0]:
                            dIx += 1
                            if p==param:
                                break;
                        if dIx < 0:
                            print("EditParamLineCallback ERROR: param not found in paramDescr")
                            return

                        if dIx == 0:
                            #print("EditParamLineCallback Warning: line already at top")
                            return

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditParamLineCallback op", WyeUILib.EditVerb.opList[opIx], " ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return

                        # move code descr
                        descr = editVerbFrm.vars.newParamDescr[0].pop(dIx)
                        editVerbFrm.vars.newParamDescr[0].insert(dIx-1, descr)

                        # move dialog row (2 inputs)
                        edLnRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx-2, edLnRef)
                        pRef = parentFrm.params.inputs[0].pop(rIx+1)
                        parentFrm.params.inputs[0].insert(rIx-1, pRef)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # add line before
                    case 1:
                         # print("EditParamLineCallback: Add up")

                        label = "  '" + newData[0] + "' " + Wye.dType.tostring(newData[1]) + " call by:" + Wye.access.tostring(newData[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, param,
                                                          editVerbFrm.vars.newParamDescr[0], label,
                                                          WyeUILib.EditVerb.EditParamLineCallback,
                                                          WyeUILib.EditVerb.EditParamCallback,
                                                          newData, insertBefore=True)

                    # copy line
                    case 2:
                        # copy param descr
                        ix = editVerbFrm.vars.newParamDescr[0].index(param)
                        copyRec = ("Parameter", (Wye.listCopy(editVerbFrm.vars.newParamDescr[0][ix])))
                        print("EditParamLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)


                    # cut Line
                    case 3:
                        # copy param descr
                        ix = editVerbFrm.vars.newParamDescr[0].index(param)
                        copyRec = ("Parameter", (Wye.listCopy(editVerbFrm.vars.newParamDescr[0][ix])))
                        print("EditParamLineCallback cut: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        print("EditParamLineCallback cut: dlg row", rIx)
                        if rIx < 0:
                            print("EditParamLineCallback cut: ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return
                        
                        # remove param descr
                        editVerbFrm.vars.newParamDescr[0].remove(param)
                        # remove dialog row (2 inputs
                        for ii in range(2):
                            frm = parentFrm.params.inputs[0].pop(rIx)[0]
                            print("EditParamLineCallback cut: remove", frm.params.label[0])
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # paste line before
                    case 4:
                        cutData = WyeCore.World.cutPasteManager.getSelected()
                        print("paste param before: cutData", cutData)
                        if cutData[0] != "Parameter":
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Incorrect Data Type", "Please select a 'paramDescr' row from Copy/Paste List",
                                                                     Wye.color.WARNING_COLOR)
                            return
                        data = cutData[1]
                        label = "  '" + data[0] + "' " + Wye.dType.tostring(data[1]) + " call by:" + Wye.access.tostring(data[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, param,
                                                          editVerbFrm.vars.newParamDescr[0], label,
                                                          WyeUILib.EditVerb.EditParamLineCallback,
                                                          WyeUILib.EditVerb.EditParamCallback,
                                                          data, insertBefore=True)

                    # delete line
                    case 5:
                        #print("EditParamLineCallback: Delete")

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditParamLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return

                        # remove param descr
                        editVerbFrm.vars.newParamDescr[0].remove(param)
                        # remove dialog row (2 inputs
                        for ii in range(2):
                            frm = parentFrm.params.inputs[0].pop(rIx)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # Add line after
                    case 6:
                        # print("EditParamLineCallback: Add down")
                        label = "  '" + newData[0] + "' " + Wye.dType.tostring(newData[1]) + " call by:" + Wye.access.tostring(newData[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, param,
                                                          editVerbFrm.vars.newParamDescr[0], label,
                                                          WyeUILib.EditVerb.EditParamLineCallback,
                                                          WyeUILib.EditVerb.EditParamCallback,
                                                          newData, insertBefore=False)


                    # move line down
                    case 7:
                        # .index(param) not working, dunno why
                        # dIx = editVerbFrm.vars.newParamDescr[0].index(param)
                        dIx = -1
                        for p in editVerbFrm.vars.newParamDescr[0]:
                            dIx += 1
                            if p==param:
                                break;
                        if dIx < 0:
                            print("EditParamLineCallback ERROR: param not found in paramDescr")
                            return

                        if dIx == len(editVerbFrm.vars.newParamDescr[0])-1:
                            #print("EditParamLineCallback Warning: line already at bottom")
                            return

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditParamLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return

                        # move code descr
                        descr = editVerbFrm.vars.newParamDescr[0].pop(dIx)
                        editVerbFrm.vars.newParamDescr[0].insert(dIx+1, descr)

                        # move dialog row (2 inputs)
                        edLnRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx+3, edLnRef)
                        pRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx+3, pRef)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                        #print("after move line")
                        #for ii in range(rIx-2, rIx+2):
                        #    print("rIx", ii," ", parentFrm.params.inputs[0][ii][0].params.label[0])

        # add/remove/move variable
        class EditVarLineCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                # print("EditVarLineCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditVarLineCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditVarLineCallback data", data)
                editLnFrm = data[1][0]  # add/del/copy button frame
                parentFrm = data[1][1]  # parent dialog
                editVerbFrm = data[1][2]
                btnFrm = data[1][3]
                var = data[1][4]

                # get selectionIx
                opIx = editLnFrm.params.selectionIx[0]

                #print("EditVarLineCallback: operator ix", opIx, " varDescr", var)
                #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Not implemented yet", Wye.color.WARNING_COLOR)

                newData = ["newVar", Wye.dType.ANY, None]  # placeholder var to insert

                # "0 Move line up",
                # "1 Add line before",
                # "2 Copy line",
                # "3 Delete Line",
                # "4 Paste line after",
                # "5 Move line down",
                match (opIx):
                    # move line up
                    case 0:
                        # .index(var) not working, dunno why
                        # dIx = editVerbFrm.vars.newParamDescr[0].index(var)
                        dIx = -1
                        for p in editVerbFrm.vars.newVarDescr[0]:
                            dIx += 1
                            if p == var:
                                break;
                        if dIx < 0:
                            print("EditVarLineCallback ERROR: var not found in varDescr")
                            return

                        if dIx == 0:
                            # print("EditVarLineCallback Warning: line already at top")
                            return

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditVarLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.vars.label[0], " not in input list")
                            return

                        # move code descr
                        descr = editVerbFrm.vars.newVarDescr[0].pop(dIx)
                        editVerbFrm.vars.newVarDescr[0].insert(dIx - 1, descr)

                        # move dialog row (2 inputs)
                        edLnRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx - 2, edLnRef)
                        pRef = parentFrm.params.inputs[0].pop(rIx + 1)
                        parentFrm.params.inputs[0].insert(rIx - 1, pRef)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # add line before
                    case 1:
                        # print("EditVarLineCallback: Add up")

                        label = "  '"+newData[0] + "' "+Wye.dType.tostring(newData[1]) + " = "+str(newData[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, var,
                                                          editVerbFrm.vars.newVarDescr[0], label,
                                                          WyeUILib.EditVerb.EditVarLineCallback,
                                                          WyeUILib.EditVerb.EditVarCallback,
                                                          newData, insertBefore=True, isParam=False)

                    # copy line
                    case 2:
                        #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Not implemented yet", Wye.color.WARNING_COLOR)
                        #pass

                        # copy var descr
                        ix = editVerbFrm.vars.newVarDescr[0].index(var)
                        copyRec = ("Variable", (Wye.listCopy(editVerbFrm.vars.newVarDescr[0][ix])))
                        print("EditVarLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)


                # cut Line
                    case 3:
                        #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Not implemented yet", Wye.color.WARNING_COLOR)
                        #pass

                        # copy var descr
                        ix = editVerbFrm.vars.newVarDescr[0].index(var)
                        copyRec = ("Variable", (Wye.listCopy(editVerbFrm.vars.newVarDescr[0][ix])))
                        print("EditVarLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditVarLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return

                        # remove var descr
                        editVerbFrm.vars.newVarDescr[0].remove(var)
                        # remove dialog row (2 inputs
                        for ii in range(2):
                            frm = parentFrm.params.inputs[0].pop(rIx)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # paste line
                    case 4:
                        #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Not implemented yet", Wye.color.WARNING_COLOR)
                        #pass

                        cutData = WyeCore.World.cutPasteManager.getSelected()
                        print("paste param before: cutData", cutData)
                        if cutData[0] != "Variable":
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Incorrect Data Type", "Please select a 'varDescr' row from Copy/Paste List",
                                                                     Wye.color.WARNING_COLOR)

                        data = cutData[1]
                        label = "  '"+data[0] + "' "+Wye.dType.tostring(data[1]) + " = "+str(data[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, var,
                                                          editVerbFrm.vars.newVarDescr[0], label,
                                                          WyeUILib.EditVerb.EditVarLineCallback,
                                                          WyeUILib.EditVerb.EditVarCallback,
                                                          data, insertBefore=True, isParam=False)

                # delete line
                    case 5:
                        # print("EditVarLineCallback: Delete")
                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditVarLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.params.label[0], " not in input list")
                            return

                        # remove var descr
                        editVerbFrm.vars.newVarDescr[0].remove(var)
                        # remove dialog row (2 inputs
                        for ii in range(2):
                            frm = parentFrm.params.inputs[0].pop(rIx)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                    # Add line after
                    case 6:
                        # print("EditVarLineCallback: Add up")
                        label = "  '" + newData[0] + "' " + Wye.dType.tostring(newData[1]) + " = " + str(newData[2])
                        editVerbFrm.verb.insertParamOrVar(parentFrm, editVerbFrm, editLnFrm, var,
                                                          editVerbFrm.vars.newVarDescr[0], label,
                                                          WyeUILib.EditVerb.EditVarLineCallback,
                                                          WyeUILib.EditVerb.EditVarCallback,
                                                          newData, insertBefore=False, isParam=False)

                    # move line down
                    case 7:
                        # .index(var) not working, dunno why
                        # dIx = editVerbFrm.vars.newVarDescr[0].index(var)
                        dIx = -1
                        for p in editVerbFrm.vars.newVarDescr[0]:
                            dIx += 1
                            if p==var:
                                break;
                        if dIx < 0:
                            print("EditVarLineCallback ERROR: var not found in varDescr")
                            return

                        if dIx == len(editVerbFrm.vars.newVarDescr[0])-1:
                            #print("EditVarLineCallback Warning: line already at bottom")
                            return

                        # find row in dlg
                        rIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        if rIx < 0:
                            print("EditVarLineCallback ERROR: input", editLnFrm, " ", editLnFrm.verb.__name__, " ",
                                  editLnFrm.vars.label[0], " not in input list")
                            return

                        # move code descr
                        descr = editVerbFrm.vars.newVarDescr[0].pop(dIx)
                        editVerbFrm.vars.newVarDescr[0].insert(dIx+1, descr)

                        # move dialog row (2 inputs)
                        edLnRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx+3, edLnRef)
                        pRef = parentFrm.params.inputs[0].pop(rIx)
                        parentFrm.params.inputs[0].insert(rIx+3, pRef)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None  # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)  # redisplay the dialog

                        #print("after move line")
                        #for ii in range(rIx-2, rIx+2):
                        #    print("rIx", ii," ", parentFrm.params.inputs[0][ii][0].params.label[0])

        # add/remove/move stream
        class EditStreamLineCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                #print("EditStreamLineCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditStreamLineCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditStreamLineCallback data", data)
                editLnFrm = data[1][0]  # add/del/copy button frame
                parentFrm = data[1][1]  # parent dialog
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                btnFrm = data[1][4]     # code frame
                level = data[1][5]      # indent level

                # get selectionIx
                opIx = editLnFrm.params.selectionIx[0]
                #print("EditStreamLineCallback: op", WyeUILib.EditVerb.modStreamOpList[opIx])

                newData = ["NewStream", [["Code", "#< your code goes here>"],]]
                #"0 Move line up",
                #"1 Add line before",
                #"2 Copy line",
                #"3 Delete Line",
                #"4 Add line after",
                #"5 Move line down",
                match (opIx):
                    # move line up
                    case 0:
                        # find the parent list for this line's code tuple
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            tIx = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return
                        if tIx == 0:
                            #print("Already at top")
                            return

                        # find the number of display rows for this tuple
                        dLen = WyeCore.Utils.countNestedLists(tuple)

                        # find the first display row of this tuple
                        dIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)

                        # get the number of rows to skip
                        preTuple = parentList[tIx-1]
                        preDLen = WyeCore.Utils.countNestedLists(preTuple)

                        # pull the tuple off and move it down one
                        tuple = parentList.pop(tIx)  # codeDescr entry
                        parentList.insert(tIx-1, tuple)  # codeDescr entry

                        # pop the display inputs (2 per row) to tmp
                        tmp = []
                        for ii in range(dIx, dIx + (dLen * 2)):
                            tmp.append(parentFrm.params.inputs[0].pop(dIx))

                        pasteStart = dIx - (preDLen*2)
                        for ii in range(dLen*2):
                            parentFrm.params.inputs[0].insert(pasteStart + ii, tmp[ii])

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # add line before
                    case 1:
                        # print("EditStreamLineCallback: Add up")
                        # get location of this frame in dialog input list

                        # insert new stream code before this one in verb's codeDescr
                        #print("EditStreamLineCallback find tuple", tuple, "\n   in", editVerbFrm.vars.newCodeDescr[0])
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            #print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        #print("EditStreamLineCallback: insert tuple", newData, "into\n ", parentList)
                        parentList.insert(ix, newData)
                        #print("  updated list\n ", parentList)

                        # create new dialog row for this code line

                        # find index to row to insert before
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditStreamLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # build dialog rows
                        rowLst = []
                        WyeUILib.EditVerb.bldStreamCodeLine(newData, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, they will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                        # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)

                    # copy line
                    case 2:
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            try:
                                ix = parentList.index(tuple)
                            except:
                                print("EditStreamLineCallback ERROR: failed to find", tuple, "\m  in", parentList)
                                return
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        copyRec = ("Stream", (Wye.listCopy(parentList[ix])))
                        #print("EditStreamLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)


                    # cut Line
                    case 3:
                        # copy line
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            try:
                                ix = parentList.index(tuple)
                            except:
                                print("EditStreamLineCallback ERROR: failed to find", tuple, "\m  in", parentList)
                                return
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        copyRec = ("Stream", (Wye.listCopy(parentList[ix])))
                        # print("EditStreamLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)

                        # get location of this frame in dialog input list
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])

                        # count the lists (verb params - shown on following rows in dialog) in tuple, including tuple itself
                        count = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # delete as many rows as there are lists
                        # find index to row to delete
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditStreamLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        count *= 2      # del both editLn and line inputs for each row
                        parent = None
                        for ii in range(count):
                            frm = parentFrm.params.inputs[0].pop(ix)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # paste line before
                    case 4:
                        # get line from cutList
                        cutData = WyeCore.World.cutPasteManager.getSelected()
                        #print("paste code before: cutData", cutData)
                        if cutData[0] != "Stream":
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Incorrect Data Type", "Please select a 'Stream' row from Copy/Paste List",
                                                                     Wye.color.WARNING_COLOR)
                            return
                        data = cutData[1]

                        # insert code before this one in verb's codeDescr
                        # print("EditStreamLineCallback codeFrm", codeFrm.verb.__name__)
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        parentList.insert(ix, data)

                        # create new dialog row for this code line

                        # find index to row to insert before
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditStreamLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # build dialog rows
                        rowLst = []  # put dialog row(s) here
                        WyeUILib.EditVerb.bldStreamCodeLine(data, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, they will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                            # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)



                    # delete line
                    case 5:
                        # print("EditStreamLineCallback: Delete")
                        # get location of this frame in dialog input list
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])

                        # Insert new line into code desr
                        # todo - it would simplify life to have an AST abstract syntax tree holding var, call, type, etc. info and
                        #  linking relevant parts to relevant controls/data

                        # count the lists (verb params - shown on following rows in dialog) in tuple, including tuple itself
                        count = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # delete as many rows as there are lists
                        # find index to row to delete
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditStreamLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        count *= 2      # del both editLn and line inputs for each row
                        parent = None
                        for ii in range(count):
                            frm = parentFrm.params.inputs[0].pop(ix)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # Add line after
                    case 6:
                        # print("EditStreamLineCallback: Add down")
                        # get location of this frame in dialog input list

                        # insert new (noop) code before this one in verb's codeDescr
                        # print("EditStreamLineCallback codeFrm", codeFrm.verb.__name__)
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: ERROR failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        ix += 1  # put after the current line

                        if ix < len(parentList):
                            parentList.insert(ix, newData)
                        else:
                            parentList.append(newData)

                        # create new dialog row for this code line

                        # find index to row to insert after
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditStreamLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # skip over current tuple rows in dialog for every row of tuple
                        tupleLen = WyeCore.Utils.countNestedLists(tuple)
                        ix += (tupleLen)*2     # put after the current line
                        #print("EditStreamLineCallback: len", tupleLen, " of tuple", tuple)
                                    # Note: there is an OK/Cancel after the last code input, so insert works even
                                    # at the end of the current code listing

                        # build dialog rows
                        rowLst = []  # put dialog row(s) here
                        WyeUILib.EditVerb.bldStreamCodeLine(newData, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, the new inputs will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                        # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)


                    # move line down
                    case 7:
                        # find the parent list for this line's code tuple
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            tIx = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditStreamLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return
                        if tIx == len(parentList)-1:
                            #print("Already at bottom")
                            return

                        # find the number of display rows for this tuple
                        dLen = WyeCore.Utils.countNestedLists(tuple)

                        # find the first display row of this tuple
                        dIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)

                        # get the number of rows to skip
                        postTuple = parentList[tIx+1]
                        postDLen = WyeCore.Utils.countNestedLists(postTuple)

                        # pull the tuple off and move it down one
                        tuple = parentList.pop(tIx)  # codeDescr entry
                        parentList.insert(tIx+1, tuple)  # codeDescr entry

                        # pop the display inputs (2 per row) to tmp
                        tmp = []
                        for ii in range(dIx, dIx + (dLen * 2)):
                            tmp.append(parentFrm.params.inputs[0].pop(dIx))

                        pasteStart = dIx + (postDLen*2)
                        for ii in range(dLen*2):
                            parentFrm.params.inputs[0].insert(pasteStart + ii, tmp[ii])

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                #print("EditStreamLineCallback: after operation\n ", editVerbFrm.vars.newCodeDescr[0])

        # add/remove/move code line
        class EditCodeLineCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                #print("EditCodeLineCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditCodeLineCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditCodeLineCallback data", data)
                editLnFrm = data[1][0]  # add/del/copy button frame
                parentFrm = data[1][1]  # parent dialog
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                btnFrm = data[1][4]     # code frame
                level = data[1][5]      # indent level

                # get selectionIx
                opIx = editLnFrm.params.selectionIx[0]

                newData = ["Code", "#< your code goes here>"]
                #"0 Move line up",
                #"1 Add line before",
                #"2 Copy line",
                #"3 Delete Line",
                #"4 Add line after",
                #"5 Move line down",
                match (opIx):
                    # move line up
                    case 0:
                        # find the parent list for this line's code tuple
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            tIx = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return
                        if tIx == 0:
                            #print("Already at top")
                            return

                        # find the number of display rows for this tuple
                        dLen = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # find the first display row of this tuple
                        dIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)

                        # get the number of rows to skip
                        preTuple = parentList[tIx-1]
                        preDLen = 1 + WyeCore.Utils.countNestedLists(preTuple)

                        # pull the tuple off and move it down one
                        tuple = parentList.pop(tIx)  # codeDescr entry
                        parentList.insert(tIx-1, tuple)  # codeDescr entry

                        # pop the display inputs (2 per row) to tmp
                        tmp = []
                        for ii in range(dIx, dIx + (dLen * 2)):
                            tmp.append(parentFrm.params.inputs[0].pop(dIx))

                        pasteStart = dIx - (preDLen*2)
                        for ii in range(dLen*2):
                            parentFrm.params.inputs[0].insert(pasteStart + ii, tmp[ii])

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # add line before
                    case 1:
                        # print("EditCodeLineCallback: Add up")
                        # get location of this frame in dialog input list

                        # insert new (noop) code before this one in verb's codeDescr
                        # print("EditCodeLineCallback codeFrm", codeFrm.verb.__name__)
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        parentList.insert(ix, newData)

                        # create new dialog row for this code line

                        # find index to row to insert before
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # build dialog rows
                        rowLst = []  # put dialog row(s) here
                        WyeUILib.EditVerb.bldEditCodeLine(newData, level, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, they will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                        # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)

                    # copy line
                    case 2:
                        #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Not implemented yet", Wye.color.WARNING_COLOR)
                        #pass

                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            try:
                                ix = parentList.index(tuple)
                            except:
                                print("EditCodeLineCallback ERROR: failed to find", tuple, "\m  in", parentList)
                                return
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        copyRec = ("Code", (Wye.listCopy(parentList[ix])))
                        #print("EditCodeLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)


                    # cut Line
                    case 3:
                        # copy line
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            try:
                                ix = parentList.index(tuple)
                            except:
                                print("EditCodeLineCallback ERROR: failed to find", tuple, "\m  in", parentList)
                                return
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        copyRec = ("Code", (Wye.listCopy(parentList[ix])))
                        # print("EditCodeLineCallback copy: copyRec", copyRec)
                        WyeCore.World.cutPasteManager.add(copyRec)

                        # get location of this frame in dialog input list
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])

                        # count the lists (verb params - shown on following rows in dialog) in tuple, including tuple itself
                        count = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # delete as many rows as there are lists
                        # find index to row to delete
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        count *= 2      # del both editLn and line inputs for each row
                        parent = None
                        for ii in range(count):
                            frm = parentFrm.params.inputs[0].pop(ix)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # paste line before
                    case 4:
                        # get line from cutList
                        cutData = WyeCore.World.cutPasteManager.getSelected()
                        print("paste code before: cutData", cutData)
                        if cutData[0] != "Code":
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Incorrect Data Type", "Please select a 'codeDescr' row from Copy/Paste List",
                                                                     Wye.color.WARNING_COLOR)
                            return
                        data = cutData[1]

                        # insert code before this one in verb's codeDescr
                        # print("EditCodeLineCallback codeFrm", codeFrm.verb.__name__)
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        parentList.insert(ix, data)

                        # create new dialog row for this code line

                        # find index to row to insert before
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # build dialog rows
                        rowLst = []  # put dialog row(s) here
                        WyeUILib.EditVerb.bldEditCodeLine(data, level, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, they will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                            # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)



                    # delete line
                    case 5:
                        # print("EditCodeLineCallback: Delete")
                        # get location of this frame in dialog input list
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])

                        # Insert new line into code desr
                        # todo - it would simplify life to have an AST abstract syntax tree holding var, call, type, etc. info and
                        #  linking relevant parts to relevant controls/data

                        # count the lists (verb params - shown on following rows in dialog) in tuple, including tuple itself
                        count = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # delete as many rows as there are lists
                        # find index to row to delete
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        count *= 2      # del both editLn and line inputs for each row
                        parent = None
                        for ii in range(count):
                            frm = parentFrm.params.inputs[0].pop(ix)[0]
                            frm.verb.close(frm)

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                    # Add line after
                    case 6:
                        # print("EditCodeLineCallback: Add down")
                        # get location of this frame in dialog input list

                        # insert new (noop) code before this one in verb's codeDescr
                        # print("EditCodeLineCallback codeFrm", codeFrm.verb.__name__)
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            ix = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: ERROR failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return

                        ix += 1
                        if ix < len(parentList):
                            parentList.insert(ix, newData)
                        else:
                            parentList.append(newData)

                        # create new dialog row for this code line

                        # find index to row to insert after
                        ix = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)
                        # Debug: if the unthinkable happens, give us a hint
                        if ix < 0:
                            print("EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")

                        # skip over current tuple rows in dialog for every row of tuple
                        tupleLen = WyeCore.Utils.countNestedLists(tuple)
                        ix += (tupleLen+1)*2     # put after the current line
                        print("EditCodeLineCallback: len", tupleLen, " of tuple", tuple)
                                    # Note: there is an OK/Cancel after the last code input, so insert works even
                                    # at the end of the current code listing

                        # build dialog rows
                        rowLst = []  # put dialog row(s) here
                        WyeUILib.EditVerb.bldEditCodeLine(newData, level, editVerbFrm, parentFrm, rowLst)

                        # insert new dialog rows into dialog
                        # display new dialog rows (don't sweat the position, the new inputs will be correctly
                        # placed by dialog redisplay, below)
                        pos = [0, 0, 0]
                        for rowFrmRef in rowLst:
                            parentFrm.params.inputs[0].insert(ix, rowFrmRef)
                            ix += 1
                            rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                        # update position of all fields
                        parentFrm.verb.redisplay(parentFrm)


                    # move line down
                    case 7:
                        # find the parent list for this line's code tuple
                        parentList = WyeCore.Utils.findTupleParent(editVerbFrm.vars.newCodeDescr[0], tuple)
                        if parentList:
                            tIx = parentList.index(tuple)
                            # print("found tuple", tuple, " at", ix, " in", parentList)
                        else:
                            print("EditCodeLineCallback: failed to find tuple '" + str(tuple) + "' in parent list:\n",
                                  editVerbFrm.vars.newCodeDescr[0])
                            return
                        if tIx == len(parentList)-1:
                            #print("Already at bottom")
                            return

                        # find the number of display rows for this tuple
                        dLen = 1 + WyeCore.Utils.countNestedLists(tuple)

                        # find the first display row of this tuple
                        dIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],editLnFrm)

                        # get the number of rows to skip
                        postTuple = parentList[tIx+1]
                        postDLen = 1 + WyeCore.Utils.countNestedLists(postTuple)

                        # pull the tuple off and move it down one
                        tuple = parentList.pop(tIx)  # codeDescr entry
                        parentList.insert(tIx+1, tuple)  # codeDescr entry

                        # pop the display inputs (2 per row) to tmp
                        tmp = []
                        for ii in range(dIx, dIx + (dLen * 2)):
                            tmp.append(parentFrm.params.inputs[0].pop(dIx))

                        pasteStart = dIx + (postDLen*2)
                        for ii in range(dLen*2):
                            parentFrm.params.inputs[0].insert(pasteStart + ii, tmp[ii])

                        # redisplay parent dialog
                        parentFrm.vars.currInp[0] = None        # we just deleted it, so clear it
                        parentFrm.verb.redisplay(parentFrm)     # redisplay the dialog

                #print("EditCodeLineCallback: after operation\n ", editVerbFrm.vars.newCodeDescr[0])

        # Edit the stream name
        class EditStreamCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                #print("EditStreamCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditStreamCallback, stack)

            def run(frame):
                data = frame.eventData
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                level = data[1][4]

                #print("EditStreamCallback btnFrm", btnFrm.params.label[0], " parentFrm", parentFrm.verb.__name__)

                match (frame.PC):
                    case 0:
                        #print("EditStreamCallback data='" + str(frame.eventData) + "'")

                        # build code dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)

                        frame.vars.tuple[0] = tuple

                        # sequential verb
                        #else:
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Edit Stream"]
                        dlgFrm.params.parent = [parentFrm]
                        dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                        # Code
                        codeFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        codeFrm.params.frame = [None]        # placeholder
                        codeFrm.params.label = ["Stream Name:"]
                        codeFrm.params.value = [tuple[0]]
                        WyeUILib.InputText.run(codeFrm)
                        dlgFrm.params.inputs[0].append([codeFrm])

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = dlgFrm.status
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            newTxt = dlgFrm.params.inputs[0][-1][0].params.value[0]

                            #print("EditStreamCallback done: newOp", newOp, "newTxt", newTxt)
                            tuple[0] = newTxt
                            #print("EditStreamCallback done: newOp", newOp, "newTxt", newTxt)

                            btnFrm.verb.setLabel(btnFrm, "Stream: " + str(tuple[0]))


        # Modify the code
        # NOTE: Order of inputs in dialog MUST BE SAME as order of ops in EditVerb.opList
        class EditCodeCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        ("prefix", Wye.dType.STRING, ""),
                        ("selectedOpIx", Wye.dType.INTEGER, 0),     # checkbox radio buttons update this
                        ("firstCheckFrm", Wye.dType.OBJECT, None),
                        ("libDropFrm", Wye.dType.OBJECT, None),
                        ("verbDropFrm", Wye.dType.OBJECT, None),
                        ("parEqDropFrm", Wye.dType.OBJECT, None),
                        ("parEqPrefDropFrm", Wye.dType.OBJECT, None),
                        ("varEqDropFrm", Wye.dType.OBJECT, None),
                        ("varEqPrefDropFrm", Wye.dType.OBJECT, None),
                        ("varDropFrm", Wye.dType.OBJECT, None),
                        ("varEqTextFrm", Wye.dType.OBJECT, None),
                        ("parEqTextFrm", Wye.dType.OBJECT, None),
                        ("constTextFrm", Wye.dType.OBJECT, None),
                        ("exprTextFrm", Wye.dType.OBJECT, None),
                        ("codeTextFrm", Wye.dType.OBJECT, None),
                        ("codeBlkTextFrm", Wye.dType.OBJECT, None),
                        ("labelTextFrm", Wye.dType.OBJECT, None),
                        ("goToTextFrm", Wye.dType.OBJECT, None),
                        ("ifExprTextFrm", Wye.dType.OBJECT, None),
                        ("ifTgtTextFrm", Wye.dType.OBJECT, None),
                        ("ifTarget", Wye.dType.STRING, ""),
                        )

            def start(stack):
                #print("EditCodeCallback started")
                f = Wye.codeFrame(WyeUILib.EditVerb.EditCodeCallback, stack)
                return f

            def run(frame):
                data = frame.eventData
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                level = data[1][4]
                editLnFrm = data[1][5]
                op = data[1][6]             # the initial operation

                #print("EditCodeCallback btnFrm", btnFrm.params.label[0], " dlgFrm", dlgFrm.verb.__name__)
                # if there is a prefix, save it
                labelStr = btnFrm.params.label[0].strip()
                if labelStr[0] == "(":  # if there's a prefix
                    endPrefIx = labelStr.find(")")
                    frame.vars.prefix[0] = labelStr[:endPrefIx + 2]

                # todo - bulletproofing - if no tuple[1], create content.
                match (frame.PC):
                    case 0:
                        #print("EditCodeCallback data='" + str(frame.eventData) + "'")
                        #print("EditCodeCallback tuple", tuple)

                        # build code dialog

                        frame.vars.tuple[0] = tuple

                        # if there is a prefix, save it
                        labelStr = btnFrm.params.label[0].strip()
                        if labelStr[0] == "(":      # if there's a prefix
                            endPrefIx = labelStr.find(")")
                            frame.vars.prefix[0] = labelStr[:endPrefIx+2]
                            #print("save prefix", frame.vars.prefix[0])
                        #else:
                        #    print("default prefix", frame.vars.prefix[0])

                        # create dialog
                        dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog("Edit Code", parent=parentFrm,
                                      position=(.5,-.3, -.5 + btnFrm.vars.position[0][2]))

                        # Verb
                        frame.vars.firstCheckFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Library Verb", [op == "Verb"], radioGroup="radGrp", selectedRadio=frame.vars.selectedOpIx)
                        # parse input for library and verb dropdowns
                        libList = [lib.__name__ for lib in WyeCore.World.libList]
                        libIx = 0
                        verbName = "<none selected>"
                        if op == "Verb":
                            #print("Do verb")
                            txtLst = tuple[0].split(".")
                            if len(txtLst) >= 2:
                                libName = txtLst[-2]
                                if libName in WyeCore.World.libDict:
                                    lib = WyeCore.World.libDict[libName]
                                    libIx = WyeCore.World.libList.index(lib)

                                verbName = txtLst[-1]

                        # build verb list for lib
                        lib = WyeCore.World.libList[libIx]
                        verbList = []
                        for verbNm in dir(lib):
                            # ignore class and Wye-generated entries
                            if verbNm[0] != "_" and verbNm[-3:] != "_rt":
                                verbList.append(verbNm)
                        if verbName in verbList:
                            verbIx = verbList.index(verbName)
                        else:
                            #print("did not find verb", verbName, " in", lib.__name__)
                            verbIx = 0

                        #print("libList", libList)
                        #print("verbList", verbList)
                        frame.vars.libDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Library",
                                                     [libList], [libIx], WyeUILib.EditVerb.EditCodeCallback.libDropCallback,
                                                     (frame,), layout=Wye.layout.ADD_RIGHT)
                        #WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, ".", layout=Wye.layout.ADD_RIGHT)
                        frame.vars.verbDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Verb",
                                                      [verbList], [verbIx], layout=Wye.layout.ADD_RIGHT)

                        # Var=
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "     Variable =", [op == "Var="], radioGroup="radGrp")
                        varList = [var[0] for var in editVerbFrm.params.verb[0].varDescr]
                        if len(varList) == 0:
                            varList = ["<no variables defined>"]     # TODO - disable input
                        txt = str(tuple[1])
                        #print("Tuple[1]", txt)
                        rest = txt
                        varIx = 0
                        varNm = "<unknown>"
                        eqPrefix = "="
                        if txt.startswith("frame.vars."):
                            txt = txt[11:]
                            brIx = txt.find("[")
                            if brIx > 0:
                                varNm = txt[:brIx]

                            rest = txt
                            eqIx = rest.find("=")
                            if eqIx >= 0:
                                if rest[eqIx-1] in ["+","-"]:       # handle -=, +=
                                    eqPrefix = rest[eqIx-1:eqIx+1]
                                rest = rest[eqIx+1:].strip()

                            if varNm in varList:
                                varIx = varList.index(varNm)
                        frame.vars.varEqDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Variable",
                                      [varList], [varIx],  layout=Wye.layout.ADD_RIGHT, showLabel=False)
                        eqIx = WyeUILib.EditVerb.eqList.index(eqPrefix)
                        frame.vars.varEqPrefDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "= / += / -=",
                                                            [WyeUILib.EditVerb.eqList], [eqIx],
                                                            layout=Wye.layout.ADD_RIGHT, showLabel=False)
                        frame.vars.varEqTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [rest],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # Par=
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, " Parameter =", [op == "Par="],
                                                                   radioGroup="radGrp")
                        txt = str(tuple[1])
                        rest = txt
                        parList = [par[0] for par in editVerbFrm.params.verb[0].paramDescr]
                        if len(parList) == 0:
                            parList = ["<no parameters defined>"]     # TODO - disable input
                        parIx = 0
                        eqPrefix = "="
                        if txt.startswith("frame.params."):
                            txt = txt[13:]
                            brIx = txt.find("[")
                            if brIx > 0:
                                parNm = txt[:brIx]

                                rest = txt[brIx + 2:]
                                eqIx = rest.find("=")
                                if eqIx >= 0:
                                    if rest[eqIx - 1] in ["+", "-"]:  # handle -=, +=
                                        eqPrefix = rest[eqIx - 1:eqIx]
                                    rest = rest[eqIx+1:].strip()
                                if parNm in parList:
                                    parIx = parList.index(parNm)
                                else:
                                    parIx = 0
                            else:
                                parIx = 0
                        frame.vars.parEqDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Parameter",
                                                       [parList], [parIx], layout=Wye.layout.ADD_RIGHT, showLabel=False)
                        eqIx = WyeUILib.EditVerb.eqList.index(eqPrefix)
                        frame.vars.parEqPrefDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "= / += -=",
                                        [WyeUILib.EditVerb.eqList], [eqIx], layout=Wye.layout.ADD_RIGHT, showLabel=False)
                        frame.vars.parEqTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [rest],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # Const
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "       Constant", [op == "Const"],
                                                                   radioGroup="radGrp")
                        frame.vars.constTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # Var ref
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, " Variable ref", [op == "Var"], radioGroup="radGrp")
                        varList = [var[0] for var in editVerbFrm.params.verb[0].varDescr]
                        if len(varList) == 0:
                            varList = ["<no varibles defined>"]     # TODO - disable input
                        txt = str(tuple[1])
                        #print("Tuple[1]", txt)
                        rest = txt
                        varIx = 0
                        varNm = "<unknown>"
                        if txt.startswith("frame.vars."):
                            varNm = txt[11:].strip()

                            brIx = txt.find("[")    # if not a parameter, strip off the deref '[0]'
                            if brIx > 0:
                                varNm = txt[:brIx]
                            if varNm in varList:
                                varIx = varList.index(varNm)
                        frame.vars.varDropFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Variable",
                                                     [varList], [varIx], layout=Wye.layout.ADD_RIGHT, showLabel=False)
                        # Expr
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "   Expression", [op == "Expr"],
                                                                   radioGroup="radGrp")
                        frame.vars.exprTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)
                        # Code
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "              Code", [op == "Code"],
                                                                   radioGroup="radGrp")
                        frame.vars.codeTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # CodeBlock
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "   Code Block", [op == "CodeBlock"],
                                                                   radioGroup="radGrp")
                        frame.vars.codeBlkTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # Label
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "             Label", [op == "Label"],
                                                                   radioGroup="radGrp")
                        frame.vars.labelTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # GoTo
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "            Go To", [op == "GoTo"],
                                                                   radioGroup="radGrp")
                        frame.vars.goToTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # IfGoTo
                        WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "                    If", [op == "IfGoTo"],
                                                                   radioGroup="radGrp")
                        frame.vars.ifExprTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [str(tuple[1])],
                                                               layout=Wye.layout.ADD_RIGHT)
                        if len(tuple) > 2:
                            lblStr = str(tuple[2])
                        else:
                            lblStr = "MyGoToLabel"
                        frame.vars.ifTgtTextFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "", [lblStr],
                                                               layout=Wye.layout.ADD_RIGHT)

                        # put dialog on stack and go do it
                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS
                        #opIx = frame.vars.selectedOpIx[0]
                        opIx = frame.vars.firstCheckFrm[0].params.selectedRadio[0]

                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            newTuple = []       # build new code here
                            match(opIx):
                                case 0:     # Verb
                                    libIx = frame.vars.libDropFrm[0].params.selectionIx[0]
                                    libTxt = frame.vars.libDropFrm[0].params.list[0][libIx]
                                    vbIx = frame.vars.verbDropFrm[0].params.selectionIx[0]
                                    vbTxt = frame.vars.verbDropFrm[0].vars.list[0][vbIx]

                                    # NOTE: I don't think we get here any more, but leave it in Justin Case
                                    if libTxt == "<none selected>" or vbTxt == "<none selected>":
                                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Invalid library.verb",
                                                "Please enter a valid library.verb or Cancel this edit", Wye.color.ERROR_COLOR)

                                        # clone the dialog and let the user try again
                                        newDlg = WyeUILib.Dialog.start(frame.SP)
                                        # clone old dialog params to new
                                        newDlg.params.title = dlgFrm.params.title
                                        newDlg.params.position = dlgFrm.params.position
                                        newDlg.params.parent = dlgFrm.params.parent
                                        newDlg.params.inputs = dlgFrm.params.inputs
                                        newDlg.params.format = dlgFrm.params.format
                                        newDlg.params.headerColor = dlgFrm.params.headerColor
                                        newDlg.params.callback = dlgFrm.params.callback
                                        newDlg.params.optData = dlgFrm.params.optData

                                        # push the copied dialog and go back to waiting
                                        # print("Pushed dialog to stack")
                                        frame.SP.append(newDlg)
                                        return

                                    # Good lib.verb, build new line(s)
                                    else:
                                        # if there's been no change, just return
                                        if op == WyeUILib.EditVerb.opList[opIx]:  # if was lib.verb before, see if same lib.verb
                                            txtLst = tuple[0].split(".")
                                            if len(txtLst) >= 2:
                                                oldLibTxt = txtLst[-2]
                                                oldVbTxt = txtLst[-1]
                                                if libTxt == oldLibTxt and vbTxt == oldVbTxt:
                                                    # exit without making any changes
                                                    return

                                        # lib changed
                                        # generate new row content
                                        newLib = WyeCore.World.libDict[libTxt]
                                        newVerb = getattr(newLib, vbTxt)
                                        newTxt = libTxt + "." + vbTxt
                                        newTuple.append("WyeCore.libs."+newTxt)
                                        for param in newVerb.paramDescr:
                                            pTuple = ["Expr", "0 # <your param value here>"]
                                            newTuple.append(pTuple)

                                case 1:     # Var=
                                    varIx = frame.vars.varEqDropFrm[0].params.selectionIx[0]
                                    varNm = frame.vars.varEqDropFrm[0].vars.list[0][varIx]
                                    eqIx = frame.vars.varEqPrefDropFrm[0].params.selectionIx[0]
                                    eqTxt = frame.vars.varEqPrefDropFrm[0].vars.list[0][eqIx]
                                    exprTxt = frame.vars.varEqTextFrm[0].vars.currVal[0]
                                    newTuple.append("Var=")
                                    newTuple.append("frame.vars."+varNm+"[0] "+eqTxt+" "+exprTxt)

                                case 2:     # Par=
                                    parIx = frame.vars.parEqDropFrm[0].params.selectionIx[0]
                                    parNm = frame.vars.parEqDropFrm[0].params.list[0][parIx]
                                    eqIx = frame.vars.parEqPrefDropFrm[0].params.selectionIx[0]
                                    eqTxt = frame.vars.parEqPrefDropFrm[0].vars.list[0][eqIx]
                                    exprTxt = frame.vars.parEqTextFrm[0].vars.currVal[0]
                                    newTuple.append("Par=")
                                    newTuple.append("frame.vars."+parNm+"[0] "+eqTxt+" "+exprTxt)

                                case 3:     # Const
                                    exprTxt = frame.vars.constTextFrm[0].vars.currVal[0]
                                    newTuple.append("Const")
                                    newTuple.append(exprTxt)

                                case 4:     # Var reference
                                    varIx = frame.vars.varDropFrm[0].params.selectionIx[0]
                                    varNm = frame.vars.varDropFrm[0].vars.list[0][varIx]
                                    newTuple.append("Var")
                                    if frame.vars.prefix[0]:    # if it's a param, don't deref the var
                                        newTuple.append("frame.vars."+varNm)
                                    else:       # used as a value, deref the var to get the value
                                        newTuple.append("frame.vars."+varNm+"[0]")

                                case 5:     # Expr
                                    exprTxt = frame.vars.exprTextFrm[0].vars.currVal[0]
                                    newTuple.append("Expr")
                                    newTuple.append(exprTxt)

                                case 6:     # Code
                                    exprTxt = frame.vars.codeTextFrm[0].vars.currVal[0]
                                    newTuple.append("Code")
                                    newTuple.append(exprTxt)

                                case 7:     # CodeBlock
                                    exprTxt = frame.vars.codeBlkTextFrm[0].vars.currVal[0]
                                    newTuple.append("CodeBlock")
                                    newTuple.append(exprTxt)

                                case 8:     # Label
                                    exprTxt = frame.vars.labelTextFrm[0].vars.currVal[0]
                                    newTuple.append("Label")
                                    newTuple.append(exprTxt)

                                case 9:     # GoTo
                                    exprTxt = frame.vars.goToTextFrm[0].vars.currVal[0]
                                    newTuple.append("GoTo")
                                    newTuple.append(exprTxt)

                                case 10:    # IfGoTo
                                    exprTxt = frame.vars.ifExprTextFrm[0].vars.currVal[0]
                                    lblTxt = frame.vars.ifTgtTextFrm[0].vars.currVal[0]
                                    newTuple.append("IfGoTo")
                                    newTuple.append(exprTxt)
                                    newTuple.append(lblTxt)

                            # delete old rows from dialog, returns insert pt for new ones
                            inpIx = WyeUILib.EditVerb.EditCodeCallback.removeOldDlgLines(editLnFrm, tuple, parentFrm)

                            # replace oontents of old tuple in newCodeDescr
                            tuple.clear()
                            for elem in newTuple:
                                tuple.append(elem)

                            # generate new row(s)
                            WyeUILib.EditVerb.EditCodeCallback.genNewDlgLines(inpIx, tuple, level, editVerbFrm,
                                                                              parentFrm, frame.vars.prefix[0])

                        #else:
                        #    print("EditCodeCallback: User cancelled")

            def removeOldDlgLines(editLnFrm, tuple, parentFrm):
                # delete the current row(s) in the mother dialog
                inpIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], editLnFrm)  # back up to edLn input
                if inpIx < 0:
                    print("removeOldDlgLines: EditCodeLineCallback ERROR: input", editLnFrm.verb.__name__, " not in input list")
                    print("editLnFrm", editLnFrm.params.label[0], " ", editLnFrm, " not found in:")
                    for frmLst in parentFrm.params.inputs[0]:
                        frm = frmLst[0]
                        if frm.verb.__name__ == "InputDropdown":
                            print("  input", frm.params.label[0], " ", frm, " ", frm.params.label[0])
                    # we're gonna crash or run very badly or something
                    return

                # count dlg rows to delete (one per nested list in codeDescr tuple)
                inpCt = WyeCore.Utils.countNestedLists(tuple) + 1   # if there are parameters, this will count them

                # remove that many rows from the dialog
                inpCt *= 2  # del both editLn and line inputs for each row
                parent = None
                for ii in range(inpCt):
                    frm = parentFrm.params.inputs[0].pop(inpIx)[0]
                    frm.verb.close(frm)

                return inpIx        # return insertion point for new lines

            def genNewDlgLines(inpIx, tuple, level, editVerbFrm, parentFrm, prefix):
                # build new dialog rows
                rowLst = []  # put dialog row(s) here
                WyeUILib.EditVerb.bldEditCodeLine(tuple, level, editVerbFrm, parentFrm, rowLst, prefix=prefix)

                # insert new dialog rows into dialog
                # display new dialog rows (don't sweat the position, they will be correctly
                # placed by dialog redisplay, below)
                pos = [0, 0, 0]
                for rowFrmRef in rowLst:
                    parentFrm.params.inputs[0].insert(inpIx, rowFrmRef)
                    inpIx += 1
                    rowFrmRef[0].verb.display(rowFrmRef[0], parentFrm, pos)

                # update position of all fields
                parentFrm.verb.redisplay(parentFrm)


            # handle lib changed so need to change verb list
            class libDropCallback:
                mode = Wye.mode.SINGLE_CYCLE
                dataType = Wye.dType.STRING
                paramDescr = ()
                varDescr = (("count", Wye.dType.INTEGER, 0),
                            ("tuple", Wye.dType.OBJECT, None),
                            ("dlgStat", Wye.dType.INTEGER, -1),
                            )

                def start(stack):
                    return Wye.codeFrame(WyeUILib.EditVerb.EditCodeCallback.libDropCallback, stack)

                def run(frame):
                    data = frame.eventData
                    edCdFrm = data[1][0]

                    # lib changed, invalidate verb list
                    libIx = edCdFrm.vars.libDropFrm[0].params.selectionIx[0]
                    lib = WyeCore.World.libList[libIx]

                    verbList = []
                    for verbNm in dir(lib):
                        # ignore class and Wye-generated entries
                        if verbNm[0] != "_" and verbNm[-3:] != "_rt":
                            verbList.append(verbNm)

                    edCdFrm.vars.verbDropFrm[0].verb.setList(edCdFrm.vars.verbDropFrm[0], verbList, 0)


        # todo - NOT CURRENTLY USED.  Do we need it?
        class EditSpecialCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("count", Wye.dType.INTEGER, 0),
                        ("tuple", Wye.dType.OBJECT, None),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                       )

            def start(stack):
                return Wye.codeFrame(WyeUILib.EditVerb.EditSpecialCallback, stack)

            def run(frame):
                data = frame.eventData
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editVerbFrm = data[1][2]
                tuple = data[1][3]
                level = data[1][4]

                match (frame.PC):
                    case 0:
                        #print("EditCodeCallback data='" + str(frame.eventData) + "'")
                        #print("EditCodeCallback tuple", tuple)

                        # build code dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)

                        frame.vars.tuple[0] = tuple

                        # if there is a prefix, save it
                        print("Do prefix")
                        labelStr = btnFrm.params.label[0].strip()
                        if labelStr[0] == "(":      # if there's a prefix
                            endPrefIx = labelStr.find(")")
                            frame.vars.prefix[0] = labelStr[:endPrefIx+2]
                            print("save prefix", frame.vars.prefix[0])
                        else:
                            print("default prefix", frame.vars.prefix[0])

                        # create dialog
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Edit Code"]
                        dlgFrm.params.parent = [parentFrm]
                        dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                        # Code type
                        verbType = tuple[0]
                        if verbType is None:
                            verbType = "Code"

                        # verb type/name
                        if not tuple[0]:
                            selIx = 1       # None -> Code
                        elif isinstance(tuple[0], str) and tuple[0].find(".") > -1:  # if there is a verb here
                            selIx = 0       # lib.verb -> Verb
                        else:
                            try:            # otherwise, look up in opList
                                selIx = WyeUILib.EditVerb.opList.index(tuple[0])
                            except:
                                selIx = 1   # unknown, default to Code
                        WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Op:", [WyeUILib.EditVerb.opList], [selIx])

                        # Code
                        WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "Expr:", [str(tuple[1])])

                        # optional Code
                        if tuple[0] == "IfGoTo":
                            tgtTxt = [str(tuple[2])]
                        else:
                            tgtTxt = ["<none>"]
                        WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "Tgt:", tgtTxt, [str(tuple[1])])

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = dlgFrm.status
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            opIx = dlgFrm.params.inputs[0][-3][0].params.selectionIx[0]
                            #print("EditCodeCallback done: opIx", opIx)
                            # if user canceled out and opIx is invalid, restore old value from tuple
                            if opIx >= 0:
                                newOp = WyeUILib.EditVerb.opList[opIx]

                                newlib = None
                                newVerb = None      # put verb here when found

                                # if user switched to/from Verb, need to add/clean up parameter rows
                                if newOp != tuple[0]:
                                    if newOp == "Verb":
                                        # first, do we have a valid lib.verb
                                        newTxt = dlgFrm.params.inputs[0][-2][0].params.value[0]
                                        txtLst = newTxt.split(".")
                                        goodLib = True  # be optimistic
                                        if len(txtLst) < 2:
                                            #print("EditCodeCallback: Fail: no '.' in", newTxt)
                                            goodLib = False
                                        elif not txtLst[-2] in WyeCore.World.libDict:
                                            #print("EditCodeCallback: Fail: ", txtLst[-2], " is not a current library")
                                            goodLib = False
                                        if goodLib:
                                            newLib = WyeCore.World.libDict[txtLst[-2]]     # get current library
                                            if not hasattr(newLib, txtLst[-1]):
                                                #print("EditCodeCallback: Fail: ", txtLst[-1], " is not a valid verb in library", lib.__name__)
                                                goodLib = False
                                            else:
                                                newVerb = getattr(newLib,  txtLst[-1])
                                        if not goodLib:
                                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Invalid library.verb",
                                                    newTxt + " is not a valid library.verb.\nPlease enter a valid library.verb or Cancel",
                                                                                     Wye.color.ERROR_COLOR)
                                            newDlg = WyeUILib.Dialog.start(frame.SP)
                                            # clone old dialog params to new
                                            newDlg.params.title = dlgFrm.params.title
                                            newDlg.params.position = dlgFrm.params.position
                                            newDlg.params.parent = dlgFrm.params.parent
                                            newDlg.params.inputs = dlgFrm.params.inputs
                                            newDlg.params.format = dlgFrm.params.format
                                            newDlg.params.headerColor = dlgFrm.params.headerColor
                                            newDlg.params.callback = dlgFrm.params.callback
                                            newDlg.params.optData = dlgFrm.params.optData

                                            # push the copied dialog and go back to waiting
                                            #print("Pushed dialog to stack")
                                            frame.SP.append(newDlg)
                                            frame.status = Wye.status.CONTINUE
                                            return
                                        else:
                                            # replace oontents of tuple in newCodeDescr
                                            tuple.clear()
                                            tuple.append(newTxt)
                                            for param in newVerb.paramDescr:
                                                pTuple = ["Expr", "0 # <your param value here>"]
                                                tuple.append(pTuple)

                                            #delete the current row in the mother dialog
                                            inpIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0], btnFrm) - 1       # back up to edLn input
                                            lnFrm = parentFrm.params.inputs[0].pop(inpIx)[0]
                                            lnFrm.verb.close(lnFrm)
                                            lnEd = parentFrm.params.inputs[0].pop(inpIx)[0]
                                            lnEd.verb.close(lnEd)

                                            # generate new row(s)
                                            newRows = []
                                            editVerbFrm.verb.bldEditCodeLine(tuple, level, editVerbFrm, parentFrm, newRows, frame.vars.prefix[0])

                                            # Insert rows in dialog
                                            rIx = 0
                                            pos = [0,0,0]       # will be fixed when dialog redisplayed
                                            for row in newRows:
                                                parentFrm.params.inputs[0].insert(inpIx+rIx, row)
                                                row[0].verb.display(row[0], parentFrm, pos)
                                                rIx += 1

                                            # update dialog
                                            parentFrm.verb.redisplay(parentFrm)

                                    elif tuple[0] == "Verb":
                                        # delete any params from tuple
                                        delRowCt = len(tuple) - 1
                                        for ii in range(delRowCt):
                                            tuple.pop(-1)

                                        # delete any params from dialog
                                        inpIx = WyeCore.Utils.nestedIndexFind(parentFrm.params.inputs[0],
                                                                              btnFrm) - 1  # back up to edLn input
                                        for ii in range(delRowCt*2):
                                            parentFrm.params.inputs[0].pop(inpIx + 2)

                                        # update dialog
                                        parentFrm.verb.redisplay(parentFrm)
                            else:
                                verbType = tuple[0]
                                if verbType is None:
                                    verbType = "Code"
                                newOp = verbType

                            newTxt = dlgFrm.params.inputs[0][-2][0].params.value[0]
                            newTgt = dlgFrm.params.inputs[0][-1][0].params.value[0]
                            #print("EditCodeCallback done: newOp", newOp, "newTxt", newTxt)
                            # save back to code
                            tuple[0] = newOp
                            tuple[1] = newTxt

                            if tuple[0] == "IfGoTo":
                                if len(tuple) < 3:
                                    tuple.append(newTgt)
                                else:
                                    tuple[2] = newTgt

                            # update display
                            indent = "".join(["   " for l in range(level)])  # indent by recursion depth

                            prefix = frame.vars.prefix[0]

                            match tuple[0]:
                                case "Verb":
                                    pass

                                case "Code" | None:  # raw Python
                                    #print("indent", indent, " prefix", prefix)
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Code: " + str(tuple[1]))

                                case "CodeBlock":  # multi-line raw Python
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "CodeBLock: " + str(tuple[1]))

                                case "Expr":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Expression: " + str(tuple[1]))

                                case "Const":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Constant: " + str(tuple[1]))

                                case "Var":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Variable: " + str(tuple[1]))

                                case "Var=":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Variable=: " + str(tuple[1]))

                                case "Par=":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Parameter=: " + str(tuple[1]))

                                case "GoTo":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + " GoTo: " + str(tuple[1]))

                                case "Label":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "Label: " + str(tuple[1]))

                                case "IfGoTo":
                                    btnFrm.verb.setLabel(btnFrm, indent + prefix + "If: " + str(tuple[1]) + " GoTo: " + str(tuple[2]))

                                case _:  # raw Python
                                    print("EditCodeCallback done: unknown operation '"+tuple[0]+"'.  Default to Code")
                                    btnFrm.verb.setLabel(btnFrm, indent + "Code: " + str(tuple[1]))

                    # user switched to
                    #case 2:


        class EditParamCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("paramName", Wye.dType.STRING, "<name>"),
                        ("paramText", Wye.dType.STRING, "<description>"),
                        ("paramAccess", Wye.dType.STRING, "<access>"),
                        ("paramDefault", Wye.dType.STRING, ""),
                        )

            def start(stack):
                #print("EditParamCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditParamCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditParamCallback data", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editVerbFrm = data[1][2]
                editLnFrm = data[1][3]
                param = data[1][4]
                #print("param ix", data[1][0], " parentFrm", parentFrm.verb.__name__, " verb", editVerbFrm.vars.oldVerb[0].__name__)

                # find index to this row's param in EditVerb's newParamDescr
                paramIx = editVerbFrm.vars.newParamDescr[0].index(param)
                if paramIx < 0:
                    print("EditParamCallback ERROR: Failed to find", param, " in ", editVerbFrm.vars.newParamDescr[0])
                    frame.status = Wye.status.FAIL
                    return

                match (frame.PC):
                    case 0:
                        #print("EditParamCallback data='" + str(data) + "'")
                        # build param dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)

                        nParams = len(editVerbFrm.vars.newParamDescr[0])

                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Edit Parameter"]
                        dlgFrm.params.parent = [parentFrm]
                        #print("EditParamCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                        dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                        # param name
                        frame.vars.paramName[0] = editVerbFrm.vars.newParamDescr[0][paramIx][0]
                        paramNameFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        paramNameFrm.params.frame = [None]        # placeholder
                        paramNameFrm.params.label = ["Name: "]
                        paramNameFrm.params.value = frame.vars.paramName
                        WyeUILib.InputText.run(paramNameFrm)
                        dlgFrm.params.inputs[0].append([paramNameFrm])

                        # param type
                        frame.vars.paramText[0] = editVerbFrm.vars.newParamDescr[0][paramIx][1]
                        paramTypeFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        paramTypeFrm.params.frame = [None]
                        paramTypeFrm.params.label = ["Description: "]
                        paramTypeFrm.params.list = [[Wye.dType.tostring(x) for x in Wye.dType.valList]]
                        paramTypeFrm.params.selectionIx = [Wye.dType.valList.index(frame.vars.paramType[0])]
                        #paramTypeFrm.params.callback = [WyeUILib.EditVerb.EditParamTypeCallback]
                        #paramTypeFrm.params.optData = ((paramTypeFrm, dlgFrm, editVerbFrm, frame.vars.paramType[0]),)    # var to return chosen type in
                        paramTypeFrm.verb.run(paramTypeFrm)
                        dlgFrm.params.inputs[0].append([paramTypeFrm])

                        # param access method
                        frame.vars.paramAccess[0] = Wye.access.tostring(editVerbFrm.vars.newParamDescr[0][paramIx][2])
                        paramAccessFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        paramAccessFrm.params.frame = [None]
                        paramAccessFrm.params.label = ["Access: "]
                        paramAccessFrm.params.value = frame.vars.paramAccess
                        WyeUILib.InputText.run(paramAccessFrm)
                        dlgFrm.params.inputs[0].append([paramAccessFrm])

                        # param default value
                        if len(editVerbFrm.vars.newParamDescr[0][paramIx]) > 3:
                            frame.vars.paramDefault[0] = str(editVerbFrm.vars.newParamDescr[0][paramIx][3])
                        else:
                            frame.vars.paramDefault[0] = ""
                        WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "Default Value:", frame.vars.paramDefault)

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    # Edit Parameter dialog completed
                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS
                        # check status to see if values should be used
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            label = dlgFrm.params.inputs[0][0][0].params.value[0]
                            typeIx = dlgFrm.params.inputs[0][1][0].params.selectionIx[0]
                            if typeIx >= 0:
                                wType = Wye.dType.valList[typeIx]
                            else:
                                wType = frame.vars.paramType[0]
                            descrip = dlgFrm.params.inputs[0][2][0].params.value[0]
                            defaultVal = frame.vars.paramDefault[0]
                            # modify existing param so +/- can still find it
                            param[0] = label
                            param[1] = wType
                            param[2] = descrip
                            if defaultVal:
                                if len(param) == 3:
                                    param.append(defaultVal)
                                else:
                                    param[3] = defaultVal

                            #print("EditParamCallback done: inserted at ",paramIx," in newParamDescr\n", editVerbFrm.vars.newParamDescr[0])
                            rowTxt = "'" + label + "' " + Wye.dType.tostring(wType) + " description:" + descrip
                            if defaultVal:
                                rowTxt += " default:"+defaultVal
                            #print("new row", rowTxt)
                            btnFrm.verb.setLabel(btnFrm, rowTxt)



        # Param edit type button callback: put up dropdown for variable type
        class EditParamTypeCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("count", Wye.dType.INTEGER, 0),)

            def start(stack):
                #print("EditParamTypeCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditParamTypeCallback, stack)

            def run(frame):
                #print("EditParamTypeCallback")
                match (frame.PC):
                    case 0:
                        data = frame.eventData
                        print("EditParamTypeCallback data='" + str(data) + "'")
                        frm = data[1][0]
                        parentFrm = frm.parentDlg
                        #print("param ix", data[1][0], " data frame", frm.verb.__name__)
                        WyeUILib.Dialog.doCallback(parentFrm, frm, "none")
                        frame.PC += 1
                    case 1:
                        frame.status = Wye.status.SUCCESS
                        pass


        # Object variable callback: put up variable edit dialog
        class EditVarCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("varName", Wye.dType.STRING, "<name>"),
                        ("varType", Wye.dType.STRING, "<type>"),
                        ("varVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                #print("EditVarCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditVarCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("EditVarCallback data='" + str(data) + "'")
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editVerbFrm = data[1][2]
                editLnFrm = data[1][3]
                var = data[1][4]

                # find index to this row's param in EditVerb's newVarDescr
                varIx = editVerbFrm.vars.newVarDescr[0].index(var)
                if varIx < 0:
                    print("EditVarCallback ERROR: Failed to find", var, " in ", editVerbFrm.vars.newVarDescr[0])
                    frame.status = Wye.status.FAIL
                    return

                #print("EditVarCallback editVerbFrm", editVerbFrm.verb.__name__)
                #print("param ix", data[1][0], " parentFrm", parentFrm.verb.__name__, " verb", editVerbFrm.vars.oldVerb[0].__name__)

                match (frame.PC):
                    case 0:
                        # build var dialog
                        dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog("Edit Variable", parentFrm, (.5,-.3, -.5 + btnFrm.vars.position[0][2]))

                        # Var name
                        frame.vars.varName[0] = editVerbFrm.vars.newVarDescr[0][varIx][0]
                        WyeCore.libs.WyeUIUtilsLib.doInputText(dlgFrm, "Name: ", frame.vars.varName)


                        # Var type
                        frame.vars.varType[0] = editVerbFrm.vars.newVarDescr[0][varIx][1]
                        varTypeFrm = WyeUILib.InputDropdown.start(dlgFrm.SP)
                        varTypeFrm.params.frame = [None]
                        varTypeFrm.params.label = ["Type: "]
                        varTypeFrm.params.list = [[Wye.dType.tostring(x) for x in Wye.dType.valList]]
                        #print("EditVarCallback find ", frame.vars.varType[0], " in", Wye.dType.valList)
                        varTypeFrm.params.selectionIx = [Wye.dType.valList.index(frame.vars.varType[0])]
                        #varTypeFrm.params.callback = [WyeUILib.EditVerb.EditVarTypeCallback]
                        #varTypeFrm.params.optData = ((varTypeFrm, dlgFrm, editVerbFrm, frame.vars.varType[0]),)    # var to return chosen type in
                        varTypeFrm.verb.run(varTypeFrm)
                        dlgFrm.params.inputs[0].append([varTypeFrm])

                        # Var initial value
                        #print("EditVarCallback val", editVerbFrm.vars.newVarDescr[0][varIx][2])
                        frame.vars.varVal[0] = str(editVerbFrm.vars.newVarDescr[0][varIx][2])
                        varValFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        varValFrm.params.frame = [None]
                        varValFrm.params.label = ["Value: "]
                        if frame.vars.varType[0] == Wye.dType.STRING and (frame.vars.varVal is None or len(frame.vars.varVal) == 0):
                            varValFrm.params.value = ['']
                        else:
                            varValFrm.params.value = frame.vars.varVal
                        WyeUILib.InputText.run(varValFrm)
                        dlgFrm.params.inputs[0].append([varValFrm])

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS   # done
                        # check status to see if values should be updated
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            label = dlgFrm.params.inputs[0][0][0].params.value[0]
                            typeIx = dlgFrm.params.inputs[0][1][0].params.selectionIx[0]
                            if typeIx >= 0:
                                wType = Wye.dType.valList[typeIx]
                            else:
                                wType = frame.vars.varType[0]
                            initVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                            #print("EditVarCallbackDone: label", label, " typeIx", typeIx, " type", wType, " initVal", initVal)

                            # convert initVal to appropriate type
                            initVal = Wye.dType.convertType(initVal, wType)

                            var[0] = label
                            var[1] = wType
                            var[2] = initVal

                            rowTxt = "'" + label + "' " + Wye.dType.tostring(wType) + " = " + str(initVal)
                            #print("new row", rowTxt)
                            btnFrm.verb.setLabel(btnFrm, rowTxt)


        # Var edit type button callback: put up dropdown for variable type
        class EditVarTypeCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("count", Wye.dType.INTEGER, 0),)

            def start(stack):
                #print("EditVarTypeCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditVarTypeCallback, stack)

            def run(frame):
                #print("EditVarTypeCallback")

                data = frame.eventData
                #print("EditVarTypeCallback data='" + str(data) + "'")
                frm = data[1][0]
                parentFrm = frm.parentDlg
                WyeUILib.Dialog.doCallback(parentFrm, frm, "none")
                #print("param ix", data[1][0], " data frame", frm.verb.__name__)



        # build the verb and push it to its library
        class UpdateCodeCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                #print("UpdateCodeCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.UpdateCodeCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("UpdateCodeCallback data=", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                editFrm.verb.updateVerb(editFrm, parentFrm)


        # check code for compile errors and TODO - highlight anything that needs fixing
        class TestCodeCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                #print("TestCodeCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.TestCodeCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("TestCodeCallback data=", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                # build a verb and try to compile it
                #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Not Implemented", "Code test not implemented yet")

                # read settings
                modeFrm = editFrm.vars.settingsFrms[0]['mode']
                modeIx = modeFrm.params.selectionIx[0]
                if modeIx >= 0:
                    mode = Wye.mode.valList[modeIx]
                else:
                    mode = editFrm.vars.newVerbSettings[0]['mode']
                editFrm.vars.newVerbSettings[0]['mode'] = mode

                autoFrm = editFrm.vars.settingsFrms[0]['autoStart']
                autoStart = autoFrm.params.value[0]
                editFrm.vars.newVerbSettings[0]['autoStart'] = autoStart

                dTypeFrm = editFrm.vars.settingsFrms[0]['dataType']
                dTypeIx = dTypeFrm.params.selectionIx[0]
                dataType = Wye.dType.valList[dTypeIx]
                editFrm.vars.newVerbSettings[0]['dataType'] = dataType

                # print("New class settings\n mode", Wye.mode.tostring(mode), "\n autoStart", autoStart, "\n dataType", Wye.dType.tostring(dataType))

                # print("params\n"+str(frame.vars.newParamDescr))
                # print("vars\n"+str(frame.vars.newVarDescr))
                # print("code\n"+str(frame.vars.newCodeDescr))

                # get verb name
                name = editFrm.vars.nameFrm[0].params.value[0]
                if name:
                    name = name.strip()
                if not name:
                    name = "TestVerb"

                # existing library
                libList = [lib for lib in WyeCore.World.libList]
                lib = libList[editFrm.vars.existingLibFrm[0].params.selectionIx[0]]

                listFlag = editFrm.vars.listCodeFrm[0].params.value[0]
                #print("TestCodeCallback: List Code")
                WyeCore.Utils.createVerb(lib, name,
                                         editFrm.vars.newVerbSettings[0],
                                         editFrm.vars.newParamDescr[0],
                                         editFrm.vars.newVarDescr[0],
                                         editFrm.vars.newCodeDescr[0],
                                         True, listFlag)

        # Update lib name var
        class EditCodeSaveLibNameCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("EditCodeSaveLibNameCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditCodeSaveLibNameCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("EditCodeSaveLibNameCallback data=", data)
                txtFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                editFrm.vars.fileName[0] = txtFrm.vars.currVal[0]
                #print("Update filename to ", editFrm.vars.fileName[0])



        # Save edited code to a library file
        class EditCodeSaveLibCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("fileName", Wye.dType.STRING, ""),
                        ("doExistsQuery", Wye.dType.BOOL, False),
                        ("libName", Wye.dType.STRING, ""),
                        ("verbName", Wye.dType.STRING, ""),
                        ("lib", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                #print("EditCodeSaveLibCallback started")
                return Wye.codeFrame(WyeUILib.EditVerb.EditCodeSaveLibCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("EditCodeSaveLibCallback data=", data)
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                editFrm = data[1][2]

                # Save verb to library file
                match(frame.PC):
                    case 0:
                        # get lib name
                        fileName = editFrm.vars.fileName[0].strip()
                        if fileName:
                            # make sure there's an extension
                            libFileName = os.path.basename(fileName)
                            libName, ext = os.path.splitext(libFileName)
                            if not ext:
                                libFileName += ".py"
                        else:
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("File Not Saved",
                                                                     "ERROR: Invalid library file name '" + fileName + "'.  Library not saved",
                                                                     color=Wye.color.WARNING_COLOR)
                            # print("ERROR: Invalid library file name '"+ fileName +"'.  Library not saved")
                            frame.status = Wye.status.SUCCESS
                            return

                        verbName = editFrm.vars.nameFrm[0].vars.currVal[0].strip()
                        if not verbName:
                            WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("File Not Saved",
                                                                     "ERROR: Invalid verb name '" + verbName + "'.  Verb not saved to library",
                                                                     color=Wye.color.WARNING_COLOR)
                            # print("ERROR: Invalid library file name '"+ fileName +"'.  Library not saved")
                            frame.status = Wye.status.SUCCESS
                            return
                        frame.vars.verbName[0] = verbName

                        # Is the lib in memory already?
                        lib = None
                        if libName in WyeCore.World.libDict:
                            lib = WyeCore.World.libDict[libName]

                            # make sure we can save it
                            if hasattr(lib, "systemLib"):
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Library",
                                                                         "System libraries cannot be saved",
                                                                         Wye.color.WARNING_COLOR)
                                frame.status = Wye.status.SUCCESS
                                return

                        frame.vars.lib[0] = lib
                        frame.vars.fileName[0] = fileName
                        frame.vars.libName[0] = libName

                        # if the file alredy exists, as the user what they want to do
                        fileExists = os.path.exists(fileName)
                        frame.vars.doExistsQuery[0] = fileExists
                        if frame.vars.doExistsQuery[0]:
                            title = fileName + " Already Exists"
                            pos = btnFrm.vars.position[0]
                            pos = [pos[0] + .5, pos[1] - .5, pos[2] - .5]
                            askSaveFrm = WyeCore.libs.WyeUIUtilsLib.doAskSaveAsFileAsync(frame, parentFrm,
                                                                                         fileName, position=pos,
                                                                                         title=title)
                            frame.SP.append(askSaveFrm)  # push dialog so it runs next cycle

                        frame.PC = 1  # on return from dialog, run save lib case
                        #print("EditCodeSaveLibCallback: case 0: save library")

                    case 1:
                        frame.status = Wye.status.SUCCESS       # make sure we exit, one way or another

                        # if we asked the user about overwrite, get the final filename
                        if frame.vars.doExistsQuery[0]:
                            askSaveFrm = frame.SP.pop()
                            print("EditCodeSaveLibCallback: case 1: askSaveFrm", askSaveFrm.verb.__name__,
                                  " user status", Wye.status.tostring(askSaveFrm.params.retVal[0]))

                            # if the user cancelled, don't save the lib
                            if askSaveFrm.params.retVal[0] != Wye.status.SUCCESS:
                                #print("User cancelled saving library")
                                return

                            # get the filename
                            fileName = askSaveFrm.params.fileName[0].strip()
                            if not fileName:
                                WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Invalid File Name", "'"+fileName+"' is not a valid library file name",
                                                       Wye.color.WARNING_COLOR)
                                frame.status = Wye.status.SUCCESS
                                return
                            frame.vars.fileName[0] = fileName
                            print("EditCodeSaveLibCallback: save lib to", fileName)

                        else:
                            fileName = frame.vars.fileName[0]

                        # force lib name to match file name
                        libName = os.path.splitext(os.path.basename(fileName))[0]

                        # gen lib code
                        outStr = WyeCore.Utils.createLibString(libName)

                        verbName = frame.vars.verbName[0]


                        # get the soure lib, if there is one
                        lib = frame.vars.lib[0]

                        if lib:
                            # create library header text and add text for all its verbs
                            print("EditCodeSaveLibCallback: lib", lib.__name__, " already exists, parse it for verbs")
                            for attr in dir(lib):
                                if attr != "__class__":
                                    verb = getattr(lib, attr)
                                    if inspect.isclass(verb):
                                        # ignore the verb we're saving
                                        if verb.__name__ != verbName:
                                            # can only export verbs that have the required data
                                            if hasattr(verb, "paramDescr") and hasattr(verb, "varDescr") and hasattr(verb, "codeDescr"):
                                                # capture the flags
                                                verbSettings = {}
                                                if hasattr(verb, 'mode'):
                                                    verbSettings['mode'] = verb.mode
                                                if hasattr(verb, 'cType'):
                                                    verbSettings['cType'] = verb.cType
                                                if hasattr(verb, 'parTermType'):
                                                    verbSettings['parTermType'] = verb.parTermType
                                                if hasattr(verb, 'autoStart'):
                                                    verbSettings['autoStart'] = verb.autoStart
                                                if hasattr(verb, 'dataType'):
                                                    verbSettings['dataType'] = verb.dataType

                                                # gen verb code
                                                print("EditCodeSaveLibCallback: copy ", verb.__name__, " from lib", lib.__name__)
                                                vrbStr = WyeCore.Utils.createVerbString(libName, verb.__name__,
                                                            verbSettings,  verb.paramDescr,  verb.varDescr,
                                                            verb.codeDescr, doTest=False, outDent=False)

                                                outStr += vrbStr
                                            else:
                                                # ignoring generated runtime code is good.  Anything else is a problem
                                                if not verb.__name__[-3:] == "_rt":
                                                    print("WARNING: Verb", verb.__name__,
                                                      " not saved to file because it does not have all required attributes")
                                        else:
                                            print("copying from lib", lib.__name__, " skip verb", verb.__name__)


                        # gen verb code
                        print("EditCodeSaveLibCallback: put new", verbName, " in lib", libName)
                        vrbStr = WyeCore.Utils.createVerbString(libName, verbName, editFrm.vars.newVerbSettings[0],
                                    editFrm.vars.newParamDescr[0], editFrm.vars.newVarDescr[0], editFrm.vars.newCodeDescr[0],
                                    doTest=False, outDent=False)
                        #print("outStr\n"+ outStr)
                        #print("vrbStr\n"+ vrbStr)

                        outStr += vrbStr
                        try:
                            # write the file
                            f = open(fileName, "w")
                            f.write(outStr)
                            f.close()
                        except Exception as e:
                            print("Failed to write library '"+libName+"' to file '"+fileName+"'\n", str(e))
                            traceback.print_exception(e)
                            frame.status = Wye.status.SUCCESS
                            return

                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("Saved Library", "Wrote "+verbName+" to "+fileName)
                        #print("EditCodeSaveLibCallback: Wrote verb ", verbName, " to library file", libFileName)



    # show active objects (currently running object stacks)
    # so user can debug them
    class DebugMain:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("objFrm", Wye.dType.OBJECT, Wye.access.REFERENCE),)  # object frame to edit
        varDescr = (("dlgFrm", Wye.dType.OBJECT, None),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    ("nRunningFrm", Wye.dType.OBJECT, None),
                    ("rows", Wye.dType.OBJECT_LIST, None)      # list of refreshable objects
                    )


        def start(stack):
            f = Wye.codeFrame(WyeUILib.DebugMain, stack)         # not stopped by breakAll or debugger debugger
            f.systemObject = True
            f.vars.rows[0] = []
            return f

        def run(frame):
            match(frame.PC):
                case 0:
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,Wye.UI.DIALOG_OFFSET,0))
                    pos = point.getPos()
                    point.removeNode()

                    # create top level debug dialog
                    dlgFrm = WyeUILib.Dialog.start(frame.SP)
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Wye Debugger"]
                    dlgFrm.systemObject = True
                    dlgFrm.params.format = [["NO_CANCEL"]]
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]
                    frame.vars.dlgFrm[0] = dlgFrm

                    # build dialog

                    breakAllFrm = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "  Pause World", [Wye.breakAll], WyeUILib.DebugMain.BreakAllCallback)
                    breakAllFrm.params.optData = [(breakAllFrm,)]

                    # refresh list of running objects
                    refreshFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Refresh List", WyeUILib.DebugMain.RefreshCallback)
                    refreshFrm.params.optData = [(frame, dlgFrm)]

                    # running objects
                    nRunningFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm,"Active Objects: "+str(len(WyeCore.World.objStacks)), color=Wye.color.SUBHD_COLOR)
                    frame.vars.nRunningFrm[0] = nRunningFrm

                    attrIx = [0]
                    row = [0]
                    # recursively display stack contents
                    for stack in WyeCore.World.objStacks:
                        WyeUILib.DebugMain.listStack(stack, dlgFrm, row, attrIx, frame, level=0, top=True)
                        attrIx[0] += 1

                    # if nothing running
                    if attrIx == 0:
                        WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "<no active objects>")
                        frame.vars.rows[0].append(dlgFrm.params.inputs[-1])

                    # WyeUILib.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    frame.SP.pop()  # remove dialog frame from stack

                    # if paused wld, unpause it
                    Wye.breakAll = False

                    frame.status = Wye.status.SUCCESS  # done

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.debugger)
                    WyeCore.World.debugger = None


        def listStack(stack, dlgFrm, rowIx, attrIx, frame, level, prefix="stack", top=False):
            #if top and len(stack) > 0:
            #        print("listStack top", stack[0].verb.__name__)
            #print("listStack level", level, " prefix", prefix, " top", top)
            indent = "".join(["  " for l in range(level)])      # indent by recursion depth
            sLen = len(stack)
            if sLen > 0:  # if there's something on the stack
                offset = 0
                for objFrm in stack:

                    # only let user delete top level non-system objects on regular stack
                    if top and offset == 0 and prefix == "stack" and not hasattr(stack[0], "systemObject"):       # HACK!
                        doKillBtn = True
                    else:
                        doKillBtn = False

                    if doKillBtn:
                        delFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "Del", WyeUILib.DebugMain.KillFrameCallback)
                        delFrm.params.optData = [(delFrm, frame, dlgFrm, objFrm),]
                        frame.vars.rows[0].append(delFrm)
                    else:
                        noDelFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "     .")
                        frame.vars.rows[0].append(noDelFrm)

                    # make the dialog row
                    if offset == 0:
                        label = indent + "  "+prefix+" " + str(attrIx[0]) + " depth " + str(offset) + ":" + objFrm.verb.__name__
                    else:
                        label = indent + "                depth " + str(offset) + ":" + objFrm.verb.__name__
                    if hasattr(stack[0], "systemObject"):
                        bg = Wye.color.LIGHT_YELLOW
                    elif hasattr(stack[0], "doBreakPt"):
                        bg = Wye.color.LIGHT_RED
                    else:
                        bg = Wye.color.TRANSPARENT
                    btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, label, WyeUILib.DebugMain.DebugFrameCallback, backgroundColor=bg)
                    btnFrm.params.layout = [Wye.layout.ADD_RIGHT]
                    btnFrm.params.optData = [(rowIx[0], btnFrm, dlgFrm, objFrm, frame)]   # button row, row frame, dialog frame, obj frame
                    frame.vars.rows[0].append(btnFrm)         # save ref to input so can delete it later
                    offset += 1
                    rowIx[0] += 1


                # if top frame is repeateEventCallbackDict show all the events
                firstFrm = stack[0]
                if firstFrm.verb == WyeCore.World.repeatEventExecObj:
                    pAttrIx = [0]
                    prefix = "RepEvt"
                    #print("Children of repeatEventExecObj")
                    for evtID in WyeCore.World.repeatEventCallbackDict:
                       #print("  evtID", evtID)
                        evt = WyeCore.World.repeatEventCallbackDict[evtID]
                        evtStk = evt[0]
                        if len(evtStk) > 0:  # if there's something on the stack
                            #print(" repeatEventExecObj child evt", evt, " level", level, " prefix", prefix)
                            WyeUILib.DebugMain.listStack(evtStk, dlgFrm, rowIx, pAttrIx, frame, level + 1, prefix=prefix)
                            pAttrIx[0] += 1
                            rowIx[0] += 1

                # if bottom frame is a parallel frame, do all its stacks
                lastFrm = stack[-1]
                if isinstance(lastFrm, Wye.parallelFrame):
                    pAttrIx = [0]
                    for pStack in lastFrm.stacks:
                        WyeUILib.DebugMain.listStack(pStack, dlgFrm, rowIx, pAttrIx, frame, level + 1, prefix=prefix)
                        pAttrIx[0] += 1
                        rowIx[0] += 1


        # replace the task rows
        def update(frame, dlgFrm):
            #print("DebugMain.update: frame", frame.verb.__name__)
            #print("                        dlgFrm", dlgFrm.verb.__name__)

            # delete all dialog task input rows
            #print("Before clear dialog task rows, inputs len", len(dlgFrm.params.inputs[0]))
            delCt = 0
            for bFrmRef in frame.vars.rows[0]:
                inpIx = WyeCore.Utils.nestedIndexFind(dlgFrm.params.inputs[0], bFrmRef)
                oldFrm = dlgFrm.params.inputs[0].pop(inpIx)[0]
                if oldFrm in dlgFrm.vars.clickedBtns[0]:
                    dlgFrm.vars.clickedBtns[0].remove(oldFrm)
                #print(" remove", oldFrm.verb.__name__, " ", oldFrm.params.label[0])
                oldFrm.verb.close(oldFrm)   # remove graphic content
                delCt+= 1
            #print("after delete", delCt," dialog rows, inputs len", len(dlgFrm.params.inputs[0]))
            frame.vars.rows[0].clear()      # old inputs gone

            # rebuild dialog task input rows
            attrIx = [0]
            row = [0]
            for stack in WyeCore.World.objStacks:
                WyeUILib.DebugMain.listStack(stack, dlgFrm, row, attrIx, frame, 0, top=True)
                attrIx[0] += 1

            # if nothing running
            if attrIx == 0:
                #print("DebugMain.update: ERROR - it thinks nothings running")
                lbl = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "<no active objects>")
                frame.vars.rows[0].append(lbl)

            # generate display elements for rows (correct pos calc by redisplay, below)
            pos = [0, 0, 0]
            for frm in frame.vars.rows[0]:
                frm.verb.display(frm, dlgFrm, pos)

            # update n running top level tasks
            nRnFrm = frame.vars.nRunningFrm[0]
            nRnFrm.verb.setLabel(nRnFrm, "Active Objects: "+str(len(WyeCore.World.objStacks)))

            #print("after rebuild dialog task rows, inputs len", len(dlgFrm.params.inputs[0]))

            dlgFrm.vars.currInp[0] = None  # we just deleted it, so clear it
            dlgFrm.verb.redisplay(dlgFrm)  # redisplay the dialog


        # User selected an object, open its frame in the debugger
        class DebugFrameCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),

                        )

            def start(stack):
                # print("DebugFrameCallback started")
                f = Wye.codeFrame(WyeUILib.DebugMain.DebugFrameCallback, stack)
                f.systemObject = True  # not stopped by breakAll o rdebugger
                return f


            def run(frame):
                #print("DebugFrameCallback")
                data = frame.eventData
                #print("DebugFrameCallback data='" + str(data) + "'")
                objRow = data[1][0]
                btnFrm = data[1][1]
                parentDlg = data[1][2]
                objFrm = data[1][3]
                mainDbgFrm = data[1][4]
                #print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)

                 # get the world position of the relative location of the dialog row the user clicked on
                objOffset = -.5 + btnFrm.vars.position[0][2]
                objPos = (2, -.5, objOffset)
                point = NodePath("point")
                point.reparentTo(render)
                point.setPos(parentDlg.vars.dragObj[0]._path, objPos)
                pos = point.getPos()
                point.removeNode()

                # launch debugger as stand alone dialog so can debug multiple objs at once
                stk = []
                dbgFrm = WyeUILib.ObjectDebugger.start(stk)
                dbgFrm.systemObject = True
                dbgFrm.params.objFrm = [objFrm]
                dbgFrm.params.position = [[pos[0], pos[1], pos[2]],]
                dbgFrm.params.parent = [None]
                stk.append(dbgFrm)
                dbgFrm.verb.run(dbgFrm)
                WyeCore.World.startActiveFrame(dbgFrm)

        # User selected an object, open its frame in the debugger
        class KillFrameCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),

                        )

            def start(stack):
                # print("KillFrameCallback started")
                f = Wye.codeFrame(WyeUILib.DebugMain.KillFrameCallback, stack)
                f.systemObject = True  # not stopped by breakAll o rdebugger
                return f


            def run(frame):
                global base
                #print("KillFrameCallback")

                data = frame.eventData
                #print("KillFrameCallback data='" + str(data) + "', case", frame.PC)
                delLnFrm = data[1][0]
                mainDbgFrm = data[1][1]
                dlgFrm = data[1][2]
                objFrm = data[1][3]

                match(frame.PC):
                    case 0:
                        #print("KillFrame delLnFrm", delLnFrm.verb.__name__, " ", delLnFrm.params.label[0])
                        #print("  mainDbgFrm", mainDbgFrm.verb.__name__)
                        #print("  dlgFrm", dlgFrm.verb.__name__, " ", dlgFrm.params.title[0])
                        #print("  objFrm", objFrm.verb.__name__)

                        #print("KillFrameCallback: stop", objFrm.verb.__name__)
                        #print("Before stop, ")
                        WyeCore.World.stopActiveObject(objFrm)

                        frame.PC += 1

                    # delay 2 frames to let object get removedd
                    case 1:
                        frame.PC += 1

                    case 2:
                        frame.status = Wye.status.SUCCESS

                        # object has stopped by now
                        # if the object has any graphic elements, delete them
                        if hasattr(objFrm.vars, "cleanUpObjs"):
                            for obj in objFrm.vars.cleanUpObjs[0]:
                                #base.loader.unloadModel(obj)
                                obj.removeNode()

                        try:
                            mainDbgFrm.verb.update(mainDbgFrm, dlgFrm)
                        except Exception as e:
                            print("KillFrame: ERROR DebugMain.update:\n", str(e))
                            traceback.print_exception(e)

        # Toggle world pause flag Wye.breakAll
        class BreakAllCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),

                        )

            def start(stack):
                # print("BreakAllCallback started")
                return Wye.codeFrame(WyeUILib.DebugMain.BreakAllCallback, stack)

            def run(frame):
                data = frame.eventData
                chkFrm = data[1][0]
                Wye.breakAll = chkFrm.params.value[0]

        # Toggle world pause flag Wye.breakAll
        class RefreshCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),
                        )

            def start(stack):
                # print("RefreshCallback started")
                return Wye.codeFrame(WyeUILib.DebugMain.RefreshCallback, stack)

            def run(frame):
                data = frame.eventData
                dbgMainFrm = data[1][0]
                dlgFrm = data[1][1]
                dbgMainFrm.verb.update(dbgMainFrm, dlgFrm)

    # Open up an object and debug it
    class ObjectDebugger:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("objFrm", Wye.dType.OBJECT, Wye.access.REFERENCE),  # object frame to edit
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE),  # object position
                      ("parent", Wye.dType.OBJECT, Wye.access.REFERENCE),  # object parent
                      )
        varDescr = (("dlgFrm", Wye.dType.OBJECT, None),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    ("paramInpLst", Wye.dType.OBJECT_LIST, None),
                    ("varInpLst", Wye.dType.OBJECT_LIST, None),
                    ("codeInpLst", Wye.dType.OBJECT_LIST, None),
                    ("breakLst", Wye.dType.OBJECT_LIST, None),
                    ("isSysObj", Wye.dType.BOOL, False),
                    )

        # global list of frames being edited
        activeObjs = {}

        def start(stack):
            # print("ObjectDebugger started")
            f = Wye.codeFrame(WyeUILib.ObjectDebugger, stack)
            f.vars.paramInpLst[0] = []
            f.vars.varInpLst[0] = []
            f.vars.codeInpLst[0] = []
            f.vars.breakLst[0] = []
            f.systemObject = True         # not stopped by breakAll or debugger
            return f

        def run(frame):
            objFrm = frame.params.objFrm[0]

            match (frame.PC):
                case 0:
                    # only debug given frame once
                    if objFrm in WyeUILib.ObjectDebugger.activeObjs:
                        #print("Already debugging this object", objFrm.verb.__name__)
                        # take self off active object list
                        WyeCore.World.stopActiveObject(frame)
                        frame.status = Wye.status.FAIL

                        dlgFrm = WyeUILib.ObjectDebugger.activeObjs[objFrm]
                        path = dlgFrm.vars.dragObj[0]._path
                        path.setPos(base.camera, (0, Wye.UI.DIALOG_OFFSET - .5, 0))
                        path.setHpr(base.camera, 0, 1, 0)
                        return

                    if len(objFrm.SP) == 0:
                        #print("Object", objFrm.verb.__name__, " no longer running")
                        WyeCore.World.stopActiveObject(frame)
                        frame.status = Wye.status.FAIL
                        return

                        ## bring lib in front of user
                        #frm = WyeUILib.ObjectDebugger.activeObjs[objFrm]
                        #frm.vars.dragObj[0].setPos(base.camera, 0, Wye.UI.DIALOG_OFFSET, 0)
                        #frm.vars.dragObj[0].setHpr(base.camera, 0, 1, 0)


                    # if it's a systemObject (immune from Wye.breakAll) don't debug it
                    if hasattr(objFrm.SP[0], "systemObject"):
                        #print("This is a system object, it must stay running")
                        WyeCore.World.stopActiveObject(frame)
                        frame.status = Wye.status.FAIL
                        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog("System Object", "Cannot debug a system object", Wye.color.WARNING_COLOR)
                        return

                    # print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)

                    # Display contents of frame in a dialog

                    # If parallel subframe, get parent frame data
                    if objFrm.verb is WyeCore.ParallelStream:
                        paramDescr = objFrm.parentFrame.verb.paramDescr
                        varDescr = objFrm.parentFrame.verb.varDescr
                        name = objFrm.parentFrame.verb.__name__
                        objFrm.parentFrame.breakpt = True
                        # todo - recheck this logic for how to break on parallel frames
                        botStkFrm = objFrm.parentFrame.SP[-1]
                        if botStkFrm != objFrm.parentFrame:
                            botStkFrm.breakpt = True
                            #print("Actual break on obj", botStkFrm.verb.__name__)
                        Wye.debugOn += 1  # make sure debugging is happening
                        #print("ObjectDebugger: set parallel parent breakpt on", objFrm.parentFrame.verb.__name__," debugOn to", Wye.debugOn)
                    else:
                        paramDescr = objFrm.verb.paramDescr
                        varDescr = objFrm.verb.varDescr
                        name = objFrm.verb.__name__
                        objFrm.breakpt = True
                        botStkFrm = objFrm.SP[-1]
                        if botStkFrm != objFrm:
                            botStkFrm.breakpt = True
                            #print("Actual break at bot of stack on", objFrm.SP[-1].verb.__name__)
                        Wye.debugOn += 1  # make sure debugging is happening
                        #print("ObjectDebugger: set breakpt on", objFrm.verb.__name__," debugOn to", Wye.debugOn)

                    dlgFrm = WyeUILib.Dialog.start(frame.SP)
                    frame.vars.dlgFrm[0] = dlgFrm
                    dlgFrm.systemObject = True      # keep this dialog running if Wye.breakAll set, don't allow debugging of it

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Debug '" + name + "'"]
                    dlgFrm.params.format = [["NO_CANCEL"]]
                    dlgFrm.params.position = [[frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2]],]
                    #print("ObjectDebugger frame.params.parent[0]", frame.params.parent[0])
                    if len(frame.params.parent) == 0 or isinstance(frame.params.parent[0], list):
                        dlgFrm.params.parent = [None]
                    else:
                        dlgFrm.params.parent = frame.params.parent

                    # Step

                    # note, do long form so can gt runChkFrm before create btnFrm, but then PUT runChkFrm AFTER btnFrm
                    runChkFrm = WyeUILib.InputCheckbox.start(dlgFrm.SP)    # Do early, Need to pass to step

                    btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Step", WyeUILib.ObjectDebugger.DebugStepCallback, color = (1,1,0,1))
                    btnFrm.params.optData = [(btnFrm, dlgFrm, objFrm, frame, runChkFrm)]  # button row, dialog frame

                    # note: step needs runChkFrm to hack run state
                    #runChkFrm = WyeUILib.InputCheckbox.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([runChkFrm])
                    runChkFrm.params.frame = [None]
                    runChkFrm.params.parent = [None]
                    runChkFrm.params.value = [False]
                    runChkFrm.params.label = ["  Toggle Run"]
                    runChkFrm.params.callback = [WyeUILib.ObjectDebugger.RunCallback]  # button callback
                    runChkFrm.params.optData = [(runChkFrm, objFrm, frame)]
                    runChkFrm.params.color = [(1, 1, 0, 1)]
                    runChkFrm.verb.run(runChkFrm)

                    # refresh var values in dialog
                    btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Refresh Values", WyeUILib.ObjectDebugger.DebugRefreshVarCallback, color = (1, 1, 0, 1))
                    btnFrm.params.optData = [(btnFrm, dlgFrm, objFrm, frame)]  # button row, dialog frame

                    # delete running verb
                    delBtnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Delete This Instance and Close Debug", WyeUILib.ObjectDebugger.DebugKillCallback, color = (1,1,0,1))
                    delBtnFrm.params.optData = [(delBtnFrm, frame, dlgFrm, objFrm)]  # button row, dialog frame

                    # delete running verb
                    edBtnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, "  Open Verb Source in Editor", WyeUILib.ObjectDebugger.DebugEditCallback, color = (1,1,0,1))
                    edBtnFrm.params.optData = [(edBtnFrm, frame, dlgFrm, objFrm)]  # button row, dialog frame

                    #print("ObjectDebugger objFrm", objFrm.tostring())
                    # params
                    lblFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]  # return value
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Parameters:"]
                    lblFrm.params.color = [Wye.color.SUBHD_COLOR]
                    WyeUILib.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if len(paramDescr) > 0:     # if we have params, list them

                        attrIx = 0

                        for param in paramDescr:
                            # make the dialog row
                            btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [None]  # return value
                            btnFrm.params.parent = [None]
                            paramVal = getattr(objFrm.params, param[0])
                            btnFrm.params.label = ["  '" + param[0] + "' " + Wye.dType.tostring(
                                param[1]) + " = " + str(paramVal)]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugParamCallback]  # button callback
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm, frame)]  # button row, dialog frame
                            WyeUILib.InputButton.run(btnFrm)

                            attrIx += 1

                    # else nothing to do here
                    else:
                        # todo fix this so it will work
                        editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [WyeUILib.EditVerb.modParamOpList], [0], WyeUILib.EditVerb.EditParamLineCallback, showText=False)
                        lblFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  <no parameters>", layout=Wye.layout.ADD_RIGHT)
                        editLnFrm.params.optData = [(editLnFrm, dlgFrm, lblFrm, None)]

                    # vars
                    WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Variables:", color=Wye.color.SUBHD_COLOR)

                    if len(varDescr) > 0:       # if we have variables, list them

                        attrIx = 0

                        for var in varDescr:
                            # make the dialog row
                            varVal = getattr(objFrm.vars, var[0])
                            label = "  '" + var[0] + "' " + Wye.dType.tostring(var[1]) + " = " + str(varVal[0])
                            btnFrm = WyeCore.libs.WyeUIUtilsLib.doInputButton(dlgFrm, label, WyeUILib.ObjectDebugger.DebugVarCallback)
                            frame.vars.varInpLst[0].append(btnFrm)
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm, frame)]  # button row, dialog frame
                            attrIx += 1


                    # else nothing to do here
                    else:
                        # todo - make this work
                        editLnFrm = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "  +/-", [WyeUILib.EditVerb.modVarOpList], [0], WyeUILib.EditVerb.EditParamLineCallback, showText=False)
                        lblFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  <no variables>")
                        editLnFrm.params.optData = [(editLnFrm, dlgFrm, lblFrm, None)]

                    # build dialog frame params list of input frames
                    lblFrm = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Wye Code:", color = Wye.color.SUBHD_COLOR)

                    if objFrm.verb is WyeCore.ParallelStream:
                        oFrm = objFrm.parentFrame
                    else:
                        oFrm = objFrm
                    if hasattr(oFrm.verb, "codeDescr"):
                        codeDescr = oFrm.verb.codeDescr

                        # if debugging parallel code, show all the streams
                        if oFrm.verb.mode == Wye.mode.PARALLEL:
                            #print("verb", oFrm.verb.__name__," has", len(codeDescr), " streams")
                            streamIx = 0
                            # loop through the stream code showing first level code lines
                            for parDescr in codeDescr:
                                WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  " + parDescr[0])

                                # find the frame for this stream
                                chldStk = oFrm.stacks[streamIx]
                                if len(chldStk) > 0:
                                    chldFrm = chldStk[0]
                                    caseIx = str(-1)
                                else:
                                    chldFrm = None
                                    caseIx = 0

                                # create stream's code line
                                WyeUILib.ObjectDebugger.bldDebugCodeLines(parDescr[1], dlgFrm, frame, chldFrm, streamIx)
                                streamIx += 1

                        # regular boring normal single stream code
                        else:
                            # create first level code lines
                            WyeUILib.ObjectDebugger.bldDebugCodeLines(codeDescr, dlgFrm, frame, oFrm, 0)

                    WyeUILib.ObjectDebugger.activeObjs[objFrm] = dlgFrm

                    # WyeUILib.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle
                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done
                    # if user closed dialog
                    print("ObjDebugger case 1, done: dlgFrm", dlgFrm.verb.__name__)
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        #print("ObjDebugger:", dlgFrm.params.title[0], " returned status", frame.vars.dlgStat[0])  # Wye.status.tostring(frame.))

                        WyeUILib.ObjectDebugger.activeObjs.pop(objFrm)

                        # turn obj breakpt off
                        objFrm = frame.params.objFrm[0]
                        if objFrm.verb is WyeCore.ParallelStream:
                            objFrm.parentFrame.breakpt = False
                            objFrm.parentFrame.SP[-1].breakpt = False   # if wasn't bottom of stack and there was break there too,
                            if hasattr(objFrm.parentFrame.SP[0], "doBreakPt"):
                                delattr(objFrm.parentFrame.SP[0], "doBreakPt")

                            #print("ObjectDebugger remove breakpt on", objFrm.parentFrame.verb.__name__," reduce debugOn to", Wye.debugOn)
                            if hasattr(objFrm.parentFrame, "prevStatus"):
                                objFrm.status = objFrm.parentFrame.prevStatus


                        else:
                            objFrm.breakpt = False
                            objFrm.SP[-1].breakpt = False   # if wasn't bottom of stack and there was break there too,
                            if hasattr(objFrm.SP[0], "doBreakPt"):
                                delattr(objFrm.SP[0], "doBreakPt")
                            #print("ObjectDebugger remove breakpt on", objFrm.verb.__name__," reduce debugOn to", Wye.debugOn)
                            if hasattr(objFrm, "prevStatus"):
                                objFrm.status = objFrm.prevStatus


                    Wye.debugOn -= 1

                # User selected an object, open its frame in the debugger


        def bldDebugCodeLines(codeDescr, dlgFrm, frame, verbFrm, streamIx):
            rowOffset = len(dlgFrm.params.inputs[0])    # get index of first row in this stream (if multiple)
            # draw the top level code rows
            tupleLst = None # assume we got nuthin
            # see if we actually have debug data
            dbgVerbFrm = verbFrm
            print("debug frame", verbFrm.verb.__name__, " streamIx", streamIx)
            if hasattr(verbFrm, "parentFrame"): # if this is a parallel stream frame, the parent has the debug data
                print("frame", verbFrm.verb.__name__, " is stream.  Go up to parent", verbFrm.parentFrame.verb.__name__)
                dbgVerbFrm = verbFrm.parentFrame
            if hasattr(dbgVerbFrm.verb, "caseCodeDictLst"):
                print("bldDebugCodeLines verb", dbgVerbFrm.verb.__name__, " caseCodeDictLst len", len(dbgVerbFrm.verb.caseCodeDictLst), " lst", dbgVerbFrm.verb.caseCodeDictLst)
                dict = dbgVerbFrm.verb.caseCodeDictLst[streamIx]   # get the case -> row dict for this stream (0 if not parallel)
                if "0" in dict:     # we're starting at the first case in stream
                    tupleLst = dict["0"]
                    print("verb", dbgVerbFrm.verb.__name__, " tupleLst for case 0:", tupleLst)
                else:
                    print("bldDebugCodeLines verb", dbgVerbFrm.verb.__name__, " caseCodeDictLst entry for case 0")
            else:
                print("bldDebugCodeLines verb", dbgVerbFrm.verb.__name__, " has no caseCodeDictLst")
            rowIx = 0
            for tuple in codeDescr:
                # make the dialog row
                # >> disable debug on code lines until decide how to actually do it! <<
                # btnFrm = WyeUILib.InputButton.start(dlgFrm.SP)
                btnFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                dlgFrm.params.inputs[0].append([btnFrm])
                frame.vars.codeInpLst[0].append(btnFrm)
                btnFrm.params.frame = [None]  # return value
                btnFrm.params.parent = [None]
                btnFrm.params.color = [Wye.color.DISABLED_COLOR]
                # highlight currently executing section of code
                if tupleLst and rowIx in tupleLst:
                    print(" highlight row", rowIx)
                    btnFrm.params.backgroundColor = [Wye.color.LIGHT_GREEN]

                # fill in text and callback based on code row type
                if tuple[0] is None:
                    btnFrm.params.label = ["  Code: " + str(tuple[1])]
                    btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugParamCallback]  # button callback
                elif "." in tuple[0]:
                    vStr = str(tuple[0])
                    if vStr.startswith("WyeCore.libs."):
                        vStr = vStr[13:]
                    btnFrm.params.label = ["  Verb: " + vStr + ", " + str(tuple[1])]
                    btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugVerbCallback]  # button callback
                else:
                    match tuple[0]:
                        case "Code":  # raw Python
                            btnFrm.params.label = ["  Code: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback
                        case "CodeBlock":  # multi-line raw Python
                            btnFrm.params.label = ["  CodeBLock: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback
                        case "Expr":
                            btnFrm.params.label = ["  Expression: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback
                        case "Const":
                            btnFrm.params.label = ["  Constant: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.DebugCodeCallback]  # button callback

                        case "Var":
                            btnFrm.params.label = ["  Variable: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback

                        case "Var=":
                            btnFrm.params.label = ["  Variable=: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback

                        case "Par=":
                            btnFrm.params.label = ["  Parameter=: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugCodeCallback]  # button callback

                        case "GoTo":
                            btnFrm.params.label = ["  GoTo: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugSpecialCallback]  # button callback

                        case "Label":
                            btnFrm.params.label = ["  Label: " + str(tuple[1])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugSpecialCallback]  # button callback

                        case "IfGoTo":
                            btnFrm.params.label = ["  If: " + str(tuple[1]) + " GoTo: " + str(tuple[2])]
                            btnFrm.params.callback = [WyeUILib.ObjectDebugger.DebugSpecialCallback]  # button callback

                btnFrm.params.optData = [(btnFrm, dlgFrm, verbFrm, tuple)]  # button row, dialog frame
                btnFrm.verb.run(btnFrm)
                rowIx += 1        # row in this stream

        # Update variable values and current-row highlight
        def update(frame):
            objFrm = frame.params.objFrm[0]
            #print("frame", frame.verb.__name__, " vars.dlgFrm", frame.vars.dlgFrm[0])
            if objFrm.verb is WyeCore.ParallelStream:
                varDescr = objFrm.parentFrame.verb.varDescr
            else:
                varDescr = objFrm.verb.varDescr

            attrIx = 0
            # clear any previous row
            #print("ObjectDebugger refresh: clear rows")
            for btnFrm in frame.vars.codeInpLst[0]:
                #print("  ", btnFrm.params.label[0])
                btnFrm.verb.setBackgroundColor(btnFrm, Wye.color.TRANSPARENT)

            # update variable values
            #print("ObjectDebugger refresh: update vars")
            for btnFrm in frame.vars.varInpLst[0]:
                # update the given input
                var = varDescr[attrIx]
                varVal = getattr(objFrm.vars, var[0])
                btnFrm.verb.setLabel(btnFrm, "  '" + var[0] + "' " + Wye.dType.tostring(var[1]) + " = " + str(varVal[0]))
                attrIx += 1

            dbgFrm = objFrm
            if hasattr(dbgFrm, "parentFrame"): # if this is parallel stream frame, get parent frame
                dbgFrm = objFrm.parentFrame
            if hasattr(dbgFrm.verb, "caseCodeDictLst"):
                #print("ObjectDebugger refresh: highlight code lines for case", dbgFrm.PC)
                # parallel streams, each with own current case
                if dbgFrm.verb.mode == Wye.mode.PARALLEL and hasattr(dbgFrm.verb, "codeDescr"):
                    print("refresh: parallel stream")
                    rowBase = 1
                    for streamIx in range(len(dbgFrm.verb.codeDescr)):
                        if streamIx < len(dbgFrm.verb.caseCodeDictLst):
                            dict = dbgFrm.verb.caseCodeDictLst[streamIx]
                            # get frame for this stream
                            if len(dbgFrm.stacks[streamIx]) > 0:
                                strmFrm = dbgFrm.stacks[streamIx][0]
                                caseStr = str(strmFrm.PC)
                                if caseStr in dict:
                                    rowLst = dict[caseStr]
                                    for rowIx in rowLst:
                                        btnFrm = frame.vars.codeInpLst[0][rowIx + rowBase]
                                        btnFrm.verb.setBackgroundColor(btnFrm, Wye.color.LIGHT_GREEN)
                        # inc to next stream's dialog rows
                        rowBase += len(dbgFrm.verb.codeDescr[streamIx]) + 1
                # single stream
                else:
                    # print("  caseCodeLst", objFrm.verb.caseCodeDictLst)
                    if len(objFrm.verb.caseCodeDictLst) > 0:
                        #print("ObjectDebugger refresh: caseCodeDictLst", objFrm.verb.caseCodeDictLst)
                        dict = objFrm.verb.caseCodeDictLst[0]
                        #print("  dict", dict)
                        caseStr = str(objFrm.PC)
                        if caseStr in dict:
                            rowLst = dict[caseStr]
                            #print(" rowLst for case", caseStr," ", rowLst)
                            for rowIx in rowLst:
                                #print(" highlight row", rowIx)
                                btnFrm = frame.vars.codeInpLst[0][rowIx]
                                btnFrm.verb.setBackgroundColor(btnFrm, Wye.color.LIGHT_GREEN)
            #else:
            #    print("ObjectDebugger refresh: verb", objFrm.verb.__name_, " has no caseCodeDictLst")


        class DebugEditCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),

                        )

            def start(stack):
                # print("DebugEditCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugEditCallback, stack)
                f.systemObject = True  # not stopped by breakAll o rdebugger
                return f

            def run(frame):
                global base
                # print("DebugEditCallback")

                data = frame.eventData
                # print("DebugEditCallback data='" + str(data) + "', case", frame.PC)
                delLnFrm = data[1][0]
                mainDbgFrm = data[1][1]
                dlgFrm = data[1][2]
                frm = data[1][3]    # the object we want to edit

                # fire up object editor with given frame
                # print("ObjEditorCtl: Create ObjEditor")
                edFrm = WyeCore.World.startActiveObject(WyeUILib.EditVerb)
                point = NodePath("point")
                point.reparentTo(render)
                point.setPos(base.camera, (0, Wye.UI.DIALOG_OFFSET - 1, 0))
                pos = point.getPos()
                point.removeNode()
                edFrm.params.position = [(pos[0], pos[1], pos[2]), ]
                # edFrm.params.position = [(frm.vars.position[0][0], frm.vars.position[0][1], frm.vars.position[0][2]),]
                edFrm.params.parent = [None]
                # print("ObjEditorCtl: Fill in ObjEditor objFrm param")

                # if this is one subframe of a parallel stream, edit the parent
                if frm.verb is WyeCore.ParallelStream:
                    # print(frm.verb.__name__, " is parallel stream, get parent", frm.parentDlg.verb.__name__)
                    frm = frm.parentFrame
                edFrm.params.verb = [frm.verb]


        class DebugKillCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                        ("dlgStat", Wye.dType.INTEGER, -1),

                        )

            def start(stack):
                # print("DebugKillCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugKillCallback, stack)
                f.systemObject = True  # not stopped by breakAll o rdebugger
                return f

            def run(frame):
                global base
                # print("DebugKillCallback")

                data = frame.eventData
                # print("DebugKillCallback data='" + str(data) + "', case", frame.PC)
                delLnFrm = data[1][0]
                mainDbgFrm = data[1][1]
                dlgFrm = data[1][2]
                objFrm = data[1][3]

                match (frame.PC):
                    case 0:
                        print("DebugKillCallback: stop", objFrm.verb.__name__)
                        WyeCore.World.stopActiveObject(objFrm)

                        frame.PC += 1

                    # delay 2 frames to let object get removedd
                    case 1:
                        frame.PC += 1

                    case 2:
                        frame.status = Wye.status.SUCCESS

                        # object has stopped by now
                        # if the object has any graphic elements, delete them
                        if hasattr(objFrm.vars, "cleanUpObjs"):
                            for obj in objFrm.vars.cleanUpObjs[0]:
                                # base.loader.unloadModel(obj)
                                obj.removeNode()

                        # shut down main dialog
                        dlgFrm.verb.closeDialog(dlgFrm)
                        dlgFrm.params.retVal[0] = Wye.status.FAIL


        # Debug parameter callback: put up parameter edit dialog
        class DebugParamCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("paramName", Wye.dType.STRING, "<name>"),
                        ("paramType", Wye.dType.STRING, "<type>"),
                        ("paramVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                # print("DebugParamCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugParamCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                data = frame.eventData
                # print("DebugParamCallback data='" + str(data) + "'")
                paramIx = data[1][0]  # offset to param in object's paramDescr list
                btnFrm = data[1][1]
                parentFrm = data[1][2]
                objFrm = data[1][3]
                if objFrm.verb is WyeCore.ParallelStream:
                    paramDescr = objFrm.parentFrame.verb.paramDescr
                else:
                    paramDescr = objFrm.verb.paramDescr

                match (frame.PC):
                    case 0:
                        # print("param ix", data[1][0], " data frame", parentFrm.verb.__name__)

                        # build param dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)

                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Debug Parameter"]
                        dlgFrm.params.parent = [parentFrm]
                        # print("DebugParamCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                        dlgFrm.params.position = [(.5, -.3, -.5 + btnFrm.vars.position[0][2]), ]

                        # Param name
                        frame.vars.paramName[0] = paramDescr[paramIx][0]
                        paramNameFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                        paramNameFrm.params.frame = [None]  # placeholder
                        paramNameFrm.params.label = ["Name: " + frame.vars.paramName[0]]
                        WyeUILib.InputLabel.run(paramNameFrm)
                        dlgFrm.params.inputs[0].append([paramNameFrm])

                        # Param type
                        frame.vars.paramType[0] = paramDescr[paramIx][1]
                        paramTypeFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                        paramTypeFrm.params.frame = [None]
                        paramTypeFrm.params.label = ["Type: " + Wye.dType.tostring(frame.vars.paramType[0])]
                        paramTypeFrm.verb.run(paramTypeFrm)
                        dlgFrm.params.inputs[0].append([paramTypeFrm])

                        # Param current value
                        print("DebugParamCallback get param", frame.vars.paramName[0])
                        frame.vars.paramVal[0] = getattr(objFrm.params, frame.vars.paramName[0])[0]
                        # print("paramVal[0]", frame.vars.paramVal[0])
                        paramValFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        paramValFrm.params.frame = [None]
                        paramValFrm.params.label = ["Value: "]
                        # todo fix back and forth to strings
                        if isinstance(frame.vars.paramVal[0], str):
                            paramValFrm.params.value = [frame.vars.paramVal[0]]
                        else:
                            paramValFrm.params.value = [str(frame.vars.paramVal[0])]
                        WyeUILib.InputText.run(paramValFrm)
                        dlgFrm.params.inputs[0].append([paramValFrm])

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS    # done
                        # check status to see if values should be used
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            strVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                            # convert val to appropriate type
                            val = Wye.dType.convertType(strVal, frame.vars.paramType[0])

                            # if value has changed, update it
                            if val != frame.vars.paramVal[0]:
                                getattr(objFrm.params, frame.vars.paramName[0])[0] = val

                            rowStr = "  '" + frame.vars.paramName[0] + "' " + Wye.dType.tostring(
                                frame.vars.paramType[0]) + " = " + str(val)
                            btnFrm.verb.setLabel(btnFrm, str(rowStr))


        # Debug variable callback: put up variable edit dialog
        class DebugVarCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("varName", Wye.dType.STRING, "<name>"),
                        ("varType", Wye.dType.STRING, "<type>"),
                        ("varVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                # print("DebugVarCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugVarCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                data = frame.eventData
                # print("DebugVarCallback data='" + str(data) + "'")
                varIx = data[1][0]  # offset to variable in object's varDescr list
                btnFrm = data[1][1]
                parentFrm = data[1][2]
                objFrm = data[1][3]

                if objFrm.verb is WyeCore.ParallelStream:
                    varDescr = objFrm.parentFrame.verb.varDescr
                else:
                    varDescr = objFrm.verb.varDescr

                match (frame.PC):
                    case 0:
                        # print("param ix", data[1][0], " data frame", parentFrm.verb.__name__)

                        # build var dialog
                        dlgFrm = WyeUILib.Dialog.start(frame.SP)

                        nParams = min(len(objFrm.verb.paramDescr), 1)
                        nVars = len(varDescr)
                        varIx = data[1][0]

                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Debug Variable"]
                        dlgFrm.params.parent = [parentFrm]
                        # print("DebugVarCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                        dlgFrm.params.position = [(.5, -.3, -.5 + btnFrm.vars.position[0][2]), ]

                        # Var name
                        frame.vars.varName[0] = varDescr[varIx][0]
                        varNameFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                        varNameFrm.params.frame = [None]  # placeholder
                        varNameFrm.params.label = ["Name: " + frame.vars.varName[0]]
                        WyeUILib.InputLabel.run(varNameFrm)
                        dlgFrm.params.inputs[0].append([varNameFrm])

                        # Var type
                        frame.vars.varType[0] = varDescr[varIx][1]
                        varTypeFrm = WyeUILib.InputLabel.start(dlgFrm.SP)
                        varTypeFrm.params.frame = [None]
                        varTypeFrm.params.label = ["Type: " + Wye.dType.tostring(frame.vars.varType[0])]
                        varTypeFrm.verb.run(varTypeFrm)
                        dlgFrm.params.inputs[0].append([varTypeFrm])

                        # Var current value
                        frame.vars.varVal[0] = getattr(objFrm.vars, frame.vars.varName[0])[0]
                        # print("varVal[0]", frame.vars.varVal[0])
                        varValFrm = WyeUILib.InputText.start(dlgFrm.SP)
                        varValFrm.params.frame = [None]
                        varValFrm.params.label = ["Value: "]
                        varValFrm.params.value = [str(frame.vars.varVal[0])]
                        WyeUILib.InputText.run(varValFrm)
                        dlgFrm.params.inputs[0].append([varValFrm])

                        frame.SP.append(dlgFrm)
                        frame.PC += 1

                    case 1:
                        dlgFrm = frame.SP.pop()
                        frame.status = Wye.status.SUCCESS
                        # check status to see if values should be used
                        if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                            strVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                            # convert initVal to appropriate type
                            val = Wye.dType.convertType(strVal, frame.vars.varType[0])
                            # print("DebugVarCallback strVal", strVal, " type", Wye.dType.tostring(frame.vars.varType[0]), "converted type", type(val), " value", val)

                            # if value has changed, update it
                            if val != frame.vars.varVal[0]:
                                getattr(objFrm.vars, frame.vars.varName[0])[0] = val

                            rowStr = "  '" + frame.vars.varName[0] + "' " + Wye.dType.tostring(
                                frame.vars.varType[0]) + " = " + str(val)
                            btnFrm.verb.setLabel(btnFrm, str(rowStr))


        # Debug code callback: ... what to do here?
        # TODO - fill this in
        class DebugVerbCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("paramName", Wye.dType.STRING, "<name>"),
                        ("paramType", Wye.dType.STRING, "<type>"),
                        ("paramVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                # print("DebugVerbCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugVerbCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                data = frame.eventData
                # print("DebugCodeCallback data='" + str(data) + "'")
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                objFrm = data[1][2]
                if objFrm.verb is WyeCore.ParallelStream:
                    codeDescr = objFrm.parentFrame.verb.paramDescr
                else:
                    codeDescr = objFrm.verb.paramDescr

                match (frame.PC):
                    case 0:
                        # stub, just be done
                        frame.status = Wye.status.SUCCESS


        # Debug code callback: ... what to do here?
        # TODO - fill this in
        class DebugCodeCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("paramName", Wye.dType.STRING, "<name>"),
                        ("paramType", Wye.dType.STRING, "<type>"),
                        ("paramVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                # print("DebugCodeCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugCodeCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                data = frame.eventData
                # print("DebugCodeCallback data='" + str(data) + "'")
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                objFrm = data[1][2]
                if objFrm.verb is WyeCore.ParallelStream:
                    codeDescr = objFrm.parentFrame.verb.paramDescr
                else:
                    codeDescr = objFrm.verb.paramDescr

                match (frame.PC):
                    case 0:
                        # stub, just be done
                        frame.status = Wye.status.SUCCESS



        # Debug code callback: ... what to do here?
        # TODO - fill this in
        class DebugSpecialCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            systemObject = True  # not stopped by breakAll debugger flag
            paramDescr = ()
            varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                        ("paramName", Wye.dType.STRING, "<name>"),
                        ("paramType", Wye.dType.STRING, "<type>"),
                        ("paramVal", Wye.dType.STRING, "<val>"),
                        )

            def start(stack):
                # print("DebugSpecialCallback started")
                return Wye.codeFrame(WyeUILib.ObjectDebugger.DebugSpecialCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("DebugSpecialCallback data='" + str(data) + "'")
                btnFrm = data[1][0]
                parentFrm = data[1][1]
                objFrm = data[1][2]
                if objFrm.verb is WyeCore.ParallelStream:
                    codeDescr = objFrm.parentFrame.verb.paramDescr
                else:
                    codeDescr = objFrm.verb.paramDescr

                match (frame.PC):
                    case 0:
                        # stub, just be done
                        frame.status = Wye.status.SUCCESS


        class DebugRefreshVarCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("DebugRefreshVarCallback started")
                return Wye.codeFrame(WyeUILib.ObjectDebugger.DebugRefreshVarCallback, stack)

            def run(frame):
                data = frame.eventData
                # print("DebugRefreshVarCallback data='" + str(data) + "'")

                dbgFrm = data[1][3]

                WyeUILib.ObjectDebugger.update(dbgFrm)

        # Step object that is at breakpoint
        # note: two cycles so can update displayed vars after exec cycle
        class DebugStepCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("count", Wye.dType.INTEGER, 0),)

            def start(stack):
                # print("DebugStepCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.DebugStepCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                #print("DebugStepCallback")
                data = frame.eventData
                objFrm = data[1][2]
                dbgFrm = data[1][3]
                chkBxFrm = data[1][4]
                # if parallel, set flag on actual object frame (parent of this frame)
                if objFrm.verb is WyeCore.ParallelStream:
                    objFrm = objFrm.parentFrame

                match frame.PC:
                    case 0:
                        if objFrm.verb is WyeCore.ParallelStream:
                            objFrm.parentFrame.breakpt = True  # make sure the brake is on
                            if objFrm.parentFrame.SP[-1] != objFrm.parentFrame:
                                objFrm.parentFrame.SP[-1].breakpt = False       # step at parent object level
                        else:
                            if not objFrm.breakpt:  # make sure the brake is on
                                objFrm.breakpt = True
                                chkBxFrm.verb.setValue(chkBxFrm, False)
                            if objFrm.SP[-1] != objFrm:
                                objFrm.SP[-1].breakpt = False           # step at parent object level

                        objFrm.breakCt += 1  # step object once
                        # print("DebugStepCallback increment breakCt to", objFrm.breakCt," on objFrm", objFrm.verb.__name__)
                        frame.PC += 1

                        # flag top of stack that we should keep running 'cause we're in breakpt (yes, this is counter intuitive, roll with it)
                        objFrm.SP[0].doBreakPt = True

                    case 1:
                        frame.status = Wye.status.SUCCESS
                        # note - allow the objFrm to cycled once
                        # todo depends on this obj being later in exec order... questionable
                        #print("Step: refresh")
                        WyeUILib.ObjectDebugger.update(dbgFrm)

        # turn run flag on/off
        class RunCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()

            def start(stack):
                # print("RunCallback started")
                f = Wye.codeFrame(WyeUILib.ObjectDebugger.RunCallback, stack)
                f.systemObject = True  # not stopped by breakAll or debugger
                return f

            def run(frame):
                #print("RunCallback")
                data = frame.eventData
                rowFrm = data[1][0]
                objFrm = data[1][1]
                dbgFrm = data[1][2]

                debugOn = not rowFrm.vars.currVal[0]  # debugOn = not run
                if objFrm.verb is WyeCore.ParallelStream:
                    objFrm.parentFrame.breakpt = debugOn
                    # if we're not the bottom of the stack, debug on that too
                    if objFrm.parentFrame.SP[-1] != objFrm.parentFrame:
                        objFrm.parentFrame.SP[-1].breakpt = debugOn
                    # and flag the top of the stack
                    objFrm.parentFrame.SP[0].doBreakPt = True
                    # print("Breakpoint on parallel parent", objFrm.parentFrame.verb.__name__, " is", debugOn)
                else:
                    objFrm.breakpt = debugOn
                    # if we're not the bottom of the stack, debug on that too
                    if objFrm.SP[-1] != objFrm:
                        objFrm.SP[-1].breakpt = debugOn
                    # print("Breakpoint on", objFrm.verb.__name__, " is", debugOn)
                    objFrm.SP[0].doBreakPt = True

                # flag top of stack
                if debugOn:
                    if objFrm.verb is WyeCore.ParallelStream:
                        if hasattr(objFrm.parentFrame.SP[0], "doBreakPt"):
                            delattr(objFrm.parentFrame.SP[0], "doBreakPt")
                    else:
                        if hasattr(objFrm.SP[0], "doBreakPt"):
                            delattr(objFrm.SP[0], "doBreakPt")
                else:
                    if objFrm.verb is WyeCore.ParallelStream:
                        objFrm.parentFrame.SP[0].doBreakPt = True
                    else:
                        objFrm.SP[0].doBreakPt = True


                WyeUILib.ObjectDebugger.update(dbgFrm)

