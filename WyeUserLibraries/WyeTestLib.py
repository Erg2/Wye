from Wye import Wye
from WyeCore import WyeCore
class WyeTestLib:
  def _build():
    WyeCore.Utils.buildLib(WyeTestLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class WyeTestLib_rt:
   pass #1

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
        ("WyeCore.libs.RecordPlaybackLib.StartFakeMouse",),
        ("Code","#<your code here>"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'Before Mouse', position=[0,0,-.5])"),
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
        ("Code","#print('TestFakeMouse move', x, ',', y)"),
        ("IfGoTo","frame.vars.count[0] < 360","Loop"),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop1', 'After Mouse',position=[x,0,y])"),
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
        # print("Build ",TestHideMouse)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestHideMouse', WyeTestLib.TestHideMouse.codeDescr, WyeTestLib.TestHideMouse, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestHideMouse, stack)

    def run(frame):
        # print('Run 'TestHideMouse)
        WyeTestLib.WyeTestLib_rt.TestHideMouse_run_rt(frame)

  class Test_WyeMainMenu:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = False
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("count","I",0),
        ("testPtr","O",None),
        ("testPtrFrm","O",None),
        ("fakeMouse","O",None))
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.HideMouse",),
        ("WyeCore.libs.RecordPlaybackLib.StartFakeMouse",),
        ("Label","Delay1Cycle"),
        ("Label","Start"),
        ("Code","frame.vars.fakeMouse[0] = WyeCore.World.findActiveObj('FakeMouse')"),
        ("Code","if not frame.vars.fakeMouse[0]:"),
        ("Code","  WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Test_WyeMainMenu Error', 'FakeMouse did not start',Wye.color.WARNING)"),
        ("Code","  return #<your code here>"),
        ("Code","if not frame.vars.fakeMouse[0].vars.gObj[0]:"),
        ("Code","    print('Test_WyeMainMenu: FakeMouse gObj not found')"),
        ("Code","    frame.status=Wye.status.SUCCESS"),
        ("Code","    return"),
        ("Code","Wye.UITest = True #disable normal mouse handling"),
        ("Code","#print('now mouse move should not call moveMouse')"),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[[0, -20, 0]] #pos"),
          ("Expr","[[0,0,0]] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Pop2', 'after delay', position=[0,0,-1])"),
        ("Code","#print('Test_WyeMainMenu ClickMouse 0,0 with Ctrl,Alt')"),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[1] # <put parameter here>"),
          ("Code","[(0,0),]#<your code here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('Test_WyeMainMenu SetFakeMousePos 0.1349, -0.4146')"),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[0.1349,-0.4146]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('Test_WyeMainMenu ClickMouse 0.1349, -0.4146')"),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1349,-0.4146),] #Show Test Fish")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('Test_WyeMainMenu SetFakeMousePos 0.1510, 0.0117')"),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[0.1510,0.0117]] # <put parameter here>")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Code","#print('Test_WyeMainMenu ClickMouse 0.1510, 0.0117')"),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[0] # <put parameter here>"),
          ("Expr","[(0.1510,0.0117),] #Close Main Menu")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[60] # <put parameter here>")),
        ("Label","Done"),
        ("Code","#print('Test_WyeMainMenu: Done') #<your code here>"),
        ("Code","frame.status = Wye.status.SUCCESS #<your code here>"),
        ("WyeCore.libs.RecordPlaybackLib.ShowMouse",
          ("Expr","[1] # <put parameter here>")),
        ("Code","Wye.UITest = False #enable normal mouse handling"),
        ("WyeCore.libs.RecordPlaybackLib.StopFakeMouse",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Test Complete', 'Finished Test', position=[0,0,1])"))

    def _build(rowRef):
        # print("Build ",Test_WyeMainMenu)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('Test_WyeMainMenu', WyeTestLib.Test_WyeMainMenu.codeDescr, WyeTestLib.Test_WyeMainMenu, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.Test_WyeMainMenu, stack)

    def run(frame):
        # print('Run 'Test_WyeMainMenu)
        WyeTestLib.WyeTestLib_rt.Test_WyeMainMenu_run_rt(frame)
