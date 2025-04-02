from Wye import Wye
from WyeCore import WyeCore
class TestLib:
  def _build():
    WyeCore.Utils.buildLib(TestLib)
  canSave = True  # all verbs can be saved with the library
  class TestLib_rt:
   pass #1

  class UpdateCallback:
      mode = Wye.mode.SINGLE_CYCLE
      dataType = Wye.dType.STRING
      paramDescr = ()
      varDescr = (("count", Wye.dType.INTEGER, 0),)

      def start(stack):
          return Wye.codeFrame(TestLib.UpdateCallback, stack)

      def run(frame):
          # print("UpdateCallback data=", frame.eventData, " verb", frame.eventData[1].verb.__name__)

          frm = frame.eventData[1]
          ctlFrm = frame.eventData[2]
          dlgFrm = ctlFrm.parentDlg
          # print("dlgFrame", dlgFrm)
          # print("UpdateCallback dlg verb", dlgFrm.verb.__name__, " dlg title ", dlgFrm.params.title[0])
          # print("Update x", int(dlgFrm.vars.XAngle[0]), " y", int(dlgFrm.vars.YAngle[0]), " z", int(dlgFrm.vars.ZAngle[0]))

          # inputs don't update parent variables until "OK" - which makes "Cancel" work correctly
          # so have to pull out the temp values from the input controls
          # Do some hackery to get to the pop up dialog's inputs' local variables
          # print("dlgFrm", dlgFrm.params.title)
          try:
              x = float(dlgFrm.params.inputs[0][0][0].vars.currVal[0])
          except:
              x = 0.
          try:
              y = float(dlgFrm.params.inputs[0][1][0].vars.currVal[0])
          except:
              y = 0.
          try:
              z = float(dlgFrm.params.inputs[0][2][0].vars.currVal[0])
          except:
              z = 0.
          frm.vars.target[0].vars.gObj[0].setHpr(x, y, z)

          WyeCore.World.dlightPath.setHpr(x, y, z)

  class ResetCallback:
      mode = Wye.mode.SINGLE_CYCLE
      dataType = Wye.dType.STRING
      paramDescr = ()
      varDescr = (("count", Wye.dType.INTEGER, 0),)

      def start(stack):
          return Wye.codeFrame(TestLib.ResetCallback, stack)

      def run(frame):
          frm = frame.eventData[1]
          ctlFrm = frame.eventData[2]
          dlgFrm = ctlFrm.parentDlg

          x = Wye.startLightAngle[0]
          y = Wye.startLightAngle[1]
          z = Wye.startLightAngle[2]

          dlgFrm.params.inputs[0][0][0].vars.currVal[0] = x
          dlgFrm.params.inputs[0][1][0].vars.currVal[0] = y
          dlgFrm.params.inputs[0][2][0].vars.currVal[0] = z

          dlgFrm.params.inputs[0][0][0].verb.update(dlgFrm.params.inputs[0][0][0])
          dlgFrm.params.inputs[0][1][0].verb.update(dlgFrm.params.inputs[0][1][0])
          dlgFrm.params.inputs[0][2][0].verb.update(dlgFrm.params.inputs[0][2][0])

          frm.vars.target[0].vars.gObj[0].setHpr(int(x), int(y), int(z))

          WyeCore.World.dlightPath.setHpr(int(x), int(y), int(z))

  class MyTestVerb:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    paramDescr =        (
        ("ret","I",1),)
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (0,75,0)),
        ("dPos","FL",
          (0.0,0.0,-0.05)),
        ("dAngle","FL",
          (0.0,0.0,-0.7)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (12,12,12)),
        ("color","FL",
          (1,1,1,1)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[2,2,2]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = base.loader.loadSfx('WyePop.wav')"),
        ("Label","Repeat"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("WyeCore.libs.WyeLib.getObjPos",
          (None,"frame.vars.position"),
          (None,"frame.vars.gObj")),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Code","if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def _build(rowRef):
        # print("Build ",MyTestVerb)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('MyTestVerb', TestLib.MyTestVerb.codeDescr, TestLib.MyTestVerb, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.MyTestVerb, stack)

    def run(frame):
        # print('Run 'MyTestVerb)
        TestLib.TestLib_rt.MyTestVerb_run_rt(frame)

  class PlaceHolder:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        ()
    codeDescr =        ()

    def _build(rowRef):
        # print("Build ",PlaceHolder)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('PlaceHolder', TestLib.PlaceHolder.codeDescr, TestLib.PlaceHolder, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.PlaceHolder, stack)

    def run(frame):
        # print('Run 'PlaceHolder)
        TestLib.TestLib_rt.PlaceHolder_run_rt(frame)

  class angleFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (-3,2,2.5)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[1,1,1]]"),
          (None,"frame.vars.objTag"),
          (None,"[[0,1,0,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
        ("Label","Repeat"),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[0]")),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[1]")),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[2]")),
        ("GoTo","Repeat"))

    def _build(rowRef):
        # print("Build ",angleFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('angleFish', TestLib.angleFish.codeDescr, TestLib.angleFish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.angleFish, stack)

    def run(frame):
        # print('Run 'angleFish)
        TestLib.TestLib_rt.angleFish_run_rt(frame)

  class clickWiggle:
    mode = Wye.mode.MULTI_CYCLE
    dataType = Wye.dType.NONE
    paramDescr =        (
        ("obj","O",1),
        ("tag","S",1),
        ("axis","I",1))
    varDescr =        (
        ("rotCt","I",0),
        ("sound","O",None),
        ("gObj","O",None),
        ("vec","FL",None),
        ("axis","I",0))
    codeDescr =        (
        ("Var=","frame.vars.rotCt[0] = 0"),
        ("Var=","frame.vars.vec[0] = frame.params.obj[0].getHpr()"),
        ("Var=","frame.vars.axis[0] = frame.params.axis[0]"),
        ("WyeCore.libs.WyeLib.waitClick",
          (None,"frame.params.tag")),
        ("Label","PlayNote"),
        ("Code","Wye.midi.playNote(91, 50, 64, 1)"),
        ("Label","WaitClick1"),
        ("Code","frame.vars.vec[0][frame.vars.axis[0]] += 5"),
        ("Code","frame.params.obj[0].setHpr(frame.vars.vec[0][0], frame.vars.vec[0][1], frame.vars.vec[0][2])"),
        ("IfGoTo","frame.vars.vec[0][frame.vars.axis[0]] < 45","WaitClick1"),
        ("Label","WaitClick2"),
        ("Code","frame.vars.vec[0][frame.vars.axis[0]] -= 5"),
        ("Code","frame.params.obj[0].setHpr(frame.vars.vec[0][0], frame.vars.vec[0][1], frame.vars.vec[0][2])"),
        ("IfGoTo","frame.vars.vec[0][frame.vars.axis[0]] > -45","WaitClick2"),
        ("Label","WaitClick3"),
        ("Var=","frame.vars.rotCt[0] += 1"),
        ("Code","#print('rotCt', frame.vars.rotCt[0])"),
        ("IfGoTo","frame.vars.rotCt[0] <= 3","WaitClick1"),
        ("Label","WaitClick4"),
        ("Code","frame.vars.vec[0][frame.vars.axis[0]] += 5"),
        ("Code","frame.params.obj[0].setHpr(frame.vars.vec[0][0], frame.vars.vec[0][1], frame.vars.vec[0][2])"),
        ("Code","#print('vec back to zero', frame.vars.vec[0], ' status', Wye.status.tostring(frame.status))"),
        ("IfGoTo","frame.vars.vec[0][frame.vars.axis[0]] < 0","WaitClick4"),
        ("Label","WaitClick5"),
        ("Code","print('After idGoTo', frame.vars.vec[0], ' status', Wye.status.tostring(frame.status))"),
        ("Code","frame.status = Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",clickWiggle)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('clickWiggle', TestLib.clickWiggle.codeDescr, TestLib.clickWiggle, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.clickWiggle, stack)

    def run(frame):
        # print('Run 'clickWiggle)
        TestLib.TestLib_rt.clickWiggle_run_rt(frame)

  class fish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("followDist","F",2),
        ("leaderName", Wye.dType.STRING, "leaderFish"),
        ("fishes","OL",None),
        ("fishTags","SL",None),
        ("position","FL",
          (0,0,0)),
        ("dPos","FL",
          (0.0,0.0,-0.02)),
        ("angle","FL",
          (0.0,90.0,0.0)),
        ("target","O",None),
        ("tgtDist","F",0),
        ("count","I",0),
        ("nFish","I",3),
        ("objAhead","O",None),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.fishes = []"),
        ("Var=","frame.vars.fishTags = []"),
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("Label","MakeFish"),
        ("Expr","frame.vars.fishes.append([None])"),
        ("Expr","frame.vars.fishTags.append([''])"),
        ("Code","objNm = 'flyer_01.glb'"),
        ("WyeCore.libs.WyeLib.loadObject",
          ("Expr","[frame]"),
          ("Expr","frame.vars.fishes[frame.vars.count[0]]"),
          ("Var","[objNm]"),
          ("Expr","[[frame.vars.count[0]*4 + 4,0, -.5]]"),
          ("Const","[[0, 90, 0]]"),
          ("Const","[[1,1,1]]"),
          ("Expr","frame.vars.fishTags[frame.vars.count[0]]"),
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
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] += 1"),
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].lookAt(frame.vars.objAhead[0])"),
        ("Code","frame.vars.fishes[frame.vars.count[0]][0].setHpr(frame.vars.fishes[frame.vars.count[0]][0], (frame.vars.count[0]-1)*20, 90, 0)"),
        ("Var=","frame.vars.tgtDist[0] = (frame.vars.fishes[frame.vars.count[0]][0].getPos() - frame.vars.objAhead[0].getPos()).length()"),
        ("Var=","frame.vars.dPos[0] = [0, 0, (frame.vars.followDist[0] - frame.vars.tgtDist[0])]"),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          ("Expr","frame.vars.fishes[frame.vars.count[0]]"),
          ("Var","frame.vars.dPos")),
        ("Var=","frame.vars.objAhead[0] = frame.vars.fishes[frame.vars.count[0]][0]"),
        ("Var=","frame.vars.count[0] = 0"),
        ("Var=","frame.vars.objAhead[0] = frame.vars.target[0].vars.fish[0]"),
        ("WyeCore.libs.WyeLib.getObjPos",
          ("Var","frame.vars.position"),
          ("Var","frame.vars.fishes[0]")),
        ("GoTo","SwimLoop"))

    def _build(rowRef):
        # print("Build ",fish)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('fish', TestLib.fish.codeDescr, TestLib.fish, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.fish, stack)

    def run(frame):
        # print('Run 'fish)
        TestLib.TestLib_rt.fish_run_rt(frame)

  class ground:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sounds","OL",
          ()),
        ("currSnd","I",0),
        ("position","FL",
          (-1,2,-1.2)),
        ("weeds","OL",
          ()),
        ("weedColorInc","FL",
          ()),
        ("bubbles","OL",
          ()),
        ("bubbleCt","IL",
          ()),
        ("bubblePop","IL",
          ()),
        ("bubbleMin","F",180),
        ("bubbleRand","F",180),
        ("bubbleFloat","FL",
          (0.001,0.001,0.075)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("CodeBlock",'''
frame.vars.cleanUpObjs[0] = []
# ground
floorPos = [] #[[0]*20]*20      # 20x20 floor tile heights
from random import random
import math
floorX = 80
floorY = 80
for yy in range(floorX + 1):
    floorPos.append([])
    for xx in range(floorY + 1):
        #angle = max(abs(xx-10), abs(yy-10)) * .11
        #print("floor x", xx, " y", yy, " angle", angle, " ht", (1 - math.cos(angle)))
        #if abs(xx) > 75 and abs(yy) > 75:
        #    floorPos[yy].append(10+random()*20)
        #else:
        #    floorPos[yy].append(random()*5)  # + (1 - math.cos(angle)) * 50)
        floorPos[yy].append(random()*5)  # + (1 - math.cos(angle)) * 50)
        #print("floorPos", yy, ",", xx, "=", floorPos[yy][xx])
floor = Wye3dObjsLib._surf(floorPos, (10,10,1), (-(int(floorX * 10/2)),-(int(floorY*10/2)),-18))
frame.vars.cleanUpObjs[0].append(floor._path)
floor.setColor((.95,.84,.44,.1))

tag = "wyeTag" + str(WyeCore.Utils.getId())
floor.setTag(tag)
#print("Set tag", tag, " on", floor._path)
WyeCore.picker.makePickable(floor._path)
#print("test floor with tagDebug")
#WyeCore.picker.tagDebug(floor._path)
            

from random import random

# load audio manager and buffer up a bunch of pop sound slots so each bubble can play a full pop before the sound gets reused
for ii in range(100):
    frame.vars.sounds[0].append(Wye.audio3d.loadSfx("WyePop.wav"))
    
# Weeds and bubbles decorating the floor
for xx in range(int(floorX * floorY * .08)):
    if xx < 35:
        posX = (random()-.5)*20 - 25
        posY = (random()-.5)*20 + 75
    else:
        posX = (random()-.5)*floorX*10
        posY = (random()-.5)*floorY*10
    ixX = int(posX/floorX)
    ixY = int(posY/floorY)
    posZ = floorPos[ixY][ixX]
    #print("ixX", ixX, " ixY", ixY, " posX", posX, " posY", posY, " posZ", posZ)
    ht  = 2+3*random()
    color = (.25+random()*.75,.25+random()*.75,.25+random()*.75, .5)
    weed = Wye3dObjsLib._box([.1, .1, ht], [posX, posY, -18 + posZ+ht*.5])
    frame.vars.cleanUpObjs[0].append(weed)
    frame.vars.weedColorInc[0].append([random() * .05, random() * .05, random() * .05])
    weed.setColor(color)
    frame.vars.weeds[0].append(weed._path)
    weed.setTag(tag)
    WyeCore.picker.makePickable(weed._path)
    #print("Set tag", tag, " on weed", weed._path)
    
    # Create bubble, init color change amt and countdown to pop
    bubble = Wye3dObjsLib._ball(.2, [posX, posY, -18 + random() * 20])
    frame.vars.cleanUpObjs[0].append(bubble._path)
    bubble.setColor(color)
    bubble.setTag(tag)
    WyeCore.picker.makePickable(bubble._path)
    frame.vars.bubbles[0].append(bubble)
    pop = 60 + frame.vars.bubbleRand[0] * random()
    frame.vars.bubblePop[0].append(pop)
    frame.vars.bubbleCt[0].append(10+random()*(pop-10))

WyeCore.World.registerObjTag(tag, frame)
'''),
        ("Label","Running"),
        ("CodeBlock",'''
# float bubbles up randomly 
from random import random


# set fall off
#Wye.audio3d.setDistanceFactor(.1)
Wye.audio3d.setDropOffFactor(5)

for ii in range(len(frame.vars.bubbles[0])):
    bubble = frame.vars.bubbles[0][ii]
    weed = frame.vars.weeds[0][ii]
    frame.vars.bubbleCt[0][ii] +=1
    if frame.vars.bubbleCt[0][ii] >= frame.vars.bubblePop[0][ii]:
        # reset bubble
        weed = frame.vars.weeds[0][ii]
        pos = weed.getPos()
        pos[2] += 2
        bubble.setPos(pos[0], pos[1], pos[2])
        frame.vars.bubbleCt[0][ii] = 0
        frame.vars.bubblePop[0][ii] = frame.vars.bubbleMin[0] + frame.vars.bubbleRand[0] * random()
        #weed.setColor(bubble.getColor())

    else:
        # float bubble up
        from panda3d.core import LVector3f
        bubble._path.setPos(bubble._path, LVector3f(frame.vars.bubbleFloat[0][0], frame.vars.bubbleFloat[0][1], frame.vars.bubbleFloat[0][2]))
        # trigger pop now so it sounds when bubble pops
        if frame.vars.bubblePop[0][ii]-9 > frame.vars.bubbleCt[0][ii] > frame.vars.bubblePop[0][ii]-10:
            # pop bubble
            viewerDist = (base.camera.getPos() - bubble.getPos()).length()
            if viewerDist < 100:
                #Wye.midi.playNote(118, 60, int(127-viewerDist), .1)
                Wye.audio3d.attachSoundToObject(frame.vars.sounds[0][frame.vars.currSnd[0]], bubble._path)
                frame.vars.sounds[0][frame.vars.currSnd[0]].play()
                frame.vars.currSnd[0] = (frame.vars.currSnd[0] + 1) % 100
            
        # do weed color
        color = weed.getColor()
        # cycle weed colors before resetting bubble
        if frame.vars.bubbleCt[0][ii] > frame.vars.bubblePop[0][ii]-30:
            for cc in range(3):
                color[cc] += frame.vars.weedColorInc[0][ii][cc]
                if color[cc] > 1:
                    color[cc] = 1
                    frame.vars.weedColorInc[0][ii][cc] *= -1
                if color[cc] < .25:
                    color[cc] = .25
                    frame.vars.weedColorInc[0][ii][cc] *= -1
            weed.setColor(color)
        # bubble reset, pick up weed color
        if frame.vars.bubbleCt[0][ii] < 2:
            bubble.setColor(color)
'''))

    def _build(rowRef):
        # print("Build ",ground)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('ground', TestLib.ground.codeDescr, TestLib.ground, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.ground, stack)

    def run(frame):
        # print('Run 'ground)
        TestLib.TestLib_rt.ground_run_rt(frame)

  class leaderFish:
    mode = Wye.mode.PARALLEL
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.OBJECT
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("tgtPos", "FL", (0, 25, 0)),
        ("posStep","F",0.04),
        ("fish","O",None),
        ("fishTag","S",""),
        ("tgtDist","F",1.0),
        ("dAngleX","F",0.5),
        ("dAngleY","F",0.5),
        ("dAngleZ","F",0.5),
        ("sound","O",None),
        ("position","FL",(0,0,0)),
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
        # print("Build ",leaderFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('TestLib', 'leaderFish', TestLib.leaderFish.codeDescr, TestLib.leaderFish)

    def start(stack):
        return TestLib.TestLib_rt.leaderFish_start_rt(stack)

    def run(frame):
        # print('Run 'leaderFish)
        frame.runParallel()

  class showFishDialog:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.STRING
    paramDescr =        ()
    varDescr =        (
        ("dlgRetVal","I",-1),
        ("XAngleID","S",""),
        ("XAngle","I",0),
        ("YAngleID","S",""),
        ("YAngle","I",0),
        ("ZAngleID","S",""),
        ("ZAngle","I",0),
        ("updateBtnId","O",None),
        ("dlgButton","O",None),
        ("doitId","O",None),
        ("target","O",None))
    codeDescr =        (
        (None,"frame.vars.dlgButton[0] = Wye3dObjsLib._3dText(text='Set Fish and Light Angle',color=(1,1,1,1), pos=(-3,2,2), scale=(.2,.2,.2))"),
        (None,"frame.vars.doitId[0] = frame.vars.dlgButton[0].getTag()"),
        ("Label","PopDialog"),
        ("WyeCore.libs.WyeLib.waitClick",
          (None,"frame.vars.doitId")),
        ("WyeCore.libs.WyeLib.setEqual",
          (None,"frame.vars.target"),
          (None,"[WyeCore.World.findActiveObj('angleFish')]")),
        ("IfGoTo","frame.vars.target[0] is None","PopDialog"),
        (None,"frame.vars.XAngle[0] = WyeCore.World.dlightPath.getHpr()[0]"),
        (None,"frame.vars.YAngle[0] = WyeCore.World.dlightPath.getHpr()[1]"),
        (None,"frame.vars.ZAngle[0] = WyeCore.World.dlightPath.getHpr()[2]"),
        ("WyeUILib.Dialog",
          (None,"frame.vars.dlgRetVal"),
          (None,"['Fish Angle Dialog']"),
          (None,"[(-3,2,1.5),]"),
          (None,"[None]"),
          ("WyeUILib.InputFloat",
            (None,"frame.vars.XAngleID"),
            (None,"['XAngle']"),
            (None,"frame.vars.XAngle"),
            (None,"[TestLib.UpdateCallback]"),
            (None,"[frame]")),
          ("WyeUILib.InputFloat",
            (None,"frame.vars.YAngleID"),
            (None,"['YAngle']"),
            (None,"frame.vars.YAngle"),
            (None,"[TestLib.UpdateCallback]"),
            (None,"[frame]")),
          ("WyeUILib.InputFloat",
            (None,"frame.vars.ZAngleID"),
            (None,"['ZAngle']"),
            (None,"frame.vars.ZAngle"),
            (None,"[TestLib.UpdateCallback]"),
            (None,"[frame]")),
          ("WyeUILib.InputButton",
            (None,"frame.vars.updateBtnId"),
            (None,"['Click to reset Position']"),
            (None,"[TestLib.ResetCallback]"),
            (None,"[frame]"))),
        ("IfGoTo","frame.vars.dlgRetVal[0] != Wye.status.SUCCESS","PopDialog"),
        ("WyeCore.libs.WyeLib.setObjAngle",
          (None,"frame.vars.target[0].vars.gObj"),
          (None,"[[int(frame.vars.XAngle[0]),int(frame.vars.YAngle[0]),int(frame.vars.ZAngle[0])]]")),
        ("GoTo","PopDialog"))

    def _build(rowRef):
        # print("Build ",showFishDialog)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('showFishDialog', TestLib.showFishDialog.codeDescr, TestLib.showFishDialog, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.showFishDialog, stack)

    def run(frame):
        # print('Run 'showFishDialog)
        TestLib.TestLib_rt.showFishDialog_run_rt(frame)

  class testLoader:
    mode = Wye.mode.SINGLE_CYCLE
    dataType = Wye.dType.NONE
    paramDescr =        (
        ("obj","O",1),
        ("file","S",1),
        ("posVec","IL",1),
        ("scaleVec","IL",1),
        ("tag","S",1),
        ("colorVec","FL",1))
    varDescr =        ()
    codeDescr =        (
        ("WyeCore.libs.WyeLib.loadModel",
          ("Var","frame.params.obj"),
          ("Var","frame.params.file")),
        ("WyeCore.libs.WyeLib.makePickable",
          ("Var","frame.params.tag"),
          ("Var","frame.params.obj")),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.params.obj"),
          ("Var","frame.params.colorVec")),
        ("WyeCore.libs.WyeLib.showModel",
          ("Var","frame.params.obj"),
          ("Var","frame.params.posVec"),
          ("Var","frame.params.scaleVec")))

    def _build(rowRef):
        # print("Build ",testLoader)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('testLoader', TestLib.testLoader.codeDescr, TestLib.testLoader, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.testLoader, stack)

    def run(frame):
        # print('Run 'testLoader)
        TestLib.TestLib_rt.testLoader_run_rt(frame)

  class testObj3:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S",""),
        ("sound","O",None),
        ("position","FL",
          (-35,75,2)),
        ("dPos","FL",
          (0.0,0.0,-0.05)),
        ("dAngle","FL",
          (0.0,0.0,-0.75)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (8,8,8)),
        ("color","FL",
          (0,0.33,0.66,1)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[2,2,2]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Label","Repeat"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("Var=","frame.vars.colorWk[0][2] = (frame.vars.colorWk[0][2] + frame.vars.colorInc[0][2])"),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Code","if frame.vars.colorWk[0][2] >= 255 or frame.vars.colorWk[0][2] <= 0:"),
        ("Code"," frame.vars.colorInc[0][2] = -1 * frame.vars.colorInc[0][2]"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def _build(rowRef):
        # print("Build ",testObj3)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('testObj3', TestLib.testObj3.codeDescr, TestLib.testObj3, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.testObj3, stack)

    def run(frame):
        # print('Run 'testObj3)
        TestLib.TestLib_rt.testObj3_run_rt(frame)

  class testObj3b:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S",""),
        ("sound","O",None),
        ("position","FL",
          (-35,75,0)),
        ("dPos","FL",
          (0.0,0.0,-0.05)),
        ("dAngle","FL",
          (0.0,0.0,-0.7)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (12,12,12)),
        ("color","FL",
          (0,0.33,0.66,1)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[2,2,2]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Label","Repeat"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("Var=","frame.vars.colorWk[0][1] = (frame.vars.colorWk[0][1] + frame.vars.colorInc[0][1])"),
        ("Code","if frame.vars.colorWk[0][1] >= 255 or frame.vars.colorWk[0][1] <= 0:"),
        ("Code"," frame.vars.colorInc[0][1] = -1 * frame.vars.colorInc[0][1]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def _build(rowRef):
        # print("Build ",testObj3b)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('testObj3b', TestLib.testObj3b.codeDescr, TestLib.testObj3b, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.testObj3b, stack)

    def run(frame):
        # print('Run 'testObj3b)
        TestLib.TestLib_rt.testObj3b_run_rt(frame)

  class testObj3c:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S",""),
        ("sound","O",None),
        ("position","FL",
          (-35,75,-2)),
        ("dPos","FL",
          (0.0,0.0,-0.05)),
        ("dAngle","FL",
          (0.0,0.0,-0.65)),
        ("colorWk","FL",
          (1,1,1)),
        ("colorInc","FL",
          (10,25,10)),
        ("color","FL",
          (0,0.33,0.66,1)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[2,2,2]]"),
          (None,"frame.vars.objTag"),
          (None,"frame.vars.color"),
          ("Var","frame.vars.cleanUpObjs")),
        ("Label","Repeat"),
        ("WyeCore.libs.WyeLib.setObjRelAngle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dAngle")),
        ("WyeCore.libs.WyeLib.setObjRelPos",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.dPos")),
        ("Var=","frame.vars.colorWk[0][0] = (frame.vars.colorWk[0][0] + frame.vars.colorInc[0][0])"),
        ("Code","if frame.vars.colorWk[0][0] >= 255 or frame.vars.colorWk[0][0] <= 0:"),
        ("Code"," frame.vars.colorInc[0][0] = -1 * frame.vars.colorInc[0][0]"),
        ("Var=","frame.vars.color[0] = (frame.vars.colorWk[0][0]/256., frame.vars.colorWk[0][1]/256., frame.vars.colorWk[0][2]/256., 1)"),
        ("WyeCore.libs.WyeLib.setObjMaterialColor",
          ("Var","frame.vars.gObj"),
          ("Var","frame.vars.color")),
        ("GoTo","Repeat"))

    def _build(rowRef):
        # print("Build ",testObj3c)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('testObj3c', TestLib.testObj3c.codeDescr, TestLib.testObj3c, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLib.testObj3c, stack)

    def run(frame):
        # print('Run 'testObj3c)
        TestLib.TestLib_rt.testObj3c_run_rt(frame)

  class parallelFish:
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
        # print("Build ",parallelFish)

        rowIxRef = [0]
        return WyeCore.Utils.buildParallelText('TestLib', 'parallelFish', TestLib.parallelFish.codeDescr, TestLib.parallelFish)

    def start(stack):
        return TestLib.TestLib_rt.parallelFish_start_rt(stack)

    def run(frame):
        # print('Run 'parallelFish)
        frame.runParallel()
