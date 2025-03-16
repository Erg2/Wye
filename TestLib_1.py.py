from Wye import Wye
from WyeCore import WyeCore
class TestLib:
    def build():
        WyeCore.Utils.buildLib(TestLib)
    canSave = True  # all verbs can be saved with the library
    class TestLib_rt:
        pass

    class PlaceHolder:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = False
        dataType = Wye.dType.NONE
        paramDescr =        ()
        varDescr =        (
            ("myVar","I",0),)
        codeDescr =        (
            ("Code","print('PlaceHolder running!')"),
            ("Label","DoNothing"))
    
        def build():
            # print("Build ",PlaceHolder)
            return WyeCore.Utils.buildCodeText('PlaceHolder', TestLib.PlaceHolder.codeDescr, TestLib.PlaceHolder)
    
        def start(stack):
            return Wye.codeFrame(TestLib.PlaceHolder, stack)
    
        def run(frame):
            # print('Run 'PlaceHolder)
            try:
              TestLib.TestLib_rt.PlaceHolder_run_rt(frame)
            except Exception as e:
              if not hasattr(frame, 'errOnce'):
                print('TestLib.TestLib_rt.PlaceHolder_run_rt failed\n', str(e))
                import traceback
                traceback.print_exception(e)
                frame.errOnce = True
    
    