from Wye import Wye
from WyeCore import WyeCore
class MyTestLib:
  def build():
    WyeCore.Utils.buildLib(MyTestLib)
  canSave = True  # all verbs can be saved with the library
  class MyTestLib_rt:
   pass #1

  class testParallelFish:
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
              (None,"['fish1a.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 90, 0]]"),
              (None,"[[.25,.25,.25]]"),
              (None,"frame.vars.objTag"),
              (None,"[[.9,0.5,0,1]]"),
              ("Var","frame.vars.cleanUpObjs")),
            ("Label","Done"))),
        ("setAngleStream",
          (
            ("Label","Repeat"),
            ("WyeCore.libs.WyeLib.setObjRelAngle",
              (None,"frame.vars.gObj"),
              (None,"frame.vars.dAngleDeg")),
            ("GoTo","Repeat"))),
        ("setPositionStream",
          (
            ("Label","Repeat"),
            ("CodeBlock",'''
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
            ("GoTo","Repeat"))))

    def build():
        # print("Build ",testParallelFish)
        return WyeCore.Utils.buildParallelText('MyTestLib','testParallelFish', MyTestLib.testParallelFish.codeDescr, MyTestLib.testParallelFish)

    def start(stack):
        return MyTestLib.MyTestLib_rt.testParallelFish_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish)
        try:
          frame.runParallel()
        except Exception as e:
          if not hasattr(frame, 'errOnce'):
            print('MyTestLib testParallelFish runParallel failed\n', str(e))
            import traceback
            traceback.print_exception(e)
            frame.errOnce = True

