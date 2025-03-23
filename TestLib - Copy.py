from Wye import Wye
from WyeCore import WyeCore
import sys
import traceback
import math
import inspect      # for debugging
from panda3d.core import LQuaternionf

class TestLib:
    def build():
        #print("build TestLib")
        WyeCore.Utils.buildLib(TestLib)

    # circling fish
    class testObj3:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, ""),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [-35,75,2]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., -.05]),
                    ("dAngle", Wye.dType.FLOAT_LIST, [0., 0., -.75]),
                    ("colorWk", Wye.dType.FLOAT_LIST, [1, 1, 1]),
                    ("colorInc", Wye.dType.FLOAT_LIST, [8, 8, 8]),
                    ("color", Wye.dType.FLOAT_LIST, [0, .33, .66, 1]),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )  # var 4

        codeDescr=(
            #(None, ("print('testObj3 case 0: start - set up object')")),
            ("Var=", "frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
                (None, "[frame]"),
                (None, "frame.vars.gObj"),
                (None, "['flyer_01.glb']"),
                (None, "frame.vars.position"),       # posVec
                (None, "[[0, 90, 0]]"),      # rotVec
                (None, "[[2,2,2]]"),    # scaleVec
                (None, "frame.vars.objTag"),
                (None, "frame.vars.color"),
                ("Var", "frame.vars.cleanUpObjs"),
            ),
            #("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            #(None, "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
            ("Label", "Repeat"),
            # set angle
            #("Code", "print('testObj3 run')"),
            ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngle")),
            # Step forward
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
            # set color
            ("Var=", "frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
            ("Var=", "frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
            # todo Next two lines are horrible - if followed by then expression indented - they have to be together
            # todo Think of a better way to do if/else than block code or sequential single expressions (EWWW!!)
            ("Code", "if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
            ("Code", " frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
            ("Code", " frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
            ("Var=", "frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.vars.gObj"), ("Var", "frame.vars.color")),

            ("GoTo", "Repeat")
        )

        def build(rowRef):
            #print("Build testObj3")
            return WyeCore.Utils.buildCodeText("testObj3", TestLib.testObj3.codeDescr, TestLib.testObj3, rowRef)

        def start(stack):
            #print("testObj3 object start")
            return Wye.codeFrame(TestLib.testObj3, stack)

        def run(frame):
            #print("Run testObj3")
            TestLib.TestLib_rt.testObj3_run_rt(frame)




    # circling fish
    class testObj3b:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, ""),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [-35,75,0]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., -.05]),
                    ("dAngle", Wye.dType.FLOAT_LIST, [0., 0., -.70]),
                    ("colorWk", Wye.dType.FLOAT_LIST, [1, 1, 1]),
                    ("colorInc", Wye.dType.FLOAT_LIST, [12, 12, 12]),
                    ("color", Wye.dType.FLOAT_LIST, [0, .33, .66, 1]),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),  # list of graphic elements to delete on Stop
                    )  # var 4

        codeDescr=(
            #(None, ("print('testObj3 case 0: start - set up object')")),
            ("Var=", "frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
                (None, "[frame]"),
                (None, "frame.vars.gObj"),
                (None, "['flyer_01.glb']"),
                (None, "frame.vars.position"),       # posVec
                (None, "[[0, 90, 0]]"),      # rotVec
                (None, "[[2,2,2]]"),    # scaleVec
                (None, "frame.vars.objTag"),
                (None, "frame.vars.color"),
                ("Var", "frame.vars.cleanUpObjs"),
             ),
            #("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            #(None, "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
            ("Label", "Repeat"),
            # set angle
            #("Code", "print('testObj3 run')"),
            ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngle")),
            # Step forward
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
            # set color
            ("Var=", "frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
            # todo Next two lines are horrible - if followed by then expression indented - they have to be together
            # todo Think of a better way to do if/else than block code or sequential single expressions (EWWW!!)
            ("Code", "if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
            ("Code", " frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
            ("Var=", "frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.vars.gObj"), ("Var", "frame.vars.color")),

            ("GoTo", "Repeat")
        )

        def build(rowRef):
            #print("Build testObj3")
            return WyeCore.Utils.buildCodeText("testObj3b", TestLib.testObj3b.codeDescr, TestLib.testObj3b, rowRef)

        def start(stack):
            #print("testObj3 object start")
            return Wye.codeFrame(TestLib.testObj3b, stack)

        def run(frame):
            #print("Run testObj3")
            TestLib.TestLib_rt.testObj3b_run_rt(frame)



    # circling fish
    class testObj3c:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, ""),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [-35,75,-2]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., -.05]),
                    ("dAngle", Wye.dType.FLOAT_LIST, [0., 0., -.65]),
                    ("colorWk", Wye.dType.FLOAT_LIST, [1, 1, 1]),
                    ("colorInc", Wye.dType.FLOAT_LIST, [10, Wye.UI.DIALOG_OFFSET, 10]),
                    ("color", Wye.dType.FLOAT_LIST, [0, .33, .66, 1]),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )

        codeDescr=(
            #(None, ("print('testObj3 case 0: start - set up object')")),
            ("Var=", "frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
                (None, "[frame]"),
                (None, "frame.vars.gObj"),
                (None, "['flyer_01.glb']"),
                (None, "frame.vars.position"),       # posVec
                (None, "[[0, 90, 0]]"),      # rotVec
                (None, "[[2,2,2]]"),    # scaleVec
                (None, "frame.vars.objTag"),
                (None, "frame.vars.color"),
                ("Var", "frame.vars.cleanUpObjs"),
            ),
            #("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            #(None, "frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
            ("Label", "Repeat"),
            # set angle
            #("Code", "print('testObj3 run')"),
            ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngle")),
            # Step forward
            ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
            # set color
            ("Var=", "frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
            # todo Next two lines are horrible - if followed by then expression indented - they have to be together
            # todo Think of a better way to do if/else than block code or sequential single expressions (EWWW!!)
            ("Code", "if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
            ("Code", " frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
            ("Var=", "frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.vars.gObj"), ("Var", "frame.vars.color")),

            ("GoTo", "Repeat")
        )

        def build(rowRef):
            #print("Build testObj3")
            return WyeCore.Utils.buildCodeText("testObj3c", TestLib.testObj3c.codeDescr, TestLib.testObj3c, rowRef)

        def start(stack):
            #print("testObj3 object start")
            return Wye.codeFrame(TestLib.testObj3c, stack)

        def run(frame):
            #print("Run testObj3")
            TestLib.TestLib_rt.testObj3c_run_rt(frame)


    # load model passed in at loc, scale passed in
    class testLoader:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE

        paramDescr = (("obj", Wye.dType.OBJECT, "Description"),
                      ("file", Wye.dType.STRING, "Description"),
                      ("posVec", Wye.dType.INTEGER_LIST, "Description"),
                      ("scaleVec", Wye.dType.INTEGER_LIST, "Description"),
                      ("tag", Wye.dType.STRING, "Description"),
                      ("colorVec", Wye.dType.FLOAT_LIST, "Description"))
        varDescr = ()
        codeDescr = (
            #(None, "print('test inline code')"),
            # call loadModel with testLoader params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", ("Var", "frame.params.obj"), ("Var", "frame.params.file")),
            ("WyeCore.libs.WyeLib.makePickable", ("Var", "frame.params.tag"), ("Var", "frame.params.obj")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", ("Var", "frame.params.obj"), ("Var", "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", ("Var", "frame.params.obj"), ("Var", "frame.params.posVec"), ("Var", "frame.params.scaleVec"))
        )
        code = None

        def build(rowRef):
            return WyeCore.Utils.buildCodeText("testLoader", TestLib.testLoader.codeDescr, TestLib.testLoader, rowRef)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader_run_rt(frame)


    # when clicked, use spin to wiggle object back and forth
    class clickWiggle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, "Description"),
                      ("tag", Wye.dType.STRING, "Description"),
                      ("axis", Wye.dType.INTEGER, "Description"))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),
                    ("sound", Wye.dType.OBJECT, None))

        codeDescr = (
            ("Code", "WyeCore.World.setEventCallback('click', frame.params.tag[0], frame)"),
            ("Label", "WaitForClick1"),
            ("Code", "Wye.midi.playNote(91, 50, 64, 1)"),
            ("Label", "WaitForClick1"),

        )

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
                    #frame.vars.sound[0] = Wye.audio3d.loadSfx("WyePew.wav")
                    #Wye.audio3d.attachSoundToObject(frame.vars.sound[0], frame.params.obj[0])
                    frame.PC += 1
                    #print("clickWiggle waiting for event 'click' on tag ", frame.params.tag[0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    #frame.vars.sound[0].play()
                    Wye.midi.playNote(91, 50, 64, 1)
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
        paramDescr = (("obj", Wye.dType.OBJECT, "Description"),
                      ("axis", Wye.dType.INTEGER, "Description"))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),)

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
                    ("fishTags", Wye.dType.STRING_LIST, None),
                    ("position", Wye.dType.FLOAT_LIST, [0,0,0]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., -0.02]),
                    ("angle", Wye.dType.FLOAT_LIST, [0., 90., 0.]),
                    ("followDist", Wye.dType.FLOAT, 2),
                    ("target", Wye.dType.OBJECT, None),             # leader fish Wye obj frame
                    ("tgtDist", Wye.dType.FLOAT, 0),
                    ("count", Wye.dType.INTEGER, 0),        # loop counter
                    ("nFish", Wye.dType.INTEGER, 3),        # total number of fish
                    ("objAhead", Wye.dType.OBJECT, None),   # object in front of this one in train
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )
        codeDescr=(
            #(None, ("print('fish case 0: set up object')")),
            # initialize arrays
            ("Var=", "frame.vars.fishes = []"),
            ("Var=", "frame.vars.fishTags = []"),
            ("Var=", "frame.vars.cleanUpObjs[0] = []"),

            ("Label", "MakeFish"),
            #(None, "print('makeFish loop start: count', frame.vars.count[0])"),
            ("Expr", "frame.vars.fishes.append([None])"),     # create entry for fish
            ("Expr", "frame.vars.fishTags.append([''])"),
            ("Var=", "objNm = 'flyer_01.glb'"),
            # load object
            ("WyeCore.libs.WyeLib.loadObject",
             ("Expr", "[frame]"),
             ("Expr", "frame.vars.fishes[frame.vars.count[0]]"),
             ("Var", "[objNm]"),
             ("Expr", "[[frame.vars.count[0]*4 + 4,0, -.5]]"),  # posVec
             ("Const", "[[0, 90, 0]]"),  # rotVec
             ("Const", "[[1,1,1]]"),  # scaleVec
             ("Expr", "frame.vars.fishTags[frame.vars.count[0]]"),
             ("Expr", "[[frame.vars.count[0] % 3,(frame.vars.count[0] + 1) % 3,(frame.vars.count[0] + 2) % 3,1]]"),  # color
             ("Var", "frame.vars.cleanUpObjs"),
             ),
            ("Var=", "frame.vars.count[0] += 1"),     # next fish
            ("IfGoTo", "frame.vars.count[0] < frame.vars.nFish[0]", "MakeFish"),      # if not done, loop for next fish

            # Find leader fish
            ("WyeCore.libs.WyeLib.setEqual", ("Var", "frame.vars.target"), ("Expr", "[WyeCore.World.findActiveObj('leaderFish')]")),
            ("Var=", "frame.vars.count[0] = 0"),
            ("Var=", "frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),  # first fish follows leader

            ("Label", "SwimLoop"),    # used to be loop moving fish.  Unrolled loop 'cause IfGoTo lost a frame to each fish so jerky movement
            # orient toward fish in front
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),  # orient toward fish in front
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),      # flip to face up
            ("Var=", "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            ("Var=", "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", ("Expr", "frame.vars.fishes[frame.vars.count[0]]"), ("Var", "frame.vars.dPos")),
            ("Var=", "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish
            ("Var=", "frame.vars.count[0] += 1"),     # next fish

            # orient toward fish in front
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
            ("Var=", "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            ("Var=", "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", ("Expr", "frame.vars.fishes[frame.vars.count[0]]"), ("Var", "frame.vars.dPos")),
            ("Var=", "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish
            ("Var=", "frame.vars.count[0] += 1"),  # next fish

            # orient toward fish in front
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
            ("Code", "frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
            ("Var=", "frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
            # move fwd
            ("Var=", "frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
            ("WyeCore.libs.WyeLib.setObjRelPos", ("Expr", "frame.vars.fishes[frame.vars.count[0]]"), ("Var", "frame.vars.dPos")),
            ("Var=", "frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),  # next fish follows this fish

            #("IfGoTo", "frame.vars.count[0] < frame.vars.nFish[0]", "SwimLoop"),  # if not done, loop for next fish
            ("Var=", "frame.vars.count[0] = 0"),
            ("Var=", "frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),  # first fish follows leader

            # Save new position
            ("WyeCore.libs.WyeLib.getObjPos", ("Var", "frame.vars.position"), ("Var", ("frame.vars.fishes[0]"))),
            ("GoTo", "SwimLoop")
        )

        def build(rowRef):
            #print("Build fish")
            return WyeCore.Utils.buildCodeText("fish", TestLib.fish.codeDescr, TestLib.fish, rowRef)

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
                    ("fishTag", Wye.dType.STRING, ""),
                    ("tgtPos", Wye.dType.FLOAT_LIST, [0, Wye.UI.DIALOG_OFFSET, 0]),
                    ("tgtDist", Wye.dType.FLOAT, 1.),
                    ("posStep", Wye.dType.FLOAT, .04),
                    ("dAngleX", Wye.dType.FLOAT, .5),
                    ("dAngleY", Wye.dType.FLOAT, .5),
                    ("dAngleZ", Wye.dType.FLOAT, .5),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, (0,0,0)),
                    ("prevState", Wye.dType.INTEGER, 0),
                    ("startQ", Wye.dType.OBJECT, None),
                    ("endQ", Wye.dType.OBJECT, None),
                    ("deltaT", Wye.dType.FLOAT, 0.005),
                    ("lerpT", Wye.dType.FLOAT, 0.),
                    ("horizLim", Wye.dType.FLOAT, 10.),
                    ("vertLim", Wye.dType.FLOAT, 3.),
                    ("tgtChgCt", Wye.dType.INTEGER, 60 * 10),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )

        codeDescr=(
            ("loaderStream", (
                ("Var=", "frame.vars.deltaV=[[0,0,0]]"),
                ("Var=", "frame.vars.cleanUpObjs[0] = []"),
                ("WyeCore.libs.WyeLib.loadObject",
                 (None, "[frame]"),
                 (None, "frame.vars.fish"),
                 (None, "['flyer_01.glb']"),
                 (None, "frame.vars.position"),  # posVec
                 (None, "[[0, 0, 0]]"),  # rotVec
                 (None, "[[1,1,1]]"),  # scaleVec
                 (None, "frame.vars.fishTag"),
                 (None, "[[1,0,0,1]]"),
                 ("Var", "frame.vars.cleanUpObjs"),
                 ),

                # convert tgtPos from list to LPoint3f
                ("Code", "from panda3d.core import LPoint3f"),
                ("Var=", "frame.vars.tgtPos[0] = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])"),
                ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.fish"), (None, "[[0,90,0]]")),

                ("Var=", "frame.vars.sound[0] = Wye.audio3d.loadSfx('WyeHop.wav')"),
                ("Code", "Wye.audio3d.attachSoundToObject(frame.vars.sound[0], frame.vars.fish[0])"),

                ("Label", "RunLoop"),
                # Test raw code block
                ("CodeBlock",'''
#quat = Quat()
#lookAt(quat, target - nodePath.getPos(), Vec3.up())
#nodePath.setQuat(quat)
  
fish = frame.vars.fish[0]
fishPos = fish.getPos()
tgtPos = frame.vars.tgtPos[0]
# stay in local area
dist = (frame.vars.fish[0].getPos() - tgtPos).length()

# if we're outside the space around the target area or we're above or below the swim lane, do turning
if fishPos[2] > (tgtPos[2] + frame.vars.vertLim[0]) or fishPos[2] < (tgtPos[2] - frame.vars.vertLim[0]) or dist > frame.vars.horizLim[0]:
    global render
    from panda3d.core import lookAt, Quat, LQuaternionf, LVector3f, Vec3

    alpha = frame.vars.deltaT[0]      # how much to rotate each step (0..1)    
            
    # if not turning (in turning state), calculate the turn toward the center
    if frame.vars.prevState[0] != 2:
        # save rotation start, calc rotation end and nlerp time delta
        
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
    
    # We'turning, lerp that nose around the curve we calc'd above
    if frame.vars.lerpT[0] < 1.0:
        fishQ = frame.vars.startQ[0]
        tgtQ = frame.vars.endQ[0]
        tt = frame.vars.lerpT[0]
        quat = WyeCore.Utils.nlerp(fishQ, tgtQ, tt)
        fish.setQuat(quat)
        frame.vars.lerpT[0] += alpha
        #fish.setP(fish, 90)
    # done turning
    else:
        # flag that we finished the turn
        frame.vars.prevState[0] = 0    

# within "nice" distance from center, just chug happily along   
else:
    #print("2<d<=10")
    fishHPR = fish.getHpr()     # get current direction         
    
    # flip turn direction every new pass through the middle area
    if frame.vars.prevState[0] != 1:
        from random import random            
        frame.vars.dAngleX[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleY[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleZ[0] *= (1 if random() >= .5 else -1)
        
    f0 = frame.vars.dAngleX[0]
    f1 = frame.vars.dAngleY[0]
    f2 = frame.vars.dAngleZ[0]
    
    moveAngle = (f0, f1/2, f2/5)
    #moveAngle = (eA, eA/10, eA/20)        
    fishHPR += moveAngle
    #print("leaderfish fishHPR", fishHPR)
    #print("leaderfish fishHPR", fishHPR, " tgtHPR", tgtHPR, " moveAngle", moveAngle," setHpr", fishHPR)
    fish.setHpr(fishHPR)        
    frame.vars.prevState[0] = 1
'''),
                # Step forward
                ("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.fish"), (None, "[[0,0,-frame.vars.posStep[0]]]")),
                # save new position
                ("WyeCore.libs.WyeLib.getObjPos", (None, "frame.vars.position"), (None, "frame.vars.fish")),
                # don't relocate target
                ("GoTo", "RunLoop"),

                # count down to next random relocation of target point to swim toward
                ("Code", "frame.vars.tgtChgCt[0] -= 1"),
                ("IfGoTo", "frame.vars.tgtChgCt[0] > 0", "RunLoop"),

                # move target around randomly in a reasonably constrained area
                ("Code", "from random import random"),
                ("Code", "from panda3d.core import LPoint3f"),
                ("Var=", "frame.vars.tgtPos[0] = LPoint3f((random()-.5)*5, (random()-.5)*5, 0)"),
                ("Var=", "frame.vars.tgtChgCt[0] = 600 + random() * 1200"),
                ("GoTo", "RunLoop")

            )),
            ("changeAngleStream", (
                ("Label", "top"),
                ("IfGoTo", "frame.vars.fishTag[0] == ''", "top"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars.fishTag")),
                ("Expr", "frame.vars.dAngleX[0] = frame.vars.dAngleX[0] * -1"),
                ("Code", "frame.vars.sound[0].play()"),
                #(None, "print('clicked leaderFish')"),

                ("GoTo", "top")
            ))
        )

        def build(rowRef):
            #print("Build leaderFish")
            return WyeCore.Utils.buildParallelText("TestLib", "leaderFish", TestLib.leaderFish.codeDescr, TestLib.leaderFish)

        def start(stack):
            #print("leaderFish object start")
            return TestLib.TestLib_rt.leaderFish_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            #print("Run leaderFish")
            frame.runParallel()


    # put up "ground" objects
    class ground:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, "objTag"),
                    ("sounds", Wye.dType.OBJECT_LIST, []),
                    ("currSnd", Wye.dType.INTEGER, 0),
                    ("position", Wye.dType.FLOAT_LIST, [-1,2,-1.2]),
                    ("weeds", Wye.dType.OBJECT_LIST, []),
                    ("weedColorInc", Wye.dType.FLOAT_LIST, []),
                    ("bubbles", Wye.dType.OBJECT_LIST, []),
                    ("bubbleCt", Wye.dType.INTEGER_LIST, []),
                    ("bubblePop", Wye.dType.INTEGER_LIST, []),
                    ("bubbleMin", Wye.dType.FLOAT, 180),
                    ("bubbleRand", Wye.dType.FLOAT, 180),
                    ("bubbleFloat", Wye.dType.FLOAT_LIST, [.001, .001, .075]),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None)
                    )

        codeDescr=(
            ("CodeBlock", '''
frame.vars.cleanUpObjs[0] = []
# ground
floorPos = [] #[[0]*20]*20      # 20x20 floor tile heights
from random import random
import math
floorX = 80
floorY = 80
for yy in range(floorX + 1):
    floorPos.append([])
    for xx in range(floorY + 1):
        #angle = max(abs(xx-10), abs(yy-10)) * .11
        #print("floor x", xx, " y", yy, " angle", angle, " ht", (1 - math.cos(angle)))
        #if abs(xx) > 75 and abs(yy) > 75:
        #    floorPos[yy].append(10+random()*20)
        #else:
        #    floorPos[yy].append(random()*5)  # + (1 - math.cos(angle)) * 50)
        floorPos[yy].append(random()*5)  # + (1 - math.cos(angle)) * 50)
        #print("floorPos", yy, ",", xx, "=", floorPos[yy][xx])
floor = Wye3dObjsLib._surf(floorPos, (10,10,1), (-(int(floorX * 10/2)),-(int(floorY*10/2)),-18))
frame.vars.cleanUpObjs[0].append(floor._path)
floor.setColor((.95,.84,.44,.1))

tag = "wyeTag" + str(WyeCore.Utils.getId())
floor.setTag(tag)
#print("Set tag", tag, " on", floor._path)
WyeCore.picker.makePickable(floor._path)
#print("test floor with tagDebug")
#WyeCore.picker.tagDebug(floor._path)
            

from random import random

# load audio manager and buffer up a bunch of pop sound slots so each bubble can play a full pop before the sound gets reused
for ii in range(100):
    frame.vars.sounds[0].append(Wye.audio3d.loadSfx("WyePop.wav"))
    
# Weeds and bubbles decorating the floor
for xx in range(int(floorX * floorY * .08)):
    if xx < 35:
        posX = (random()-.5)*20 - 25
        posY = (random()-.5)*20 + 75
    else:
        posX = (random()-.5)*floorX*10
        posY = (random()-.5)*floorY*10
    ixX = int(posX/floorX)
    ixY = int(posY/floorY)
    posZ = floorPos[ixY][ixX]
    #print("ixX", ixX, " ixY", ixY, " posX", posX, " posY", posY, " posZ", posZ)
    ht  = 2+3*random()
    color = (.25+random()*.75,.25+random()*.75,.25+random()*.75, .5)
    weed = Wye3dObjsLib._box([.1, .1, ht], [posX, posY, -18 + posZ+ht*.5])
    frame.vars.cleanUpObjs[0].append(weed)
    frame.vars.weedColorInc[0].append([random() * .05, random() * .05, random() * .05])
    weed.setColor(color)
    frame.vars.weeds[0].append(weed._path)
    weed.setTag(tag)
    WyeCore.picker.makePickable(weed._path)
    #print("Set tag", tag, " on weed", weed._path)
    
    # Create bubble, init color change amt and countdown to pop
    bubble = Wye3dObjsLib._ball(.2, [posX, posY, -18 + random() * 20])
    frame.vars.cleanUpObjs[0].append(bubble._path)
    bubble.setColor(color)
    bubble.setTag(tag)
    WyeCore.picker.makePickable(bubble._path)
    frame.vars.bubbles[0].append(bubble)
    pop = 60 + frame.vars.bubbleRand[0] * random()
    frame.vars.bubblePop[0].append(pop)
    frame.vars.bubbleCt[0].append(10+random()*(pop-10))

WyeCore.World.registerObjTag(tag, frame)
'''),
        ("Label", "Running"),
        ("CodeBlock", '''
# float bubbles up randomly 
from random import random


# set fall off
#Wye.audio3d.setDistanceFactor(.1)
Wye.audio3d.setDropOffFactor(5)

for ii in range(len(frame.vars.bubbles[0])):
    bubble = frame.vars.bubbles[0][ii]
    weed = frame.vars.weeds[0][ii]
    frame.vars.bubbleCt[0][ii] +=1
    if frame.vars.bubbleCt[0][ii] >= frame.vars.bubblePop[0][ii]:
        # reset bubble
        weed = frame.vars.weeds[0][ii]
        pos = weed.getPos()
        pos[2] += 2
        bubble.setPos(pos[0], pos[1], pos[2])
        frame.vars.bubbleCt[0][ii] = 0
        frame.vars.bubblePop[0][ii] = frame.vars.bubbleMin[0] + frame.vars.bubbleRand[0] * random()
        #weed.setColor(bubble.getColor())

    else:
        # float bubble up
        from panda3d.core import LVector3f
        bubble._path.setPos(bubble._path, LVector3f(frame.vars.bubbleFloat[0][0], frame.vars.bubbleFloat[0][1], frame.vars.bubbleFloat[0][2]))
        # trigger pop now so it sounds when bubble pops
        if frame.vars.bubblePop[0][ii]-9 > frame.vars.bubbleCt[0][ii] > frame.vars.bubblePop[0][ii]-10:
            # pop bubble
            viewerDist = (base.camera.getPos() - bubble.getPos()).length()
            if viewerDist < 100:
                #Wye.midi.playNote(118, 60, int(127-viewerDist), .1)
                Wye.audio3d.attachSoundToObject(frame.vars.sounds[0][frame.vars.currSnd[0]], bubble._path)
                frame.vars.sounds[0][frame.vars.currSnd[0]].play()
                frame.vars.currSnd[0] = (frame.vars.currSnd[0] + 1) % 100
            
        # do weed color
        color = weed.getColor()
        # cycle weed colors before resetting bubble
        if frame.vars.bubbleCt[0][ii] > frame.vars.bubblePop[0][ii]-30:
            for cc in range(3):
                color[cc] += frame.vars.weedColorInc[0][ii][cc]
                if color[cc] > 1:
                    color[cc] = 1
                    frame.vars.weedColorInc[0][ii][cc] *= -1
                if color[cc] < .25:
                    color[cc] = .25
                    frame.vars.weedColorInc[0][ii][cc] *= -1
            weed.setColor(color)
        # bubble reset, pick up weed color
        if frame.vars.bubbleCt[0][ii] < 2:
            bubble.setColor(color)
''')
        )

        def build(rowRef):
            #print("Build ground")
            return WyeCore.Utils.buildCodeText("ground", TestLib.ground.codeDescr, TestLib.ground, rowRef)

        def start(stack):
            #print("ground object start")
            return Wye.codeFrame(TestLib.ground, stack)

        def run(frame):
            #print("Run ground")
            TestLib.TestLib_rt.ground_run_rt(frame)




    # Put up "clickWiggle" fish
    class angleFish:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()  # gotta have a ret param
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, "objTag"),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [-3,2,2.5]),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )

        codeDescr=(
            #(None, ("print('angleFish 1 case', frame.PC)")),
            ("Var=", "frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
                (None, "[frame]"),
                (None, "frame.vars.gObj"),
                (None, "['flyer_01.glb']"),
                (None, "frame.vars.position"),       # posVec
                (None, "[[0, 90, 0]]"),      # rotVec
                (None, "[[1,1,1]]"),    # scaleVec
                (None, "frame.vars.objTag"),
                (None, "[[0,1,0,1]]"),
                ("Var", "frame.vars.cleanUpObjs"),
             ),
            #("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),

            #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "[0,5,-.5]")),
            (None, "frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
            ("Label", "Repeat"),
            #(None, ("print('angleFish 2 case', frame.PC)")),
            ("WyeCore.libs.TestLib.clickWiggle", (None, "frame.vars.gObj"), (None, "frame.vars.objTag"), (None, "[0]")),
            #(None, ("print('angleFish 3 case', frame.PC)")),
            ("WyeCore.libs.TestLib.clickWiggle", (None, "frame.vars.gObj"), (None, "frame.vars.objTag"), (None, "[1]")),
            #(None, ("print('angleFish 4 case', frame.PC)")),
            ("WyeCore.libs.TestLib.clickWiggle", (None, "frame.vars.gObj"), (None, "frame.vars.objTag"), (None, "[2]")),
            #(None, ("print('angleFish 5 case', frame.PC)")),
            ("GoTo", "Repeat"),
            #(None, ("print('angleFish end case', frame.PC)")),
        )

        def build(rowRef):
            #print("Build angleFish")
            return WyeCore.Utils.buildCodeText("angleFish", TestLib.angleFish.codeDescr, TestLib.angleFish, rowRef)

        def start(stack):
            #print("angleFish object start")
            return Wye.codeFrame(TestLib.angleFish, stack)

        def run(frame):
            #print("Run angleFish")
            TestLib.TestLib_rt.angleFish_run_rt(frame)




    # circling fish
    class testParallelFish:
        cType = Wye.cType.OBJECT
        mode = Wye.mode.PARALLEL
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        # varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("gObj", Wye.dType.OBJECT, None),
                    ("objTag", Wye.dType.STRING, ""),
                    ("sound", Wye.dType.OBJECT, None),
                    ("position", Wye.dType.FLOAT_LIST, [3 ,2,-1]),
                    ("dPos", Wye.dType.FLOAT_LIST, [0., 0., .03]),
                    ("posAngle", Wye.dType.FLOAT, 4.712388),
                    ("dAngleDeg", Wye.dType.FLOAT_LIST, [0., 0., .5]),
                    ("dAngleRad", Wye.dType.FLOAT, -0.0087266462),
                    ("cleanUpObjs", Wye.dType.OBJECT_LIST, None),           # list of graphic elements to delete on Stop
                    )

        codeDescr=(
            ("loaderStream", (
                #("Code", "print('testParallelFish run stream 0 loadObject')"),
                #(None, ("print('testParallelFish case 0: start - set up object')")),
                ("Var=", "frame.vars.cleanUpObjs[0] = []"),
                ("WyeCore.libs.WyeLib.loadObject",
                    (None, "[frame]"),
                    (None, "frame.vars.gObj"),
                    (None, "['fish1a.glb']"),
                    (None, "frame.vars.position"),       # posVec
                    (None, "[[0, 90, 0]]"),      # rotVec
                    (None, "[[.25,.25,.25]]"),    # scaleVec
                    (None, "frame.vars.objTag"),
                    (None, "[[.9,0.5,0,1]]"),
                    ("Var", "frame.vars.cleanUpObjs"),
                ),
                # ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.vars.gObj"), (None, "[-90,90,0]")),
                #("WyeCore.libs.WyeLib.setObjPos", (None, "frame.vars.gObj"),(None, "frame.vars.dPos")),
                #(None, "frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePop.wav')"),
                ("Label", "Done"),
            )),
            ("setAngleStream", (
                ("Label", "Repeat"),
                # set angle
                #("Code", "print('testParallelFish run stream 1 setRelAngle', frame.vars.gObj[0].getHpr())"),
                ("WyeCore.libs.WyeLib.setObjRelAngle", (None, "frame.vars.gObj"), (None, "frame.vars.dAngleDeg")),
                ("GoTo", "Repeat")
            )),
            ("setPositionStream", (
                ("Label", "Repeat"),
                # Step forward
                #("Code", "print('testParallelFish run stream 2 setRelPos', frame.vars.gObj[0].getPos())"),
                ("CodeBlock", '''
import math
angle = frame.vars.posAngle[0]
ctrPos = frame.vars.position[0]
x = ctrPos[0] + math.sin(angle)
y = ctrPos[1] + math.cos(angle)
frame.vars.gObj[0].setPos(x,y,ctrPos[2])
angle += frame.vars.dAngleRad[0]
#if angle < 0:
#    angle = math.pi * 2
#if angle > math.pi * 2:
#    angle = 0
angle = angle % (math.pi * 2)
frame.vars.posAngle[0] = angle
                '''),
                #("WyeCore.libs.WyeLib.setObjRelPos", (None, "frame.vars.gObj"), (None, "frame.vars.dPos")),
                ("GoTo", "Repeat")
            ))
        )

        def build(rowRef):
            #print("Build testParallelFish")
            return WyeCore.Utils.buildParallelText("TestLib", "testParallelFish", TestLib.testParallelFish.codeDescr, TestLib.testParallelFish)

        def start(stack):
            #print("testParallelFish object start")
            #return Wye.codeFrame(TestLib.testParallelFish, stack)
            return TestLib.TestLib_rt.testParallelFish_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            #print("Run testParallelFish")
            #TestLib.TestLib_rt.testParallelFish_run_rt(frame)
            frame.runParallel()





    class PlaceHolder:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = False
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("myVar", Wye.dType.INTEGER, 0),)
        codeDescr = (
            ("Code", "print('PlaceHolder running!')"),
            ("Label", "DoNothing"),
        )

        def build(rowRef):
            #print("Build PlaceHolder")
            return WyeCore.Utils.buildCodeText("PlaceHolder", TestLib.PlaceHolder.codeDescr, TestLib.PlaceHolder, rowRef)

        def start(stack):
            #print("PlaceHolder object start")
            return Wye.codeFrame(TestLib.PlaceHolder, stack)

        def run(frame):
            #print("Run PlaceHolder")
            TestLib.TestLib_rt.PlaceHolder_run_rt(frame)