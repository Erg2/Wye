# Wye TestLib2

from Wye import Wye
from WyeCore import WyeCore

from panda3d.core import *

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
        dataType = Wye.type.NONE
        paramDescr = ()    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("txtObj", Wye.type.OBJECT, None), ("val", Wye.type.INTEGER, 10), ("ct", Wye.type.INTEGER, 0))

        def start(stack):
            return Wye.codeFrame(TestLib2.testObj3, stack)

        def run(frame):
            global base
            global render

            match frame.PC:
                case 0:
                    # cross call to other library
                    ll = WyeCore.libs
                    f = ll.TestLib.wyePrint.start(frame.SP)
                    f.params = [["The number two="], [2], [". Cool, huh?"]]
                    f.verb.run(f)   # demonstrate wyePrint verb

                    # demonstrate WyeCore function that returns params as a string
                    f.params[1][0] = 3
                    print(WyeCore.Utils.paramsToString(f))

                    # put up 3d text
                    txt = WyeCore.libs.WyeUI.label3d("Text String 1", (1,0,0,1), pos=(-.5,10,0), scale=(.2,.2,.2))
                    frame.vars[0][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    #print("testObj3 case 1")
                    # wait for click on 3d text
                    #lib = WyeCore.World.libDict["TestLib"]
                    f = WyeCore.libs.WyeLib.waitClick.start(frame.SP)  # create multi-cycle verb (frame default status is CONTINUE
                    f.params = [[frame.vars[0][0].getTag()], ]  # pass tag to waitClick
                    frame.SP.append(f)  # note2:  put its frame on the stack.  Execution will continue in spin until it's done
                    # print("tstObj2 Obj waiting for click")
                    frame.PC += 1  # bump forward a step - when event happens we'll pick up at the next case

                case 2:
                    evtFrm = frame.SP.pop()      # remove waitclick or delay frame

                    #change text
                    txt = "Text String " + str(frame.vars[1][0])
                    frame.vars[0][0].setText(txt)

                    # Increase size of text by one place for next time
                    frame.vars[1][0] *= 10
                    frame.vars[2][0] += 1
                    if frame.vars[2][0] > 10:
                        frame.vars[2][0] = 0        # restart reset counter
                        frame.vars[1][0] = 1        # reset text display number

                    f = WyeCore.libs.WyeLib.delay.start(frame.SP)
                    f.params = [[60]]
                    frame.SP.append(f)

                    frame.PC += 1

                case 3:
                    # NOTE: don't pop stack here 'cause prev case pops stack first think.  Reuse that pop
                    #frame.SP.pop()      # remove waitclick frame
                    frame.PC -= 1       # go back a step
                    pass



    class testPar():
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("stack", Wye.type.OBJECT, [[],[]]), ("txtObj0", Wye.type.OBJECT, None), ("txtObj1", Wye.type.OBJECT, None),
                    ("txtBuff", Wye.type.INTEGER, 10))

        codeDescr = ()

        code = '''
def Stream0():
    # code for first parallel path
def Stream1():
    # code for 2nd parallel path
'''

#        def build():
#            return

        def start(stack):
            f = Wye.parallelFrame(TestLib2.testPar, stack)
            f.stacks.extend([[], []])   # stacks for parallel processing

            fS0 = Wye.codeFrame(TestLib2.testPar.singleStream, f.stacks[0])
            fS0.vars = f.vars
            fS0.params = f.params
            fS0.run = TestLib2.testPar.Stream0
            f.stacks[0].append(fS0)

            fS1 = Wye.codeFrame(TestLib2.testPar.singleStream, f.stacks[1])
            fS1.vars = f.vars
            fS1.params = f.params
            fS1.run = TestLib2.testPar.Stream0
            f.stacks[1].append(fS1)

            return f

        def run(frame):
            global base
            global render

            #print("testPar ", len(frame.stacks), " stacks")
            dbgIx = 0
            for stack in frame.stacks:
                if len(stack) > 0:
                    #print("testPar run stack ", dbgIx)
                    f = stack[-1]
                    if f.status == Wye.status.CONTINUE:
                        f.verb.run(f)
                    dbgIx += 1

        def Stream0(frame):
            match(frame.PC):
                case 0:
                    # put up 3d text
                    txt = WyeCore.libs.WyeUI.label3d("Stream 0", color=(0, 1, 0, 1), pos=(2,10,2), scale=(.2,.2,.2))
                    frame.vars[1][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    print("testObj3 case 1")
                    # wait for click on 3d text
                    # lib = WyeCore.World.libDict["TestLib"]
                    f = WyeCore.libs.WyeLib.waitClick.start(frame.SP)  # create multi-cycle verb (frame default status is CONTINUE
                    f.params = [[frame.vars[1][0].getTag()], ]  # pass tag to waitClick
                    frame.SP.append(f)  # note2:  put its frame on the stack.  Execution will continue in spin until it's done
                    # print("tstObj2 Obj waiting for click")
                    frame.PC += 1  # bump forward a step - when event happens we'll pick up at the next case

                case  2:
                    evtFrm = frame.SP.pop()  # remove waitclick or delay frame
                    frame.PC += 1
                case 3:
                    pass    # just hang out here for now

        def Stream1(frame):
            match(frame.PC):
                case 0:
                    # put up 3d text
                    txt = WyeCore.libs.WyeUI.label3d("Stream 0", color=(0, 1, 0, 1), pos=(-2,10,2), scale=(.2,.2,.2))
                    frame.vars[2][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    print("testObj3 case 1")
                    # wait for click on 3d text
                    # lib = WyeCore.World.libDict["TestLib"]
                    f = WyeCore.libs.WyeLib.waitClick.start(frame.SP)  # create multi-cycle verb (frame default status is CONTINUE
                    f.params = [[frame.vars[2][0].getTag()], ]  # pass tag to waitClick
                    frame.SP.append(f)  # note2:  put its frame on the stack.  Execution will continue in spin until it's done
                    # print("tstObj2 Obj waiting for click")
                    frame.PC += 1  # bump forward a step - when event happens we'll pick up at the next case

                case  2:
                    evtFrm = frame.SP.pop()  # remove waitclick or delay frame
                    frame.PC += 1
                case 3:
                    pass    # just hang out here for now


        class singleStream:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.type.NONE
            paramDescr = ()
            varDescr = ()

            def start(stack):
                return Wye.codeFrame()
            def run(frame):
               frame.run(frame)