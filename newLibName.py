from Wye import Wye
from WyeCore import WyeCore
class newLibName:
  def build():
    WyeCore.Utils.buildLib(newLibName)
  canSave = True  # all verbs can be saved with the library
  class newLibName_rt:
   pass #1

  class MyAngleFish:
    mode = Wye.mode.MULTI_CYCLE
    autoStart = True
    dataType = Wye.dType.NONE
    cType = Wye.cType.VERB
    parTermType = Wye.parTermType.FIRST_FAIL
    paramDescr =        ()
    varDescr =        (
        ("gObj","O",None),
        ("objTag","S","objTag"),
        ("sound","O",None),
        ("position","FL",
          (3.0,2.0,2.5)),
        ("cleanUpObjs","OL",None))
    codeDescr =        (
        ("Var=","frame.vars.cleanUpObjs[0] = []"),
        ("WyeCore.libs.WyeLib.loadObject",
          (None,"[frame]"),
          (None,"frame.vars.gObj"),
          (None,"['flyer_01.glb']"),
          (None,"frame.vars.position"),
          (None,"[[0, 90, 0]]"),
          (None,"[[1,1,1]]"),
          (None,"frame.vars.objTag"),
          (None,"[[0,1,0,1]]"),
          ("Var","frame.vars.cleanUpObjs")),
        (None,"frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
        ("Label","Repeat"),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[0]")),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[1]")),
        ("WyeCore.libs.TestLib.clickWiggle",
          (None,"frame.vars.gObj"),
          (None,"frame.vars.objTag"),
          (None,"[2]")),
        ("GoTo","Repeat"))

    def build():
        # print("Build ",MyAngleFish)
        return WyeCore.Utils.buildCodeText('MyAngleFish', newLibName.MyAngleFish.codeDescr, newLibName.MyAngleFish)

    def start(stack):
        return Wye.codeFrame(newLibName.MyAngleFish, stack)

    def run(frame):
        # print('Run 'MyAngleFish)
        try:
          newLibName.newLibName_rt.MyAngleFish_run_rt(frame)
        except Exception as e:
          if not hasattr(frame, 'errOnce'):
            print('newLibName.newLibName_rt.MyAngleFish_run_rt failed\n', str(e))
            import traceback
            traceback.print_exception(e)
            frame.errOnce = True

