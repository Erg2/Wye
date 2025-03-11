from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback
import math
import inspect      # for debugging

class EditLib:

    def build():
        WyeCore.Utils.buildLib(EditLib)

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
            dlgFrm = ctlFrm.parentDlg
            #print("dlgFrame", dlgFrm)
            # print("UpdateCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
            #print("Update x", int(dlgFrm.vars.XAngle[0]), " y", int(dlgFrm.vars.YAngle[0]), " z", int(dlgFrm.vars.ZAngle[0]))

            # inputs don't update parent variables until "OK" - which makes "Cancel" work correctly
            # so have to pull out the temp values from the input controls
            # Do some hackery to get to the pop up dialog's inputs' local variables
            #print("dlgFrm", dlgFrm.params.title)
            x = float(dlgFrm.params.inputs[0][0][0].vars.currVal[0])
            y = float(dlgFrm.params.inputs[0][1][0].vars.currVal[0])
            z = float(dlgFrm.params.inputs[0][2][0].vars.currVal[0])

            frm.vars.target[0].vars.gObj[0].setHpr(x, y, z)

            WyeCore.World.dlightPath.setHpr(x, y, z)


    class ResetCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(EditLib.ResetCallback, stack)

        def run(frame):
            frm = frame.eventData[1]
            ctlFrm = frame.eventData[2]
            dlgFrm = ctlFrm.parentDlg

            x = Wye.startLightAngle[0]
            y = Wye.startLightAngle[1]
            z = Wye.startLightAngle[2]

            dlgFrm.params.inputs[0][0][0].vars.currVal[0] = x
            dlgFrm.params.inputs[0][1][0].vars.currVal[0] = y
            dlgFrm.params.inputs[0][2][0].vars.currVal[0] = z

            dlgFrm.params.inputs[0][0][0].verb.update(dlgFrm.params.inputs[0][0][0])
            dlgFrm.params.inputs[0][1][0].verb.update(dlgFrm.params.inputs[0][1][0])
            dlgFrm.params.inputs[0][2][0].verb.update(dlgFrm.params.inputs[0][2][0])

            frm.vars.target[0].vars.gObj[0].setHpr(int(x), int(y), int(z))

            WyeCore.World.dlightPath.setHpr(int(x), int(y), int(z))

    # find and set angle of wiggle fish (angleFish)
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
            (None, "frame.vars.dlgButton[0] = WyeUI._3dText(text='Set Fish and Light Angle',color=(1,1,1,1), pos=(-3,2,2), scale=(.2,.2,.2))"),
            (None, "frame.vars.doitId[0] = frame.vars.dlgButton[0].getTag()"),

            ("Label", "PopDialog"),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),

            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.target"),
             (None, "[WyeCore.World.findActiveObj('angleFish')]")),
            ("IfGoTo", "frame.vars.target[0] is None", "PopDialog"),
            # read current value
#            (None, "frame.vars.XAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[0])"),
#            (None, "frame.vars.YAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[1])"),
#            (None, "frame.vars.ZAngle[0] = int(frame.vars.target[0].vars.gObj[0].getHpr()[2])"),
            (None, "frame.vars.XAngle[0] = WyeCore.World.dlightPath.getHpr()[0]"),
            (None, "frame.vars.YAngle[0] = WyeCore.World.dlightPath.getHpr()[1]"),
            (None, "frame.vars.ZAngle[0] = WyeCore.World.dlightPath.getHpr()[2]"),

            ("WyeUI.Dialog", (None, "frame.vars.dlgRetVal"),    # frame
                (None, "['Fish Angle Dialog']"),                   # title
                (None, "[(-3,2,1.5),]"),                                # position
                (None, "[None]"),                                  # parent
                ("WyeUI.InputFloat", (None, "frame.vars.XAngleID"),   # inputs (variable length)
                    (None, "['XAngle']"),
                    (None, "frame.vars.XAngle"),
                    (None, "[EditLib.UpdateCallback]"),
                    (None, "[frame]")
                ),
                ("WyeUI.InputFloat", (None, "frame.vars.YAngleID"),
                    (None, "['YAngle']"),
                    (None, "frame.vars.YAngle"),
                    (None, "[EditLib.UpdateCallback]"),
                    (None, "[frame]")
                 ),
                ("WyeUI.InputFloat", (None, "frame.vars.ZAngleID"),
                    (None, "['ZAngle']"),
                    (None, "frame.vars.ZAngle"),
                    (None, "[EditLib.UpdateCallback]"),
                    (None, "[frame]")
                 ),
                ("WyeUI.InputButton", (None, "frame.vars.updateBtnId"),
                    (None, "['Click to reset Position']"),
                    (None, "[EditLib.ResetCallback]"),
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
            return WyeCore.Utils.buildCodeText("showFishDialog", EditLib.showFishDialog.codeDescr, EditLib.showFishDialog)

        def start(stack):
            #print("showFishDialog object start")
            return Wye.codeFrame(EditLib.showFishDialog, stack)

        def run(frame):
            #print("Run testDialogshowFishDialog")
            EditLib.EditLib_rt.showFishDialog_run_rt(frame)

###########################

    class MyTestVerb:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        paramDescr = (
            ("ret", Wye.dType.INTEGER, Wye.access.REFERENCE),
        )
        varDescr = (
("gObj", Wye.dType.OBJECT, None),
("objTag", Wye.dType.STRING, "objTag"),
("sound", Wye.dType.OBJECT, None),
("position", Wye.dType.FLOAT_LIST, [0, 75, 0]),
("dPos", Wye.dType.FLOAT_LIST, [0., 0., -.05]),
("dAngle", Wye.dType.FLOAT_LIST, [0., 0., -.70]),
("colorWk", Wye.dType.FLOAT_LIST, [1, 1, 1]),
("colorInc", Wye.dType.FLOAT_LIST, [12, 12, 12]),
#("color", Wye.dType.FLOAT_LIST, [0, .33, .66, 1]),
("color", Wye.dType.FLOAT_LIST, [1,1,1, 1]),
        )
        codeDescr = (
            # (None, ("print('TestObject123 case 0: start - set up object')")),
            ("WyeCore.libs.WyeLib.loadObject",
             (None, "[frame]"),
             (None, "frame.vars.gObj"),
             (None, "['flyer_01.glb']"),
             (None, "frame.vars.position"),  # posVec
             (None, "[[0, 90, 0]]"),  # rotVec
             (None, "[[2,2,2]]"),  # scaleVec
             (None, "frame.vars.objTag"),
             (None, "frame.vars.color")
             ),
            # ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
            # ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            (None, "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
            ("Label", "Repeat"),
            # set angle
            # ("Code", "print('TestObject123 run')"),
            ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngle")),
            # Step forward
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
            ("WyeCore.libs.WyeLib.getObjPos", (None, "frame.vars.position"), (None, "frame.vars.gObj")),
            # set color
            ("Var=", "frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
            # todo Next two lines are horrible - if followed by then expression indented - they have to be together
            # todo Think of a better way to do if/else than block code or sequential single expressions (EWWW!!)
            ("Code", "if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
            ("Code", " frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
            ("Var=",
             "frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
            (
                "WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.vars.gObj"), ("Var", "frame.vars.color")),

            ("GoTo", "Repeat")
        )

        def build():
            # print("Build ",MyTestVerb)
            return WyeCore.Utils.buildCodeText('MyTestVerb', EditLib.MyTestVerb.codeDescr, EditLib.MyTestVerb)

        def start(stack):
            # print('MyTestVerb object start')
            return Wye.codeFrame(EditLib.MyTestVerb, stack)

        def run(frame):
            # print("Run "+name+"")    
            EditLib.EditLib_rt.MyTestVerb_run_rt(frame)
