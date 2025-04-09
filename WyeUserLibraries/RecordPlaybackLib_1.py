from Wye import Wye
from WyeCore import WyeCore
class RecordPlaybackLib_1:
  def _build():
    WyeCore.Utils.buildLib(RecordPlaybackLib_1)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class RecordPlaybackLib_1_rt:
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
        ("Code","x = frame.params.position[0][0] #"),
        ("Code","y = frame.params.position[0][1] #"),
        ("Code","mb1 = True if frame.params.MBtn == 1 else False #"),
        ("Code","mb2 = True if frame.params.MBtn == 2 else False #"),
        ("Code","mb3 = True if frame.params.MBtn == 3 else False #"),
        ("Code","shift = frame.params.shift[0] #"),
        ("Code","alt = frame.params.alt[0] #"),
        ("Code","ctl = frame.params.ctrl[0] #"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(x,y, mb1, mb2, mb3, shift, ctl, alt)"))

    def _build(rowRef):
        # print("Build ",ClickMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('ClickMouse', RecordPlaybackLib_1.ClickMouse.codeDescr, RecordPlaybackLib_1.ClickMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.ClickMouse, stack)

    def run(frame):
        # print('Run 'ClickMouse)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.ClickMouse_run_rt(frame)

  class Delay:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        (
        ("nFrames","I",1),)
    varDescr =        (
        ("frameCt","I",0),)
    codeDescr =        (
        ("IfGoTo","frame.vars.frameCt[0] >= frame.params.nFrames[0]","Done"),
        ("Var=","frame.vars.frameCt[0] += 1"),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"))

    def _build(rowRef):
        # print("Build ",Delay)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Delay', RecordPlaybackLib_1.Delay.codeDescr, RecordPlaybackLib_1.Delay, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.Delay, stack)

    def run(frame):
        # print('Run 'Delay)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.Delay_run_rt(frame)

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
        ("Code","WyeCore.World.mouseHandler.mouseMove(x,y, mb1, mb2, mb3, shift, ctl, alt)"),
        ("Var=","frame.vars.frameNum[0] += 1"),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",DoMouseMove)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('DoMouseMove', RecordPlaybackLib_1.DoMouseMove.codeDescr, RecordPlaybackLib_1.DoMouseMove, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.DoMouseMove, stack)

    def run(frame):
        # print('Run 'DoMouseMove)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.DoMouseMove_run_rt(frame)

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
        return WyeCore.Utils.buildCodeText('DoMouseWheel', RecordPlaybackLib_1.DoMouseWheel.codeDescr, RecordPlaybackLib_1.DoMouseWheel, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.DoMouseWheel, stack)

    def run(frame):
        # print('Run 'DoMouseWheel)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.DoMouseWheel_run_rt(frame)

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
        ("Code","frame.vars.camLblFrm[0].verb.setLabel(frame.vars.camLblFrm[0], ('Cam HPR %0.3f,%0.3f,%0.3f' %(h,p,r))+(' pos %0.3f,%0.3f,%0.3f' %(x,y,z))) #"))

    def _build(rowRef):
        # print("Build ",MouseDisplay)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('MouseDisplay', RecordPlaybackLib_1.MouseDisplay.codeDescr, RecordPlaybackLib_1.MouseDisplay, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.MouseDisplay, stack)

    def run(frame):
        # print('Run 'MouseDisplay)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.MouseDisplay_run_rt(frame)

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
        return WyeCore.Utils.buildCodeText('MoveCameraToPosHpr', RecordPlaybackLib_1.MoveCameraToPosHpr.codeDescr, RecordPlaybackLib_1.MoveCameraToPosHpr, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.MoveCameraToPosHpr, stack)

    def run(frame):
        # print('Run 'MoveCameraToPosHpr)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.MoveCameraToPosHpr_run_rt(frame)

  class RecordDialog:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
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
        return WyeCore.Utils.buildCodeText('RecordDialog', RecordPlaybackLib_1.RecordDialog.codeDescr, RecordPlaybackLib_1.RecordDialog, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.RecordDialog, stack)

    def run(frame):
        # print('Run 'RecordDialog)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.RecordDialog_run_rt(frame)

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
        return WyeCore.Utils.buildCodeText('SendControlKey', RecordPlaybackLib_1.SendControlKey.codeDescr, RecordPlaybackLib_1.SendControlKey, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.SendControlKey, stack)

    def run(frame):
        # print('Run 'SendControlKey)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.SendControlKey_run_rt(frame)

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
        return WyeCore.Utils.buildCodeText('SendKey', RecordPlaybackLib_1.SendKey.codeDescr, RecordPlaybackLib_1.SendKey, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.SendKey, stack)

    def run(frame):
        # print('Run 'SendKey)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.SendKey_run_rt(frame)

  class Test1:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("count","I",0),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[[0, 0, 0]] #pos"),
          ("Expr","[[0,0,0]] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[[0, -10, 0]] #pos"),
          ("Expr","[[0,0,0]] # HPR")),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"))

    def _build(rowRef):
        # print("Build ",Test1)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Test1', RecordPlaybackLib_1.Test1.codeDescr, RecordPlaybackLib_1.Test1, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib_1.Test1, stack)

    def run(frame):
        # print('Run 'Test1)
        RecordPlaybackLib_1.RecordPlaybackLib_1_rt.Test1_run_rt(frame)
