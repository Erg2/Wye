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
        ("position","FL",1))
    varDescr =        ()
    codeDescr =        (
        ("Code","WyeCore.World.mouseHandler.mouseMove(frame.params.position[0][0], frame.params.position[0][1])"),)

    def _build(rowRef):
        # print("Build ",ClickMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('ClickMouse', RecordPlaybackLib.ClickMouse.codeDescr, RecordPlaybackLib.ClickMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(RecordPlaybackLib.ClickMouse, stack)

    def run(frame):
        # print('Run 'ClickMouse)
        RecordPlaybackLib.RecordPlaybackLib_rt.ClickMouse_run_rt(frame)

  class DoMouseMove:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        (
        ("MBtn","I",1),
        ("startPos","FL",1),
        ("endPos","FL",1),
        ("nFrames","I",1))
    varDescr =        (
        ("frameNum","I",0),)
    codeDescr =        (
        ("Code","dx = int((frame.params.endPos[0][0] - frame.params.startPos[0][0]) / frame.params.nFrames[0])#"),
        ("Code","dy = int((frame.params.endPos[0][1] - frame.params.startPos[0][1]) / frame.params.nFrames[0])#"),
        ("Code","x = frame.params.startPos[0][0] + dx #"),
        ("Code","y = frame.params.startPos[0][1] + dy #"),
        ("Code","WyeCore.World.mouseHandler.mouseMove(x, y) #"))

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

  class MouseDisplay:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("lblFrm","O",None),
        ("dlgFrm","O",None))
    codeDescr =        (
        ("Code","dlgFrm = WyeCore.libs.WyeUIUtilsLib.doDialog('Mouse Position', None) #"),
        ("Code","frame.vars.dlgFrm[0] = dlgFrm "),
        ("Code","frame.vars.lblFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, 'Mouse [x,y]') #"),
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
        ("Code","except: #<your code here>"),
        ("Code","    frame.status = Wye.status.SUCCESS #dialog went away, exit"))

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
