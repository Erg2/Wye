from Wye import Wye
from WyeCore import WyeCore
class TestLibrary:
  def _build():
    WyeCore.Utils.buildLib(TestLibrary)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class TestLibrary_rt:
   pass #1

  class TestVerb:
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
          ("Expr","[(0.000000,0.000000,0.000000)] # HPR")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[10]")),
        ("WyeCore.libs.RecordPlaybackLib.SetFakeMousePos",
          ("Expr","[[0.026042,-0.449515]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[True]"),
          ("Expr","[True]"),
          ("Expr","[[0.026042,-0.449515]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.131250,-0.410680]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.131250,-0.410680]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.131250,-0.410680]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.131250,-0.410680]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[0.207813,-0.380583]]"),
          ("Expr","[[-0.086979,0.008738]]"),
          ("Expr","[85]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.281771,-0.345631]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.DoMouseMove",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[[-0.163021,-0.322330]]"),
          ("Expr","[[0.386458,-0.325243]]"),
          ("Expr","[90]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeLib.noop",),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Code","frame.status=Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",TestVerb)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestVerb', TestLibrary.TestVerb.codeDescr, TestLibrary.TestVerb, rowIxRef)

    def start(stack):
        return Wye.codeFrame(TestLibrary.TestVerb, stack)

    def run(frame):
        # print('Run 'TestVerb)
        TestLibrary.TestLibrary_rt.TestVerb_run_rt(frame)
