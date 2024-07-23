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
                (None, "print('received char=', frame.vars[2][0])"),
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
            ("WyeUI.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
                                (None, "(-2,10,0)"), (None, "None"),
                                ("WyeUI.LabelInput", (None, "frame.vars[13]"), (None, "['LabelInput']")),
                                ("WyeUI.TextInput", (None, "frame.vars[2]"),
                                  (None, "['T1Label']"),
                                  (None, "frame.vars[3]")
                                ),
                                ("WyeUI.TextInput", (None, "frame.vars[4]"),
                                 (None, "['T2Label']"),
                                 (None, "frame.vars[5]")
                                ),
                                ("WyeUI.ButtonInput", (None, "frame.vars[12]"),
                                  (None, "['Click Me for Dialog']"),
                                  (None, "[WyeUI.BtnCallback2]")
                                ),
             ),
            #(None, "print('DlgTst frame 1 vars', frame.vars)"),
            #(None, "print('DlgTst frame after Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("WyeUI.Dialog", (None, "frame.vars[6]"), (None, "frame.vars[7]"),
                               (None, "(2,10,0)"), (None, "None"),
                               ("WyeUI.TextInput", (None, "frame.vars[8]"),
                                (None, "['T3Label']"),
                                (None, "frame.vars[9]")
                               ),
                               ("WyeUI.TextInput", (None, "frame.vars[10]"),
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