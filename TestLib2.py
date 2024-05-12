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


    class testObj3():
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.INTEGER
        paramDescr = ()    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("txtObj", Wye.type.OBJECT, None), ("val", Wye.type.INTEGER, 10), ("ct", Wye.type.INTEGER, 0))

        class testObj3Callback:
            pass

        def start(stack):
            return Wye.codeFrame(TestLib2.testObj3, stack)

        def run(frame):
            global base
            global render

            match frame.PC:
                case 0:
                    # cross call to other library
                    ll = WyeCore.World.libObj
                    f = ll.TestLib.wyePrint.start(frame.SP)
                    f.params = [["The number two="], [2], [". Cool, huh?"]]
                    f.verb.run(f)   # demonstrate wyePrint verb

                    # demonstrate WyeCore function that returns params as a string
                    f.params[1][0] = 3
                    print(WyeCore.Utils.paramsToString(f))

                    # put up 3d text
                    txt = WyeCore.Text3d("Text String 1", (1,0,0,1))
                    frame.vars[0][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    print("testObj3 case 1")
                    # wait for click on 3d text
                    lib = WyeCore.World.libDict["TestLib"]
                    f = lib.waitClick.start(frame.SP)  # create multi-cycle verb (frame default status is CONTINUE
                    f.params = [[frame.vars[0][0].getTag()], ]  # pass tag to waitClick
                    frame.SP.append(f)  # note2:  put its frame on the stack.  Execution will continue in spin until it's done
                    # print("tstObj2 Obj waiting for click")
                    frame.PC += 1  # bump forward a step - when event happens we'll pick up at the next case

                case 2:
                    frame.SP.pop()      # remove waitclick or delay frame
                    #change text
                    txt = "Text String " + str(frame.vars[1][0])
                    frame.vars[0][0].setText(txt)

                    # Increase size of text by one place for next time
                    frame.vars[1][0] *= 10
                    frame.vars[2][0] += 1
                    if frame.vars[2][0] > 10:
                        frame.vars[2][0] = 0        # restart reset counter
                        frame.vars[1][0] = 1        # reset text display number

                    f = WyeCore.World.libDict["TestLib"].delay.start(frame.SP)
                    f.params = [[60]]
                    frame.SP.append(f)

                    frame.PC += 1

                case 3:
                    # NOTE: don't pop stack here 'cause prev case pops stack first think.  Reuse that pop
                    #frame.SP.pop()      # remove waitclick frame
                    frame.PC -= 1       # go back a step
                    pass

        def keyFunc(keyName):
            print("keyFunc: key ", keyName)