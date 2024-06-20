from Wye import Wye
from WyeCore import WyeCore

class TestLib3:

    def build():
        WyeCore.Utils.buildLib(TestLib3)

    class doitButton:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.PARALLEL
        parType = Wye.parType.FIRST_FAIL
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
                (None, "WyeCore.libs.WyeUI._displayLib(WyeCore.libs.TestLib3, (.1,10,.8))"),
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
            return WyeCore.Utils.buildParallelText("TestLib3", "doitButton", TestLib3.doitButton.codeDescr)

        def start(stack):
            return TestLib3.TestLib3_rt.doitButton_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            WyeCore.Utils.runParallelCode(frame)      # run compiled run code

    # Effectively this is a factory generating an input object frame for dialog to use
    class TextInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),    # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),    # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))    # user supplied var to return value in
        varDescr = (("currPos", Wye.dType.INTEGER, 0),)  # 0

        def start(stack):
            return Wye.codeFrame(TestLib3.TextInput, stack)

        def run(frame):
            frame.params[0][0] = frame      # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

    # Effectively this is a factory generating a dialog object for the UI to use
    class Dialog:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),    # return own frame
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # user supplied title for dialog
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE))   # parent dialog, if any
                      # This parameter list is dynamic.  TODO Figger out how to specify this
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib3.TextInput, stack)

        def run(frame):
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS


    class DlgTst:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("Title", Wye.dType.INTEGER, "Test Dialog"),
                    ("id", Wye.dType.STRING, "0"),
                    ("text1", Wye.dType.INTEGER, 0),
                    ("text2", Wye.dType.INTEGER, 0),
                    )  # 0

        codeDescr = (
            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars[1]"),
             ("TestLib3.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
                                              (None, "None"))),
            ("Label", "Done")
            #("WyeCore.libs.WyeLib.makePickable", (None, "frame.params[4]"), (None, "frame.params[0]")),
            #("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params[0]"), (None, "frame.params[5]")),
            #("WyeCore.libs.WyeLib.showModel", (None, "frame.params[0]"), (None, "frame.params[2]"), (None, "frame.params[3]"))
        )

        def build():
            return WyeCore.Utils.buildCodeText("DlgTst", TestLib3.DlgTst.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib3.DlgTst, stack)

        def run(frame):
            TestLib3.TestLib3_rt.DlgTst_run_rt(frame)