from Wye import Wye
from WyeCore import WyeCore
class RecordPlaybackLib:
  def _build():
    WyeCore.Utils.buildLib(RecordPlaybackLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class RecordPlaybackLib_rt:
   pass #1

  class ClickMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("MBtn",Wye.dType.INTEGER,1),
        ("shift",Wye.dType.BOOL,1),
        ("ctrl",Wye.dType.BOOL,1),
        ("alt",Wye.dType.BOOL,1),
        ("position",Wye.dType.FLOAT_LIST,1),)
    varDescr =  ()
    codeDescr =        (
        ("Code","if not frame.params.position:  # DEBUG - null param not supposed to happen"),
        ("Code","    print('>>>>> ClickMouse position is null!')  "),
        ("Code","    return"),
        ("Code","#print('ClickMouse mb', frame.params.MBtn[0], ' shift', frame.params.shift[0], ' ctrl', frame.params.ctrl[0], ' alt', frame.params.alt[0], ' position', frame.params.position[0], flush=True)"),
        ("Code","#Clear mouse"),
        ("Code","# clear mouse"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(0,0, 0, 0, 0, 0, 0, 0)"),
        ("Code","# Do mouse"),
        ("Code","x = frame.params.position[0][0] #"),
        ("Code","y = frame.params.position[0][1] #"),
        ("Code","#print('ClickMouse', frame.params.MBtn[0] )"),
        ("Code","mb1 = True if frame.params.MBtn[0] == 1 else False #"),
        ("Code","mb2 = True if frame.params.MBtn[0] == 2 else False #"),
        ("Code","mb3 = True if frame.params.MBtn[0] == 3 else False #"),
        ("Code","shift = frame.params.shift[0] #"),
        ("Code","alt = frame.params.alt[0] #"),
        ("Code","ctl = frame.params.ctrl[0] #"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(x,y, mb1, mb2, mb3, shift, ctl, alt)"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(0,0, 0, 0, 0, 0, 0, 0)"))

    def _build(rowRef):
        # print("Build ",ClickMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('ClickMouse', RecordPlaybackLib.ClickMouse.codeDescr, RecordPlaybackLib.ClickMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.ClickMouse, stack)

    def run(frame):
        # print('Run 'ClickMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.ClickMouse_run_rt(frame)

  class Delay:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("nFrames",Wye.dType.INTEGER,1),)
    varDescr =  (
        ("frameCt",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("Label","Loop"),
        ("IfGoTo","frame.vars.frameCt[0] >= frame.params.nFrames[0]","Done"),
        ("Var=","frame.vars.frameCt[0] += 1"),
        ("GoTo","Loop"),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"))

    def _build(rowRef):
        # print("Build ",Delay)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Delay', RecordPlaybackLib.Delay.codeDescr, RecordPlaybackLib.Delay, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.Delay, stack)

    def run(frame):
        # print('Run 'Delay)
        RecordPlaybackLib.RecordPlaybackLib_rt.Delay_run_rt(frame)

  class DoMouseMove:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("MBtn",Wye.dType.INTEGER,1),
        ("shift",Wye.dType.BOOL,1),
        ("ctrl",Wye.dType.BOOL,1),
        ("alt",Wye.dType.BOOL,1),
        ("startPos",Wye.dType.FLOAT_LIST,1),
        ("endPos",Wye.dType.FLOAT_LIST,1),
        ("nFrames",Wye.dType.INTEGER,1),)
    varDescr =  (
        ("frameNum",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("IfGoTo","frame.vars.frameNum[0] > frame.params.nFrames","Done"),
        ("Code","frac = frame.vars.frameNum[0] / params.nFrames[0]"),
        ("Code","dx = int((frame.params.endPos[0][0] - frame.params.startPos[0][0])  * frac)#"),
        ("Code","dy = int((frame.params.endPos[0][1] - frame.params.startPos[0][1]) * frac)#"),
        ("Code","x = frame.params.startPos[0][0] + dx #"),
        ("Code","y = frame.params.startPos[0][1] + dy #"),
        ("Code","mb1 = True if frame.params.MBtn == 1 else False #"),
        ("Code","mb2 = True if frame.params.MBtn == 2 else False #"),
        ("Code","mb3 = True if frame.params.MBtn == 3 else False #"),
        ("Code","shift = frame.params.shift[0] #"),
        ("Code","alt = frame.params.alt[0] #"),
        ("Code","ctl = frame.params.ctrl[0] #"),
        ("Code","base.win.movePointer(0, x,y)"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(x,y, mb1, mb2, mb3, shift, ctl, alt)"),
        ("Var=","frame.vars.frameNum[0] += 1"),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",DoMouseMove)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('DoMouseMove', RecordPlaybackLib.DoMouseMove.codeDescr, RecordPlaybackLib.DoMouseMove, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.DoMouseMove, stack)

    def run(frame):
        # print('Run 'DoMouseMove)
        RecordPlaybackLib.RecordPlaybackLib_rt.DoMouseMove_run_rt(frame)

  class DoMouseWheel:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("dir",Wye.dType.INTEGER,1),)
    varDescr =  ()
    codeDescr =        (
        ("Code","WyeCore.focusManager._mouseHandler.mouseWheel(frame.params.dir[0])"),)

    def _build(rowRef):
        # print("Build ",DoMouseWheel)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('DoMouseWheel', RecordPlaybackLib.DoMouseWheel.codeDescr, RecordPlaybackLib.DoMouseWheel, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.DoMouseWheel, stack)

    def run(frame):
        # print('Run 'DoMouseWheel)
        RecordPlaybackLib.RecordPlaybackLib_rt.DoMouseWheel_run_rt(frame)

  class FakeMouse:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("gObj",Wye.dType.OBJECT,None),
        ("tag",Wye.dType.STRING,"None"),
        ("cleanUpObjs",Wye.dType.OBJECT_LIST,"None"),
        ("dbgCt",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("Code","frame.vars.gObj[0] = WyeCore.libs.Wye3dObjsLib._pointer(size=[.05,.01,.05], pos=[0,0,0])"),
        ("Code","#Note: don't put on tag or register tag 'cause don't want mouse ptr to be clickable"),
        ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.gObj[0]) "),
        ("Label","HangingOut"),
        ("Code","#if frame.vars.dbgCt[0] <= 0:"),
        ("Code","#    #print('FakeMouse HangingOut gObj', frame.vars.gObj[0])"),
        ("Code","#    frame.vars.dbgCt[0] = 10"),
        ("Code","#frame.vars.dbgCt[0] -= 1"),
        ("Code","# Outside agent has to set PC += 1 to force FakeMouse to the Done case"),
        ("GoTo","HangingOut"),
        ("Label","Done"),
        ("Code","#print('FakeMouse done, remove gObj')"),
        ("Code","frame.vars.gObj[0].removeNode()"),
        ("Code","frame.status = Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",FakeMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('FakeMouse', RecordPlaybackLib.FakeMouse.codeDescr, RecordPlaybackLib.FakeMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.FakeMouse, stack)

    def run(frame):
        # print('Run 'FakeMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.FakeMouse_run_rt(frame)

  class HideMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  ()
    codeDescr =        (
        ("Code","#<your code here>"),
        ("Code","from panda3d.core import WindowProperties #"),
        ("Code","props = WindowProperties() #"),
        ("Code","props.setCursorHidden(True) #"),
        ("Code","base.win.requestProperties(props) #"))

    def _build(rowRef):
        # print("Build ",HideMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('HideMouse', RecordPlaybackLib.HideMouse.codeDescr, RecordPlaybackLib.HideMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.HideMouse, stack)

    def run(frame):
        # print('Run 'HideMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.HideMouse_run_rt(frame)

  class MouseDisplay:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("lblFrm",Wye.dType.OBJECT,None),
        ("camLblFrm",Wye.dType.OBJECT,None),
        ("dlgFrm",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("Code","dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog('Mouse Position', None, formatLst=['NO_OK']) #"),
        ("Code","frame.vars.dlgFrm[0] = dlgFrm "),
        ("Code","frame.vars.lblFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, 'Mouse [x,y]') #"),
        ("Code","frame.vars.camLblFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, 'Cam ') #"),
        ("Code","dlgFrm.verb.run(dlgFrm)"),
        ("Code","WyeCore.World.startActiveFrame(dlgFrm)"),
        ("Label","Wait1Frame"),
        ("Code","x = WyeCore.World.mouseHandler.pos[0] #"),
        ("Code","y = WyeCore.World.mouseHandler.pos[1] #"),
        ("Code","lbl = 'Mouse [%0.4f,%0.4f]' %(x,y)"),
        ("Code","#print('Mouse', lbl)"),
        ("Code","#print('frame', frame.vars.lblFrm[0].params.label[0])"),
        ("Code","try: #<your code here>"),
        ("Code","   frame.vars.lblFrm[0].verb.setLabel(frame.vars.lblFrm[0], lbl)"),
        ("Code","   frame.vars.dlgFrm[0].verb.redisplay(frame.vars.dlgFrm[0])"),
        ("Code","except Exception as e: #<your code here>"),
        ("Code","    #WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('AAAAH!', 'setLabel/redisplay fell over'+str(e))"),
        ("Code","    frame.status = Wye.status.SUCCESS #dialog went away, exit"),
        ("Code","    return #<your code here>"),
        ("Code","camHPR = base.camera.getHpr() #"),
        ("Code","h = camHPR[0] #"),
        ("Code","p = camHPR[1] #"),
        ("Code","r = camHPR[2] #"),
        ("Code","camPos = base.camera.getPos() #"),
        ("Code","x = camPos[0] #"),
        ("Code","y = camPos[1] #"),
        ("Code","z = camPos[2] #"),
        ("Code","frame.vars.camLblFrm[0].verb.setLabel(frame.vars.camLblFrm[0], ('Cam HPR %0.3f,%0.3f,%0.3f' %(h,p,r))+(' Pos %0.3f,%0.3f,%0.3f' %(x,y,z))) #"))

    def _build(rowRef):
        # print("Build ",MouseDisplay)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('MouseDisplay', RecordPlaybackLib.MouseDisplay.codeDescr, RecordPlaybackLib.MouseDisplay, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.MouseDisplay, stack)

    def run(frame):
        # print('Run 'MouseDisplay)
        RecordPlaybackLib.RecordPlaybackLib_rt.MouseDisplay_run_rt(frame)

  class MoveCameraToPosHpr:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("position",Wye.dType.FLOAT_LIST,1),
        ("Hpr",Wye.dType.FLOAT_LIST,1),)
    varDescr =  ()
    codeDescr =        (
        ("Code","base.camera.setPos(frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2]) #"),
        ("Code","base.camera.setHpr(frame.params.Hpr[0][0], frame.params.Hpr[0][1], frame.params.Hpr[0][2]) #"))

    def _build(rowRef):
        # print("Build ",MoveCameraToPosHpr)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('MoveCameraToPosHpr', RecordPlaybackLib.MoveCameraToPosHpr.codeDescr, RecordPlaybackLib.MoveCameraToPosHpr, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.MoveCameraToPosHpr, stack)

    def run(frame):
        # print('Run 'MoveCameraToPosHpr)
        RecordPlaybackLib.RecordPlaybackLib_rt.MoveCameraToPosHpr_run_rt(frame)

  class RecordManager:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("newVar",Wye.dType.ANY,None),)
    codeDescr =        (
        ("Code","pass #"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"),
        ("Code","#"))

    def _build(rowRef):
        # print("Build ",RecordManager)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('RecordManager', RecordPlaybackLib.RecordManager.codeDescr, RecordPlaybackLib.RecordManager, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.RecordManager, stack)

    def run(frame):
        # print('Run 'RecordManager)
        RecordPlaybackLib.RecordPlaybackLib_rt.RecordManager_run_rt(frame)

  class SendControlKey:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("key",Wye.dType.INTEGER,1),)
    varDescr =  ()
    codeDescr =        (
        ("Code","WyeCore.World.keyHandler.controlKeyFunc(frame.params.key[0]) #"),)

    def _build(rowRef):
        # print("Build ",SendControlKey)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('SendControlKey', RecordPlaybackLib.SendControlKey.codeDescr, RecordPlaybackLib.SendControlKey, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.SendControlKey, stack)

    def run(frame):
        # print('Run 'SendControlKey)
        RecordPlaybackLib.RecordPlaybackLib_rt.SendControlKey_run_rt(frame)

  class SendKey:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("key",Wye.dType.STRING,1),)
    varDescr =  ()
    codeDescr =        (
        ("Code","WyeCore.World.keyHandler.keyFunc(frame.params.key[0])"),)

    def _build(rowRef):
        # print("Build ",SendKey)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('SendKey', RecordPlaybackLib.SendKey.codeDescr, RecordPlaybackLib.SendKey, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.SendKey, stack)

    def run(frame):
        # print('Run 'SendKey)
        RecordPlaybackLib.RecordPlaybackLib_rt.SendKey_run_rt(frame)

  class SetFakeMousePos:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  (
        ("position",Wye.dType.FLOAT_LIST,1,"[0,0]"),)
    varDescr =  (
        ("fakeMouseFrm",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("Code","#print('SetFakeMousePos position', frame.params.position[0])"),
        ("Code","frame.vars.fakeMouseFrm[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("Code","if not frame.vars.fakeMouseFrm[0]:  # if FakeMouse not running, nevermind!"),
        ("Code","    WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('SetFakeMousePos Error', 'Did not find running FakeMouse', Wye.color.WARNING)"),
        ("Code","    return"),
        ("Code","else:"),
        ("Code","    if not frame.vars.fakeMouseFrm[0].vars.gObj[0]:"),
        ("Code","        #print('SetFakeMousePos error: FakeMouse found but gObj is None.  FakeMouse frame', frame.vars.fakeMouseFrm[0])"),
        ("Code","        WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('SetFakeMousePos Error', 'FakeMouse found but gObj is None. Frame'+str(frame.vars.fakeMouseFrm[0]), color=Wye.color.WARNING_COLOR)"),
        ("Code","        #print('SetFakeMousePos: Oh help.  fakeMouse gObj is null')"),
        ("Code","        return"),
        ("Code","    #print('setFakeMousePos: Found FakeMouse. frame', frame.vars.fakeMouseFrm[0],' gObj=', frame.vars.fakeMouseFrm[0].vars.gObj[0])"),
        ("Code","#Place plane close to camera across view, project mouse pos onto plane for 3d point, put fake mouse graphic at 3d point."),
        ("Code","from panda3d.core import NodePath, LPlanef, LPoint2f, Point3, LVecBase3f"),
        ("Code","point=NodePath('point')"),
        ("Code","point.reparentTo(render)"),
        ("Code","point.setPos(base.camera, 0,5,0)"),
        ("Code","pos=point.getPos(render)"),
        ("Code","fwd=render.getRelativeVector(base.camera,(0,-1,0))"),
        ("Code","point.removeNode()"),
        ("Code","objPlane=LPlanef(fwd, pos)"),
        ("Code","x = frame.params.position[0][0]"),
        ("Code","y = frame.params.position[0][1]"),
        ("Code","#Offset ptr graphic so point at mouse pos"),
        ("Code","mpos = LPoint2f(x-.02, y-.04)"),
        ("Code","wldPos=Point3(0,0,0)"),
        ("Code","newPos = Point3(0,0,0)"),
        ("Code","near=Point3()"),
        ("Code","far=Point3()"),
        ("Code","base.camLens.extrude(mpos, near, far)"),
        ("Code","objPlane.intersectsLine(newPos,render.getRelativePoint(base.camera, near),render.getRelativePoint(base.camera, far))"),
        ("Code","#print('setFakeMousePos mouse', frame.params.position[0][0],',',frame.params.position[0][1],' 3d pos', newPos)"),
        ("Code","fwd=base.camera.getHpr()"),
        ("Code","#print('setHpr on _pointer', frame.vars.fakeMouseFrm[0].vars.gObj[0]) #<your code here>"),
        ("Code","frame.vars.fakeMouseFrm[0].vars.gObj[0].setHpr(fwd[0], fwd[1], fwd[2])"),
        ("Code","#print('did setHpr on _pointer') #<your code here>"),
        ("Code","frame.vars.fakeMouseFrm[0].vars.gObj[0].setPos(newPos[0], newPos[1], newPos[2])"))

    def _build(rowRef):
        # print("Build ",SetFakeMousePos)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('SetFakeMousePos', RecordPlaybackLib.SetFakeMousePos.codeDescr, RecordPlaybackLib.SetFakeMousePos, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.SetFakeMousePos, stack)

    def run(frame):
        # print('Run 'SetFakeMousePos)
        RecordPlaybackLib.RecordPlaybackLib_rt.SetFakeMousePos_run_rt(frame)

  class ShowMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  ()
    codeDescr =        (
        ("Code","from panda3d.core import WindowProperties #"),
        ("Code","props = WindowProperties() #"),
        ("Code","props.setCursorHidden(0) #"),
        ("Code","base.win.requestProperties(props) #"))

    def _build(rowRef):
        # print("Build ",ShowMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('ShowMouse', RecordPlaybackLib.ShowMouse.codeDescr, RecordPlaybackLib.ShowMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.ShowMouse, stack)

    def run(frame):
        # print('Run 'ShowMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.ShowMouse_run_rt(frame)

  class StartFakeMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  ()
    codeDescr =        (
        ("Code","WyeCore.World.startActiveObject(WyeCore.libs.RecordPlaybackLib.FakeMouse)"),)

    def _build(rowRef):
        # print("Build ",StartFakeMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('StartFakeMouse', RecordPlaybackLib.StartFakeMouse.codeDescr, RecordPlaybackLib.StartFakeMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.StartFakeMouse, stack)

    def run(frame):
        # print('Run 'StartFakeMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.StartFakeMouse_run_rt(frame)

  class StopFakeMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("fakeMouseFrm",Wye.dType.ANY,None),)
    codeDescr =        (
        ("Code","frame.vars.fakeMouseFrm[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("Code","if not frame.vars.fakeMouseFrm[0]:  # if mouse not running, nevermind!"),
        ("Code"," return"),
        ("Code","frame.vars.fakeMouseFrm[0].PC += 1"))

    def _build(rowRef):
        # print("Build ",StopFakeMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('StopFakeMouse', RecordPlaybackLib.StopFakeMouse.codeDescr, RecordPlaybackLib.StopFakeMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.StopFakeMouse, stack)

    def run(frame):
        # print('Run 'StopFakeMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.StopFakeMouse_run_rt(frame)
