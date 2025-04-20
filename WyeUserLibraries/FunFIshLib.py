from Wye import Wye
from WyeCore import WyeCore
class FunFishLib:
  def _build():
    WyeCore.Utils.buildLib(FunFishLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class FunFishLib_rt:
   pass #1

  class Jelly:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("tCount",Wye.dType.INTEGER,0),
        ("nSegs",Wye.dType.INTEGER,5),
        ("body",Wye.dType.OBJECT,None),
        ("tag", Wye.dType.STRING, ""),
        ("t1",Wye.dType.OBJECT_LIST,[]),
        ("t1Tags",Wye.dType.STRING_LIST,[]),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),
        ("noop", Wye.dType.INTEGER, 0),)
    codeDescr = (
        ("CreateJFishStream",
          (
            ("Code","frame.vars.body[0] = Wye3dObjsLib._ball(.5, [0,0,0]) #"),
            ("Code", "frame.vars.body[0].setScale((1,1,.25))"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.body[0]._path) #"),
            ("WyeCore.libs.WyeLib.makePickable",
             ("Expr", "frame.vars.tag"),
             ("Expr", "[frame.vars.body[0]._path]")),
            ("Code", "WyeCore.World.registerObjTag(frame.vars.tag[0], frame)"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t1[0].append([Wye3dObjsLib._ball(.2-(frame.vars.tCount[0] * .05), [.5,0,-.5 - (frame.vars.tCount[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t1[0][frame.vars.tCount[0]][0]._path) #"),
            ("Code","frame.vars.t1Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
             ("Expr","frame.vars.t1Tags[0][frame.vars.tCount[0]]"),
             ("Expr","[frame.vars.t1[0][frame.vars.tCount[0]][0]._path]")),
            ("Code", "WyeCore.World.registerObjTag(frame.vars.t1Tags[0][frame.vars.tCount[0]][0], frame)"),
            ("Var=","frame.vars.tCount[0] += 1 #"),
            ("IfGoTo","frame.vars.tCount[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("WyeLib.noop",),
            ("Label", "Done"),
          )
        ),
        ("DummyStream", (("Code", "frame.vars.noop[0] = 0"),
            ("Label", "Done")))
    )
    def _build(rowRef):
        # print("Build ",Jelly)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'Jelly', FunFishLib.Jelly.codeDescr, FunFishLib.Jelly)

    def start(stack):
        return FunFishLib.FunFishLib_rt.Jelly_start_rt(stack)

    def run(frame):
        # print('Run 'Jelly)
        frame.runParallel()

  class parallelWanderFish:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("objTag",Wye.dType.STRING,""),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(3, 2, -1)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.03)),
        ("posAngle",Wye.dType.FLOAT,4.712388),
        ("dAngleDeg",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.5)),
        ("dAngleRad",Wye.dType.FLOAT,-0.0087266462),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("loaderStream",
          (
            ("Var=","frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.gObj"),
              ("Const","['fish1a.glb']"),
              (None,"frame.vars.position"),
              ("Const","[[0, 90, 0]]"),
              ("Const","[[.25,.25,.25]]"),
              (None,"frame.vars.objTag"),
              ("Const","[[.9,0.5,5,1]]"),
              ("Var","frame.vars.cleanUpObjs")),
            ("Label","Done"))),
        ("setColorStream",
          (
            ("Code","from random import random"),)),
        ("setAngleStream",
          (
            ("Label","Repeat"),
            ("WyeCore.libs.WyeLib.setObjRelAngle",
              ("Var","frame.vars.gObj"),
              (None,"frame.vars.dAngleDeg")),
            ("Code","from random import random"),
            ("Code","frame.vars.dAngleDeg[0][2] += (random()-.5)*.25 if frame.vars.dAngleDeg[0][2] < 1 else (random()-.75)*.25"),
            ("Code","frame.vars.dAngleDeg[0][2] = frame.vars.dAngleDeg[0][2] if frame.vars.dAngleDeg[0][2] > 0 else 0 - frame.vars.dAngleDeg[0][2]"),
            ("GoTo","Repeat"))),
        ("setPositionStream",
          (
            ("Label","Repeat"),
            ("Code","frame.vars.gObj[0].setPos(frame.vars.gObj[0], frame.vars.dPos[0][0], frame.vars.dPos[0][1], frame.vars.dPos[0][2]) #"),
            ("GoTo","Repeat"))))

    def _build(rowRef):
        # print("Build ",parallelWanderFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'parallelWanderFish', FunFishLib.parallelWanderFish.codeDescr, FunFishLib.parallelWanderFish)

    def start(stack):
        return FunFishLib.FunFishLib_rt.parallelWanderFish_start_rt(stack)

    def run(frame):
        # print('Run 'parallelWanderFish)
        frame.runParallel()
