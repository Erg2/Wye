from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback
from direct.showbase import Audio3DManager
import math
import inspect      # for debugging
from panda3d.core import LQuaternionf

class TestLib:
    def build():
        WyeCore.Utils.buildLib(TestLib)

    class showAvailLibs:
        cType = Wye.cType.VERB
        mode = Wye.mode.MULTI_CYCLE

    class libDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        # autoStart = True
        paramDescr = (("retStat", Wye.dType.INTEGER, Wye.access.REFERENCE),
                      ("coord", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE))
        varDescr = (("dlgFrm", Wye.dType.OBJECT, [None]),
                    ("selVerb", Wye.dType.INTEGER, -1),)

        def start(stack):
            return Wye.codeFrame(TestLib.libDialog, stack)

        def run(frame):
            match (frame.PC):
                case 0:
                    #print("libDialog, put up lib dropdown")
                    lib = WyeCore.libs.TestLib
                    dlgFrm = WyeCore.libs.WyeUI.DropDown.start([])

                    dlgFrm.params.retVal = frame.params.retStat
                    dlgFrm.params.title = [lib.__name__]
                    dlgFrm.params.position = [frame.params.coord[0]]
                    dlgFrm.params.parent = [None]
                    frame.vars.dlgFrm[0] = dlgFrm

                    # build dialog frame params list of input frames
                    attrIx = 0
                    # print("_displayLib: process library", lib.__name__)
                    for attr in dir(lib):
                        if attr != "__class__":
                            verb = getattr(lib, attr)
                            if inspect.isclass(verb):
                                # print("lib", lib.__name__, " verb", verb.__name__)
                                btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                                dlgFrm.params.inputs[0].append([btnFrm])

                                txt = lib.__name__ + "." + verb.__name__
                                btnFrm.params.frame = [None]
                                btnFrm.params.parent = [None]  # return value
                                btnFrm.params.label = [txt]  # button label is verb name
                                btnFrm.params.callback = [WyeCore.libs.WyeUI.DropdownCallback]  # button callback
                                btnFrm.params.optData = [(attrIx, frame)]  # button data - offset to button
                                WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                                attrIx += 1

                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)     # push dialog so it runs next cycle

                    frame.PC += 1               # on return from dialog, run next case

                case 1:
                    frame.SP.pop()  # remove dialog frame from stack
                    print("libDialog: returned status", frame.params.retStat[0]) # Wye.status.tostring(frame.))
                    frame.status = Wye.status.SUCCESS  # done
                    #frame.PC = 0    # do it again


    class libButton:
        cType = Wye.cType.OBJECT
        #autoStart = True
        mode = Wye.mode.PARALLEL
        parTermType = Wye.parTermType.FIRST_FAIL
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("libButton", Wye.dType.OBJECT, None),                # 0
                    ("doitId", Wye.dType.STRING, ""),                   # 1
                    ("retChar", Wye.dType.STRING, ""),                   # 2
                    ("retStat", Wye.dType.INTEGER, -1),                   # 2
                    )

        codeDescr = (
            (
                (None, "frame.vars.libButton[0] = WyeCore.libs.WyeUI._3dText(text='Display Library',color=(1,1,1,1), pos=(1.5,10,2), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.libButton[0].getTag()"),
                #(None, "print('libButton frame0: loaded button & id vars')"),
                (None, "frame.status = Wye.status.SUCCESS")
            ),
            (
                ("Label", "ClickLoop"),
                #(None, "print('libButton wait for click')"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                #(None, "print('libButton put up lib dialog')"),
                ("WyeCore.libs.TestLib.libDialog", (None, "frame.vars.retStat"), (None, "[(1.5,10,1.5)]")),
                #(None, "print('libButton returned from libDialog. retVal', frame.vars.retStat)"),
                ("GoTo", "ClickLoop"),
            ),
        #    (
        #        ("Label", "TextLoop"),
        #        #(None, "print('libButton stream2: wait for char')"),
        #        ("WyeCore.libs.WyeLib.waitChar", (None, "frame.vars.retChar"), (None, "frame.vars.doitId")),
        #        (None, "print('libButton stream2: received char', frame.vars.retChar[0])"),
        #        ("GoTo", "TextLoop")
        #    )
        )

        def build():
            #print("Testlib2 build testCompiledPar")
            return WyeCore.Utils.buildParallelText("TestLib", "libButton", TestLib.libButton.codeDescr)

        def start(stack):
            return TestLib.TestLib_rt.libButton_start_rt(stack)        # run compiled start code to build parallel code stacks

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
            inFrm = frame.eventData[1][0]       #
            var = frame.eventData[1][1]         # caller's counter variable
            # print("data [1]", frame.eventData[1][1], " var", var)
            dlgFrm = inFrm.parentFrame
            # print("BtnCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])

            var[0] += 1

            # get label input's frame from parent dialog
            lblFrame = dlgFrm.params.inputs[0][3][0]

            # supreme hackery - look up the display label in the label's graphic widget list
            # Update its text string with the current count value
            inWidg = lblFrame.vars.gWidgetStack[0][0]
            txt = "Count " + str(var[0])
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(txt)

            if var[0] >= 10:
                var[0] = 0

    class testDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.INTEGER
        #autoStart = True
        paramDescr = ()
        varDescr = (("dlgRetVal", Wye.dType.INTEGER, -1),
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
            #(None, "print('testDialog, startup - create param list ')"),
            ("WyeUI.Dialog", (None, "frame.vars.dlgRetVal"),    # frame
             (None, "frame.vars.Title"),                        # title
             (None, "((-1,11,1))"),                              # position
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
            #(None, "print('testDialog retList=', frame.vars.retList[0])"),
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


    class fishDlgButton:
        cType = Wye.cType.OBJECT
        #autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        #parTermType = Wye.parTermType.FIRST_FAIL
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("libButton", Wye.dType.OBJECT, None),                # 0
                    ("doitId", Wye.dType.STRING, ""),                   # 1
                    ("retChar", Wye.dType.STRING, ""),                   # 2
                    ("dlgStatus", Wye.dType.INTEGER, 0)
                    )

        codeDescr = (

                (None, "frame.vars.libButton[0] = WyeCore.libs.WyeUI._3dText(text='Open Fish Angle Dialog',color=(1,1,1,1), pos=(-3,10,1), scale=(.2,.2,.2))"),
                (None, "frame.vars.doitId[0] = frame.vars.libButton[0].getTag()"),
                #(None, "print('libButton frame0: loaded button & id vars')"),

                ("Label", "ClickLoop"),
                #(None, "print('fishbutton: waitclick')"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),
                #(None, "print('fishbutton: open showFishDialog')"),
                ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.dlgStatus"), ("TestLib.showFishDialog",(None, "[1]"))),
                #(None, "print('passed showFishDialog. Status', frame.vars.dlgStatus[0], ' go loop')"),
                ("GoTo", "ClickLoop")
            )

        def build():
            print("Build fishDlgButton")
            return WyeCore.Utils.buildCodeText("fishDlgButton", TestLib.fishDlgButton.codeDescr)

        def start(stack):
            #print("fishDlgButton object start")
            return Wye.codeFrame(TestLib.fishDlgButton, stack)

        def run(frame):
            #print("Run testDialog")
            TestLib.TestLib_rt.fishDlgButton_run_rt(frame)

    class UpdateCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            return Wye.codeFrame(TestLib.UpdateCallback, stack)

        def run(frame):
            #print("UpdateCallback data=", frame.eventData, " verb", frame.eventData[1].verb.__name__)

            frm = frame.eventData[1]
            ctlFrm = frame.eventData[2]
            dlgFrm = ctlFrm.parentFrame
            print("dlgFrame", dlgFrm)
            # print("UpdateCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
            #print("Update x", int(dlgFrm.vars.XAngle[0]), " y", int(dlgFrm.vars.YAngle[0]), " z", int(dlgFrm.vars.ZAngle[0]))

            # inputs don't update parent variables until "OK" - which makes "Cancel" work correctly
            # so have to pull out the temp values from the input controls
            # Do some hackery to get to the pop up dialog's inputs' local variables
            #print("dlgFrm", dlgFrm.params.title)
            x = dlgFrm.params.inputs[0][0][0].vars.currVal[0]
            y = dlgFrm.params.inputs[0][1][0].vars.currVal[0]
            z = dlgFrm.params.inputs[0][2][0].vars.currVal[0]

            frm.vars.target[0].vars.gObj[0].setHpr(int(x), int(y), int(z))


    # find and set angle of wiggle fish (testObj2)
    class showFishDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        #autoStart = True
        paramDescr = (("dummy", Wye.dType.INTEGER,  Wye.access.REFERENCE),)
        varDescr = (("dlgRetVal", Wye.dType.INTEGER, -1),
                    ("dialogFrm", Wye.dType.OBJECT, None),
                    ("XAngleID", Wye.dType.STRING, ""),
                    ("XAngle", Wye.dType.INTEGER, 0),
                    ("YAngleID", Wye.dType.STRING, ""),
                    ("YAngle", Wye.dType.INTEGER, 0),
                    ("ZAngleID", Wye.dType.STRING, ""),
                    ("ZAngle", Wye.dType.INTEGER, 0),
                    ("updateBtnId", Wye.dType.OBJECT, None),
                    ("dlgButton", Wye.dType.OBJECT, None),
                    ("doitId", Wye.dType.OBJECT, None),
                    ("target", Wye.dType.OBJECT, None),
                    )

        codeDescr = (


            #(None, "frame.vars.dlgButton[0] = WyeCore.libs.WyeUI._3dText(text='Set Fish Angle',color=(1,1,1,1), pos=(-3,9,1), scale=(.2,.2,.2))"),
            #(None, "print('TestLib ShowFishDialog')"),
            (None, "frame.vars.dlgButton[0] = WyeCore.libs.WyeUI._3dText(text='Set Fish Angle',color=(1,1,1,1), pos=(-3,0,1), scale=(.2,.2,.2))"),
            (None, "frame.vars.doitId[0] = frame.vars.dlgButton[0].getTag()"),

            ("Label", "PopDialog"),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.doitId")),

            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.target"),
             (None, "[WyeCore.World.findActiveObj('testObj2')]")),
            ("IfGoTo", "frame.vars.target[0] is None", "PopDialog"),
            ("WyeCore.libs.WyeLib.setEqual",
                (None, "frame.vars.dialogFrm"),
                ("WyeUI.Dialog", (None, "frame.vars.dlgRetVal"),    # frame
                 (None, "['Fish Angle Dialog']"),                   # title
                 (None, "((-3,8,1),)"),                              # position
                 (None, "[None]"),                                  # parent
                 ("WyeUI.InputInteger", (None, "frame.vars.XAngleID"),   # inputs (variable length)
                  (None, "['XAngle']"),
                  (None, "frame.vars.XAngle")
                  ),
                 ("WyeUI.InputInteger", (None, "frame.vars.YAngleID"),
                  (None, "['YAngle']"),
                  (None, "frame.vars.YAngle")
                  ),
                 ("WyeUI.InputInteger", (None, "frame.vars.ZAngleID"),
                  (None, "['ZAngle']"),
                  (None, "frame.vars.ZAngle")
                  ),
                 ("WyeUI.InputButton", (None, "frame.vars.updateBtnId"),
                  (None, "['Update']"),
                  (None, "[TestLib.UpdateCallback]"),
                  (None, "[frame]")
                  ),
                 ),
             ),
            #(None, "print('showFishDialog closed. status', frame.vars.dlgRetVal[0])"),
            ("IfGoTo", "frame.vars.dlgRetVal[0] != Wye.status.SUCCESS", "PopDialog"),
            #(None, "print('showFishDialog OK, set angle')"),
            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.target[0].vars.gObj"),
                (None, "[[int(frame.vars.XAngle[0]),int(frame.vars.YAngle[0]),int(frame.vars.ZAngle[0])]]")),
            ("GoTo", "PopDialog")
        )

        def build():
            print("Build showFishDialog")
            return WyeCore.Utils.buildCodeText("showFishDialog", TestLib.showFishDialog.codeDescr)

        def start(stack):
            #print("showFishDialog object start")
            return Wye.codeFrame(TestLib.showFishDialog, stack)

        def run(frame):
            #print("Run testDialogshowFishDialog")
            TestLib.TestLib_rt.showFishDialog_run_rt(frame)



    # load model passed in at loc, scale passed in
    class testLoader:
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
            # call loadModel with testLoader params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.params.obj"), (None, "frame.params.file")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params.tag"), (None, "frame.params.obj")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params.obj"), (None, "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.params.obj"), (None, "frame.params.posVec"), (None, "frame.params.scaleVec"))
        )
        code = None

        def build():
            return WyeCore.Utils.buildCodeText("testLoader", TestLib.testLoader.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader_run_rt(frame)


    # when clicked, use spin to wiggle object back and forth
    class clickWiggle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),
                    ("sound", Wye.dType.OBJECT, None))
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.clickWiggle, stack)

        def run(frame):
            global base
            #print('execute spin, params', frame.params, ' vars', frame.vars)

            gObj = frame.params.obj[0]
            vec = gObj.getHpr()
            axis = frame.params.axis[0]
            #print("Current HPR ", vec)
            match frame.PC:
                case 0:
                    WyeCore.World.setEventCallback("click", frame.params.tag[0], frame)
                    # frame.vars.sound[0] = base.loader.loadSfx("WyePop.wav")
                    audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                    frame.vars.sound[0] = audio3d.loadSfx("WyePew.wav")
                    audio3d.attachSoundToObject(frame.vars.sound[0], frame.params.obj[0])
                    frame.PC += 1
                    #print("clickWiggle waiting for event 'click' on tag ", frame.params.tag[0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    frame.vars.sound[0].play()
                    frame.PC += 1

                case 3:
                    vec[axis] += 5
                    #print("spin (pos) obj", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] > 45:   # end of swing this way
                        frame.PC += 1  # go to next state

                case 4:
                    vec[axis] -= 5
                    #print("spin (neg) obj ", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] < -45:    # end of swing other way
                        frame.PC += 1   # go to previous state

                case 5:
                    frame.vars.rotCt[0] += 1  # count cycles
                    if frame.vars.rotCt[0] < 2:  # wiggle this many times, then exit
                        frame.PC = 3    # go do another wiggle
                    else:
                        # finish by coming back to zero
                        vec[axis] += 5
                        #print("spin (neg) obj ", gObj, "to", vec)
                        gObj.setHpr(vec[0], vec[1], vec[2])
                        if vec[axis] >= 0:    # end of swing other way
                            #print("clickWiggle: done")
                            frame.status = Wye.status.SUCCESS


                case _:
                    frame.status = Wye.status.SUCCESS


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

    # school of fish chase leaderFish
    class fish:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("fishes", Wye.dType.OBJECT_LIST, None),        # fish graphic objs
                    ("fishTags", Wye.dType.STRING, ""),
                    ("position", Wye.dType.FLOAT_LIST, [0,0,0]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., -0.02]),
                    ("angle", Wye.dType.FLOAT_LIST, [0., 90., 0.]),
                    ("followDist", Wye.dType.FLOAT, .4),
                    ("target", Wye.dType.OBJECT, None),             # leader fish Wye obj frame
                    ("tgtDist", Wye.dType.FLOAT, 0),
                    ("count", Wye.dType.INTEGER, 0),        # loop counter
                    ("nFish", Wye.dType.INTEGER, 3),        # total number of fish
                    ("objAhead", Wye.dType.OBJECT, None),   # object in front of this one in train
                    )
        codeDescr=(
            #(None, ("print('fish case 0: set up object')")),
            # initialize arrays
            (None, "frame.vars.fishes = []"),
            (None, "frame.vars.fishTags = []"),

            ("Label", "MakeFish"),
            #(None, "print('makeFish loop start: count', frame.vars.count[0])"),
            (None, "frame.vars.fishes.append([None])"),     # create entry for fish
            (None, "frame.vars.fishTags.append([''])"),
            (None, "objNm = 'flyer_0'+str((frame.vars.count[0] % 3)+2)+'.glb'"),
            # load object
            ("WyeCore.libs.WyeLib.loadObject",
             (None, "[frame]"),
             (None, "frame.vars.fishes[frame.vars.count[0]]"),
             (None, "[objNm]"),
             (None, "[[frame.vars.count[0] ,2, -.5]]"),  # posVec
             (None, "[[0, 90, 0]]"),  # rotVec
             (None, "[[.25,.25,.25]]"),  # scaleVec
             (None, "frame.vars.fishTags[frame.vars.count[0]]"),
             (None, "[[((frame.vars.count[0] % 3)+1)/3.,1,0,1]]")  # color
             ),
            (None, "frame.vars.count[0] += 1"),     # next fish
            ("IfGoTo", "frame.vars.count[0] < frame.vars.nFish[0]", "MakeFish"),      # if not done, loop for next fish

            # Find leader fish
            ("WyeCore.libs.WyeLib.setEqual", (None, "frame.vars.target"), (None, "[WyeCore.World.findActiveObj('leaderFish')]")),
            (None, "frame.vars.count[0] = 0"),
            (None, "frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),  # first fish follows leader

            ("Label", "SwimLoop"),    # used to be loop moving fish.  Unrolled loop 'cause IfGoTo lost a frame to each fish so jerky movement
            # orient toward fish in front
            (None, "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),  # orient toward fish in front
            (None, "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),      # flip to face up
            (None, "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            (None, "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.fishes[frame.vars.count[0]]"), (None, "frame.vars.dPos")),
            (None, "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish
            (None, "frame.vars.count[0] += 1"),     # next fish

            # orient toward fish in front
            (None, "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
            (None, "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
            (None, "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            (None, "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.fishes[frame.vars.count[0]]"), (None, "frame.vars.dPos")),
            (None, "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish
            (None, "frame.vars.count[0] += 1"),  # next fish

            # orient toward fish in front
            (None, "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
            (None, "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
            (None, "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            (None, "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.fishes[frame.vars.count[0]]"), (None, "frame.vars.dPos")),
            (None, "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish

            #("IfGoTo", "frame.vars.count[0] < frame.vars.nFish[0]", "SwimLoop"),  # if not done, loop for next fish
            (None, "frame.vars.count[0] = 0"),
            (None, "frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),  # first fish follows leader

            # Save new position
            ("WyeCore.libs.WyeLib.getObjPos", (None, "frame.vars.position"), (None, ("frame.vars.fishes[0]"))),
            ("GoTo", "SwimLoop")
        )

        def build():
            #print("Build fish")
            return WyeCore.Utils.buildCodeText("fish", TestLib.fish.codeDescr)

        def start(stack):
            #print("fish object start")
            return Wye.codeFrame(TestLib.fish, stack)

        def run(frame):
            #print("Run fish")
            TestLib.TestLib_rt.fish_run_rt(frame)

    # fish chases target
    class leaderFish:
        cType = Wye.cType.OBJECT
        mode = Wye.mode.PARALLEL
        parTermType = Wye.parTermType.FIRST_FAIL
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("fish", Wye.dType.OBJECT, None),
                    ("fishTag", Wye.dType.STRING, "obj1Tag"),
                    ("tgtPos", Wye.dType.FLOAT_LIST, [0, 0, 0]),
                    ("tgtDist", Wye.dType.FLOAT, 1.),
                    ("dPos", Wye.dType.FLOAT_LIST, [0.,0.,0]),
                    ("posStep", Wye.dType.FLOAT, .03),
                    ("fudge0", Wye.dType.FLOAT, .5),
                    ("fudge1", Wye.dType.FLOAT, .5),
                    ("fudge2", Wye.dType.FLOAT, .5),
                    ("sound", Wye.dType.OBJECT, None),
                    ("box", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, (0,0,0)),
                    ("prevState", Wye.dType.INTEGER, 0),
                    ("startQ", Wye.dType.OBJECT, None),
                    ("endQ", Wye.dType.OBJECT, None),
                    ("deltaT", Wye.dType.FLOAT, 0.005),
                    ("lerpT", Wye.dType.FLOAT, 0.),
                    ("border", Wye.dType.FLOAT, 5.),
                    ("ceil", Wye.dType.FLOAT, 2.),
                    )

        codeDescr=(
            (
                ("Code", "frame.vars.deltaV=[[0,0,0]]"),
                ("WyeCore.libs.WyeLib.loadObject",
                 (None, "[frame]"),
                 (None, "frame.vars.fish"),
                 (None, "['flyer_01.glb']"),
                 (None, "frame.vars.position"),  # posVec
                 (None, "[[0, 0, 0]]"),  # rotVec
                 (None, "[[.25,.25,.25]]"),  # scaleVec
                 (None, "frame.vars.fishTag"),
                 (None, "[[1,0,0,1]]")
                 ),


                #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.obj1"),(None, "[0,5,-.5]")),
                ("Code", "from panda3d.core import LPoint3f"),
                #(None, "print('tgtPos', frame.vars.tgtPos)"),
                # convert tgtPos from list to LPoint3f
                ("Expr", "frame.vars.tgtPos[0] = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])"),
                ("Expr", "frame.vars.dPos[0][2] = -frame.vars.posStep[0]"),
                ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.fish"), (None, "[[0,90,0]]")),
                #(None, "frame.vars.box[0] = WyeCore.libs.WyeUI._box([.1,.1,.1], frame.vars.tgtPos[0])"),
                ("Expr", "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),

                ("Label", "StartLoop"),

                # Test raw code block
                ("Code",'''
#quat = Quat()
#lookAt(quat, target - nodePath.getPos(), Vec3.up())
#nodePath.setQuat(quat)
                
                
#  if (_start_quat.dot(_end_quat) < 0.0f) {
#    // Make sure both quaternions are on the same side.
#    _start_quat = -_start_quat;
#  }
  
  
fish = frame.vars.fish[0]
fishPos = fish.getPos()
tgtPos = frame.vars.tgtPos[0]
# stay in local area
dist = (frame.vars.fish[0].getPos() - tgtPos).length()
if fishPos[2] > (tgtPos[2] + frame.vars.ceil[0]) or fishPos[2] < (tgtPos[2] - frame.vars.ceil[0]) or dist > frame.vars.border[0]:
        #print(">10")
        global render
        from panda3d.core import lookAt, Quat, LQuaternionf, LVector3f, Vec3
        

        alpha = frame.vars.deltaT[0]      # how much to rotate each step (0..1)    
                
        # first time this cycle
        if frame.vars.prevState[0] != 2:
            # save rotation start, calc rotation end and save
            
            # start
            fishQ = LQuaternionf()
            fishHPR = fish.getHpr()
            fishQ.setHpr(fishHPR)

            # end
            tgtDeltaVec = tgtPos - fishPos    # note: guaranteed 10 units away, so zero length not an issue
            tgtVec = (tgtDeltaVec).normalized()
            
            #fwdVec = render.getRelativeVector(fish, Vec3.down()).normalized()
            #deltaVec = LVector3f(tgtVec[0]-fwdVec[0], tgtVec[1]-fwdVec[1], tgtVec[2]-fwdVec[2])
            #deltaVec = tgtVec - fwdVec            
            #newVec = fwdVec + deltaVec * alpha
            #tgtQuat = Quat()
            #lookAt(tgtQuat, newVec, Vec3.up())
            
            tgtQuat = Quat()
            lookAt(tgtQuat, tgtVec, Vec3.up())
            q90 = Quat()
            q90.setHpr((0,90,0))
            tgtQ = q90 * tgtQuat
            
            # put info in frame for nlerp
            frame.vars.startQ[0] = fishQ   
            frame.vars.endQ[0] = tgtQ
            frame.vars.lerpT[0] = alpha
            
            frame.vars.prevState[0] = 2    
            
            #print("tgtPos", tgtPos, " tgtQ", tgtQ) #fish.setQuat(tgtQ)")
            #fish.setQuat(tgtQ)
            
            
        if frame.vars.lerpT[0] < 1.0:
            fishQ = frame.vars.startQ[0]
            tgtQ = frame.vars.endQ[0]
            tt = frame.vars.lerpT[0]
            quat = WyeCore.Utils.nlerp(fishQ, tgtQ, tt)
            fish.setQuat(quat)
            frame.vars.lerpT[0] += alpha
            #fish.setP(fish, 90)
        else:
            frame.vars.prevState[0] = 0    
        
else:
        #print("2<d<=10")
        fishHPR = fish.getHpr()     # get current direction         
        
        # flip directions every new cycle
        if frame.vars.prevState[0] != 1:
            from random import random            
            frame.vars.fudge0[0] *= (1 if random() > .5 else -1)
            frame.vars.fudge1[0] *= (1 if random() > .5 else -1)
            frame.vars.fudge2[0] *= (1 if random() > .5 else -1)
            
        f0 = frame.vars.fudge0[0]
        f1 = frame.vars.fudge1[0]
        f2 = frame.vars.fudge2[0]
        
        moveAngle = (f0, f1/2, f2/5)
        #moveAngle = (eA, eA/10, eA/20)        
        fishHPR += moveAngle
        #print("fishHPR", fishHPR, " tgtHPR", tgtHPR, " moveAngle", moveAngle," setHpr", fishHPR)
        fish.setHpr(fishHPR)        
        frame.vars.prevState[0] = 1

                '''),
                # Step forward
                ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.fish"), (None, "frame.vars.dPos")),

                # save new position
                ("WyeCore.libs.WyeLib.getObjPos", (None, "frame.vars.position"), (None, "frame.vars.fish")),

                ("GoTo", "StartLoop"),

                # randomly move target around
                ("Code", "from random import random"),
                ("IfGoTo", "random() < .99", "StartLoop"),

                ("Code", "from panda3d.core import LPoint3f"),
                ("Expr", "frame.vars.tgtPos[0] = LPoint3f((random()-.5)*5, (random()-.5)*5 + 10, 0)"),
                (None, "print('new target point', frame.vars.tgtPos[0])"),
                #("Expr", "frame.vars.fudge[0] = frame.vars.fudge[0] * -1"),
                #(None, "frame.vars.box[0].path.setPos(frame.vars.tgtPos[0])"),



                ("GoTo", "StartLoop")

            ),
            (
                ("Label", "top"),
                ("IfGoTo", "frame.vars.fishTag[0] == ''", "top"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.fishTag")),
                ("Expr", "frame.vars.fudge[0] = frame.vars.fudge[0] * -1"),
                ("Code", "frame.vars.sound[0].play()"),
                #(None, "print('clicked leaderFish')"),

                ("GoTo", "top")
            )
        )


        def build():
            #print("Build leaderFish")
            #return WyeCore.Utils.buildCodeText("leaderFish", TestLib.leaderFish.codeDescr)
            return WyeCore.Utils.buildParallelText("TestLib", "leaderFish", TestLib.leaderFish.codeDescr)

        def start(stack):
            #print("leaderFish object start")
            #return Wye.codeFrame(TestLib.leaderFish, stack)
            return TestLib.TestLib_rt.leaderFish_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            #print("Run leaderFish")
            #TestLib.TestLib_rt.leaderFish_run_rt(frame)
            frame.runParallel()

    # Put up "clickWiggle" fish
    class testObj2:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = (("ret", Wye.dType.INTEGER, Wye.access.REFERENCE),)  # gotta have a ret param
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, "objTag"),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [-1,5,-.5]),
                    )  # var 4

        codeDescr=(
            #(None, ("print('testObj2 case 0: start - set up object')")),
            ("WyeCore.libs.WyeLib.loadObject",
                (None, "[frame]"),
                (None, "frame.vars.gObj"),
                (None, "['flyer_01.glb']"),
                (None, "frame.vars.position"),       # posVec
                (None, "[[0, 90, 0]]"),      # rotVec
                (None, "[[.75,.75,.75]]"),    # scaleVec
                (None, "frame.vars.objTag"),
                (None, "[[0,1,0,1]]")
            ),
            #("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),

            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            (None, "frame.vars.sound[0] = base.loader.loadSfx('WyePew.wav')"),
            ("Label", "Repeat"),
            ("TestLib.clickWiggle", (None, "frame.vars.gObj"), (None, "frame.vars.objTag"), (None, "[1]")),
            #("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.objTag")),
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


