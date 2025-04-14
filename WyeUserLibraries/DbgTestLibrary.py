from Wye import Wye
from WyeCore import WyeCore
class DbgTestLibrary:
  def _build():
    WyeCore.Utils.buildLib(DbgTestLibrary)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class DbgTestLibrary_rt:
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
          ("Expr","[[-0.144792,-0.631068]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeCore.libs.RecordPlaybackLib.ClickMouse",
          ("Expr","[1]"),
          ("Expr","[False]"),
          ("Expr","[False]"),
          ("Expr","[True]"),
          ("Expr","[[-0.144792,-0.631068]]")),
        ("WyeCore.libs.RecordPlaybackLib.Delay",
          ("Expr","[30]")),
        ("WyeLib.noop",),
        ("WyeCore.libs.RecordPlaybackLib.FinishTest",),
        ("Code","WyeCore.libs.WyeUIUtilsLib.doPopUpDialog('Playback Complete', 'Finished TestVerb')"),
        ("Code","frame.status=Wye.status.SUCCESS"))

    def _build(rowRef):
        # print("Build ",TestVerb)
        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('TestVerb', DbgTestLibrary.TestVerb.codeDescr, DbgTestLibrary.TestVerb, rowIxRef)

    def start(stack):
        return Wye.codeFrame(DbgTestLibrary.TestVerb, stack)

    def run(frame):
        # print('Run 'TestVerb)
        DbgTestLibrary.DbgTestLibrary_rt.TestVerb_run_rt(frame)
