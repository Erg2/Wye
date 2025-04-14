from Wye import Wye
from WyeCore import WyeCore
class WyeTestLib:
  def _build():
    WyeCore.Utils.buildLib(WyeTestLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class WyeTestLib_rt:
   pass #1

  class TestDrag:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("newVar",Wye.dType.ANY,None),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartTest",),
        ("Label","OpenWyeMainDialog"),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[[0,0]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Label","DoMouseMove"),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[[0,0]] # <put parameter here>"),
          ("Expr","[[0,.5]] # <put parameter here>"),
          ("Expr","[60] # <put parameter here>")),
        ("Label","DoFinishTest"),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[.1421,.5036]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[[.1521,.5036]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",TestDrag)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestDrag', WyeTestLib.TestDrag.codeDescr, WyeTestLib.TestDrag, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestDrag, stack)

    def run(frame):
        # print('Run 'TestDrag)
        WyeTestLib.WyeTestLib_rt.TestDrag_run_rt(frame)

  class TestFakeMouse:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("ptrFrm",Wye.dType.OBJECT,None),
        ("count",Wye.dType.INTEGER,0),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartFakeMouse",),
        ("Code","#<your code here>"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Start mouse test', position=[0,0,-.5])"),
        ("Label","Wait1Frame"),
        ("Label","Wait2Frame"),
        ("Code","frame.vars.ptrFrm[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] #")),
        ("Label","Loop"),
        ("Code","frame.vars.count[0] += 1"),
        ("Code","import math"),
        ("Code","x = math.sin(frame.vars.count[0] * .0174)/2"),
        ("Code","y = math.cos(frame.vars.count[0] * .0174)/2"),
        ("Code","#frame.vars.ptrFrm[0].vars.gObj[0].setPos(x,0,y)"),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[x,y]]")),
        ("IfGoTo","frame.vars.count[0] < 360","Loop"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Done mouse test',position=[x,0,y])"),
        ("Code","#frame.vars.ptrFrm[0].status = Wye.status.SUCCESS #shut down pointer object"),
        ("WyeCore.libs.RecordPlaybackLib.StopFakeMouse",),
        ("Code","frame.status = Wye.status.SUCCESS "))

    def _build(rowRef):
        # print("Build ",TestFakeMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestFakeMouse', WyeTestLib.TestFakeMouse.codeDescr, WyeTestLib.TestFakeMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestFakeMouse, stack)

    def run(frame):
        # print('Run 'TestFakeMouse)
        WyeTestLib.WyeTestLib_rt.TestFakeMouse_run_rt(frame)

  class TestHideMouse:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("newVar",Wye.dType.ANY,None),)
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
        # print("Build ",TestHideMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestHideMouse', WyeTestLib.TestHideMouse.codeDescr, WyeTestLib.TestHideMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestHideMouse, stack)

    def run(frame):
        # print('Run 'TestHideMouse)
        WyeTestLib.WyeTestLib_rt.TestHideMouse_run_rt(frame)

  class TestKeys:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  ()
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartTest",),
        ("WyeCore.libs.RecordPlaybackLib.SendControlKey",
          ("Expr","[Wye.ctlKeys.CTL_R] # Open record window")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[[-.8771, -.6806]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SendKey",
          ("Expr","['a'] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SendKey",
          ("Expr","['b'] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SendKey",
          ("Expr","['c'] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[-.9563, -.8301]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[[-.9563, -.8301]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("WyeLib.noop"))

    def _build(rowRef):
        # print("Build ",TestKeys)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestKeys', WyeTestLib.TestKeys.codeDescr, WyeTestLib.TestKeys, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestKeys, stack)

    def run(frame):
        # print('Run 'TestKeys)
        WyeTestLib.WyeTestLib_rt.TestKeys_run_rt(frame)

  class TestWyeMainMenu:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =  ()
    varDescr =  (
        ("count",Wye.dType.INTEGER,0),
        ("testPtr",Wye.dType.OBJECT,None),
        ("testPtrFrm",Wye.dType.OBJECT,None),
        ("fakeMouse",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.HideMouse",),
        ("WyeCore.libs.RecordPlaybackLib.StartFakeMouse",),
        ("Label","Delay1Cycle"),
        ("Label","Start"),
        ("Code","frame.vars.fakeMouse[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("Code","if not frame.vars.fakeMouse[0]:"),
        ("Code","  WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('TestWyeMainMenu Error', 'FakeMouse did not start',Wye.color.WARNING_COLOR)"),
        ("Code","  return #<your code here>"),
        ("Code","if not frame.vars.fakeMouse[0].vars.gObj[0]:"),
        ("Code","    print('TestWyeMainMenu: FakeMouse gObj not found')"),
        ("Code","    frame.status=Wye.status.SUCCESS"),
        ("Code","    return"),
        ("Code","Wye.UITest = True #disable normal mouse handling"),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[[0, -20, 0]] #pos"),
          ("Expr","[[0,0,0]] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop2', 'after delay', position=[0,0,-1])"),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Code","[(0,0),]#<your code here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[0.1349,-0.4146]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1349,-0.4146),] #Show Test Fish")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[0.1510,0.0117]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1510,0.0117),] #Close Main Menu")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Label","Done"),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"),
        ("WyeCore.libs.RecordPlaybackLib.ShowMouse",
          ("Expr","[1] # <put parameter here>")),
        ("Code","Wye.UITest = False #enable normal mouse handling"),
        ("WyeCore.libs.RecordPlaybackLib.StopFakeMouse",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Test Complete', 'Finished Test', position=[0,0,1])"))

    def _build(rowRef):
        # print("Build ",TestWyeMainMenu)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestWyeMainMenu', WyeTestLib.TestWyeMainMenu.codeDescr, WyeTestLib.TestWyeMainMenu, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestWyeMainMenu, stack)

    def run(frame):
        # print('Run 'TestWyeMainMenu)
        WyeTestLib.WyeTestLib_rt.TestWyeMainMenu_run_rt(frame)
