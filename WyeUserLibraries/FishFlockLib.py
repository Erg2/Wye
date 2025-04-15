from Wye import Wye
from WyeCore import WyeCore
class FishFlockLib:
  def _build():
    WyeCore.Utils.buildLib(FishFlockLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class FishFlockLib_rt:
   pass #1

  class fish2:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"leaderFish2"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 2,(frame.vars.count[0] + .5) % 3,(frame.vars.count[0] + 2) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",fish2)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('fish2', FishFlockLib.fish2.codeDescr, FishFlockLib.fish2, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.fish2, stack)

    def run(frame):
        # print('Run 'fish2)
        FishFlockLib.FishFlockLib_rt.fish2_run_rt(frame)

  class fish3:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"leaderFish3"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 3,(frame.vars.count[0] + .5) % 3,(frame.vars.count[0] + 1) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",fish3)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('fish3', FishFlockLib.fish3.codeDescr, FishFlockLib.fish3, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.fish3, stack)

    def run(frame):
        # print('Run 'fish3)
        FishFlockLib.FishFlockLib_rt.fish3_run_rt(frame)

  class followFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"fish"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 3,(frame.vars.count[0] + 1) % 3,(frame.vars.count[0] + 2) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("Label","Wait1Cycle"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Code","#print('follow target fish', frame.vars.target[0], ' fishes', frame.vars.target[0].vars.fishes[0])"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",followFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('followFish', FishFlockLib.followFish.codeDescr, FishFlockLib.followFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.followFish, stack)

    def run(frame):
        # print('Run 'followFish)
        FishFlockLib.FishFlockLib_rt.followFish_run_rt(frame)

  class followFish2:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"fish2"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 3,(frame.vars.count[0] + 1) % 3,(frame.vars.count[0] + 2) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("Label","Wait1Cycle"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Code","#print('follow target fish', frame.vars.target[0], ' fishes', frame.vars.target[0].vars.fishes[0])"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",followFish2)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('followFish2', FishFlockLib.followFish2.codeDescr, FishFlockLib.followFish2, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.followFish2, stack)

    def run(frame):
        # print('Run 'followFish2)
        FishFlockLib.FishFlockLib_rt.followFish2_run_rt(frame)

  class followFish3:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"fish3"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 3,(frame.vars.count[0] + 1) % 3,(frame.vars.count[0] + 2) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("Label","Wait1Cycle"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Code","#print('follow target fish', frame.vars.target[0], ' fishes', frame.vars.target[0].vars.fishes[0])"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fishes[0][2][0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",followFish3)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('followFish3', FishFlockLib.followFish3.codeDescr, FishFlockLib.followFish3, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.followFish3, stack)

    def run(frame):
        # print('Run 'followFish3)
        FishFlockLib.FishFlockLib_rt.followFish3_run_rt(frame)

  class leaderFish2:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("tgtPos",Wye.dType.FLOAT_LIST,(20.0, 20.0, 0.0)),
        ("fish",Wye.dType.OBJECT,None),
        ("fishTag",Wye.dType.STRING,""),
        ("tgtDist",Wye.dType.FLOAT,1.0),
        ("posStep",Wye.dType.FLOAT,0.04),
        ("dAngleX",Wye.dType.FLOAT,0.5),
        ("dAngleY",Wye.dType.FLOAT,0.5),
        ("dAngleZ",Wye.dType.FLOAT,0.5),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("prevState",Wye.dType.INTEGER,0),
        ("startQ",Wye.dType.OBJECT,None),
        ("endQ",Wye.dType.OBJECT,None),
        ("deltaT",Wye.dType.FLOAT,0.005),
        ("deltaV",Wye.dType.FLOAT_LIST,[0, 0, 0]),
        ("lerpT",Wye.dType.FLOAT,0.0),
        ("horizLim",Wye.dType.FLOAT,10.0),
        ("vertLim",Wye.dType.FLOAT,3.0),
        ("tgtChgCt",Wye.dType.INTEGER,600),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("loaderStream",
          (
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.fish"),
              (None,"['flyer_01.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 0, 0]]"),
              (None,"[[1,1,1]]"),
              (None,"frame.vars.fishTag"),
              ("Code","[[0,1,.25,1]]"),
              ("Var","frame.vars.cleanUpObjs")),
            ("Code","from panda3d.core import LPoint3f"),
            ("Var=","frame.vars.tgtPos[0] = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])"),
            ("WyeCore.libs.WyeLib.setObjRelAngle",
              (None,"frame.vars.fish"),
              (None,"[[0,90,0]]")),
            ("Var=","frame.vars.sound[0] = Wye.audio3d.loadSfx('WyeHop.wav')"),
            ("Code","Wye.audio3d.attachSoundToObject(frame.vars.sound[0], frame.vars.fish[0])"),
            ("Label","RunLoop"),
            ("CodeBlock",'''
#quat = Quat()
#lookAt(quat, target - nodePath.getPos(), Vec3.up())
#nodePath.setQuat(quat)

fish = frame.vars.fish[0]
fishPos = fish.getPos()

from panda3d.core import LPoint3f
tgtPos = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])
# stay in local area
dist = (frame.vars.fish[0].getPos() - tgtPos).length()

# if we're outside the space around the target area or we're above or below the swim lane, do turning
if fishPos[2] > (tgtPos[2] + frame.vars.vertLim[0]) or fishPos[2] < (tgtPos[2] - frame.vars.vertLim[0]) or dist > frame.vars.horizLim[0]:
    global render
    from panda3d.core import lookAt, Quat, LQuaternionf, LVector3f, Vec3

    alpha = frame.vars.deltaT[0]      # how much to rotate each step (0..1)    

    # if not turning (in turning state), calculate the turn toward the center
    if frame.vars.prevState[0] != 2:
        # save rotation start, calc rotation end and nlerp time delta

        # start
        fishQ = LQuaternionf()
        fishHPR = fish.getHpr()
        fishQ.setHpr(fishHPR)

        # end
        tgtDeltaVec = tgtPos - fishPos    # note: guaranteed 10 units away, so zero length not an issue
        tgtVec = (tgtDeltaVec).normalized()

        #fwdVec = render.getRelativeVector(fish, Vec3.down()).normalized()
        #deltaVec = LVector3f(tgtVec[0]-fwdVec[0], tgtVec[1]-fwdVec[1], tgtVec[2]-fwdVec[2])
        #deltaVec = tgtVec - fwdVec            
        #newVec = fwdVec + deltaVec * alpha
        #tgtQuat = Quat()
        #lookAt(tgtQuat, newVec, Vec3.up())

        tgtQuat = Quat()
        lookAt(tgtQuat, tgtVec, Vec3.up())
        q90 = Quat()
        q90.setHpr((0,90,0))
        tgtQ = q90 * tgtQuat

        # put info in frame for nlerp
        frame.vars.startQ[0] = fishQ   
        frame.vars.endQ[0] = tgtQ
        frame.vars.lerpT[0] = alpha

        frame.vars.prevState[0] = 2    

        #print("tgtPos", tgtPos, " tgtQ", tgtQ) #fish.setQuat(tgtQ)")
        #fish.setQuat(tgtQ)

    # We'turning, lerp that nose around the curve we calc'd above
    if frame.vars.lerpT[0] < 1.0:
        fishQ = frame.vars.startQ[0]
        tgtQ = frame.vars.endQ[0]
        tt = frame.vars.lerpT[0]
        quat = WyeCore.Utils.nlerp(fishQ, tgtQ, tt)
        fish.setQuat(quat)
        frame.vars.lerpT[0] += alpha
        #fish.setP(fish, 90)
    # done turning
    else:
        # flag that we finished the turn
        frame.vars.prevState[0] = 0    

# within "nice" distance from center, just chug happily along   
else:
    #print("2<d<=10")
    fishHPR = fish.getHpr()     # get current direction         

    # flip turn direction every new pass through the middle area
    if frame.vars.prevState[0] != 1:
        from random import random            
        frame.vars.dAngleX[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleY[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleZ[0] *= (1 if random() >= .5 else -1)

    f0 = frame.vars.dAngleX[0]
    f1 = frame.vars.dAngleY[0]
    f2 = frame.vars.dAngleZ[0]

    moveAngle = (f0, f1/2, f2/5)
    #moveAngle = (eA, eA/10, eA/20)        
    fishHPR += moveAngle
    #print("leaderfish fishHPR", fishHPR)
    #print("leaderfish fishHPR", fishHPR, " tgtHPR", tgtHPR, " moveAngle", moveAngle," setHpr", fishHPR)
    fish.setHpr(fishHPR)        
    frame.vars.prevState[0] = 1
'''),
            ("WyeCore.libs.WyeLib.setObjRelPos",
              (None,"frame.vars.fish"),
              (None,"[[0,0,-frame.vars.posStep[0]]]")),
            ("WyeCore.libs.WyeLib.getObjPos",
              (None,"frame.vars.position"),
              (None,"frame.vars.fish")),
            ("GoTo","RunLoop"),
            ("Code","frame.vars.tgtChgCt[0] -= 1"),
            ("IfGoTo","frame.vars.tgtChgCt[0] > 0","RunLoop"),
            ("Code","from random import random"),
            ("Code","from panda3d.core import LPoint3f"),
            ("Var=","frame.vars.tgtPos[0] = LPoint3f((random()-.5)*5, (random()-.5)*5, 0)"),
            ("Var=","frame.vars.tgtChgCt[0] = 600 + random() * 1200"),
            ("GoTo","RunLoop"))),
        ("changeAngleStream",
          (
            ("Label","top"),
            ("IfGoTo","frame.vars.fishTag[0] == ''","top"),
            ("WyeCore.libs.WyeLib.waitClick",
              (None,"frame.vars.fishTag")),
            ("Expr","frame.vars.dAngleX[0] = frame.vars.dAngleX[0] * -1"),
            ("Code","frame.vars.sound[0].play()"),
            ("GoTo","top"))))

    def _build(rowRef):
        # print("Build ",leaderFish2)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FishFlockLib', 'leaderFish2', FishFlockLib.leaderFish2.codeDescr, FishFlockLib.leaderFish2)

    def start(stack):
        return FishFlockLib.FishFlockLib_rt.leaderFish2_start_rt(stack)

    def run(frame):
        # print('Run 'leaderFish2)
        frame.runParallel()

  class leaderFish3:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("tgtPos",Wye.dType.FLOAT_LIST,(-20.0, 20.0, 0.0)),
        ("fish",Wye.dType.OBJECT,None),
        ("fishTag",Wye.dType.STRING,""),
        ("tgtDist",Wye.dType.FLOAT,1.0),
        ("posStep",Wye.dType.FLOAT,0.04),
        ("dAngleX",Wye.dType.FLOAT,0.5),
        ("dAngleY",Wye.dType.FLOAT,0.5),
        ("dAngleZ",Wye.dType.FLOAT,0.5),
        ("sound",Wye.dType.OBJECT,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("prevState",Wye.dType.INTEGER,0),
        ("startQ",Wye.dType.OBJECT,None),
        ("endQ",Wye.dType.OBJECT,None),
        ("deltaT",Wye.dType.FLOAT,0.005),
        ("deltaV",Wye.dType.FLOAT_LIST,[0, 0, 0]),
        ("lerpT",Wye.dType.FLOAT,0.0),
        ("horizLim",Wye.dType.FLOAT,10.0),
        ("vertLim",Wye.dType.FLOAT,3.0),
        ("tgtChgCt",Wye.dType.INTEGER,600),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("loaderStream",
          (
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.fish"),
              (None,"['flyer_01.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 0, 0]]"),
              (None,"[[1,1,1]]"),
              (None,"frame.vars.fishTag"),
              ("Code","[[1,.5,.25,1]]"),
              ("Var","frame.vars.cleanUpObjs")),
            ("Code","from panda3d.core import LPoint3f"),
            ("Var=","frame.vars.tgtPos[0] = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])"),
            ("WyeCore.libs.WyeLib.setObjRelAngle",
              (None,"frame.vars.fish"),
              (None,"[[0,90,0]]")),
            ("Var=","frame.vars.sound[0] = Wye.audio3d.loadSfx('WyeHop.wav')"),
            ("Code","Wye.audio3d.attachSoundToObject(frame.vars.sound[0], frame.vars.fish[0])"),
            ("Label","RunLoop"),
            ("CodeBlock",'''
#quat = Quat()
#lookAt(quat, target - nodePath.getPos(), Vec3.up())
#nodePath.setQuat(quat)

fish = frame.vars.fish[0]
fishPos = fish.getPos()

from panda3d.core import LPoint3f
tgtPos = LPoint3f(frame.vars.tgtPos[0][0],frame.vars.tgtPos[0][1],frame.vars.tgtPos[0][2])
# stay in local area
dist = (frame.vars.fish[0].getPos() - tgtPos).length()

# if we're outside the space around the target area or we're above or below the swim lane, do turning
if fishPos[2] > (tgtPos[2] + frame.vars.vertLim[0]) or fishPos[2] < (tgtPos[2] - frame.vars.vertLim[0]) or dist > frame.vars.horizLim[0]:
    global render
    from panda3d.core import lookAt, Quat, LQuaternionf, LVector3f, Vec3

    alpha = frame.vars.deltaT[0]      # how much to rotate each step (0..1)    

    # if not turning (in turning state), calculate the turn toward the center
    if frame.vars.prevState[0] != 2:
        # save rotation start, calc rotation end and nlerp time delta

        # start
        fishQ = LQuaternionf()
        fishHPR = fish.getHpr()
        fishQ.setHpr(fishHPR)

        # end
        tgtDeltaVec = tgtPos - fishPos    # note: guaranteed 10 units away, so zero length not an issue
        tgtVec = (tgtDeltaVec).normalized()

        #fwdVec = render.getRelativeVector(fish, Vec3.down()).normalized()
        #deltaVec = LVector3f(tgtVec[0]-fwdVec[0], tgtVec[1]-fwdVec[1], tgtVec[2]-fwdVec[2])
        #deltaVec = tgtVec - fwdVec            
        #newVec = fwdVec + deltaVec * alpha
        #tgtQuat = Quat()
        #lookAt(tgtQuat, newVec, Vec3.up())

        tgtQuat = Quat()
        lookAt(tgtQuat, tgtVec, Vec3.up())
        q90 = Quat()
        q90.setHpr((0,90,0))
        tgtQ = q90 * tgtQuat

        # put info in frame for nlerp
        frame.vars.startQ[0] = fishQ   
        frame.vars.endQ[0] = tgtQ
        frame.vars.lerpT[0] = alpha

        frame.vars.prevState[0] = 2    

        #print("tgtPos", tgtPos, " tgtQ", tgtQ) #fish.setQuat(tgtQ)")
        #fish.setQuat(tgtQ)

    # We'turning, lerp that nose around the curve we calc'd above
    if frame.vars.lerpT[0] < 1.0:
        fishQ = frame.vars.startQ[0]
        tgtQ = frame.vars.endQ[0]
        tt = frame.vars.lerpT[0]
        quat = WyeCore.Utils.nlerp(fishQ, tgtQ, tt)
        fish.setQuat(quat)
        frame.vars.lerpT[0] += alpha
        #fish.setP(fish, 90)
    # done turning
    else:
        # flag that we finished the turn
        frame.vars.prevState[0] = 0    

# within "nice" distance from center, just chug happily along   
else:
    #print("2<d<=10")
    fishHPR = fish.getHpr()     # get current direction         

    # flip turn direction every new pass through the middle area
    if frame.vars.prevState[0] != 1:
        from random import random            
        frame.vars.dAngleX[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleY[0] *= (1 if random() >= .5 else -1)
        frame.vars.dAngleZ[0] *= (1 if random() >= .5 else -1)

    f0 = frame.vars.dAngleX[0]
    f1 = frame.vars.dAngleY[0]
    f2 = frame.vars.dAngleZ[0]

    moveAngle = (f0, f1/2, f2/5)
    #moveAngle = (eA, eA/10, eA/20)        
    fishHPR += moveAngle
    #print("leaderfish fishHPR", fishHPR)
    #print("leaderfish fishHPR", fishHPR, " tgtHPR", tgtHPR, " moveAngle", moveAngle," setHpr", fishHPR)
    fish.setHpr(fishHPR)        
    frame.vars.prevState[0] = 1
'''),
            ("WyeCore.libs.WyeLib.setObjRelPos",
              (None,"frame.vars.fish"),
              (None,"[[0,0,-frame.vars.posStep[0]]]")),
            ("WyeCore.libs.WyeLib.getObjPos",
              (None,"frame.vars.position"),
              (None,"frame.vars.fish")),
            ("GoTo","RunLoop"),
            ("Code","frame.vars.tgtChgCt[0] -= 1"),
            ("IfGoTo","frame.vars.tgtChgCt[0] > 0","RunLoop"),
            ("Code","from random import random"),
            ("Code","from panda3d.core import LPoint3f"),
            ("Var=","frame.vars.tgtPos[0] = LPoint3f((random()-.5)*5, (random()-.5)*5, 0)"),
            ("Var=","frame.vars.tgtChgCt[0] = 600 + random() * 1200"),
            ("GoTo","RunLoop"))),
        ("changeAngleStream",
          (
            ("Label","top"),
            ("IfGoTo","frame.vars.fishTag[0] == ''","top"),
            ("WyeCore.libs.WyeLib.waitClick",
              (None,"frame.vars.fishTag")),
            ("Expr","frame.vars.dAngleX[0] = frame.vars.dAngleX[0] * -1"),
            ("Code","frame.vars.sound[0].play()"),
            ("GoTo","top"))))

    def _build(rowRef):
        # print("Build ",leaderFish3)
        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('FishFlockLib', 'leaderFish3', FishFlockLib.leaderFish3.codeDescr, FishFlockLib.leaderFish3)

    def start(stack):
        return FishFlockLib.FishFlockLib_rt.leaderFish3_start_rt(stack)

    def run(frame):
        # print('Run 'leaderFish3)
        frame.runParallel()

  class randomFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("followDist",Wye.dType.FLOAT,2),
        ("leaderName",Wye.dType.STRING,"leaderFish"),
        ("fishes",Wye.dType.OBJECT_LIST,None),
        ("fishTags",Wye.dType.STRING_LIST,None),
        ("position",Wye.dType.FLOAT_LIST,(0, 0, 0)),
        ("dPos",Wye.dType.FLOAT_LIST,(0.0, 0.0, -0.02)),
        ("angle",Wye.dType.FLOAT_LIST,(0.0, 90.0, 0.0)),
        ("target",Wye.dType.OBJECT,None),
        ("tgtDist",Wye.dType.FLOAT,0),
        ("count",Wye.dType.INTEGER,0),
        ("nFish",Wye.dType.INTEGER,3),
        ("objAhead",Wye.dType.OBJECT,None),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None),)
    codeDescr =        (
        ("Code","from random import random"),
        ("Var=","frame.vars.followDist[0] = random()*2+1.5"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes[0].append([None])"),
        ("Expr","frame.vars.fishTags[0].append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[0][frame.vars.count[0]]"),
          ("Expr","[[frame.vars.count[0] % 3,(frame.vars.count[0] + 1) % 3,(frame.vars.count[0] + 2) % 3,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Var=","frame.vars.count[0] += 1"),
        ("IfGoTo","frame.vars.count[0] < frame.vars.nFish[0]","MakeFish"),
        ("WyeCore.libs.WyeLib.setEqual",
          ("Var","frame.vars.target"),
          ("Expr","[WyeCore.World.findActiveObj(frame.vars.leaderName[0])]")),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("Label","SwimLoop"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[0][frame.vars.count[0]][0].setHpr(frame.vars.fishes[0][frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[0][frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[0][frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[0][frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0][0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",randomFish)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('randomFish', FishFlockLib.randomFish.codeDescr, FishFlockLib.randomFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(FishFlockLib.randomFish, stack)

    def run(frame):
        # print('Run 'randomFish)
        FishFlockLib.FishFlockLib_rt.randomFish_run_rt(frame)
