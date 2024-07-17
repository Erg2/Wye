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
                #(None, "print('received char=', frame.vars[2][0])"),
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
    # Each input run method just returns its frame as p0
    #
    # Dialog sets up input graphics when it runs
    # Since the input has run before the dialog does, it cannot do any graphic setup
    # because it doesn't know where it's going to be.  The Dialog manages that.
    # Therefore, all it can do is set up its info in its frame and return the frame for the
    # dialog to use.
    #
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
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE))  # 2 user supplied var to return value in
        varDescr = (("currPos", Wye.dType.INTEGER, 0),      # 0 3d pos
                    ("currVal", Wye.dType.STRING, ""),      # 1 current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),    # 2 text insertion point
                    ("gWidget", Wye.dType.OBJECT, None)     # 3 stashed graphic widget
                    )
        def start(stack):
            frm = Wye.codeFrame(TestLib3.TextInput, stack)
            return frm

        def run(frame):
            frame.vars[1][0] = frame.params[2][0]
            frame.params[0][0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS


    # text input field
    class ButtonInput:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("verb", Wye.dType.STRING, Wye.access.REFERENCE))   # 2 verb to call when button clicked
        varDescr = (("currPos", Wye.dType.INTEGER, 0),      # 0
                    ("gWidget", Wye.dType.OBJECT, None),    # 1 associated graphic widget
                    ("verb", Wye.dType.OBJECT, None),       # 2 verb to call
                    ("verbFrame", Wye.dType.OBJECT, None),  # 3 verb frame for call
                    ("clickCount", Wye.dType.INTEGER, 0),   # 4 button depressed count
                    ("verbStack", Wye.dType.OBJECT_LIST, None), # 5 verb callback stack
                    )

        def start(stack):
            frm = Wye.codeFrame(TestLib3.ButtonInput, stack)
            frm.vars[TestLib3.ButtonInput.vConst["verbStack"]][0] = []
            return frm

        def run(frame):
            frame.vars[2][0] = frame.params[2][0]       # save verb to call
            frame.params[0] = [frame]  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS


    # Dialog object.
    # Display and
    class Dialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.OBJECT, Wye.access.REFERENCE),    # 0 return own frame
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE)) # 4+ variable length list of input control frames
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),          # 0 pos copy
                    ("dlgWidgets", Wye.dType.OBJECT_LIST, None),            # 1 standard dialog widgets
                    ("dlgTags", Wye.dType.STRING_LIST, None),               # 2 OK, Cancel widget tags
                    ("inpTags", Wye.dType.OBJECT, None),                    # 3 dictionary return param ix of input by graphic tag
                    ("currInp", Wye.dType.INTEGER, -1),                     # 4 index to current focus widget, if any
                    ("clickedBtns", Wye.dType.OBJECT_LIST, None),           # 5 list of buttons that need to be unclicked
                    )
        def start(stack):
            #print("Dialog start")

            frame = Wye.codeFrame(TestLib3.Dialog, stack)
            frame.vars[1][0] = []
            frame.vars[2][0] = []
            frame.vars[3][0] = {}
            frame.vars[5][0] = []
            return frame

        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    #print("Dialog pConst", TestLib3.Dialog.pConst)
                    #print("Dialog vConst", TestLib3.Dialog.vConst)
                    #print("Dialog Add dialog", frame.params[TestLib3.Dialog.pConst["title"]][0], ", ", frame, "to focus manager")
                    WyeCore.libs.WyeUI.FocusManager.openDialog(frame, None)

                    print("Dialog run: TestLib3.Dialog.pConst['frame']=", TestLib3.Dialog.pConst["frame"])
                    print("Dialog run: frame.params:", frame.params)
                    frame.params[TestLib3.Dialog.pConst["frame"]][0] = frame  # self referential!
                    #print("Dialog put frame in param[0][0]", frame)
                    frame.vars[TestLib3.Dialog.vConst["position"]] = (frame.params[2])        # save display position
                    # return frame

                    #print("Dialog display: pos=frame.params[2]", frame.params[2])
                    dlg = WyeCore.libs.WyeUI._label3d(text=frame.params[1][0], color=(1, 1, 1, 1), pos=frame.params[2], scale=(.2, .2, .2))
                    frame.vars[1][0].append(dlg)

                    pos = [x for x in frame.params[2]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = (len(frame.params) - 4)
                    #print("Dialog ", nInputs, " user widgets. nParams=", len(frame.params))
                    # draw user- supplied label and text inputs
                    for ii in range(nInputs):
                        pos[2] -= .3

                        #print("Dialog input", ii, " param ", 4+(ii*2))
                        inFrm = frame.params[4+ii][0]
                        #print("    Dialog input ", ii, " inFrm", inFrm)
                        #print("       inFrm.params[1]", inFrm.params[1])
                        print("")
                        if inFrm.verb is TestLib3.TextInput:
                            #print("Input is TextInput")
                            lbl = WyeCore.libs.WyeUI._label3d(inFrm.params[1][0], (1, 0, 0, 1), pos=tuple(pos),
                                                          scale=(.2, .2, .2))
                            frame.vars[1][0].append(lbl)    # save graphic widget for deleting on dialog close

                            # add tag, input index to dictionary
                            frame.vars[3][0][lbl.getTag()] = ii     # tag => inp index dictionary (both label and entry fields point to inp frm)
                            # offset 3d input field past end of 3d label
                            lblGFrm = lbl.text.getFrameActual()
                            width = (lblGFrm[1] - lblGFrm[0]) * .2 + .1
                            txt = WyeCore.libs.WyeUI._label3d(inFrm.vars[1][0], (1, 0, 0, 1),
                                                              pos=(pos[0] + width, pos[1], pos[2]), scale=(.2, .2, .2))
                            #print("    Dialog inWdg", txt)
                            frame.vars[1][0].append(txt)    # save graphic widget for deleting on dialog close
                            inFrm.vars[3][0] = txt          # stash graphic obj in input's frame
                            frame.vars[3][0][txt.getTag()] = ii     # add tag and inp param index to dict (so evt can find inp frame)
                        elif inFrm.verb is TestLib3.ButtonInput:
                            #print("Input is ButtonInput")

                            btn = WyeCore.libs.WyeUI._label3d(inFrm.params[1][0], (1, 0, 0, 1), pos=tuple(pos),
                                                              scale=(.2, .2, .2))
                            frame.vars[1][0].append(btn)  # save for deleting on dialog close
                            frame.vars[3][0][btn.getTag()] = ii  # add tag and inp param index to dict (so evt can find inp frame)
                            inFrm.vars[1][0] = btn  # stash graphic obj in input's frame
                        else:
                            print("Dialog: Error. Unknown input verb", inFrm.verb.__class__)

                    #print("Dialog has input widgets", frame.vars[3])

                    # display OK, Cancel buttons
                    pos[2] -= .3
                    txt = WyeCore.libs.WyeUI._label3d("OK", color=(1, 1, 1, 1), pos=tuple(pos), scale=(.2, .2, .2))
                    frame.vars[1][0].append(txt)
                    frame.vars[2][0].append(txt.getTag())
                    pos[0] += .5
                    txt = WyeCore.libs.WyeUI._label3d("Cancel", color=(1, 1, 1, 1), pos=tuple(pos),
                                                      scale=(.2, .2, .2))
                    frame.vars[1][0].append(txt)
                    frame.vars[2][0].append(txt.getTag())
                    # done setup, go to next case to process events
                    frame.PC += 1

                case 1:
                    # do click-blink for buttons
                    delLst = []
                    # decrement blink count.  if zero, turn off button highlight
                    for btnFrm in frame.vars[TestLib3.Dialog.vConst["clickedBtns"]][0]:
                        btnFrm.vars[TestLib3.ButtonInput.vConst["clickCount"]][0] -= 1
                        if btnFrm.vars[TestLib3.ButtonInput.vConst["clickCount"]][0] <= 0:
                            print("Dialog run: Done click flash for button ", btnFrm.verb.__name__)
                            delLst.append(btnFrm)
                            btnFrm.vars[1][0].setColor((0, 0, 0, 1))
                    # remove any buttons whose count is finished
                    for btnFrm in delLst:
                        print("Dialog run: Remove clicked btn frame", btnFrm.verb.__name__)
                        frame.vars[TestLib3.Dialog.vConst["clickedBtns"]][0].remove(btnFrm)

        def doSelect(frame, tag):
            #print("Dialog doSelect: ", frame.verb, " tag", tag)
            prevSel = frame.vars[4][0]      # get current selection
            # if tag is input field in this dialog, select it
            closing = False

            # if clicked on input field
            if tag in frame.vars[3][0]:        # do we have a matching tag?
                ix = frame.vars[3][0][tag]     # Yes
                inFrm = frame.params[4+ix][0]
                # if is text input make it selected
                if inFrm.verb is TestLib3.TextInput:
                    inWidg = inFrm.vars[3][0]
                    #print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                    inWidg.setColor((0,.25,0,1))        # set input background to "has focus" color
                    frame.vars[TestLib3.Dialog.vConst["currInp"]][0] = ix           # save as current input focus
                # button callback
                elif inFrm.verb is TestLib3.ButtonInput:
                    callVerb = inFrm.vars[2][0]
                    inFrm.vars[1][0].setColor((0, .25, 0, 1)) # set button color pressed
                    if inFrm.vars[TestLib3.ButtonInput.vConst["clickCount"]][0] == 0:
                        inFrm.vars[TestLib3.ButtonInput.vConst["clickCount"]][0] = 10       # start click count down (in display frames)
                        frame.vars[TestLib3.Dialog.vConst["clickedBtns"]][0].append(inFrm)    # stash button for flash countdown
                    # if there
                    if not callVerb is None:
                        print("Dialog doSelect: clicked btn, verb ", callVerb.__name__)
                        print("Dialog frame.params", frame.params)
                        if inFrm.vars[TestLib3.ButtonInput.vConst["verbFrame"]][0] is None:
                            print("       start verb", callVerb.__name__)
                            inFrm.vars[TestLib3.ButtonInput.vConst["verbFrame"]][0] = callVerb.start([])
                        else:
                            print("       already have verb frame", inFrm.vars[TestLib3.ButtonInput.vConst["verbFrame"]][0].verb.__name__)
                        verbFrm = inFrm.vars[TestLib3.ButtonInput.vConst["verbFrame"]][0]
                        # if there's something on the callback verb's stack, call it
                        if len(verbFrm.SP) > 0:
                            print("       verb stack len", len(verbFrm.SP), " run top of stack", verbFrm.SP[-1].verb.__name__)
                            runFrm = verbFrm.SP[-1]
                            runFrm.verb.run(runFrm)
                        else:
                            # nothing on stack, just call verb
                            print("       nothing on verb stack, run verb", verbFrm.verb.__name__)
                            verbFrm.verb.run(verbFrm)
                        if verbFrm.status != Wye.status.CONTINUE:
                            print("       verb done, status", Wye.status.tostring(verbFrm.status))
                            inFrm.vars[TestLib3.ButtonInput.vConst["verbFrame"]][0] = None
                        else:
                            print("       verb run done, status CONTINUE")
                        print("Dialog doSelect done, frame.params", frame.params)
                    frame.vars[TestLib3.Dialog.vConst["currInp"]][0] = -1       # no input has focus

            # if clicked on OK or Cancel
            elif tag in frame.vars[2][0]:
                # if is OK button
                if tag == frame.vars[2][0][0]:
                    #print("Dialog", frame.params[1][0], " OK Button pressed")
                    nInputs = (len(frame.params) - 4)
                    for ii in range(nInputs):
                        inFrm = frame.params[4+ii][0]
                        # for any text inputs, copy working string to return string
                        if inFrm.verb is TestLib3.TextInput:
                            #print("input", ii, " frame", inFrm, "\n", WyeCore.Utils.frameToString(inFrm))
                            #print("input old val '"+ inFrm.params[2][0]+ "' replaced with '"+ inFrm.vars[1][0]+"'")
                            inFrm.params[2][0] = inFrm.vars[1][0]
                    frame.status = Wye.status.SUCCESS

                # else is Cancel button
                else:
                    #print("Dialog", frame.params[1][0], " Cancel Button pressed")
                    frame.status = Wye.status.FAIL
                # clean up dialog
                #print("Close dialog")
                # remove dialog from active dialog list
                WyeCore.libs.WyeUI.FocusManager.closeDialog(frame)
                # delete the graphic widgets associated with the dialog
                for wdg in frame.vars[1][0]:
                    #print("del ctl ", wdg.text.name)
                    wdg.removeNode()
                closing = True

            # selected graphic tag not recognized as a control in this dialog
            else:
                frame.vars[4][0] = -1   # no currInp

            # If there was a diff selection before, fix that
            # (if closing dialog, nevermind)
            if prevSel > -1 and prevSel != frame.vars[4][0] and not closing:
                inFrm =frame.params[4+prevSel][0]
                if inFrm.verb is TestLib3.TextInput:
                    inWidg = inFrm.vars[3][0]
                    inWidg.setColor((0,0,0, 1))

        def doKey(frame, key):
            # if we have an input with focus
            ix = frame.vars[4][0]
            if ix >= 0:
                inFrm = frame.params[4 + ix][0]
                txt = inFrm.vars[1][0]
                insPt = inFrm.vars[2][0]
                preTxt = txt[:insPt]
                postTxt = txt[insPt:]
                # delete key
                if key == '\u0008':
                    if insPt > 0:
                        preTxt = preTxt[:-1]
                        insPt -= 1
                        inFrm.vars[2][0] = insPt
                    txt = preTxt + postTxt
                # arrow keys
                elif key == Wye.ctlKeys.LEFT:
                    if insPt > 0:
                        insPt -= 1
                        inFrm.vars[2][0] = insPt
                    return
                elif key == Wye.ctlKeys.RIGHT:
                    if insPt < len(txt):
                        insPt += 1
                        inFrm.vars[2][0] = insPt
                    return
                # printable key, insert it in the string
                else:
                    txt = preTxt + key + postTxt
                    insPt += 1
                    inFrm.vars[2][0] = insPt
                inFrm.vars[1][0] = txt
                inWidg = inFrm.vars[3][0]
                #print("  set text", txt," ix", ix, " txtWidget", inWidg)
                inWidg.setText(txt)

    class BtnCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(TestLib3.BtnCallback, stack)

        def run(frame):
            print("BtnCallback! count = ", frame.vars[TestLib3.BtnCallback.vConst["count"]][0])
            frame.vars[TestLib3.BtnCallback.vConst["count"]][0] += 1
            if frame.vars[TestLib3.BtnCallback.vConst["count"]][0] > 5:
                frame.status = Wye.status.SUCCESS

    class BtnCallback2:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("id", Wye.dType.OBJECT, None),                 # 0
                    ("Title", Wye.dType.INTEGER, "Test Dialog 3"),    # 1
                    ("text1ID", Wye.dType.STRING, ""),              # 2
                    ("text1Val", Wye.dType.STRING, ""),        # 3
                    ("text2ID", Wye.dType.STRING, ""),              # 4
                    ("text2Val", Wye.dType.STRING, "<val1>"),        # 5

                    ("id1", Wye.dType.OBJECT, None),  # 6
        )

        codeDescr = (
            (None, "print('Callback 2, create dialog')"),
            ("TestLib3.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
             (None, "(0,10,0)"), (None, "None"),
             ("TestLib3.TextInput", (None, "frame.vars[2]"),
              (None, "['TextLabel']"),
              (None, "frame.vars[3]")
              ),
             ("TestLib3.TextInput", (None, "frame.vars[4]"),
              (None, "['Text2Label']"),
              (None, "frame.vars[5]")
              ),
             ("TestLib3.ButtonInput", (None, "frame.vars[6]"),
              (None, "['Click Me!']"),
              (None, "[TestLib3.BtnCallback]")
              ),
             ),
            ("Label", "Done"),
            (None, "print('Callback 2 done with SUCCESS')"),
            (None, "frame.status = Wye.status.SUCCESS")
        )

        def build():
            return WyeCore.Utils.buildCodeText("BtnCallback2", TestLib3.BtnCallback2.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib3.BtnCallback2, stack)

        def run(frame):
            TestLib3.TestLib3_rt.BtnCallback2_run_rt(frame)


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

                    ("id1", Wye.dType.OBJECT, None), # 12
                    )

        codeDescr = (
            #(None, "print('DlgTst frame before Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("TestLib3.Dialog", (None, "frame.vars[0]"), (None, "frame.vars[1]"),
                                (None, "(-1,10,0)"), (None, "None"),
                                ("TestLib3.TextInput", (None, "frame.vars[2]"),
                                  (None, "['T1Label']"),
                                  (None, "frame.vars[3]")
                                ),
                                ("TestLib3.TextInput", (None, "frame.vars[4]"),
                                 (None, "['T2Label']"),
                                 (None, "frame.vars[5]")
                                ),
                                ("TestLib3.ButtonInput", (None, "frame.vars[12]"),
                                  (None, "['Click Me!']"),
                                  (None, "[TestLib3.BtnCallback2]")
                                ),
             ),
            #(None, "print('DlgTst frame 1 vars', frame.vars)"),
            #(None, "print('DlgTst frame after Dialog 1',WyeCore.Utils.frameToString(frame))"),
            ("TestLib3.Dialog", (None, "frame.vars[6]"), (None, "frame.vars[7]"),
                               (None, "(1,10,0)"), (None, "None"),
                               ("TestLib3.TextInput", (None, "frame.vars[8]"),
                                (None, "['T3Label']"),
                                (None, "frame.vars[9]")
                               ),
                               ("TestLib3.TextInput", (None, "frame.vars[10]"),
                                  (None, "['T4Label']"),
                                  (None, "frame.vars[11]")
                               )
            ),
            ("Label", "Done")
        )

        def build():
            return WyeCore.Utils.buildCodeText("DlgTst", TestLib3.DlgTst.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib3.DlgTst, stack)

        def run(frame):
            TestLib3.TestLib3_rt.DlgTst_run_rt(frame)