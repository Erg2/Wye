from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback

class TestLib:

    def build():
        WyeCore.Utils.buildLib(TestLib)

    class showAvailLibs:
        cType = Wye.cType.VERB
        mode = Wye.mode.MULTI_CYCLE

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
                (None, "frame.vars.doitBtn[0] = WyeCore.libs.WyeUI._label3d(text='Click',color=(1,1,1,1), pos=(1,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.doitBtn[0].getTag()"),
                #(None, "print('doitbutton frame0: loaded button & id vars')"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("Label", "ClickLoop"),
                #(None, "print('doitbutton stream1: waitclick. status=', Wye.status.tostring(frame.status))"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                (None, "WyeCore.libs.WyeUI._displayLib(frame, (1,10,1), WyeCore.libs.TestLib, (.1,10,.8))"),
                ("Label", "Dummy"),         # display pushed a dialog frame.  label creates a case
                (None, "frame.SP.pop()"),   # when return from stack, pop display's pushed frame
                ("GoTo", "ClickLoop"),
                ("Label", "Done"),
            ),
            (
                ("Label", "TextLoop"),
                #(None, "print('doitbutton stream2: wait for char')"),
                ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars.retChar"), (None, "frame.vars.doitId")),
                (None, "print('doitButton stream2: received char', frame.vars.retChar[0])"),
                ("GoTo", "TextLoop")
            )
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
        autoStart = True
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
            #(None, "print('testDialog, create param list ')"),
            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"),    # frame
             (None, "frame.vars.Title"),                        # title
             (None, "(-3,8,1)"),                                # position
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
            (None, "print('testDialog retList=', frame.vars.retList[0])"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            print("Build testDialog")
            return WyeCore.Utils.buildCodeText("testDialog", TestLib.testDialog.codeDescr)

        def start(stack):
            #print("testDialog object start")
            return Wye.codeFrame(TestLib.testDialog, stack)

        def run(frame):
            #print("Run testDialog")
            TestLib.TestLib_rt.testDialog_run_rt(frame)

    # generated code for
    # load model passed in at loc, scale passed in
    class testLoader3:
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
            # call loadModel with testLoader3 params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.params.obj"), (None, "frame.params.file")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params.tag"), (None, "frame.params.obj")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params.obj"), (None, "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.params.obj"), (None, "frame.params.posVec"), (None, "frame.params.scaleVec"))
        )
        code = None

        def build():
            return WyeCore.Utils.buildCodeText("testLoader3", TestLib.testLoader3.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader3, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader3_run_rt(frame)



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

        # TODO - make multi-cycle
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



    class testObj2:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = (("ret", Wye.dType.INTEGER, Wye.access.REFERENCE),)  # gotta have a ret param
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("obj1", Wye.dType.OBJECT, None),
                    ("obj2", Wye.dType.OBJECT, None),
                    ("obj1Tag", Wye.dType.STRING, "obj1Tag"),
                    ("obj2Tag", Wye.dType.STRING, "obj2Tag"),
                    ("sound", Wye.dType.OBJECT, None))  # var 4

        codeDescr=(
            (None, ("print('testObj2 case 0: start - set up object')")),
            ("TestLib.testLoader3",
                (None, "frame.vars.obj1"),
                (None, "['flyer_01.glb']"),
                (None, "[-1,5,-.5]"),
                (None, "[.75,.75,.75]"),
                (None, "frame.vars.obj1Tag"),
                (None, "[0,1,0,1]")
            ),
            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.obj1"),(None, "[0,5,-.5]")),
            (None, "frame.vars.sound[0] = base.loader.loadSfx('WyePew.wav')"),
            ("Label", "Repeat"),
            ("TestLib.spin", (None, "frame.vars.obj1"), (None, "[1]")),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.obj1Tag")),
            ("GoTo", "Repeat")
        )

        def build():
            print("Build testObj2")
            return WyeCore.Utils.buildCodeText("testObj2", TestLib.testObj2.codeDescr)

        def start(stack):
            #print("testObj2 object start")
            return Wye.codeFrame(TestLib.testObj2, stack)

        def run(frame):
            #print("Run testObj2")
            TestLib.TestLib_rt.testObj2_run_rt(frame)