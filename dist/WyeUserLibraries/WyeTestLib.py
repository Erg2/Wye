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
    paramDescr =  ()
    varDescr =  (
        ("count",Wye.dType.INTEGER,0),
        ("testPtr",Wye.dType.OBJECT,None),
        ("testPtrFrm",Wye.dType.OBJECT,None),
        ("fakeMouse",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartTest",),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[(1.756807,-14.166591,0.048544)] #pos"),
          ("Expr","[(-0.505469,0.000000,0.000000)] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[10]")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[-0.937500,0.831068]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.937500,0.831068]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.937500,0.831068]]"),
          ("Expr","[[0.601562,0.485437]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.601562,0.485437]]"),
          ("Expr","[[0.378646,0.195146]]"),
          ("Expr","[60]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.378646,0.195146]]"),
          ("Expr","[[0.303646,0.120388]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.303646,0.120388]]"),
          ("Expr","[[0.258333,0.278641]]"),
          ("Expr","[50]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.258333,0.278641]]"),
          ("Expr","[[0.122396,0.622330]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.122396,0.622330]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.122396,0.622330]]"),
          ("Expr","[[-0.100521,-0.075728]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[3]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.100521,-0.075728]]"),
          ("Expr","[[0.311979,-0.098058]]"),
          ("Expr","[86]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.311979,-0.098058]]"),
          ("Expr","[[0.360417,-0.145631]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.360417,-0.145631]]"),
          ("Expr","[[0.366146,0.500000]]"),
          ("Expr","[70]")),
        ("WyeLib.noop",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.366146,0.500000]]"),
          ("Expr","[[-0.950000,-0.832039]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeLib.noop",),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Playback Complete', 'Finished TestDrag')"),
        ("Code","frame.status=Wye.status.SUCCESS"))

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
    paramDescr =  ()
    varDescr =  (
        ("count",Wye.dType.INTEGER,0),
        ("testPtr",Wye.dType.OBJECT,None),
        ("testPtrFrm",Wye.dType.OBJECT,None),
        ("fakeMouse",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartTest",),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[(8.520441,-27.843611,-0.455459)] #pos"),
          ("Expr","[(14.738599,0.000000,0.000000)] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[10]")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[-0.113542,-0.674757]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.113542,-0.674757]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.113542,-0.674757]]"),
          ("Expr","[[-0.257812,-0.543689]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.257812,-0.543689]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.257812,-0.543689]]"),
          ("Expr","[[-0.335417,-0.166019]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.335417,-0.165049]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.335417,-0.165049]]"),
          ("Expr","[[-0.188021,0.065049]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.188021,0.065049]]"),
          ("Expr","[[-0.187500,0.066019]]"),
          ("Expr","[9]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.187500,0.066019]]"),
          ("Expr","[[0.010417,0.060194]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.010417,0.060194]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.010417,0.060194]]"),
          ("Expr","[[0.124479,-0.100971]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.124479,-0.100971]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.124479,-0.100971]]"),
          ("Expr","[[0.122396,-0.376699]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.122396,-0.376699]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.122396,-0.376699]]"),
          ("Expr","[[0.043229,-0.585437]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.043229,-0.585437]]"),
          ("Expr","[[0.042187,-0.585437]]"),
          ("Expr","[6]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[0.042187,-0.585437]]"),
          ("Expr","[[-0.114583,-0.626214]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.114583,-0.626214]]")),
        ("WyeLib.noop",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.114583,-0.626214]]"),
          ("Expr","[[-0.955729,-0.830097]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeLib.noop",),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Playback Complete', 'Finished TestFakeMouse')"),
        ("Code","frame.status=Wye.status.SUCCESS"))

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
          ("Expr","[120] #")),
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
        ("WyeLib.noop",))

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
    paramDescr =  ()
    varDescr =  (
        ("count",Wye.dType.INTEGER,0),
        ("testPtr",Wye.dType.OBJECT,None),
        ("testPtrFrm",Wye.dType.OBJECT,None),
        ("fakeMouse",Wye.dType.OBJECT,None),)
    codeDescr =        (
        ("WyeCore.libs.RecordPlaybackLib.StartTest",),
        ("WyeCore.libs.RecordPlaybackLib.MoveCameraToPosHpr",
          ("Expr","[(0.000000,-10.000000,0.000000)] #pos"),
          ("Expr","[(-0.000521,0.000000,0.000000)] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[10]")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[-0.215104,-0.381553]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[True]"),
          ("Expr","[True]"),
          ("Expr","[[-0.215104,-0.381553]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.215104,-0.381553]]"),
          ("Expr","[[0.355729,0.016505]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.355729,0.016505]]"),
          ("Expr","[[-0.066146,-0.600000]]"),
          ("Expr","[81]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.066146,-0.600000]]"),
          ("Expr","[[-0.046354,-0.289320]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.046354,-0.289320]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.046354,-0.289320]]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.046354,-0.290291]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.046354,-0.290291]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.046354,-0.290291]]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.046354,-0.290291]]"),
          ("Expr","[[-0.028646,0.141748]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.028646,0.141748]]")),
        ("WyeLib.noop",
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[0]"),
          ("Expr","[[-0.028646,0.141748]]"),
          ("Expr","[[-0.952083,-0.832039]]"),
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeLib.noop",),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Playback Complete', 'Finished TestWyeMainMenu')"),
        ("Code","frame.status=Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",TestWyeMainMenu)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestWyeMainMenu', WyeTestLib.TestWyeMainMenu.codeDescr, WyeTestLib.TestWyeMainMenu, rowIxRef)

    def start(stack):
        return Wye.codeFrame(WyeTestLib.TestWyeMainMenu, stack)

    def run(frame):
        # print('Run 'TestWyeMainMenu)
        WyeTestLib.WyeTestLib_rt.TestWyeMainMenu_run_rt(frame)
