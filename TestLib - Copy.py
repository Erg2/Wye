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
                (None, "frame.vars.doitBtn[0] = WyeCore.libs.WyeUI._label3d(text='Click',color=(1,1,1,1), pos=(0,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.doitBtn[0].getTag()"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("Label", "Loop"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                #(None, "print('doitButton call _displayLib with frame', frame.tostring())"),
                (None, "WyeCore.libs.WyeUI._displayLib(frame, (0,10,1), WyeCore.libs.TestLib, (.1,10,.8))"),
                ("GoTo", "Loop"),
                ("Label", "Done")
            ),
            (
                ("Label", "Loop"),
                ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars.retChar"), (None, "frame.vars.doitId")),
                (None, "print('doitButton received char', frame.vars.retChar[0])"),
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
            #print("BtnCallback data=", frame.eventData, " count = ", frame.vars.count[0])

            # really bad coding / wizardry required here
            # Get the text widget of the
            inFrm = frame.eventData[1][0]
            var = frame.eventData[1][1]
            #print("data [1]", frame.eventData[1][1], " var", var)
            dlgFrm = inFrm.parentFrame
            #print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])

            var[0] += 1

    # todo - revisit this after changing over vars and params
    #        # get label input's frame from parent dialog
    #        lblFrame = dlgFrm.params.inputs[3]

    #        # supreme hackery - look up the display label in the label's graphic widget list
    #        inWidg = lblFrame.vars.gWidgetStack[0][0]
    #        txt = "Count " + str(var[0])
    #        # print("  set text", txt," ix", ix, " txtWidget", inWidg)
    #        inWidg.setText(txt)

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
            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"), (None, "frame.vars.Title"),
             (None, "((1,-1,-1),)"), (None, "[frame.eventData[1]]"),
             ("WyeUI.InputText", (None, "frame.vars.txt1ID"),
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
             ("WyeUI.InputLabel", (None, "frame.vars.lblID"), (None, "['Count -1']")),
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
        varDescr = (("tstDlg3Frm", Wye.dType.OBJECT, None),     # 0
                    ("Title", Wye.dType.INTEGER, "DropDown"),   # 1
                    ("text1frm", Wye.dType.STRING, ""),         # 2
                    ("text1Val", Wye.dType.STRING, ""),         # 3
                    ("text2frm", Wye.dType.STRING, ""),         # 4
                    ("text2Val", Wye.dType.STRING, "<val1>"),   # 5
                    ("id1", Wye.dType.OBJECT, None),            # 6
                    ("selRow", Wye.dType.INTEGER, -1),          # 7
        )

        codeDescr = (
            (None, "print('Callback 3, create dropdown. parent ', frame.eventData[1])"),
            (None, "print('           frame.eventData ', frame.eventData)"),
            ("WyeCore.libs.WyeLib.setEqual",
                (None, "frame.vars.selRow"),
                ("WyeUI.DropDown", (None, "frame.vars.tstDlg3Frm"), (None, "frame.vars.Title"),
                 (None, "(1,-1,-1.5*5)"), (None, "[frame.eventData[1]]"),
                 (None, "(('Line 0'), ('Line 1'), ('Line 2'), ('Line 3'))"),
                )
             ),
            #("WyeUI.DropDown", (None, "frame.vars.tstDlg3Frm"), (None, "frame.vars.Title"),
            #  (None, "(1,-1,-1.5*5)"), (None, "[frame.eventData[1]]"),
            #  (None, "(('Line 0'), ('Line 1'), ('Line 2'), ('Line 3'))"),
            #),
            #("Label", "Done"),
            (None, "print('Callback 3 dropDown done with SUCCESS.  User picked entry', frame.vars.selRow[0])"),
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
        varDescr = (("frame", Wye.dType.OBJECT, None),                 # 0
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
                    ("click2Id", Wye.dType.OBJECT, None),  # 14
                    )

        codeDescr = (
            #(None, "print('DlgTst frame before Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUI.Dialog", (None, "frame.vars.frame"), (None, "frame.vars.Title"),
                                (None, "((-2,10,0),)"), (None, "[None]"),
                                ("WyeUI.InputLabel", (None, "frame.vars.labelId"), (None, "['InputLabel']")),
                                ("WyeUI.InputText", (None, "frame.vars.test1frm"),
                                  (None, "['Enter Text 1']"),
                                  (None, "frame.vars.text1Val")
                                ),
                                ("WyeUI.InputText", (None, "frame.vars.test2frm"),
                                 (None, "['Enter Text 2']"),
                                 (None, "frame.vars.test2Val")
                                ),
                                ("WyeUI.InputButton", (None, "frame.vars.id1"),
                                  (None, "['Click Me for Dialog']"),
                                  (None, "[TestLib.BtnCallback2]"),
                                  (None, "frame.vars.frame")
                                ),
                                ("WyeUI.InputButton", (None, "frame.vars.click2Id"),
                                  (None, "['Click Me for Dropdown']"),
                                  (None, "[TestLib.BtnCallback3]"),
                                  (None, "frame.vars.frame")
                                ),
             ),
            #(None, "print('DlgTst frame 1 vars', frame.vars)"),
            #(None, "print('DlgTst frame after Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUI.Dialog", (None, "frame.vars.Dlg2Frm"), (None, "frame.vars.Title2"),
                               (None, "((2,10,0),)"), (None, "[None]"),
                               ("WyeUI.InputText", (None, "frame.vars.text1frm2"),
                                (None, "['T3Label']"),
                                (None, "frame.vars.test1Val2")
                               ),
                               ("WyeUI.InputText", (None, "frame.vars.text2frm2"),
                                  (None, "['T4Label']"),
                                  (None, "frame.vars.text2Val2")
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
            frame.vars.objs[0] = []    # init object list
            return frame

        def run(frame):
            match frame.PC:
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