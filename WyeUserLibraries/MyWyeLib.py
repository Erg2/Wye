from Wye import Wye
from WyeCore import WyeCore
class MyWyeLib:
  def _build():
    WyeCore.Utils.buildLib(MyWyeLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class MyWyeLib_rt:
   pass #1

  class followFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
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
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,None))
    codeDescr =        (
        ("Var=","frame.vars.fishes[0] = []"),
        ("Var=","frame.vars.fishTags[0] = []"),
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
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
        ("Code","print('follow target fish', frame.vars.target[0], ' fishes', frame.vars.target[0].vars.fishes[0])"),
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
        return WyeCore.Utils.buildCodeText('followFish', MyWyeLib.followFish.codeDescr, MyWyeLib.followFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(MyWyeLib.followFish, stack)

    def run(frame):
        # print('Run 'followFish)
        MyWyeLib.MyWyeLib_rt.followFish_run_rt(frame)
