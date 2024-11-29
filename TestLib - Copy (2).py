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
                #(None, "WyeCore.libs.WyeUI._displayLib(frame, (0,10,1), WyeCore.libs.TestLib, (.1,10,.8))"),
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




    class test:
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
            #(None, "print('test, create param list ')"),
            ("WyeUI.Dialog", (None, "frame.vars.tstDlg3ID"), (None, "frame.vars.Title"),
             (None, "((1,-1,-1),)"), (None, "[frame.eventData[1]]"),
             ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.retList"),

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
              )
             ),
            ("WyeCore.libs.WyeLib.setEqual",
                (None, "frame.vars.retList"),
                (None, "[10]"),
             ),
            #(None, "print('test retList=', frame.vars.retList[0])"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            print("Build test")
            return WyeCore.Utils.buildCodeText("test", TestLib.test.codeDescr)

        def start(stack):
            print("Start test")
            return Wye.codeFrame(TestLib.test, stack)

        def run(frame):
            #print("Run test_run_rt")
            TestLib.TestLib_rt.test_run_rt(frame)

