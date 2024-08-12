from Wye import Wye
from WyeCore import WyeCore

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
                (None, "frame.vars[0][0] = WyeCore.libs.WyeUI._label3d(text='Click',color=(1,1,1,1), pos=(0,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars[1][0] = frame.vars[0][0].getTag()"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars[1]")),
                (None, "WyeCore.libs.WyeUI._displayLib(WyeCore.libs.TestLib, (.1,10,.8))"),
                ("Label", "Done")
            ),
            (
                #(None, "print('doitButton: before key loop')"),
                ("Label", "Loop"),
                #(None, "print('doitButton: top of key loop')"),
                #(None, "print('doitButton: wait for char')"),
                ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars[2]"), (None, "frame.vars[1]")),
                #(None, "print('received char=', frame.vars[2][0])"),
                ("GoTo", "Loop")
            )
        )

        def build():
            #print("Testlib2 build testCompiledPar")
            return WyeCore.Utils.buildParallelText("TestLib", "doitButton", TestLib.doitButton.codeDescr)

        def start(stack):
            return TestLib.TestLib_rt.doitButton_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            frame.runParallel()      # run compiled run code


    # Test Dialog 3 "Click Me counter" button callback
    # Increment variable in parent dialog and show value in text label
    class BtnCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(TestLib.BtnCallback, stack)

        def run(frame):
            print("BtnCallback data=", frame.eventData, " count = ", frame.vars[TestLib.BtnCallback.vConst.count][0])

            # really bad coding / wizardry required here
            # Get the text widget of the
            inFrm = frame.eventData[1][0]
            var = frame.eventData[1][1]
            #print("data [1]", frame.eventData[1][1], " var", var)
            dlgFrm = inFrm.parentFrame
            #print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params[1][0])

            var[0] += 1

            # get label input's frame from parent dialog
            lblFrame = dlgFrm.params[WyeCore.libs.WyeUI.Dialog.pConst.inputs+3][0]

            # supreme hackery - look up the display label in the label's graphic widget list
            inWidg = lblFrame.vars[0][0][0]
            txt = "Count " + str(var[0])
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(txt)

            if var[0] >= 10:
                var[0] = 0

    class BtnCallback2:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("tstDlg3ID", Wye.dType.OBJECT, None),              # 0
                    ("Title", Wye.dType.INTEGER, "Test Dialog 3"),      # 1
                    ("txt1ID", Wye.dType.STRING, ""),                   # 2
                    ("text1Val", Wye.dType.STRING, ""),                 # 3
                    ("txt2IO", Wye.dType.STRING, ""),                   # 4
                    ("text2Val", Wye.dType.STRING, "starting text"),    # 5
                    ("BtnID", Wye.dType.OBJECT, None),                  # 6
                    ("lblID", Wye.dType.OBJECT, None),                  # 7
                    ("clickCt", Wye.dType.INTEGER, 0),                  # 8
        )

        codeDescr = (
            (None, "print('Callback 2, create dialog. parent ', frame.eventData[1])"),
            (None, "print('           frame.eventData ', frame.eventData)"),
            ("WyeUI.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
             (None, "(1,-1,-1)"), (None, "[frame.eventData[1]]"),
             ("WyeUI.InputText", (None, "frame.vars[2]"),
              (None, "['TextLabel']"),
              (None, "frame.vars[3]")
              ),
             ("WyeUI.InputText", (None, "frame.vars[4]"),
              (None, "['Text2Label']"),
              (None, "frame.vars[5]")
              ),
             ("WyeUI.InputButton", (None, "frame.vars[6]"),
              (None, "['Click Me counter']"),
              (None, "[TestLib.BtnCallback]"),
              (None, "[[f1,frame.vars[8]]]")
              ),
             ("WyeUI.InputLabel", (None, "frame.vars[7]"), (None, "['Count -1']")),
             ),
            #("Label", "Done"),
            (None, "print('Callback 2 done with SUCCESS')"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            return WyeCore.Utils.buildCodeText("BtnCallback2", TestLib.BtnCallback2.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib.BtnCallback2, stack)

        def run(frame):
            TestLib.TestLib_rt.BtnCallback2_run_rt(frame)



    class BtnCallback3:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("tstDlg3Frm", Wye.dType.OBJECT, None),                 # 0
                    ("Title", Wye.dType.INTEGER, "DropDown"),    # 1
                    ("text1frm", Wye.dType.STRING, ""),              # 2
                    ("text1Val", Wye.dType.STRING, ""),        # 3
                    ("text2frm", Wye.dType.STRING, ""),              # 4
                    ("text2Val", Wye.dType.STRING, "<val1>"),        # 5
                    ("id1", Wye.dType.OBJECT, None),  # 6
        )

        codeDescr = (
            (None, "print('Callback 3, create dropdown. parent ', frame.eventData[1])"),
            (None, "print('           frame.eventData ', frame.eventData)"),
            ("WyeUI.DropDown", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
             (None, "(1,-1,-1.5*5)"), (None, "[frame.eventData[1]]"),
             (None, "(('Line 0'), ('Line 1'), ('Line 2'), ('Line 3'))"),
             ),
            #("Label", "Done"),
            (None, "print('Callback 2 done with SUCCESS')"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            print("Build BtnCallback3")
            return WyeCore.Utils.buildCodeText("BtnCallback3", TestLib.BtnCallback3.codeDescr)

        def start(stack):
            print("Start BtnCallback3")
            return Wye.codeFrame(TestLib.BtnCallback3, stack)

        def run(frame):
            print("Run BtnCallback3")
            TestLib.TestLib_rt.BtnCallback3_run_rt(frame)



    class DlgTst:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("Dlg1Frm", Wye.dType.OBJECT, None),                 # 0
                    ("Title", Wye.dType.INTEGER, "Test Dialog 1"),    # 1
                    ("text1frm", Wye.dType.STRING, ""),              # 2
                    ("text1Val", Wye.dType.STRING, ""),        # 3
                    ("text2frm", Wye.dType.STRING, ""),              # 4
                    ("text2Val", Wye.dType.STRING, "<val1>"),        # 5

                    ("Dlg2Frm", Wye.dType.OBJECT, None),  # 6
                    ("Title2", Wye.dType.INTEGER, "Test Dialog 2"),  # 7
                    ("text1frm2", Wye.dType.STRING, ""),  # 8
                    ("text1Val2", Wye.dType.STRING, ""),  # 9
                    ("text2frm2", Wye.dType.STRING, ""),  # 10
                    ("text2Val2", Wye.dType.STRING, "initial value"),  # 11

                    ("id1", Wye.dType.OBJECT, None),  # 12

                    ("labelId", Wye.dType.OBJECT, None), # 13
                    ("clidk2ID", Wye.dType.OBJECT, None),  # 14
                    )

        codeDescr = (
            #(None, "print('DlgTst frame before Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUI.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
                                (None, "(-2,10,0)"), (None, "[None]"),
                                ("WyeUI.InputLabel", (None, "frame.vars[13]"), (None, "['InputLabel']")),
                                ("WyeUI.InputText", (None, "frame.vars[2]"),
                                  (None, "['Enter Text 1']"),
                                  (None, "frame.vars[3]")
                                ),
                                ("WyeUI.InputText", (None, "frame.vars[4]"),
                                 (None, "['Enter Text 2']"),
                                 (None, "frame.vars[5]")
                                ),
                                ("WyeUI.InputButton", (None, "frame.vars[12]"),
                                  (None, "['Click Me for Dialog']"),
                                  (None, "[TestLib.BtnCallback2]"),
                                  (None, "frame.vars[0]")
                                ),
                                ("WyeUI.InputButton", (None, "frame.vars[14]"),
                                  (None, "['Click Me for Dropdown']"),
                                  (None, "[TestLib.BtnCallback3]"),
                                  (None, "frame.vars[0]")
                                ),
             ),
            #(None, "print('DlgTst frame 1 vars', frame.vars)"),
            #(None, "print('DlgTst frame after Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUI.Dialog", (None, "frame.vars[6]"), (None, "frame.vars[7]"),
                               (None, "(2,10,0)"), (None, "[None]"),
                               ("WyeUI.InputText", (None, "frame.vars[8]"),
                                (None, "['T3Label']"),
                                (None, "frame.vars[9]")
                               ),
                               ("WyeUI.InputText", (None, "frame.vars[10]"),
                                  (None, "['T4Label']"),
                                  (None, "frame.vars[11]")
                               )
            ),
            ("Label", "Done")
        )

        def build():
            return WyeCore.Utils.buildCodeText("DlgTst", TestLib.DlgTst.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib.DlgTst, stack)

        def run(frame):
            TestLib.TestLib_rt.DlgTst_run_rt(frame)


    class editProto:
        cType = Wye.cType.OBJECT
        #autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        paramDescr = ()
        varDescr = (("objs", Wye.dType.OBJECT_LIST, None),     # 0
                    )

        def start(stack):
            frame = Wye.codeFrame(TestLib.editProto, stack)
            frame.vars[0][0] = []    # init object list
            return frame

        def run(frame):
            match(frame.PC):
                case 0:
                    tgt = TestLib.DlgTst
                    tgtFrm = TestLib.DlgTst.start(frame.SP)
                    # generate text inputs for header info

                    # generate click inputs for params

                    # generate click inputs for vars

                    # generate click inputs for code

                    # open dialog
                case 1:
                    pass
                    # get here when dialog done
                    # if success, add/replace new dlg object