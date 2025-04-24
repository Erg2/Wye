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
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),
        ("tAngle",Wye.dType.FLOAT,0.0),
        ("segAngle",Wye.dType.FLOAT,0.0),
        ("dAngle",Wye.dType.FLOAT,0.001),
        ("color",Wye.dType.FLOAT_LIST,[0.5, 0.3, 0.3, 1.0]),
        ("colorInc",Wye.dType.FLOAT_LIST,[0.001, 0.002, 0.003]),
        ("tColorInc",Wye.dType.FLOAT_LIST,[0.1, 0.1, 0.1]),
        ("noop",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("CreateJBodStream",
          (
            ("Code","#hang everything off central point"),
            ("Code","from panda3d.core import NodePath"),
            ("Code","frame.vars.gObj[0] = NodePath('JFish')"),
            ("Code","frame.vars.gObj[0].reparentTo(render)"),
            ("Code","from random import random"),
            ("Code","frame.vars.gObj[0].setPos(((random()-.5)*20, (random()-.5) * 20, random()))"),
            ("Code","frame.vars.gObj[0].setScale((.5,.5,.5))"),
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
            ("Label","Done"))),
        ("CreateT1Stream",
          (
            ("Label","Wait1Cycle"),
            ("Label","BldTentacles"),
            ("Var=","frame.vars.tSegCt[0] = 0"),
            ("Code","# one t list per tentacle"),
            ("Code","frame.vars.t[0].append([])"),
            ("Code","# base pos for this tentacle"),
            ("Label","BldTentacle"),
            ("Code","import math"),
            ("Code","x = math.sin(frame.vars.tAngle[0])"),
            ("Code","y = math.cos(frame.vars.tAngle[0])"),
            ("Code","obj = Wye3dObjsLib._ball(.2-(frame.vars.tSegCt[0] * .05), [x,y,-.5 - (frame.vars.tSegCt[0] *.5)])"),
            ("Code","obj._path.reparentTo(frame.vars.gObj[0])"),
            ("Code","frame.vars.t[0][frame.vars.tCt[0]].append([obj])"),
            ("Code","frame.vars.cleanUpObjs[0].append(obj._path)"),
            ("Code","obj.setColor((frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2], 1))"),
            ("Code","frame.vars.tTags[0].append(['']) # make array elem for tag"),
            ("WyeCore.libs.WyeLib.makePickable",
              ("Expr","frame.vars.tTags[0][frame.vars.tgCt[0]]"),
              ("Expr","[obj._path]")),
            ("Code","WyeCore.World.registerObjTag(frame.vars.tTags[0][frame.vars.tgCt[0]][0], frame)"),
            ("Var=","frame.vars.tSegCt[0] += 1 #Next segment of this tentacle"),
            ("Code","#loop to build next tentacle seg"),
            ("IfGoTo","frame.vars.tSegCt[0] < 6","BldTentacle"),
            ("Var=","frame.vars.tAngle[0] += math.pi/3."),
            ("Var=","frame.vars.tCt[0] += 1 # Next tentacle"),
            ("Code","#Loop to build next tentacle"),
            ("IfGoTo","frame.vars.tCt[0] < 6","BldTentacles"),
            ("Label","Drift"),
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
            ("Code","for tIx in range(6):"),
            ("Code"," x = math.sin(frame.vars.tAngle[0])"),
            ("Code"," y = math.cos(frame.vars.tAngle[0])"),
            ("Code"," frame.vars.tAngle[0] += math.pi/3."),
            ("Code"," color = [frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2]]"),
            ("Code"," #print('start tentacle, color', color)"),
            ("Code"," frame.vars.tColorInc[0] = [abs(frame.vars.tColorInc[0][0]), abs(frame.vars.tColorInc[0][1]), abs(frame.vars.tColorInc[0][2])]"),
            ("Code"," for sIx in range(frame.vars.nSegs[0]):"),
            ("Code","  frame.vars.segAngle[0] = frame.vars.segAngle[0] + frame.vars.dAngle[0] if frame.vars.segAngle[0] < 360 else 0"),
            ("Code","  obj = frame.vars.t[0][tIx][sIx][0]"),
            ("Code","  obj.setPos(x + math.sin(frame.vars.segAngle[0]+sIx*.25) * (sIx+1)*.05, y, -.5 - (sIx*.5))"),
            ("Code","  #print('color', color)"),
            ("Code","  obj.setColor((color[0], color[1], color[2], 1))"),
            ("Code","  frame.vars.tColorInc[0][0] *= 1 if 0 < color[0] + frame.vars.tColorInc[0][0] < 1 else -1"),
            ("Code","  frame.vars.tColorInc[0][1] *= 1 if 0 < color[1] + frame.vars.tColorInc[0][1] < 1 else -1"),
            ("Code","  frame.vars.tColorInc[0][2] *= 1 if 0 < color[2] + frame.vars.tColorInc[0][2] < 1 else -1"),
            ("Code","  color[0] += frame.vars.tColorInc[0][0]"),
            ("Code","  color[1] += frame.vars.tColorInc[0][1]"),
            ("Code","  color[2] += frame.vars.tColorInc[0][2]"))),
        ("Move",
          (
            ("Label","Wait1Cycle"),
            ("Label","Wait1Cycle"),
            ("Label","Wait1Cycle"),
            ("Label","Wait1Cycle"),
            ("Code","#print('gObj', frame.vars.gObj[0])"),
            ("Code","pos = frame.vars.gObj[0].getPos()"),
            ("Code","pos[0]+=.001"),
            ("Code","if pos[0] > 400:"),
            ("Code"," pos[0] -= 800"),
            ("Code","frame.vars.gObj[0].setPos(pos)"))))

    def _build(rowRef):
        # print("Build ",Jelly)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'Jelly', FunFishLib.Jelly.codeDescr, FunFishLib.Jelly)

    def start(stack):
        return FunFishLib.FunFishLib_rt.Jelly_start_rt(stack)

    def run(frame):
        # print('Run 'Jelly)
        frame.runParallel()

  class Jelly2:
    mode = Wye.mode.PARALLEL
    autoStart = False
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
        ("segOffs",Wye.dType.FLOAT_LIST,[]),
        ("tAngle",Wye.dType.FLOAT,0.0),
        ("tOff",Wye.dType.FLOAT_LIST,[0.0]),
        ("segAngle",Wye.dType.FLOAT,0.0),
        ("dAngle",Wye.dType.FLOAT,0.001),
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
            ("Code","f = random()*.5"),
            ("Code","frame.vars.gObj[0].setPos(((random()-.5)*20, (random()-.5) * 20, random()))"),
            ("Code","frame.vars.gObj[0].setScale((.25+f,.25+f,.25+f))"),
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
            ("Code","frame.status=Wye.status.SUCCESS"))),
        ("CreateT1Stream",
          (
            ("Label","Wait1Cycle"),
            ("Code","frame.vars.tOff[0] = []"),
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
            ("Code","obj = Wye3dObjsLib._ball(.2-(frame.vars.tSegCt[0] * .05), [frame.vars.tOff[0][frame.vars.tCt[0]][0], frame.vars.tOff[0][frame.vars.tCt[0]][1],-.5 - (frame.vars.tSegCt[0] *.5)])"),
            ("Code","obj._path.reparentTo(frame.vars.gObj[0])"),
            ("Code","frame.vars.t[0][frame.vars.tCt[0]].append([obj])"),
            ("Code","frame.vars.cleanUpObjs[0].append(obj._path)"),
            ("Code","obj.setColor((frame.vars.color[0][0], frame.vars.color[0][1], frame.vars.color[0][2], 1))"),
            ("Code","frame.vars.tTags[0].append(['']) # make array elem for tag"),
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
            ("Code","  obj.setPos(x + frame.vars.segOffs[0][sIx], y, -.5 - (sIx*.5))"),
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
            ("Code","frame.vars.gObj[0].setPos(pos)"))))

    def _build(rowRef):
        # print("Build ",Jelly2)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'Jelly2', FunFishLib.Jelly2.codeDescr, FunFishLib.Jelly2)

    def start(stack):
        return FunFishLib.FunFishLib_rt.Jelly2_start_rt(stack)

    def run(frame):
        # print('Run 'Jelly2)
        frame.runParallel()

  class Jelly3:
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
        ("tOff",Wye.dType.FLOAT_LIST,[0.0]),
        ("segAngle",Wye.dType.FLOAT,0.0),
        ("dAngle",Wye.dType.FLOAT,0.001),
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
            ("Code","f = random()*.5"),
            ("Code","frame.vars.gObj[0].setPos(((random()-.5)*20, (random()-.5) * 20, random()))"),
            ("Code","frame.vars.gObj[0].setScale((.25+f,.25+f,.25+f))"),
            ("Code","frame.vars.note[0] = int(f*10) + 45"),
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
            ("Code","frame.vars.tOff[0] = []"),
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
            ("Code","obj = Wye3dObjsLib._ball(.2-(frame.vars.tSegCt[0] * .05), [frame.vars.tOff[0][frame.vars.tCt[0]][0], frame.vars.tOff[0][frame.vars.tCt[0]][1],-.5 - (frame.vars.tSegCt[0] *frame.vars.segSep[0])])"),
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
            ("Code","  obj.setPos(x + frame.vars.segOffs[0][sIx], y, -.5 - (sIx*frame.vars.segSep[0]))"),
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
            ("Code","Wye.midi.playNote(98, frame.vars.note[0], 127, .5)"),
            ("Label","Shrink"),
            ("Code","frame.vars.segSep[0] -= .1"),
            ("IfGoTo","frame.vars.segSep[0] > .2","Shrink"),
            ("WyeCore.libs.WyeLib.delay",
              ("Expr","[60] # wait this many cycles")),
            ("Label","Restore"),
            ("Code","frame.vars.segSep[0] += .001"),
            ("IfGoTo","frame.vars.segSep[0] < .5","Restore"),
            ("GoTo","Loop"))))

    def _build(rowRef):
        # print("Build ",Jelly3)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FunFishLib', 'Jelly3', FunFishLib.Jelly3.codeDescr, FunFishLib.Jelly3)

    def start(stack):
        return FunFishLib.FunFishLib_rt.Jelly3_start_rt(stack)

    def run(frame):
        # print('Run 'Jelly3)
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
