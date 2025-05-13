from Wye import Wye
from WyeCore import WyeCore
class FunFishLib:
  def _build():
    WyeCore.Utils.buildLib(FunFishLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class FunFishLib_rt:
   pass #1

  class JellyFish:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("nSegs",Wye.dType.INTEGER,5),
        ("body",Wye.dType.OBJECT,None),
        ("tag",Wye.dType.STRING,""),
        ("tCt",Wye.dType.INTEGER,0),
        ("tSegCt",Wye.dType.INTEGER,0),
        ("segLen",Wye.dType.INTEGER,5),
        ("t",Wye.dType.OBJECT_LIST,[]),
        ("tTags",Wye.dType.STRING_LIST,[]),
        ("tgCt",Wye.dType.INTEGER,0),
        ("segSep",Wye.dType.FLOAT,0.5),
        ("segOffs",Wye.dType.FLOAT_LIST,[]),
        ("tAngle",Wye.dType.FLOAT,0.0),
        ("tOff",Wye.dType.FLOAT_LIST,[]),
        ("segAngle",Wye.dType.FLOAT,0.0),
        ("dAngle",Wye.dType.FLOAT,0.001),
        ("size",Wye.dType.FLOAT,1.0),
        ("shrinkSize",Wye.dType.FLOAT,1.0),
        ("note",Wye.dType.INTEGER,48),
        ("color",Wye.dType.FLOAT_LIST,[0.5, 0.3, 0.3, 1.0]),
        ("colorInc",Wye.dType.FLOAT_LIST,[0.001, 0.005, 0.01]),
        ("tColorInc",Wye.dType.FLOAT_LIST,[0.1, 0.05, 0.03]),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("CreateJBodStream",
          (
            ("Code","#hang everything off central point"),
            ("Code","from panda3d.core import NodePath"),
            ("Code","frame.vars.gObj[0] = NodePath('JFish')"),
            ("Code","frame.vars.gObj[0].reparentTo(render)"),
            ("Code","from random import random"),
            ("Code","f = random() + .25"),
            ("Code","frame.vars.size[0] = f"),
            ("Code","frame.vars.gObj[0].setPos(((random()-.5)*20, (random()+.5) * 20, random()))"),
            ("Code","frame.vars.gObj[0].setScale((f,f,f))"),
            ("Code","frame.vars.note[0] = int((1.25-f)*10) + 45"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.gObj[0]) #"),
            ("Code","frame.vars.body[0] = Wye3dObjsLib._ball(1.1, [0,0,0]) #"),
            ("Code","frame.vars.body[0]._path.reparentTo(frame.vars.gObj[0])"),
            ("Code","frame.vars.body[0].setScale((1,1,.25))"),
            ("Code","frame.vars.body[0].setColor((frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2], 1))"),
            ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.body[0]._path) #"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.tag"),
              ("Expr","[frame.vars.body[0]._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.tag[0], frame)"),
            ("Label","Done"),
            ("Label","BldTentacles"),
            ("Var=","frame.vars.tSegCt[0] = 0"),
            ("Code","# one t list per tentacle"),
            ("Code","frame.vars.t[0].append([])"),
            ("Code","# base pos for this tentacle"),
            ("Code","import math"),
            ("Code","x = math.sin(frame.vars.tAngle[0])"),
            ("Code","y = math.cos(frame.vars.tAngle[0])"),
            ("Code","frame.vars.tOff[0].append([x,y])"),
            ("Label","BldTentacle"),
            ("Code","obj = Wye3dObjsLib._ball(.2-(frame.vars.tSegCt[0] * .05), [frame.vars.tOff[0][frame.vars.tCt[0]][0], frame.vars.tOff[0][frame.vars.tCt[0]][1],-.25 - (frame.vars.tSegCt[0] *frame.vars.segSep[0])])"),
            ("Code","obj._path.reparentTo(frame.vars.gObj[0])"),
            ("Code","frame.vars.t[0][frame.vars.tCt[0]].append([obj])"),
            ("Code","frame.vars.cleanUpObjs[0].append(obj._path)"),
            ("Code","obj.setColor((frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2], 1))"),
            ("Code","frame.vars.tTags[0].append(['']) # make array elem for tag"),
            ("Code","obj.setTag(frame.vars.tag[0])"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.tTags[0][frame.vars.tgCt[0]]"),
              ("Expr","[obj._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.tTags[0][frame.vars.tgCt[0]][0], frame)"),
            ("Var=","frame.vars.tSegCt[0] += 1 #Next segment of this tentacle"),
            ("Code","#loop to build next tentacle seg"),
            ("IfGoTo","frame.vars.tSegCt[0] < 6","BldTentacle"),
            ("Code","import math"),
            ("Var=","frame.vars.tAngle[0] += math.pi/3."),
            ("Var=","frame.vars.tCt[0] += 1 # Next tentacle"),
            ("Code","#Loop to build next tentacle"),
            ("IfGoTo","frame.vars.tCt[0] < 6","BldTentacles"),
            ("Label","Drift"),
            ("Code","import math"),
            ("Code","import math"),
            ("Code","frame.vars.body[0].setColor((frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2], 1))"),
            ("Code","frame.vars.colorInc[0][0] *= 1 if 0 < frame.vars.color[0][0] + frame.vars.colorInc[0][0] < 1 else -1"),
            ("Code","frame.vars.colorInc[0][1] *= 1 if 0< frame.vars.color[0][1] + frame.vars.colorInc[0][1] < 1 else -1"),
            ("Code","frame.vars.colorInc[0][2] *= 1 if 0 < frame.vars.color[0][2] + frame.vars.colorInc[0][2] < 1 else -1"),
            ("Code","frame.vars.color[0][0] += frame.vars.colorInc[0][0]"),
            ("Code","frame.vars.color[0][1] += frame.vars.colorInc[0][1]"),
            ("Code","frame.vars.color[0][2] += frame.vars.colorInc[0][2]"),
            ("Code","#print('start jFish cycle, color', frame.vars.color[0])"),
            ("Code","frame.vars.tAngle[0] = 0."),
            ("Code","frame.vars.segOffs[0] = []"),
            ("Code","for sIx in range(frame.vars.nSegs[0]):"),
            ("Code"," frame.vars.segOffs[0].append(math.sin(frame.vars.segAngle[0]+sIx*.25) * (sIx+1)*.05)"),
            ("Code","for tIx in range(6):"),
            ("Code"," x = frame.vars.tOff[0][tIx][0]"),
            ("Code"," y = frame.vars.tOff[0][tIx][1]"),
            ("Code"," color = [frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2]]"),
            ("Code"," #print('start tentacle, color', color)"),
            ("Code"," frame.vars.tColorInc[0] = [abs(frame.vars.tColorInc[0][0]), abs(frame.vars.tColorInc[0][1]), abs(frame.vars.tColorInc[0][2])]"),
            ("Code"," for sIx in range(frame.vars.nSegs[0]):"),
            ("Code","  frame.vars.segAngle[0] = frame.vars.segAngle[0] + frame.vars.dAngle[0] if frame.vars.segAngle[0] < 360 else 0"),
            ("Code","  obj = frame.vars.t[0][tIx][sIx][0]"),
            ("Code","  obj.setPos(x + frame.vars.segOffs[0][sIx], y, -.25 - (sIx*frame.vars.segSep[0]))"),
            ("Code","  #print('color', color)"),
            ("Code","  obj.setColor((color[0], color[1], color[2], 1))"),
            ("Code","  frame.vars.tColorInc[0][0] *= 1 if 0 < (color[0] + frame.vars.tColorInc[0][0]) < 1 else -1"),
            ("Code","  frame.vars.tColorInc[0][1] *= 1 if 0 < (color[1] + frame.vars.tColorInc[0][1]) < 1 else -1"),
            ("Code","  frame.vars.tColorInc[0][2] *= 1 if 0 < (color[2] + frame.vars.tColorInc[0][2]) < 1 else -1"),
            ("Code","  color[0] += frame.vars.tColorInc[0][0]"),
            ("Code","  color[1] += frame.vars.tColorInc[0][1]"),
            ("Code","  color[2] += frame.vars.tColorInc[0][2]"),
            ("Code","pos = frame.vars.gObj[0].getPos()"),
            ("Code","pos[0]+=.001"),
            ("Code","if pos[0] > 400:"),
            ("Code"," pos[0] -= 800"),
            ("Code","frame.vars.gObj[0].setPos(pos)"))),
        ("NewStream",
          (
            ("Label","Loop"),
            ("WyeCore.libs.WyeLib.waitClick",
              ("Expr","frame.vars.tag")),
            ("Code","frame.vars.color[0] = [1,.25,.25,1]"),
            ("Code","Wye.midi.playNote(98, frame.vars.note[0], 64, .5)"),
            ("Code","frame.vars.shrinkSize[0] = frame.vars.size[0]"),
            ("Label","Shrink"),
            ("Code","frame.vars.segSep[0] -= .1"),
            ("Code","frame.vars.shrinkSize[0] -= .02"),
            ("Code","frame.vars.gObj[0].setScale(frame.vars.shrinkSize[0], frame.vars.shrinkSize[0], frame.vars.size[0])"),
            ("IfGoTo","frame.vars.segSep[0] > .2","Shrink"),
            ("WyeCore.libs.WyeLib.delay",
              ("Expr","[60] # wait this many cycles")),
            ("Label","Restore"),
            ("Code","frame.vars.shrinkSize[0] += .002"),
            ("Code","frame.vars.gObj[0].setScale(frame.vars.shrinkSize[0], frame.vars.shrinkSize[0], frame.vars.size[0])"),
            ("Code","frame.vars.segSep[0] += .01"),
            ("IfGoTo","frame.vars.segSep[0] < .5","Restore"),
            ("Code","frame.vars.gObj[0].setScale(frame.vars.size[0], frame.vars.size[0], frame.vars.size[0])"),
            ("GoTo","Loop"))))

    def _build(rowRef):
        # print("Build ",JellyFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'JellyFish', FunFishLib.JellyFish.codeDescr, FunFishLib.JellyFish)

    def start(stack):
        return FunFishLib.FunFishLib_rt.JellyFish_start_rt(stack)

    def run(frame):
        # print('Run 'JellyFish)
        frame.runParallel()

  class flashingFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("objTag",Wye.dType.STRING,"objTag"),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(0.0, 15.0, -4.0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.1)),
        ("dAngle",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.0)),
        ("colorWk",Wye.dType.FLOAT_LIST,(1, 1, 1)),
        ("colorInc",Wye.dType.FLOAT_LIST,(1, 2, 10)),
        ("color",Wye.dType.FLOAT_LIST,(0.75, 0.75, 0.75, 1.0)),
        ("skew",Wye.dType.FLOAT,0),
        ("delta",Wye.dType.FLOAT,0),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
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
        ("Code","# Stay within bounds"),
        ("Code","frame.vars.position[0][0] = frame.vars.position[0][0] if -400 < frame.vars.position[0][0] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][1] = frame.vars.position[0][1] if -400 < frame.vars.position[0][1] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][2] = frame.vars.position[0][2] if -400 < frame.vars.position[0][2] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.gObj[0].setPos(frame.vars.position[0][0],frame.vars.position[0][1],frame.vars.position[0][2])"),
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

    def _build(rowRef):
        # print("Build ",flashingFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('flashingFish', FunFishLib.flashingFish.codeDescr, FunFishLib.flashingFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FunFishLib.flashingFish, stack)

    def run(frame):
        # print('Run 'flashingFish)
        FunFishLib.FunFishLib_rt.flashingFish_run_rt(frame)

  class flashingFlyerFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("objTag",Wye.dType.STRING,"objTag"),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(-4.0, 15.0, 4.0)),
        ("dPos",Wye.dType.FLOAT_LIST,[0.0, 0.0, -0.1]),
        ("dAngle",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.0)),
        ("colorWk",Wye.dType.FLOAT_LIST,(1, 1, 1)),
        ("colorInc",Wye.dType.FLOAT_LIST,(1, 5, 10)),
        ("color",Wye.dType.FLOAT_LIST,(0.5, 0.5, 0.5, 1)),
        ("skew",Wye.dType.FLOAT,0),
        ("delta",Wye.dType.FLOAT,0),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
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
        ("Code","frame.vars.dPos[0][2] = max(min(frame.vars.dPos[0][2], -.05), -.3)"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("WyeCore.libs.WyeLib.getObjPos",
          (None,"frame.vars.position"),
          (None,"frame.vars.gObj")),
        ("Code","# Stay within bounds"),
        ("Code","frame.vars.position[0][0] = frame.vars.position[0][0] if -400 < frame.vars.position[0][0] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][1] = frame.vars.position[0][1] if -400 < frame.vars.position[0][1] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][2] = frame.vars.position[0][2] if -400 < frame.vars.position[0][2] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.gObj[0].setPos(frame.vars.position[0][0],frame.vars.position[0][1],frame.vars.position[0][2])"),
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

    def _build(rowRef):
        # print("Build ",flashingFlyerFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('flashingFlyerFish', FunFishLib.flashingFlyerFish.codeDescr, FunFishLib.flashingFlyerFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FunFishLib.flashingFlyerFish, stack)

    def run(frame):
        # print('Run 'flashingFlyerFish)
        FunFishLib.FunFishLib_rt.flashingFlyerFish_run_rt(frame)

  class smallFlashingFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("objTag",Wye.dType.STRING,"objTag"),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(4.0, 15.0, 2.0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.1)),
        ("dAngle",Wye.dType.FLOAT_LIST,(0.0, 0.0, 0.0)),
        ("colorWk",Wye.dType.FLOAT_LIST,(1, 1, 1)),
        ("colorInc",Wye.dType.FLOAT_LIST,(2, 5, 15)),
        ("color",Wye.dType.FLOAT_LIST,(0.5, 0.5, 0.5, 1)),
        ("skew",Wye.dType.FLOAT,0),
        ("delta",Wye.dType.FLOAT,0),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
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
        ("Code","# Stay within bounds"),
        ("Code","frame.vars.position[0][0] = frame.vars.position[0][0] if -400 < frame.vars.position[0][0] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][1] = frame.vars.position[0][1] if -400 < frame.vars.position[0][1] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.position[0][2] = frame.vars.position[0][2] if -400 < frame.vars.position[0][2] < 400 else (random()-.5)*100"),
        ("Code","frame.vars.gObj[0].setPos(frame.vars.position[0][0],frame.vars.position[0][1],frame.vars.position[0][2])"),
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

    def _build(rowRef):
        # print("Build ",smallFlashingFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('smallFlashingFish', FunFishLib.smallFlashingFish.codeDescr, FunFishLib.smallFlashingFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FunFishLib.smallFlashingFish, stack)

    def run(frame):
        # print('Run 'smallFlashingFish)
        FunFishLib.FunFishLib_rt.smallFlashingFish_run_rt(frame)
