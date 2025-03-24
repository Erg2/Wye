from Wye import Wye
from WyeCore import WyeCore
class MyTestLib:
  def _build():
    WyeCore.Utils.buildLib(MyTestLib)
  canSave = True  # all verbs can be saved with the library
  class MyTestLib_rt:
   pass #1

  class leaderFish:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("fish","O",None),
        ("fishTag","S",""),
        ("tgtPos","FL",
          (0,10,0)),
        ("tgtDist","F",1.0),
        ("posStep","F",0.04),
        ("dAngleX","F",0.5),
        ("dAngleY","F",0.5),
        ("dAngleZ","F",0.5),
        ("sound","O",None),
        ("position","FL",
          (0,0,0)),
        ("prevState","I",0),
        ("startQ","O",None),
        ("endQ","O",None),
        ("deltaT","F",0.005),
        ("lerpT","F",0.0),
        ("horizLim","F",10.0),
        ("vertLim","F",3.0),
        ("tgtChgCt","I",600),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("loaderStream",
          (
            ("Var=","frame.vars.deltaV=[[0,0,0]]"),
            ("Var=","frame.vars.cleanUpObjs[0] = []"),
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.fish"),
              (None,"['flyer_01.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 0, 0]]"),
              (None,"[[1,1,1]]"),
              (None,"frame.vars.fishTag"),
              (None,"[[1,0,0,1]]"),
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
tgtPos = frame.vars.tgtPos[0]
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
        # print("Build ",leaderFish)
        return WyeCore.Utils.buildParallelText('MyTestLib','leaderFish', MyTestLib.leaderFish.codeDescr, MyTestLib.leaderFish)

    def start(stack):
        return MyTestLib.MyTestLib_rt.leaderFish_start_rt(stack)

    def run(frame):
        # print('Run 'leaderFish)
        try:
          frame.runParallel()
        except Exception as e:
          if not hasattr(frame, 'errOnce'):
            print('MyTestLib leaderFish runParallel failed\n', str(e))
            import traceback
            traceback.print_exception(e)
            frame.errOnce = True

