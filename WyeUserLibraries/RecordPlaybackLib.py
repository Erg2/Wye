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
    paramDescr =        (
        ("MBtn","I",1),
        ("shift","B",1),
        ("ctrl","B",1),
        ("alt","B",1),
        ("position","FL",1))
    varDescr =        ()
    codeDescr =        (
        ("Code","#<your code here>"),
        ("Code","#Clear mouse"),
        ("Code","#Clear mouse"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(0,0, 0, 0, 0, 0, 0, 0)"),
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
    paramDescr =        (
        ("nFrames","I",1),)
    varDescr =        (
        ("frameCt","I",0),)
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
    paramDescr =        (
        ("MBtn","I",1),
        ("shift","B",1),
        ("ctrl","B",1),
        ("alt","B",1),
        ("startPos","FL",1),
        ("endPos","FL",1),
        ("nFrames","I",1))
    varDescr =        (
        ("frameNum","I",0),)
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
    paramDescr =        (
        ("dir","I",1),)
    varDescr =        ()
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
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("cleanUpObjs","OL","None"))
    codeDescr =        (
        ("Code","frame.vars.cleanUpObjs[0] = []"),
        ("Code","frame.vars.gObj[0] = WyeCore.libs.Wye3dObjsLib._pointer(size=[.1,.05,.1], pos=[0,0,0])"),
        ("Code","frame.vars.gObj[0].setTag('wyeTag'+str(WyeCore.Utils.getId()))"),
        ("Code","frame.vars.cleanUpObjs[0].append(frame.vars.gObj[0]) "),
        ("Label","Done"))

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
    paramDescr =        ()
    varDescr =        ()
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
    paramDescr =        ()
    varDescr =        (
        ("lblFrm","O",None),
        ("camLblFrm","O",None),
        ("dlgFrm","O",None))
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
    paramDescr =        (
        ("position","FL",1),
        ("Hpr","FL",1))
    varDescr =        ()
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

  class RecordDialog:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("newVar","A",None),)
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
        # print("Build ",RecordDialog)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('RecordDialog', RecordPlaybackLib.RecordDialog.codeDescr, RecordPlaybackLib.RecordDialog, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.RecordDialog, stack)

    def run(frame):
        # print('Run 'RecordDialog)
        RecordPlaybackLib.RecordPlaybackLib_rt.RecordDialog_run_rt(frame)

  class SendControlKey:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        (
        ("key","I",1),)
    varDescr =        ()
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
    paramDescr =        (
        ("key","S",1),)
    varDescr =        ()
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

  class ShowMouse:
    mode = Wye.mode.SINGLE_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        ()
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

  class Test1:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("count","I",0),
        ("testPtr","O",None),
        ("testPtrFrm","O",None))
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.HideMouse",),
        ("Label","Start"),
        ("Code","Wye.UITest = True #disable normal mouse handling"),
        ("Code","#print('now mouse move should not call moveMouse')"),
        ("Code","frame.vars.testPtrFrm[0] = WyeCore.World.startActiveObject(WyeCore.libs.RecordPlaybackLib.FakeMouse)"),
        ("Var=","frame.vars.testPtr[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[[0, -20, 0]] #pos"),
          ("Expr","[[0,0,0]] # HPR")),
        ("Code","#WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'before delay', position=[0,0,1])"),
        ("Code","frame.vars.testPtrFrm[0].vars.gObj[0].setPos(-1,0,0)"),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop2', 'after delay', position=[0,0,-1])"),
        ("Code","#print('>>>>>>>>> do click M1, ctrl, alt for WyeMainMenu') "),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[(0,0,0)] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('>>>>>>>>>> do click m1 at .1349, -.4146 for Show Test Fish') "),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1349,-0.4146)] #Show Test Fish")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('>>>>>>> do m1 at .1510, .0117 for Wye Main Menu OK') "),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1510,0.0117)] #Close Main Menu")),
        ("Code","#<your code here>"),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"),
        ("WyeCore.libs.RecordPlaybackLib.ShowMouse",
          ("Expr","[1] # <put parameter here>")),
        ("Code","Wye.UITest = False #enable normal mouse handling"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Test Complete', 'Finished Test', position=[0,0,1])"))

    def _build(rowRef):
        # print("Build ",Test1)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Test1', RecordPlaybackLib.Test1.codeDescr, RecordPlaybackLib.Test1, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.Test1, stack)

    def run(frame):
        # print('Run 'Test1)
        RecordPlaybackLib.RecordPlaybackLib_rt.Test1_run_rt(frame)

  class Test2:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("newVar","A",None),)
    codeDescr =        (
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Hide Mouse', position=[0,0,-.5])"),
        ("WyeCore.libs.RecordPlaybackLib.HideMouse",),
        ("Label","Wait1Frame"),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[90] #")),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Show Mouse',position=[0,0,.5])"),
        ("WyeCore.libs.RecordPlaybackLib.ShowMouse",),
        ("Code","frame.status = Wye.status.SUCCESS "))

    def _build(rowRef):
        # print("Build ",Test2)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Test2', RecordPlaybackLib.Test2.codeDescr, RecordPlaybackLib.Test2, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.Test2, stack)

    def run(frame):
        # print('Run 'Test2)
        RecordPlaybackLib.RecordPlaybackLib_rt.Test2_run_rt(frame)

  class TestFakeMouse:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("ptrFrm","O",None),
        ("count","I",0))
    codeDescr =        (
        ("Code","#<your code here>"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Before Mouse', position=[0,0,-.5])"),
        ("Code","#<your code here>"),
        ("Code","frame.vars.ptrFrm[0] = WyeCore.World.startActiveObject(WyeCore.libs.RecordPlaybackLib.FakeMouse)"),
        ("Label","Wait1Frame"),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[90] #")),
        ("Label","Loop"),
        ("Code","frame.vars.count[0] += 1"),
        ("Code","import math"),
        ("Code","x = math.sin(frame.vars.count[0] * .0174)"),
        ("Code","y = math.cos(frame.vars.count[0] * .0174)"),
        ("IfGoTo","frame.vars.count[0] < 360","Loop"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'After Mouse',position=[x,0,y])"),
        ("Code","frame.vars.ptrFrm[0].status = Wye.status.SUCCESS #shut down pointer object"),
        ("Code","frame.status = Wye.status.SUCCESS "))

    def _build(rowRef):
        # print("Build ",TestFakeMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestFakeMouse', RecordPlaybackLib.TestFakeMouse.codeDescr, RecordPlaybackLib.TestFakeMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.TestFakeMouse, stack)

    def run(frame):
        # print('Run 'TestFakeMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.TestFakeMouse_run_rt(frame)
