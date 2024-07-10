from Wye import Wye
from WyeCore import WyeCore

class TestLib3:

    def build():
        WyeCore.Utils.buildLib(TestLib3)

    class doitButton:
        cType = Wye.cType.OBJECT
        #autoStart = True
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

    # Input field classes
    # Runtime returns frame as p0

    # Effectively each is a factory generating an input object frame for dialog to use

    # label field
    # Technically not an input, but is treated as one for space
    class LabelInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE))  # user supplied label for field
        varDescr = (("currPos", Wye.dType.INTEGER, 0),)  # 0

        def start(stack):
            return Wye.codeFrame(TestLib3.TextInput, stack)

        def run(frame):
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

    # text input field
    class TextInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))  # user supplied var to return value in
        varDescr = (("currPos", Wye.dType.INTEGER, 0),)  # 0

        def start(stack):
            return Wye.codeFrame(TestLib3.TextInput, stack)

        def run(frame):
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

    # Effectively this is a factory generating a dialog object for the UI to use
    class Dialog:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),    # 0 return own frame
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE)) # 4+ variable length list of input control frames
                      # This parameter list is dynamic.  TODO Figger out how to specify this
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),          # 0 pos copy
                    ("dlgWidgets", Wye.dType.OBJECT_LIST, []),              # 1 default obj ids
                    ("inpWidgets", Wye.dType.OBJECT_LIST, []))              # 2 input obj ids

        def start(stack):
            print("Dialog start")
            frame = Wye.codeFrame(TestLib3.Dialog, stack)
            print("Dialog Add dialog to focus manager")
            WyeCore.Utils.setFocusManager(WyeCore.libs.WyeUI.FocusManager.openDialog(frame, None))
            return frame

        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    frame.params[0][0] = frame  # self referential!
                    print("Dialog put frame in param[0][0]", frame)
                    frame.vars[0] = (frame.params[2])        # save display position
                    # return frame

                    print("Dialog display: pos=frame.params[2]", frame.params[2])
                    txt = WyeCore.libs.WyeUI._label3d(text=frame.params[1][0], color=(1, 1, 1, 1), pos=frame.params[2], scale=(.2, .2, .2))
                    frame.vars[1][0].append(txt)

                    pos = [x for x in frame.params[2]]    # copy position

                    # do user inputs
                    nInputs = len(frame.params) - 4
                    print("Dialog ", nInputs, " user widgets")
                    #for ii in range(nInputs):
                    #

                    # display buttons
                    pos[2] -= .3
                    txt = WyeCore.libs.WyeUI._label3d("OK", color=(1, 1, 1, 1), pos=tuple(pos), scale=(.2, .2, .2))
                    frame.vars[1][0].append(txt)
                    pos[0] += .5
                    txt = WyeCore.libs.WyeUI._label3d("Cancel", color=(1, 1, 1, 1), pos=tuple(pos),
                                                      scale=(.2, .2, .2))
                    frame.vars[1][0].append(txt)
                    # user supplied input widgets
                    

                    frame.PC += 1   #
                case 1:
                    # handle events
                    pass


    class DlgTst:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("id", Wye.dType.OBJECT, None),
                    ("Title", Wye.dType.INTEGER, "Test Dialog"),
                    ("text1", Wye.dType.INTEGER, 0),
                    ("text2", Wye.dType.INTEGER, 0),
                    )  # 0

        codeDescr = (
            (None, "print('DlgTst frame',WyeCore.Utils.frameToString(frame))"),
            ("TestLib3.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
                               (None, "(0,10,0)"), (None, "None"),
                               #("TestLib3.TextInput", )
                                ),
            #(None, "print('DlgTst: Dialog returned frame ',frame.vars[0][0])"),
            #(None, "print('DlgTst: frame for verb ',frame.vars[0][0].verb)"),
            #(None, "print('DlgTst: frame for verb name ',frame.vars[0][0].verb.__name__)"),
            #(None, "frame.vars[0][0].verb.display(frame.vars[0][0])"),
            #("WyeCore.libs.WyeLib.makePickable", (None, "frame.params[4]"), (None, "frame.params[0]")),
            #("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params[0]"), (None, "frame.params[5]")),
            #("WyeCore.libs.WyeLib.showModel", (None, "frame.params[0]"), (None, "frame.params[2]"), (None, "frame.params[3]")),
            ("Label", "Done")
        )

        def build():
            return WyeCore.Utils.buildCodeText("DlgTst", TestLib3.DlgTst.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib3.DlgTst, stack)

        def run(frame):
            TestLib3.TestLib3_rt.DlgTst_run_rt(frame)