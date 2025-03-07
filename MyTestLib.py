from Wye import Wye
from WyeCore import WyeCore
class MyTestLib:
    def build():
        WyeCore.Utils.buildLib(MyTestLib)
    class MyTestLib_rt:
        pass

    class PlaceHolder:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        cType = Wye.cType.VERB
        parTermType = Wye.parTermType.FIRST_FAIL
        paramDescr =        (
            ("ret","I",1),)
        varDescr =        (
            ("myVar","I",0),)
        codeDescr =        (
            ("Code","print(len(WyeCore.World.objStacks), 'objects running!')"),
            ("Label","DoNothing"))
    
        def build():
            # print("Build ",PlaceHolder)
            return WyeCore.Utils.buildCodeText('PlaceHolder', MyTestLib.PlaceHolder.codeDescr)
    
        def start(stack):
            # print('PlaceHolder object start')
                        return Wye.codeFrame(MyTestLib.PlaceHolder, stack)
    
        def run(frame):
            # print('Run 'PlaceHolder)
            try:
              MyTestLib.MyTestLib_rt.PlaceHolder_run_rt(frame)
            except Exception as e:
              if not hasattr(MyTestLib.MyTestLib_rt.PlaceHolder_run_rt, 'errOnce'):
                print('MyTestLib.MyTestLib_rt.PlaceHolder_run_rt failed\n', str(e))
                import traceback
                traceback.print_exception(e)
                setattr(MyTestLib.MyTestLib_rt.PlaceHolder_run_rt, 'errOnce', True)
    
    