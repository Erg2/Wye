from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback
from direct.showbase import Audio3DManager
import math
import inspect      # for debugging

class EditLib:

    def build():
        WyeCore.Utils.buildLib(EditLib)

    class ShowAvailLibs:
        cType = Wye.cType.VERB
        mode = Wye.mode.MULTI_CYCLE


    class UpdateCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(EditLib.UpdateCallback, stack)

        def run(frame):
            #print("UpdateCallback data=", frame.eventData, " verb", frame.eventData[1].verb.__name__)

            frm = frame.eventData[1]
            ctlFrm = frame.eventData[2]
            dlgFrm = ctlFrm.parentFrame
            #print("dlgFrame", dlgFrm)
            # print("UpdateCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
            #print("Update x", int(dlgFrm.vars.XAngle[0]), " y", int(dlgFrm.vars.YAngle[0]), " z", int(dlgFrm.vars.ZAngle[0]))

            # inputs don't update parent variables until "OK" - which makes "Cancel" work correctly
            # so have to pull out the temp values from the input controls
            # Do some hackery to get to the pop up dialog's inputs' local variables
            #print("dlgFrm", dlgFrm.params.title)
            x = dlgFrm.params.inputs[0][0][0].vars.currVal[0]
            y = dlgFrm.params.inputs[0][1][0].vars.currVal[0]
            z = dlgFrm.params.inputs[0][2][0].vars.currVal[0]

            frm.vars.target[0].vars.gObj[0].setHpr(int(x), int(y), int(z))
            #print("  hpr", dlgFrm.vars.target[0].vars.gObj[0].getHpr())



    # find and set angle of wiggle fish (testObj2)
    class showFishDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = True
        paramDescr = ()
        varDescr = (("dlgRetVal", Wye.dType.INTEGER, -1),
                    ("XAngleID", Wye.dType.STRING, ""),
                    ("XAngle", Wye.dType.INTEGER, 0),
                    ("YAngleID", Wye.dType.STRING, ""),
                    ("YAngle", Wye.dType.INTEGER, 0),
                    ("ZAngleID", Wye.dType.STRING, ""),
                    ("ZAngle", Wye.dType.INTEGER, 0),
                    ("updateBtnId", Wye.dType.OBJECT, None),
                    ("dlgButton", Wye.dType.OBJECT, None),
                    ("doitId", Wye.dType.OBJECT, None),
                    ("target", Wye.dType.OBJECT, None),
                    )

        codeDescr = (

            #(None, "print('EditLib ShowFishDialog')"),
            (None, "frame.vars.dlgButton[0] = WyeCore.libs.WyeUI._label3d(text='Set Fish Angle',color=(1,1,1,1), pos=(-3,9,1), scale=(.2,.2,.2))"),
            (None, "frame.vars.doitId[0] = frame.vars.dlgButton[0].getTag()"),

            ("Label", "PopDialog"),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),

            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.target"),
             (None, "[WyeCore.World.findActiveObj('testObj2')]")),
            ("IfGoTo", "frame.vars.target[0] is None", "PopDialog"),
            # read current value
            (None, "frame.vars.XAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[0])"),
            (None, "frame.vars.YAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[1])"),
            (None, "frame.vars.ZAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[2])"),
            ("WyeUI.Dialog", (None, "frame.vars.dlgRetVal"),    # frame
                (None, "['Fish Angle Dia    log']"),                   # title
                (None, "((-3,8,1),)"),                                # position
                (None, "[None]"),                                  # parent
                ("WyeUI.InputInteger", (None, "frame.vars.XAngleID"),   # inputs (variable length)
                    (None, "['XAngle']"),
                    (None, "frame.vars.XAngle")
                ),
                ("WyeUI.InputInteger", (None, "frame.vars.YAngleID"),
                    (None, "['YAngle']"),
                    (None, "frame.vars.YAngle")
                ),
                ("WyeUI.InputInteger", (None, "frame.vars.ZAngleID"),
                    (None, "['ZAngle']"),
                    (None, "frame.vars.ZAngle")
                ),
                ("WyeUI.InputButton", (None, "frame.vars.updateBtnId"),
                    (None, "['Update']"),
                    (None, "[EditLib.UpdateCallback]"),
                    (None, "[frame]")
                ),
            ),
            #(None, "print('showFishDialog closed. status', frame.vars.dlgRetVal[0])"),
            ("IfGoTo", "frame.vars.dlgRetVal[0] != Wye.status.SUCCESS", "PopDialog"),
            #(None, "print('showFishDialog OK, set angle')"),
            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.target[0].vars.gObj"),
                (None, "[[int(frame.vars.XAngle[0]),int(frame.vars.YAngle[0]),int(frame.vars.ZAngle[0])]]")),
            ("GoTo", "PopDialog")
        )

        def build():
            return WyeCore.Utils.buildCodeText("showFishDialog", EditLib.showFishDialog.codeDescr)

        def start(stack):
            #print("showFishDialog object start")
            return Wye.codeFrame(EditLib.showFishDialog, stack)

        def run(frame):
            #print("Run testDialogshowFishDialog")
            EditLib.EditLib_rt.showFishDialog_run_rt(frame)

