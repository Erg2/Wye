from Wye import Wye
from WyeCore import WyeCore
class MyWyeLib:
  def _build():
    WyeCore.Utils.buildLib(MyWyeLib)
  canSave = True  # all verbs can be saved with the library
  class MyWyeLib_rt:
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
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,0,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#< your code goes here>"))),
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

    def _build(rowRef):
        # print("Build ",testParallelFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('MyWyeLib', 'testParallelFish', MyWyeLib.testParallelFish.codeDescr, MyWyeLib.testParallelFish)

    def start(stack):
        return MyWyeLib.MyWyeLib_rt.testParallelFish_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish)
        frame.runParallel()

  class testParallelFish1:
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
          (1.0,2.0,-1.0)),
        ("dPos","FL",
          (0.0,0.0,0.03)),
        ("posAngle","F",4.712388),
        ("dAngleDeg","FL",
          (0.0,0.0,0.5)),
        ("dAngleRad","F",-0.0087266462),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,0,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#< your code goes here>"))),
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

    def _build(rowRef):
        # print("Build ",testParallelFish1)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('MyWyeLib', 'testParallelFish1', MyWyeLib.testParallelFish1.codeDescr, MyWyeLib.testParallelFish1)

    def start(stack):
        return MyWyeLib.MyWyeLib_rt.testParallelFish1_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish1)
        frame.runParallel()

  class testParallelFish2:
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
          (0.0,2.0,-1.0)),
        ("dPos","FL",
          (0.0,0.0,0.03)),
        ("posAngle","F",4.712388),
        ("dAngleDeg","FL",
          (0.0,0.0,0.5)),
        ("dAngleRad","F",-0.0087266462),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (0,0,1,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#< your code goes here>"))),
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

    def _build(rowRef):
        # print("Build ",testParallelFish2)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('MyWyeLib', 'testParallelFish2', MyWyeLib.testParallelFish2.codeDescr, MyWyeLib.testParallelFish2)

    def start(stack):
        return MyWyeLib.MyWyeLib_rt.testParallelFish2_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish2)
        frame.runParallel()

  class testParallelFish3:
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
          (2.0,2.0,-1.0)),
        ("dPos","FL",
          (0.0,0.0,0.03)),
        ("posAngle","F",4.712388),
        ("dAngleDeg","FL",
          (0.0,0.0,0.5)),
        ("dAngleRad","F",-0.0087266462),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,1,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#< your code goes here>"))),
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

    def _build(rowRef):
        # print("Build ",testParallelFish3)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('MyWyeLib', 'testParallelFish3', MyWyeLib.testParallelFish3.codeDescr, MyWyeLib.testParallelFish3)

    def start(stack):
        return MyWyeLib.MyWyeLib_rt.testParallelFish3_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish3)
        frame.runParallel()
