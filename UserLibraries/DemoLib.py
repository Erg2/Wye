from Wye import Wye
from WyeCore import WyeCore
class DemoLib:
  def _build():
    WyeCore.Utils.buildLib(DemoLib)
  canSave = True  # all verbs can be saved with the library
  class DemoLib_rt:
   pass #1

  class NewVerb:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        (
        ("newParam","A",1),)
    varDescr =        (
        ("newVar","A",None),)
    codeDescr =        (
        ("WyeLib.noop",
          ("Code","0")),)

    def _build(rowRef):
        # print("Build ",NewVerb)

        rowIxRef = [0]
        return WyeCore.Utils.buildCodeText('NewVerb', DemoLib.NewVerb.codeDescr, DemoLib.NewVerb, rowIxRef)

    def start(stack):
        return Wye.codeFrame(DemoLib.NewVerb, stack)

    def run(frame):
        # print('Run 'NewVerb)
        DemoLib.DemoLib_rt.NewVerb_run_rt(frame)
