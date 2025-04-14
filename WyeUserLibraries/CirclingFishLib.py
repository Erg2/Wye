from Wye import Wye
from WyeCore import WyeCore
class CirclingFishLib:
  def _build():
    WyeCore.Utils.buildLib(CirclingFishLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class CirclingFishLib_rt:
   pass #1

  class testParallelFish:
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
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,0,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#<your code here>"))),
        ("loaderStream",
          (
            #("Var=","frame.vars.cleanUpObjs[0] = []"),
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
        return WyeCore.Utils.buildParallelText('CirclingFishLib', 'testParallelFish', CirclingFishLib.testParallelFish.codeDescr, CirclingFishLib.testParallelFish)

    def start(stack):
        return CirclingFishLib.CirclingFishLib_rt.testParallelFish_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish)
        frame.runParallel()

  class testParallelFish1:
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
        ("position",Wye.dType.FLOAT_LIST,(1.0, 2.0, -1.0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.03)),
        ("posAngle",Wye.dType.FLOAT,4.712388),
        ("dAngleDeg",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.5)),
        ("dAngleRad",Wye.dType.FLOAT,-0.0087266462),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,0,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#<your code here>"))),
        ("loaderStream",
          (
            #("Var=","frame.vars.cleanUpObjs[0] = []"),
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
        return WyeCore.Utils.buildParallelText('CirclingFishLib', 'testParallelFish1', CirclingFishLib.testParallelFish1.codeDescr, CirclingFishLib.testParallelFish1)

    def start(stack):
        return CirclingFishLib.CirclingFishLib_rt.testParallelFish1_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish1)
        frame.runParallel()

  class testParallelFish2:
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
        ("position",Wye.dType.FLOAT_LIST,(0.0, 2.0, -1.0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.03)),
        ("posAngle",Wye.dType.FLOAT,4.712388),
        ("dAngleDeg",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.5)),
        ("dAngleRad",Wye.dType.FLOAT,-0.0087266462),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (0,0,1,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#<your code here>"))),
        ("loaderStream",
          (
            #("Var=","frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.gObj"),
              (None,"['fish1a.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 90, 0]]"),
              (None,"[[.25,.25,.25]]"),
              (None,"frame.vars.objTag"),
              ("Code","[[.1,0.9,0,1]]"),
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
        return WyeCore.Utils.buildParallelText('CirclingFishLib', 'testParallelFish2', CirclingFishLib.testParallelFish2.codeDescr, CirclingFishLib.testParallelFish2)

    def start(stack):
        return CirclingFishLib.CirclingFishLib_rt.testParallelFish2_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish2)
        frame.runParallel()

  class testParallelFish3:
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
        ("position",Wye.dType.FLOAT_LIST,(2.0, 2.0, -1.0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.03)),
        ("posAngle",Wye.dType.FLOAT,4.712388),
        ("dAngleDeg",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.5)),
        ("dAngleRad",Wye.dType.FLOAT,-0.0087266462),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None))
    codeDescr =        (
        ("NewStream",
          (
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","#print('case', frame.PC, ' gObj', frame.vars.gObj[0])"),
            ("Label","DelayOneFrame"),
            ("Code","WyeCore.libs.WyeLib.setObjMaterialColor.setColor(frame.vars.gObj[0], (1,0,1,1))"),
            ("Label","DelayOneFrame"),
            ("Code","#<your code here>"))),
        ("loaderStream",
          (
            #("Var=","frame.vars.cleanUpObjs[0] = []"),
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
        return WyeCore.Utils.buildParallelText('CirclingFishLib', 'testParallelFish3', CirclingFishLib.testParallelFish3.codeDescr, CirclingFishLib.testParallelFish3)

    def start(stack):
        return CirclingFishLib.CirclingFishLib_rt.testParallelFish3_start_rt(stack)

    def run(frame):
        # print('Run 'testParallelFish3)
        frame.runParallel()
