from Wye import Wye
from WyeCore import WyeCore

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


#    class BtnCallback:
#        mode = Wye.mode.SINGLE_CYCLE
#        dataType = Wye.dType.STRING
#        paramDescr = ()
#        varDescr = (("count", Wye.dType.INTEGER, 0),)
#
#        def start(stack):
#            return Wye.codeFrame(TestLib.BtnCallback, stack)
#
#        def run(frame):
#            print("BtnCallback data=", frame.eventData, " count = ", frame.vars.count[0])
#
#            # really bad coding / wizardry required here
#            # Get the text widget of the
#            inFrm = frame.eventData[1][0]
#            var = frame.eventData[1][1]
#            # print("data [1]", frame.eventData[1][1], " var", var)
#            dlgFrm = inFrm.parentFrame
#            # print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
#
#            var[0] += 1
#
#            # get label input's frame from parent dialog
#            lblFrame = dlgFrm.params.inputs[0][3][0]
#
#            # supreme hackery - look up the display label in the label's graphic widget list
#            inWidg = lblFrame.vars.gWidgetStack[0][0]
#            txt = "Count " + str(var[0])
#            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
#            inWidg.setText(txt)
#
#            if var[0] >= 10:
#                var[0] = 0
#
#    class test:
#        mode = Wye.mode.MULTI_CYCLE
#        dataType = Wye.dType.STRING
#        #autoStart = True
#        paramDescr = ()
#        varDescr = (("tstDlg3ID", Wye.dType.OBJECT, None),
#                    ("Title", Wye.dType.INTEGER, "Test Dialog 3"),
#                    ("txt1ID", Wye.dType.STRING, ""),
#                    ("text1Val", Wye.dType.STRING, ""),
#                    ("txt2IO", Wye.dType.STRING, ""),
#                    ("text2Val", Wye.dType.STRING, "starting text"),
#                    ("BtnID", Wye.dType.OBJECT, None),
#                    ("lblID", Wye.dType.OBJECT, None),
#                    ("clickCt", Wye.dType.INTEGER, 0),
#                    ("retList", Wye.dType.INTEGER, -1),
#        )
#
#        codeDescr = (
#            #(None, "print('test, create param list ')"),
#            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"),    # frame
#             (None, "frame.vars.Title"),                        # title
#             (None, "(-3,8,1)"),                                # position
#             (None, "[None]"),                                  # parent
#             ("WyeUI.InputText", (None, "frame.vars.txt1ID"),   # inputs (variable length)
#              (None, "['TextLabel']"),
#              (None, "frame.vars.text1Val")
#              ),
#             ("WyeUI.InputText", (None, "frame.vars.txt2IO"),
#              (None, "['Text2Label']"),
#              (None, "frame.vars.text2Val")
#              ),
#             ("WyeUI.InputButton", (None, "frame.vars.BtnID"),
#              (None, "['Click Me counter']"),
#              (None, "[TestLib.BtnCallback]"),
#              (None, "[[frame.f1,frame.vars.clickCt]]")
#              ),
#             ("WyeUI.InputLabel", (None, "frame.vars.lblID"), (None, "['Count -1']")
#              ),
#            ),
#            ("WyeCore.libs.WyeLib.setEqual",
#                (None, "frame.vars.retList"),
#                (None, "[10]"),
#             ),
#            (None, "print('test retList=', frame.vars.retList[0])"),
#            (None, "frame.status = Wye.status.SUCCESS")
#        )
#
#        def build():
#            print("Build test")
#            return WyeCore.Utils.buildCodeText("test", TestLib.test.codeDescr)
#
#        def start(stack):
#            #print("test object start")
#            return Wye.codeFrame(TestLib.test, stack)
#
#        def run(frame):
#            #print("Run test_run_rt")
#            TestLib.TestLib_rt.test_run_rt(frame)

