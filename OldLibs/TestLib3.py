from Wye import Wye
from WyeCore import WyeCore

class TestLib3:

    def _build():
        WyeCore.Utils.buildLib(TestLib3)

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
                (None, "frame.vars.doitBtn[0] = Wye3dObjsLib._3dText(text='Click',color=(1,1,1,1), pos=(0,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.doitBtn[0].getTag()"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitid")),
                (None, "WyeUILib._displayLib(WyeCore.libs.TestLib3, (.1,10,.8))"),
                ("Label", "Done")
            ),
            (
                #(None, "print('doitButton: before key loop')"),
                ("Label", "Loop"),
                #(None, "print('doitButton: top of key loop')"),
                #(None, "print('doitButton: wait for char')"),
                ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars.retChar"), (None, "frame.vars.doitId")),
                #(None, "print('received char=', frame.vars.retChar[0])"),
                ("GoTo", "Loop")
            )
        )

        def _build(rowRef):
            #print("Testlib2 build testCompiledPar")
            return WyeCore.Utils.buildParallelText("TestLib3", "doitButton", TestLib3.doitButton.codeDescr)

        def start(stack):
            return TestLib3.TestLib3_rt.doitButton_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            frame.runParallel()      # run compiled run code

    class DlgTst:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("id", Wye.dType.OBJECT, None),                 # 0
                    ("Title", Wye.dType.INTEGER, "Test Dialog 1"),    # 1
                    ("text1ID", Wye.dType.STRING, ""),              # 2
                    ("text1Val", Wye.dType.STRING, ""),        # 3
                    ("text2ID", Wye.dType.STRING, ""),              # 4
                    ("text2Val", Wye.dType.STRING, "<val1>"),        # 5

                    ("id2", Wye.dType.OBJECT, None),  # 6
                    ("Title2", Wye.dType.INTEGER, "Test Dialog 2"),  # 7
                    ("text1ID2", Wye.dType.STRING, ""),  # 8
                    ("text1Val2", Wye.dType.STRING, ""),  # 9
                    ("text2ID2", Wye.dType.STRING, ""),  # 10
                    ("text2Val2", Wye.dType.STRING, "<val2>"),  # 11

                    ("id1", Wye.dType.OBJECT, None),  # 12

                    ("labelId", Wye.dType.OBJECT, None), # 13
                    )

        codeDescr = (
            #(None, "print('DlgTst frame before Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUILib.Dialog", (None, "frame.vars.id"), (None, "frame.vars.Title"),
                                (None, "[(-2,10,0),]"), (None, "None"),
                                ("WyeUILib.InputLabel", (None, "frame.vars.labelId"), (None, "['InputLabel']")),
                                ("WyeUILib.InputText", (None, "frame.vars.text1ID"),
                                  (None, "['T1Label']"),
                                  (None, "frame.vars.Text1Val")
                                ),
                                ("WyeUILib.InputText", (None, "frame.vars.text2ID"),
                                 (None, "['T2Label']"),
                                 (None, "frame.vars.text2Val")
                                ),
                                ("WyeUILib.InputButton", (None, "frame.vars.id1"),
                                  (None, "['Click Me for Dialog']"),
                                  (None, "[WyeUILib.BtnCallback2]")
                                ),
             ),
            #(None, "print('DlgTst frame 1 vars', frame.vars)"),
            #(None, "print('DlgTst frame after Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUILib.Dialog", (None, "frame.vars.id2"), (None, "frame.vars.Title2"),
                               (None, "[(2,10,0),]"), (None, "None"),
                               ("WyeUILib.InputText", (None, "frame.vars.text1ID2"),
                                (None, "['T3Label']"),
                                (None, "frame.vars.text1Val2")
                               ),
                               ("WyeUILib.InputText", (None, "frame.vars.text2ID2"),
                                  (None, "['T4Label']"),
                                  (None, "frame.vars.text2Val2")
                               )
            ),
            ("Label", "Done")
        )

        def _build(rowRef):
            return WyeCore.Utils.buildCodeText("DlgTst", TestLib3.DlgTst.codeDescr, rowRef)

        def start(stack):
            return Wye.codeFrame(TestLib3.DlgTst, stack)

        def run(frame):
            TestLib3.TestLib3_rt.DlgTst_run_rt(frame)