from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback
from direct.showbase import Audio3DManager
import math

class TestLib:

    def build():
        WyeCore.Utils.buildLib(TestLib)

    class doitButton:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.PARALLEL
        parTermType = Wye.parTermType.FIRST_FAIL
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("doitBtn", Wye.dType.OBJECT, None),                # 0
                    ("doitId", Wye.dType.STRING, ""),                   # 1
                    ("retChar", Wye.dType.STRING, ""),                   # 2
                    )

        codeDescr = (
            (
                (None, "frame.vars.doitBtn[0] = WyeUI._3dText(text='Click',color=(1,1,1,1), pos=(1,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.doitBtn[0].getTag()"),
                #(None, "print('doitbutton frame0: loaded button & id vars')"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("Label", "ClickLoop"),
                #(None, "print('doitbutton stream1: waitclick. status=', Wye.status.tostring(frame.status))"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                (None, "WyeUI._displayLib(frame, (1,10,1), WyeCore.libs.TestLib, (.1,10,.8))"),
                ("Label", "Dummy"),         # display pushed a dialog frame.  label creates a case
                (None, "frame.SP.pop()"),   # when return from stack, pop display's pushed frame
                ("GoTo", "ClickLoop"),
                ("Label", "Done"),
            ),
        #    (
        #        ("Label", "TextLoop"),
        #        #(None, "print('doitbutton stream2: wait for char')"),
        #        ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars.retChar"), (None, "frame.vars.doitId")),
        #        (None, "print('doitButton stream2: received char', frame.vars.retChar[0])"),
        #        ("GoTo", "TextLoop")
        #    )
        )

        def build():
            #print("Testlib2 build testCompiledPar")
            return WyeCore.Utils.buildParallelText("TestLib", "doitButton", TestLib.doitButton.codeDescr)

        def start(stack):
            return TestLib.TestLib_rt.doitButton_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            frame.runParallel()      # run compiled run code


    class BtnCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(TestLib.BtnCallback, stack)

        def run(frame):
            #print("BtnCallback data=", frame.eventData, " count = ", frame.vars.count[0])

            # really bad coding / wizardry required here
            # Get the text widget of the
            inFrm = frame.eventData[1][0]
            var = frame.eventData[1][1]
            # print("data [1]", frame.eventData[1][1], " var", var)
            dlgFrm = inFrm.parentFrame
            # print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])

            var[0] += 1

            # get label input's frame from parent dialog
            lblFrame = dlgFrm.params.inputs[0][3][0]

            # supreme hackery - look up the display label in the label's graphic widget list
            inWidg = lblFrame.vars.gWidgetStack[0][0]
            txt = "Count " + str(var[0])
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(txt)

            if var[0] >= 10:
                var[0] = 0

    class testDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        #autoStart = True
        paramDescr = ()
        varDescr = (("tstDlg3ID", Wye.dType.OBJECT, None),
                    ("Title", Wye.dType.INTEGER, "Test Dialog 3"),
                    ("txt1ID", Wye.dType.STRING, ""),
                    ("text1Val", Wye.dType.STRING, ""),
                    ("txt2IO", Wye.dType.STRING, ""),
                    ("text2Val", Wye.dType.STRING, "starting text"),
                    ("BtnID", Wye.dType.OBJECT, None),
                    ("lblID", Wye.dType.OBJECT, None),
                    ("clickCt", Wye.dType.INTEGER, 0),
                    ("retList", Wye.dType.INTEGER, -1),
        )

        codeDescr = (
            #(None, "print('testDialog, startup - create param list ')"),
            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"),    # frame
             (None, "frame.vars.Title"),                        # title
             (None, "[(-3,8,1)]"),                                # position
             (None, "[None]"),                                  # parent
             ("WyeUI.InputText", (None, "frame.vars.txt1ID"),   # inputs (variable length)
              (None, "['TextLabel']"),
              (None, "frame.vars.text1Val")
              ),
             ("WyeUI.InputText", (None, "frame.vars.txt2IO"),
              (None, "['Text2Label']"),
              (None, "frame.vars.text2Val")
              ),
             ("WyeUI.InputButton", (None, "frame.vars.BtnID"),
              (None, "['Click Me counter']"),
              (None, "[TestLib.BtnCallback]"),
              (None, "[[frame.f1,frame.vars.clickCt]]")
              ),
             ("WyeUI.InputLabel", (None, "frame.vars.lblID"), (None, "['Count -1']")
              ),
            ),
            ("WyeCore.libs.WyeLib.setEqual",
                (None, "frame.vars.retList"),
                (None, "[10]"),
             ),
            #(None, "print('testDialog retList=', frame.vars.retList[0])"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            return WyeCore.Utils.buildCodeText("testDialog", TestLib.testDialog.codeDescr)

        def start(stack):
            #print("testDialog object start")
            return Wye.codeFrame(TestLib.testDialog, stack)

        def run(frame):
            #print("Run testDialog")
            TestLib.TestLib_rt.testDialog_run_rt(frame)


    class fishDlgButton:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        #parTermType = Wye.parTermType.FIRST_FAIL
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("doitBtn", Wye.dType.OBJECT, None),                # 0
                    ("doitId", Wye.dType.STRING, ""),                   # 1
                    ("retChar", Wye.dType.STRING, ""),                   # 2
                    )

        codeDescr = (

                (None, "frame.vars.doitBtn[0] = WyeUI._3dText(text='Open Fish Angle Dialog',color=(1,1,1,1), pos=(-3,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.doitBtn[0].getTag()"),
                #(None, "print('doitbutton frame0: loaded button & id vars')"),
                ("Label", "ClickLoop"),
                #(None, "print('fishbutton: waitclick')"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                #(None, "print('fishbutton: open fishDialog')"),
                ("TestLib.fishDialog",),
                ("GoTo", "ClickLoop")
            )

        def build():
            return WyeCore.Utils.buildCodeText("fishDlgButton", TestLib.fishDlgButton.codeDescr)

        def start(stack):
            #print("fishDlgButton object start")
            return Wye.codeFrame(TestLib.fishDlgButton, stack)

        def run(frame):
            #print("Run testDialog")
            TestLib.TestLib_rt.fishDlgButton_run_rt(frame)


    class fishDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        #autoStart = True
        paramDescr = ()
        varDescr = (("tstDlg3ID", Wye.dType.OBJECT, None),
                    ("XAngleID", Wye.dType.STRING, ""),
                    ("XAngle", Wye.dType.STRING, "0"),
                    ("YAngleID", Wye.dType.STRING, ""),
                    ("YAngle", Wye.dType.STRING, "0"),
                    ("ZAngleID", Wye.dType.STRING, ""),
                    ("ZAngle", Wye.dType.STRING, "0"),
                    ("target", Wye.dType.OBJECT, None)
        )

        codeDescr = (
            ("Label", "PopDialog"),
            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"),    # frame
             (None, "['Fish Angle Dialog']"),                        # title
             (None, "[(-3,8,1)]"),                                # position
             (None, "[None]"),                                  # parent
             ("WyeUI.InputText", (None, "frame.vars.XAngleID"),   # inputs (variable length)
              (None, "['XAngle']"),
              (None, "frame.vars.XAngle")
              ),
             ("WyeUI.InputText", (None, "frame.vars.YAngleID"),
              (None, "['YAngle']"),
              (None, "frame.vars.YAngle")
              ),
             ("WyeUI.InputText", (None, "frame.vars.ZAngleID"),
              (None, "['ZAngle']"),
              (None, "frame.vars.ZAngle")
              ),

             ),

            #(None, "print('fishDialog XAngle', frame.vars.XAngle, ' YAngle', frame.vars.YAngle, ' ZAngle', frame.vars.ZAngle)"),
            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.target"), (None, "[TestLib.fishDialog.findActiveObj('testObj2')]")),
            ("IfGoTo", "frame.vars.target[0] is None", "PopDialog"),
            #(None, "print('testObj2 frm', frame.vars.target[0].verb.__name__)"),
            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.target[0].vars.obj"),
                (None, "[[int(frame.vars.XAngle[0]),int(frame.vars.YAngle[0]),int(frame.vars.ZAngle[0])]]")),
            ("GoTo", "PopDialog")
        )

        def build():
            #print("Build fishDialog")
            return WyeCore.Utils.buildCodeText("fishDialog", TestLib.fishDialog.codeDescr)

        def start(stack):
            #print("fishDialog object start")
            return Wye.codeFrame(TestLib.fishDialog, stack)

        def run(frame):
            #print("Run testDialogfishDialog")
            TestLib.TestLib_rt.fishDialog_run_rt(frame)

        # Find first active instance of object with given name
        def findActiveObj(name):
            print(WyeCore.World.objStacks)
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

    # generated code for
    # load model passed in at loc, scale passed in
    class testLoader:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE

        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("file", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),
                      ("scaleVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("colorVec", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = (
            #(None, "print('test inline code')"),
            # call loadModel with testLoader params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.params.obj"), (None, "frame.params.file")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params.tag"), (None, "frame.params.obj")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params.obj"), (None, "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.params.obj"), (None, "frame.params.posVec"), (None, "frame.params.scaleVec"))
        )
        code = None

        def build():
            return WyeCore.Utils.buildCodeText("testLoader", TestLib.testLoader.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader_run_rt(frame)


    # when clicked, spin object back and forth
    class clickWiggle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),
                    ("sound", Wye.dType.OBJECT, None))
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.clickWiggle, stack)

        def run(frame):
            global base
            #print('execute spin, params', frame.params, ' vars', frame.vars)

            gObj = frame.params.obj[0]
            vec = gObj.getHpr()
            axis = frame.params.axis[0]
            #print("Current HPR ", vec)
            match frame.PC:
                case 0:
                    WyeCore.World.setEventCallback("click", frame.params.tag[0], frame)
                    # frame.vars.sound[0] = Wye.audio3d.loadSfx("WyePop.wav")
                    frame.vars.sound[0] = Wye.audio3d.loadSfx("WyePew.wav")
                    Wye.audio3d.attachSoundToObject(frame.vars.sound[0], frame.params.obj[0])
                    frame.PC += 1
                    #print("clickWiggle waiting for event 'click' on tag ", frame.params.tag[0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    frame.vars.sound[0].play()
                    frame.PC += 1

                case 3:
                    vec[axis] += 5
                    #print("spin (pos) obj", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] > 45:   # end of swing this way
                        frame.PC += 1  # go to next state

                case 4:
                    vec[axis] -= 5
                    #print("spin (neg) obj ", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] < -45:    # end of swing other way
                        frame.PC += 1   # go to previous state

                case 5:
                    frame.vars.rotCt[0] += 1  # count cycles
                    if frame.vars.rotCt[0] < 2:  # wiggle this many times, then exit
                        frame.PC = 3    # go do another wiggle
                    else:
                        # finish by coming back to zero
                        vec[axis] += 5
                        #print("spin (neg) obj ", gObj, "to", vec)
                        gObj.setHpr(vec[0], vec[1], vec[2])
                        if vec[axis] >= 0:    # end of swing other way
                            #print("clickWiggle: done")
                            frame.status = Wye.status.SUCCESS


                case _:
                    frame.status = Wye.status.SUCCESS


    # spin object back and forth
    class spin:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),)
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.spin, stack)

        def run(frame):
            gObj = frame.params.obj[0]
            vec = gObj.getHpr()
            axis = frame.params.axis[0]
            #print("Current HPR ", vec)
            match frame.PC:
                case 0:
                    vec[axis] += 5
                    #print("spin (pos) obj", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if frame.vars.rotCt[0] < 4:  # wiggle this many times, then exit
                        if vec[axis] > 45:  # end of swing this way
                            frame.vars.rotCt[0] += 1  # count cycles
                            frame.PC += 1   # go to next state
                    else:   # last spin cycle, stop at zero
                        #print("spin: done")
                        if vec[axis] >= 0:  # end of swing this way
                            frame.PC = -1  # undefined case value so will go to default to exit


                    frame.status = Wye.status.CONTINUE

                case 1:
                    vec[axis] -= 5
                    #print("spin (neg) obj ", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] < -45:    # end of swing other way
                        frame.PC -= 1   # go to previous state

                    frame.status = Wye.status.CONTINUE

                case _:
                    frame.status = Wye.status.SUCCESS

    class fish:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("fish", Wye.dType.OBJECT, None),
                    ("fishTag", Wye.dType.STRING, "obj1Tag"),
                    ("pos", Wye.dType.STRING, [0,0,0]),
                    ("sound", Wye.dType.OBJECT, None))  # var 4
        codeDescr=(
            (None, ("print('fish case 0: set up object')")),
            ("TestLib.testLoader",
                (None, "frame.vars.fish"),
                (None, "['flyer_02.glb']"),
                (None, "[1,5,-.5]"),
                (None, "[.75,.75,.75]"),
                (None, "frame.vars.fishTag"),
                (None, "[1,1,0,1]")
            ),
            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.obj1"),(None, "[0,5,-.5]")),
            #(None, "frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
            ("Label", "Repeat"),
            ("TestLib.clickWiggle", (None, "frame.vars.fish"), (None, "frame.vars.fishTag"), (None, "[1]")),
            #("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.fishTag")),
            ("GoTo", "Repeat")
        )

        def build():
            #print("Build fish")
            return WyeCore.Utils.buildCodeText("fish", TestLib.fish.codeDescr)

        def start(stack):
            #print("fish object start")
            return Wye.codeFrame(TestLib.fish, stack)

        def run(frame):
            #print("Run fish")
            TestLib.TestLib_rt.fish_run_rt(frame)


    class leaderFish:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = ()
        varDescr = (("fish", Wye.dType.OBJECT, None),
                    ("fishTag", Wye.dType.STRING, "obj1Tag"),
                    ("pos", Wye.dType.STRING, [0,5,0]),
                    ("angle", Wye.dType.STRING, [0,90,0]),
                    ("piAngle", Wye.dType.FLOAT, 0.),
                    ("sound", Wye.dType.OBJECT, None))  # var 4

        codeDescr=(
            (None, ("print('leaderFish case 0: set up object')")),
            ("TestLib.testLoader",
                (None, "frame.vars.fish"),
                (None, "['flyer_02.glb']"),
                (None, "[0,5,-.5]"),
                (None, "[.75,.75,.75]"),
                (None, "frame.vars.fishTag"),
                (None, "[1,0,0,1]")
            ),

            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.obj1"),(None, "[0,5,-.5]")),
            ("Label", "StartLoop"),
            #(None, "print('angle', frame.vars.angle)"),

            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.fish"), (None, "frame.vars.angle")),
            (None, "from math import pi"),      # apparently import has to be within the match case
            (None, "from math import cos"),     # it doesn't stick between cycles
            (None, "from math import sin"),
            (None, "frame.vars.piAngle[0] = pi/2 + pi * -2 * frame.vars.angle[0][0] / 360"),
            (None, "frame.vars.piAngle[0] = round(frame.vars.piAngle[0] if frame.vars.piAngle[0] < (2*pi) else frame.vars.piAngle[0] - 2*pi, 2)"),
            (None, "frame.vars.pos[0][0] = round(sin(frame.vars.piAngle[0])*2, 2)"),
            (None, "frame.vars.pos[0][1] = round(10+cos(frame.vars.piAngle[0])*2, 2)"),
            #(None, "print('angle', frame.vars.angle[0], ' sin', round(sin(frame.vars.piAngle[0]),2), ' cos', round(cos(frame.vars.piAngle[0]),2))"),
            #(None, "print('angle', frame.vars.angle[0], ' piAngle', frame.vars.piAngle[0], ' pos', frame.vars.pos[0])"),
            ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.fish"), (None, "frame.vars.pos")),

            (None, "frame.vars.angle[0][0] += 1"),

            ("IfGoTo", "frame.vars.angle[0][0] < 360", "StartLoop"),
            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.angle"), (None, "[[0,90,0]]")),
            #(None, "print('angle', frame.vars.angle)"),
            ("GoTo", "StartLoop")

#            ("Label", "Right"),
#            (None, "frame.vars.pos[0] += .01"),
#            ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.fish"), (None, "frame.vars.pos")),
#            ("IfGoTo", "frame.vars.pos[0] < 1", "Right"),
#
#            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.fish"), (None, "[0,0,-90]")),
#
#            ("Label", "Back"),
#            (None, "frame.vars.pos[0] += .01"),
#            ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.fish"), (None, "frame.vars.pos")),
#            ("IfGoTo", "frame.vars.pos[1] < 6", "Back"),
#
#            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.fish"), (None, "[0,0,90]")),
#
#            ("Label", "Left"),
#            ("IfGoTo", "frame.vars.pos[0] < -1", "Front"),
#            (None, "frame.vars.pos[0] -= .01"),
#            ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.fish"), (None, "frame.vars.pos")),
#            ("IfGoTo", "frame.vars.pos[0] > -1", "Left"),
#
#            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.fish"), (None, "[-90,0,-90]")),
#
#            ("Label", "Front"),
#            (None, "frame.vars.pos[0][1] -= .01"),
#            ("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.fish"), (None, "frame.vars.pos[0]")),
#            ("IfGoTo", "frame.vars.pos[0][1] > 5", "Front"),
#
#            ("GoTo", "Start"),   # Back to the top
        )

        def build():
            #print("Build leaderFish")
            return WyeCore.Utils.buildCodeText("leaderFish", TestLib.leaderFish.codeDescr)

        def start(stack):
            #print("leaderFish object start")
            return Wye.codeFrame(TestLib.leaderFish, stack)

        def run(frame):
            #print("Run leaderFish")
            TestLib.TestLib_rt.leaderFish_run_rt(frame)


    class testObj2:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = (("ret", Wye.dType.INTEGER, Wye.access.REFERENCE),)  # gotta have a ret param
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("obj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, "objTag"),
                    ("sound", Wye.dType.OBJECT, None))  # var 4

        codeDescr=(
            (None, ("print('testObj2 case 0: start - set up object')")),
            ("TestLib.testLoader",
                (None, "frame.vars.obj"),
                (None, "['flyer_01.glb']"),
                (None, "[-1,5,-.5]"),
                (None, "[.75,.75,.75]"),
                (None, "frame.vars.objTag"),
                (None, "[0,1,0,1]")
            ),
            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.obj"), (None, "[-90,90,0]")),

            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.obj"),(None, "[0,5,-.5]")),
            (None, "frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
            ("Label", "Repeat"),
            ("TestLib.clickWiggle", (None, "frame.vars.obj"), (None, "frame.vars.objTag"), (None, "[1]")),
            #("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.objTag")),
            ("GoTo", "Repeat")
        )

        def build():
            #print("Build testObj2")
            return WyeCore.Utils.buildCodeText("testObj2", TestLib.testObj2.codeDescr)

        def start(stack):
            #print("testObj2 object start")
            return Wye.codeFrame(TestLib.testObj2, stack)

        def run(frame):
            #print("Run testObj2")
            TestLib.TestLib_rt.testObj2_run_rt(frame)


