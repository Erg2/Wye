# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
from WyeUILib import WyeUILib
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
class WyeUIUtilsLib(Wye.staticObj):
    systemLib = True        # prevent overwriting
    modified = False  # no changes
    canSave = False

    # Build run_rt methods on each class in library
    def _build():
        WyeCore.Utils.buildLib(WyeUIUtilsLib)


    # utilities

    # Helper functions for building dialogs

    # put up independently running popup dialog box with given color (see Wye.color.NORMAL_COLOR, WARNING_COLOR, ERROR_COLOR
    def doPopUpDialog(titleText, mainText, headerColor=Wye.color.HEADER_COLOR, color=Wye.color.NORMAL_COLOR,
                      formatLst=["NO_CANCEL"], parent=None, position=(0,0,0), okOnCr=True):
        global base
        global render
        #print("doPopUpDialog title", titleText, " text", mainText, " color", color, " parent", parent)

        if parent or position[0] != 0 or position[1] != 0 or position[2] != 0:
            pos = position
        else:
            # position in front of other dialogs
            point = NodePath("point")
            point.reparentTo(render)
            point.setPos(base.camera, Wye.UI.NICE_NOTIFICATION_POS)
            pos = point.getPos()
            point.removeNode()

        dlgFrm = WyeUIUtilsLib.doDialog(titleText, parent=parent, position=pos, formatLst=formatLst, headerColor=headerColor, okOnCr=okOnCr)
        WyeUIUtilsLib.doInputLabel(dlgFrm, mainText, color)
        dlgFrm.systemObject = True      # Show warnings even if system paused
        #dlgFrm.SP.append(dlgFrm)
        #dlgFrm.verb.run(dlgFrm)
        WyeCore.World.startActiveFrame(dlgFrm)


    # create and return popup dialog box with given color (see Wye.color.NORMAL_COLOR, WARNING_COLOR, ERROR_COLOR
    def doPopUpDialogAsync(frame, titleText, mainText, headerColor=Wye.color.HEADER_COLOR, color=Wye.color.NORMAL_COLOR,
                           formatLst=["NO_CANCEL",], parent=None, position=(0,0,0), okOnCr=True):
        global base
        global render
        # print("doPopUpDialog title", titleText, " text", mainText, " color", color)

        if parent:
            pos = position
        else:
            # position in front of other dialogs
            point = NodePath("point")
            point.reparentTo(render)
            point.setPos(base.camera, Wye.UI.NICE_NOTIFICATION_POS)
            pos = point.getPos()
            point.removeNode()

        dlgFrm = WyeUIUtilsLib.doDialog(titleText, parent=parent, position=pos, formatLst=formatLst, headerColor=headerColor, okOnCr=okOnCr)
        WyeUIUtilsLib.doInputLabel(dlgFrm, mainText, color=color)
        dlgFrm.systemObject = True  # Show warnings even if system paused
        if parent:
            dlgFrm.SP = frame.SP
        #dlgFrm.verb.run(dlgFrm)
        return dlgFrm

    # create and return file save/overwrite dialog box
    def doAskSaveAsFileAsync(frame, parent, fileName, position=(0,0,0), fileType=".py", title="Save As",
                             retValRef=[Wye.status.CONTINUE], okOnCr=True):
        askSaveFrm = WyeUILib.AskSaveAsFile.start(frame.SP)
        askSaveFrm.params.retVal = retValRef
        askSaveFrm.params.fileName = [fileName]
        askSaveFrm.params.fileType = [fileType]
        askSaveFrm.params.title = [title]
        askSaveFrm.params.parent = [parent]
        askSaveFrm.params.okOnCr = [okOnCr]
        if not parent and position == (0,0,0):
            point = NodePath("point")
            point.reparentTo(render)
            point.setPos(base.camera, Wye.UI.NICE_NOTIFICATION_POS)
            position = point.getPos()
            point.removeNode()
        askSaveFrm.params.position = [position]
        return askSaveFrm

    # dialog.  If no position supplied, puts in front of viewpoint
    def doDialog(title, parent=None, position=None, formatLst=[""], headerColor=Wye.color.HEADER_COLOR, okOnCr=False):
        if parent:
            stack = parent.SP
        else:
            stack = []
        dlgFrm = WyeUILib.Dialog.start(stack)
        dlgFrm.params.retVal = [None]           # used in Wye code, not important for inline code
        dlgFrm.params.title = [title]
        if not position:
            point = NodePath("point")
            point.reparentTo(render)
            point.setPos(base.camera, Wye.UI.NICE_DIALOG_POS)
            position = point.getPos()
            point.removeNode()

        dlgFrm.params.position = [(position[0], position[1], position[2]), ]
        dlgFrm.params.parent = [parent]
        dlgFrm.params.format = [formatLst]
        dlgFrm.params.headerColor = [headerColor]
        dlgFrm.params.okOnCr = [okOnCr]
        return dlgFrm


    # dialog.  If no position supplied, puts in front of viewpoint
    def doHUDDialog(title, parent=None, position=(0,0,0), formatLst=[""], headerColor=Wye.color.HEADER_COLOR, okOnCr=False):
        if parent:
            stack = parent.SP
        else:
            stack = []
        dlgFrm = WyeUILib.HUDDialog.start(stack)
        dlgFrm.params.retVal = [None]           # used in Wye code, not important for inline code
        dlgFrm.params.title = [title]
        dlgFrm.params.position = [[position[0], position[1], position[2]],]
        dlgFrm.params.parent = [parent]
        dlgFrm.params.format = [formatLst]
        dlgFrm.params.headerColor = [headerColor]
        dlgFrm.params.okOnCr = [okOnCr]
        return dlgFrm


    def doInputLabel(dlgFrm, label, color=Wye.color.LABEL_COLOR, backgroundColor=Wye.color.TRANSPARENT,
                     layout=Wye.layout.VERTICAL, padding=(0,0,0,0), fixedWidth=0, hidden=False):
        frm = WyeUILib.InputLabel.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm

    # Note: valueRef is a list with the value in it.  It can the name of a param or var
    def doInputText(dlgFrm, label, valueRef, callback=None, optData=None, color=Wye.color.LABEL_COLOR, textColor=Wye.color.ACTIVE_COLOR,
                    backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL, padding=(0,0,0,0), fixedWidth=0,
                    hidden=False):
        frm = WyeUILib.InputText.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.value = valueRef
        frm.params.callback = [callback]
        frm.params.optData = [optData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.textColor = [textColor]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm

    def doInputInteger(dlgFrm, label, valurRef, callback=None, optData=None, color=Wye.color.LABEL_COLOR, textColor=Wye.color.ACTIVE_COLOR,
                       backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL, padding=(0,0,0,0), fixedWidth=0,
                       hidden=False):
        frm = WyeUILib.InputInteger.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.value = valurRef
        frm.params.callback = [callback]
        frm.params.optData = [optData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.textColor = [textColor]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm


    def doInputFloat(dlgFrm, label, valurRef, callback=None, optData=None, color=Wye.color.LABEL_COLOR, textColor=Wye.color.ACTIVE_COLOR,
                     backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL, padding=(0,0,0,0), fixedWidth=0,
                     hidden=False):
        frm = WyeUILib.InputFloat.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.value = valurRef
        frm.params.callback = [callback]
        frm.params.optData = [optData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.textColor = [textColor]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm

    def doInputButton(dlgFrm, label, callback=None, optData=None, color=Wye.color.ACTIVE_COLOR,
                      backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL, padding=(0,0,0,0), fixedWidth=0,
                     hidden=False):
        frm = WyeUILib.InputButton.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.callback = [callback] if callback else None
        frm.params.optData = [optData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm

    def doInputCheckbox(dlgFrm, label, valueRef, callback=None, optData=None, color=Wye.color.ACTIVE_COLOR,
                      backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL, radioGroup=None,
                      selectedRadio=0, padding=(0,0,0,0), fixedWidth=0, hidden=False):
        frm = WyeUILib.InputCheckbox.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.value = valueRef
        frm.params.callback = [callback]
        frm.params.optData = [optData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.radioGroup = [radioGroup]
        frm.params.selectedRadio = [selectedRadio]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm

    # note: dropdownListRef is a list of strings
    def doInputDropdown(dlgFrm, label, dropdownListRef, selectionIxRef, callback=None, optData=None,
                        preDropCallback=None, preDropOptData=None, color=Wye.color.LABEL_COLOR,
                      textColor=Wye.color.ACTIVE_COLOR, backgroundColor=Wye.color.TRANSPARENT, layout=Wye.layout.VERTICAL,
                        showText=True, showLabel=True, padding=(0,0,0,0), fixedWidth=0, hidden=False):
        frm = WyeUILib.InputDropdown.start(dlgFrm.SP)
        frm.params.frame = [None]  # return value
        frm.params.parent = [None]
        frm.params.list = dropdownListRef
        frm.params.selectedIx = selectionIxRef
        frm.params.callback = [callback]
        frm.params.optData = [optData]
        frm.params.preDropCallback = [preDropCallback]
        frm.params.preDropOptData = [preDropOptData]
        frm.params.label = [label]
        frm.params.layout = [layout]
        frm.params.color = [color]
        frm.params.textColor = [textColor]
        frm.params.showText = [showText]
        frm.params.showLabel = [showLabel]
        frm.params.backgroundColor = [backgroundColor]
        frm.params.padding = [padding]
        frm.params.fixedWidth = [fixedWidth]
        frm.params.hidden = [hidden]
        frm.verb.run(frm)
        dlgFrm.params.inputs[0].append([frm])
        return frm
