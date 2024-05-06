# Wye TestLib2

from Wye import Wye
from WyeCore import WyeCore
from panda3d.core import *
from WyeUI import WyeUI
import inspect
#import partial
import traceback
import sys
from sys import exit
from direct.showbase import Audio3DManager

from direct.showbase.DirectObject import DirectObject

# test loading code from another library

class TestLib2:

    # Build run_rt methods on each class
    def build():
        WyeCore.Utils.buildLib(TestLib2)

    class crossCall:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()     # takes arbitrary number of params.  Need to create a way to specify that
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib2.crossCall, stack)

        def run(frame):
            lib = WyeCore.World.libDict["TestLib"]
            f = lib.printParams.start()
            f.params = [["one"], [2], ["C"]]
            lib.printParams.run(f)


    class testObj3(DirectObject):
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.INTEGER
        paramDescr = ()    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("obj", Wye.type.OBJECT, None),("obj1Tag", Wye.type.STRING, "obj1Tag"),
                    ("sound", Wye.type.OBJECT, None))   # var 4
        def start(stack):
            return Wye.codeFrame(TestLib2.testObj3, stack)

        def run(frame):
            global base

            match frame.PC:
                case 0:
                    # cross call to other library
                    ll = WyeCore.World.libObj
                    f = ll.TestLib.wyePrint.start(frame.SP)
                    f.params = [["The number two="], [2], [". Cool, huh?"]]
                    f.verb.run(f)
                    frame.status = Wye.status.SUCCESS

                    frame.PC += 1

                case 1:
                    pass

        def keyFunc(keyName):
            print("keyFunc: key ", keyName)