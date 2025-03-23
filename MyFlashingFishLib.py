from Wye import Wye
from WyeCore import WyeCore
class MyFlashingFishLib:
  def build():
    WyeCore.Utils.buildLib(MyFlashingFishLib)
  canSave = True  # all verbs can be saved with the library
  class MyFlashingFishLib_rt:
   pass #1

  class FlashingTestFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (0.0,15.0,-4.0)),
        ("dPos","FL",
          (0.0,0.0,-0.1)),
        ("dAngle","FL",
          (0.0,0.0,0.0)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (1,2,10)),
        ("color","FL",
          (0.75,0.75,0.75,1.0)),
        ("skew","F",0),
        ("delta","F",0),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          ("Code","['fish1a.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          ("Code","[[1,1,1]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
        ("Label","Repeat"),
        ("Code","from random import random"),
        ("Code","frame.vars.skew[0] = .25 if abs(frame.vars.dAngle[0][2]) > .8 else .5"),
        ("Code","frame.vars.skew[0] = 1-frame.vars.skew[0] if frame.vars.dAngle[0][2] > .0 else frame.vars.skew[0]"),
        ("Code","frame.vars.delta[0] = (random()-frame.vars.skew[0])/10"),
        ("Code","frame.vars.dAngle[0][2] += frame.vars.delta[0]"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("Code","frame.vars.dPos[0][2] += (random()-.5)/100"),
        ("Code","frame.vars.dPos[0][2] = max(min(frame.vars.dPos[0][2], .3), .05)"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("WyeCore.libs.WyeLib.getObjPos",
          (None,"frame.vars.position"),
          (None,"frame.vars.gObj")),
        ("Var=","frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Var=","frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
        ("Code","if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
        ("Code"," frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
        ("Code","if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Code","if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
        ("Code"," frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def build(rowRef):
        # print("Build ",FlashingTestFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('FlashingTestFish', MyFlashingFishLib.FlashingTestFish.codeDescr, MyFlashingFishLib.FlashingTestFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(MyFlashingFishLib.FlashingTestFish, stack)

    def run(frame):
        # print('Run 'FlashingTestFish)
        MyFlashingFishLib.MyFlashingFishLib_rt.FlashingTestFish_run_rt(frame)

  class FlyerTestFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (-4.0,15.0,4.0)),
        ("dPos","FL",
          (0.0,0.0,-0.1)),
        ("dAngle","FL",
          (0.0,0.0,0.0)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (1,5,10)),
        ("color","FL",
          (0.5,0.5,0.5,1)),
        ("skew","F",0),
        ("delta","F",0),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          ("Code","['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          ("Code","[[1,1,1]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
        ("Label","Repeat"),
        ("Code","from random import random"),
        ("Code","frame.vars.skew[0] = .25 if abs(frame.vars.dAngle[0][2]) > .8 else .5"),
        ("Code","frame.vars.skew[0] = 1-frame.vars.skew[0] if frame.vars.dAngle[0][2] > .0 else frame.vars.skew[0]"),
        ("Code","frame.vars.delta[0] = (random()-frame.vars.skew[0])/10"),
        ("Code","frame.vars.dAngle[0][2] += frame.vars.delta[0]"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("Code","frame.vars.dPos[0][2] += (random()-.5)/100"),
        ("Code","frame.vars.dPos[0][2] = max(min(frame.vars.dPos[0][2], .3), .05)"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("WyeCore.libs.WyeLib.getObjPos",
          (None,"frame.vars.position"),
          (None,"frame.vars.gObj")),
        ("Var=","frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Var=","frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
        ("Code","if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
        ("Code"," frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
        ("Code","if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Code","if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
        ("Code"," frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def build(rowRef):
        # print("Build ",FlyerTestFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('FlyerTestFish', MyFlashingFishLib.FlyerTestFish.codeDescr, MyFlashingFishLib.FlyerTestFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(MyFlashingFishLib.FlyerTestFish, stack)

    def run(frame):
        # print('Run 'FlyerTestFish)
        MyFlashingFishLib.MyFlashingFishLib_rt.FlyerTestFish_run_rt(frame)

  class SmallFlashingFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (4.0,15.0,2.0)),
        ("dPos","FL",
          (0.0,0.0,-0.1)),
        ("dAngle","FL",
          (0.0,0.0,0.0)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (2,5,15)),
        ("color","FL",
          (0.5,0.5,0.5,1)),
        ("skew","F",0),
        ("delta","F",0),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          ("Code","['fish.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          ("Code","[[.5,.5,.5]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
        ("Label","Repeat"),
        ("Code","from random import random"),
        ("Code","frame.vars.skew[0] = .25 if abs(frame.vars.dAngle[0][2]) > .8 else .5"),
        ("Code","frame.vars.skew[0] = 1-frame.vars.skew[0] if frame.vars.dAngle[0][2] > .0 else frame.vars.skew[0]"),
        ("Code","frame.vars.delta[0] = (random()-frame.vars.skew[0])/10"),
        ("Code","frame.vars.dAngle[0][2] += frame.vars.delta[0]"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("Code","frame.vars.dPos[0][2] += (random()-.5)/100"),
        ("Code","frame.vars.dPos[0][2] = max(min(frame.vars.dPos[0][2], .3), .05)"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("WyeCore.libs.WyeLib.getObjPos",
          (None,"frame.vars.position"),
          (None,"frame.vars.gObj")),
        ("Var=","frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Var=","frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
        ("Code","if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
        ("Code"," frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
        ("Code","if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Code","if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
        ("Code"," frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def build(rowRef):
        # print("Build ",SmallFlashingFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('SmallFlashingFish', MyFlashingFishLib.SmallFlashingFish.codeDescr, MyFlashingFishLib.SmallFlashingFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(MyFlashingFishLib.SmallFlashingFish, stack)

    def run(frame):
        # print('Run 'SmallFlashingFish)
        MyFlashingFishLib.MyFlashingFishLib_rt.SmallFlashingFish_run_rt(frame)
