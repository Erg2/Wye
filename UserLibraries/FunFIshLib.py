from Wye import Wye
from WyeCore import WyeCore
class FunFIshLib:
  def _build():
    WyeCore.Utils.buildLib(FunFIshLib)
  canSave = True  # all verbs can be saved with the library
  class FunFIshLib_rt:
   pass #1

  class Jelly:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("newVar","A",None),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeLib.noop",
          ("Code","0")))

    def _build(rowRef):
        # print("Build ",Jelly)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Jelly', FunFIshLib.Jelly.codeDescr, FunFIshLib.Jelly, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FunFIshLib.Jelly, stack)

    def run(frame):
        # print('Run 'Jelly)
        FunFIshLib.FunFIshLib_rt.Jelly_run_rt(frame)

  class parallelWanderFish:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S",""),
        ("sound","O",None),
        ("position","FL",
          (3,2,-1)),
        ("dPos","FL",
          (0.0,0.0,0.03)),
        ("posAngle","F",4.712388),
        ("dAngleDeg","FL",
          (0.0,0.0,0.5)),
        ("dAngleRad","F",-0.0087266462),
        ("cleanUpObjs","OL",None))
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
        return WyeCore.Utils.buildParallelText('FunFIshLib', 'parallelWanderFish', FunFIshLib.parallelWanderFish.codeDescr, FunFIshLib.parallelWanderFish)

    def start(stack):
        return FunFIshLib.FunFIshLib_rt.parallelWanderFish_start_rt(stack)

    def run(frame):
        # print('Run 'parallelWanderFish)
        frame.runParallel()
