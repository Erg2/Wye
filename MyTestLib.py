from Wye import Wye
from WyeCore import WyeCore
class MyTestLib:
    def build():
        WyeCore.Utils.buildLib(MyTestLib)
    class MyTestLib_rt:
        pass

    class testObj2:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        cType = Wye.cType.VERB
        parTermType = Wye.parTermType.FIRST_FAIL
        paramDescr =        (
            ("ret","I",1),)
        varDescr =        (
            ("gObj","O",None),
            ("objTag","S","objTag"),
            ("sound","O",None),
            ("position","FL",
              (-1.0,2.0,2.5)))
        codeDescr =        (
            ("WyeCore.libs.WyeLib.loadObject",
              (None,"[frame]"),
              (None,"frame.vars.gObj"),
              (None,"['flyer_01.glb']"),
              (None,"frame.vars.position"),
              (None,"[[0, 90, 0]]"),
              (None,"[[1,1,1]]"),
              (None,"frame.vars.objTag"),
              ("Code","[[1,1,0,1]]")),
            (None,"frame.vars.sound[0] = Wye.audio3d.loadSfx('WyePew.wav')"),
            ("Label","Repeat"),
            ("WyeCore.libs.TestLib.clickWiggle",
              (None,"frame.vars.gObj"),
              (None,"frame.vars.objTag"),
              (None,"[1]")),
            ("GoTo","Repeat"))
    
        def build():
            # print("Build ",testObj2)
            return WyeCore.Utils.buildCodeText('testObj2', MyTestLib.testObj2.codeDescr)
    
        def start(stack):
            # print('testObj2 object start')
                        return Wye.codeFrame(MyTestLib.testObj2, stack)
    
        def run(frame):
            # print('Run 'testObj2)
            try:
              MyTestLib.MyTestLib_rt.testObj2_run_rt(frame)
            except Exception as e:
              if not hasattr(MyTestLib.MyTestLib_rt.testObj2_run_rt, 'errOnce'):
                print('MyTestLib.MyTestLib_rt.testObj2_run_rt failed\n', str(e))
                import traceback
                traceback.print_exception(e)
                setattr(MyTestLib.MyTestLib_rt.testObj2_run_rt, 'errOnce', True)
    
    