from Wye import Wye
from WyeCore import WyeCore
class FunFIshLib:
  def _build():
    WyeCore.Utils.buildLib(FunFIshLib)
  canSave = True  # all verbs can be saved with the library
  class FunFIshLib_rt:
   pass #1

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
              ("Const","[[.1,0.5,5,1]]"),
              ("Var","frame.vars.cleanUpObjs")),
            ("Label","Done"))),
        ("setAngleStream",
          (
            ("Label","Repeat"),
            ("WyeCore.libs.WyeLib.setObjRelAngle",
              ("Var","frame.vars.gObj"),
              (None,"frame.vars.dAngleDeg")),
            ("Code","from random import random #< your code goes here>"),
            ("Var=","frame.vars.dAngleDeg[0] += (random()-.5)*.25 if frame.vars.dAngleDeg[0] < 1 else (random()-.75)*.25 #< your code goes here>"),
            ("Var=","frame.vars.dAngleDeg[0] = frame.vars.dAngleDeg[0] if frame.vars.dAngleDeg[0] > 0 else 0 - frame.vars.dAngleDeg[0] #"),
            ("GoTo","Repeat"))),
        ("setPositionStream",
          (
            ("Label","Repeat"),
            ("Code","import math #"),
            ("Code","angle = frame.vars.posAngle[0] #"),
            ("Code","ctrPos = frame.vars.position[0] #"),
            ("Code","x = ctrPos[0] + math.sin(angle)#"),
            ("Code","y = ctrPos[1] + math.cos(angle)#"),
            ("Code","frame.vars.gObj[0].setPos(x,y,ctrPos[2]) #"),
            ("Code","angle += frame.vars.dAngleRad[0] #"),
            ("Code","angle=angle%(math.pi*2) #"),
            ("Code","frame.vars.posAngle[0]=angle #"),
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
