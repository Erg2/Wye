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
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("nSegs",Wye.dType.INTEGER,5),
        ("body",Wye.dType.OBJECT,None),
        ("tag",Wye.dType.STRING,""),
        ("t1Count",Wye.dType.INTEGER,0),
        ("t2Count",Wye.dType.INTEGER,0),
        ("t3Count",Wye.dType.INTEGER,0),
        ("t4Count",Wye.dType.INTEGER,0),
        ("t5Count",Wye.dType.INTEGER,0),
        ("t6Count",Wye.dType.INTEGER,0),
        ("t1",Wye.dType.OBJECT_LIST,[]),
        ("t1Tags",Wye.dType.STRING_LIST,[]),
        ("t2",Wye.dType.OBJECT_LIST,[]),
        ("t2Tags",Wye.dType.STRING_LIST,[]),
        ("t3",Wye.dType.OBJECT_LIST,[]),
        ("t3Tags",Wye.dType.STRING_LIST,[]),
        ("t4",Wye.dType.OBJECT_LIST,[]),
        ("t4Tags",Wye.dType.STRING_LIST,[]),
        ("t5",Wye.dType.OBJECT_LIST,[]),
        ("t5Tags",Wye.dType.STRING_LIST,[]),
        ("t6",Wye.dType.OBJECT_LIST,[]),
        ("t6Tags",Wye.dType.STRING_LIST,[]),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),
        ("angle",Wye.dType.FLOAT,0.0),
        ("dAngle",Wye.dType.FLOAT,0.005),
        ("noop",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("CreateJBodStream",
          (
            ("Code","frame.vars.body[0] = Wye3dObjsLib._ball(1, [0,0,0]) #"),
            ("Code","frame.vars.body[0].setScale((1,1,.25))"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.body[0]._path) #"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.tag"),
              ("Expr","[frame.vars.body[0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.tag[0], frame)"),
            ("Label","Done"))),
        ("CreateT1Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t1Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t1[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t1Count[0] * .05), [1,0,-.5 - (frame.vars.t1Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t1[0][frame.vars.t1Count[0]][0]._path) #"),
            ("Code","frame.vars.t1Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t1Tags[0][frame.vars.t1Count[0]]"),
              ("Expr","[frame.vars.t1[0][frame.vars.t1Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t1Tags[0][frame.vars.t1Count[0]][0], frame)"),
            ("Var=","frame.vars.t1Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t1Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Done"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t1[0][ii][0]"),
            ("Code","  obj.setPos(1 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, 0, -.5 - (ii*.5))"),
            )),
        ("CreateT2Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t2Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t2[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t2Count[0] * .05), [.5,.866,-.5 - (frame.vars.t2Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t2[0][frame.vars.t2Count[0]][0]._path) #"),
            ("Code","frame.vars.t2Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t2Tags[0][frame.vars.t2Count[0]]"),
              ("Expr","[frame.vars.t2[0][frame.vars.t2Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t2Tags[0][frame.vars.t2Count[0]][0], frame)"),
            ("Var=","frame.vars.t2Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t2Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Done"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t2[0][ii][0]"),
            ("Code","  obj.setPos(.5 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, .866, -.5 - (ii*.5))"),)),
        ("CreateT3Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t3Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t3[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t3Count[0] * .05), [-.5,.866,-.5 - (frame.vars.t3Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t3[0][frame.vars.t3Count[0]][0]._path) #"),
            ("Code","frame.vars.t3Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t3Tags[0][frame.vars.t3Count[0]]"),
              ("Expr","[frame.vars.t3[0][frame.vars.t3Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t3Tags[0][frame.vars.t3Count[0]][0], frame)"),
            ("Var=","frame.vars.t3Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t3Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Done"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t3[0][ii][0]"),
            ("Code","  obj.setPos(-.5 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, .866, -.5 - (ii*.5))"),)),
        ("CreateT4Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t4Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t4[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t4Count[0] * .05), [-1,0,-.5 - (frame.vars.t4Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t4[0][frame.vars.t4Count[0]][0]._path) #"),
            ("Code","frame.vars.t4Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t4Tags[0][frame.vars.t4Count[0]]"),
              ("Expr","[frame.vars.t4[0][frame.vars.t4Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t4Tags[0][frame.vars.t4Count[0]][0], frame)"),
            ("Var=","frame.vars.t4Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t4Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Done"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t4[0][ii][0]"),
            ("Code","  obj.setPos(-1 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, 0, -.5 - (ii*.5))"),)),
        ("CreateT5Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t5Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t5[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t5Count[0] * .05), [-.5,-.866,-.5 - (frame.vars.t5Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t5[0][frame.vars.t5Count[0]][0]._path) #"),
            ("Code","frame.vars.t5Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t5Tags[0][frame.vars.t5Count[0]]"),
              ("Expr","[frame.vars.t5[0][frame.vars.t5Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t5Tags[0][frame.vars.t5Count[0]][0], frame)"),
            ("Var=","frame.vars.t5Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t5Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Done"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t5[0][ii][0]"),
            ("Code","  obj.setPos(-.5 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, -.8660, -.5 - (ii*.5))"),)),
        ("CreateT6Stream",
          (
            ("Label","BldTentacles"),
            ("Var=","frame.vars.t6Count[0] = 0"),
            ("Label","buildTentacle"),
            ("Code","frame.vars.t6[0].append([Wye3dObjsLib._ball(.2-(frame.vars.t6Count[0] * .05), [.5,-.866,-.5 - (frame.vars.t6Count[0] *.5)])]) #"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.t6[0][frame.vars.t6Count[0]][0]._path) #"),
            ("Code","frame.vars.t6Tags[0].append(['']) # make row for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.t6Tags[0][frame.vars.t6Count[0]]"),
              ("Expr","[frame.vars.t6[0][frame.vars.t6Count[0]][0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.t6Tags[0][frame.vars.t6Count[0]][0], frame)"),
            ("Var=","frame.vars.t6Count[0] += 1 #"),
            ("IfGoTo","frame.vars.t6Count[0] < frame.vars.nSegs[0]","buildTentacle"),
            ("Label","Wave"),
            ("Code","from panda3d.core import LVecBase3f"),
            ("Code","import math"),
            ("Var=","frame.vars.angle[0] += frame.vars.dAngle[0]"),
            ("Code","for ii in range(frame.vars.nSegs[0]):"),
            ("Code","  obj = frame.vars.t6[0][ii][0]"),
            ("Code","  obj.setPos(.51 + math.sin(frame.vars.angle[0]+ii*.25) * (ii+1)*.05, -.866, -.5 - (ii*.5))"),)),
        ("Move",
          (
            ("Code","frame.vars.noop[0] = 0"),
            ("Label","Done"))))

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
