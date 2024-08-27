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
        #print("build TestLib2")
        WyeCore.Utils.buildLib(TestLib2)

    class crossCall:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
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
        autoStart = True
        dataType = Wye.dType.NONE
        paramDescr = ()
        #varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("txtObj", Wye.dType.OBJECT, None), ("val", Wye.dType.INTEGER, 10), ("ct", Wye.dType.INTEGER, 0))

        def start(stack):
            return Wye.codeFrame(TestLib2.testObj3, stack)

        def run(frame):
            global base
            global render

            match frame.PC:
                case 0:
                    # cross call to other library
                    f = WyeCore.libs.TestLib.wyePrint.start(frame.SP)
                    f.params = [["The number two="], [2], [". Cool, huh?"]]
                    f.verb.run(f)   # demonstrate wyePrint verb

                    # demonstrate WyeCore function that returns params as a string
                    f.params[1][0] = 3
                    print(f.paramsToString())

                    # put up 3d text
                    txt = WyeCore.libs.WyeUI._label3d("Text String 1", (1,0,0,1), pos=(-.5,10,0), scale=(.2,.2,.2))
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


    # test concept of parallel processing
    # note: Wye compiled parallel code will put stream functions on library
    class testPar:
        mode = Wye.mode.PARALLEL
        dataType = Wye.dType.NONE
        paramDescr = ()
        #varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("stack", Wye.dType.OBJECT, [[],[]]), ("txtObj0", Wye.dType.OBJECT, None), ("txtObj1", Wye.dType.OBJECT, None),
                    ("txtBuff", Wye.dType.INTEGER, 10))
        parTermType = Wye.parTermType.FIRST_SUCCESS
        codeDescr = ()

        def start(stack):
            f = Wye.parallelFrame(TestLib2.testPar, stack)
            f.stacks.extend([[], []])   # stacks for parallel processing

            fS0 = Wye.codeFrame(WyeCore.ParallelStream, f.stacks[0])
            fS0.vars = f.vars
            fS0.params = f.params

            fS0.run = TestLib2.testPar.Stream0
            f.stacks[0].append(fS0)

            fS1 = Wye.codeFrame(WyeCore.ParallelStream, f.stacks[1])
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
                    txt = WyeCore.libs.WyeUI._label3d("Stream 0", color=(0, 1, 0, 1), pos=(2,10,2), scale=(.2,.2,.2))
                    frame.vars[1][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    print("testObj3 Stream 0 case 1")
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
                    txt = WyeCore.libs.WyeUI._label3d("Stream 1", color=(0, 1, 0, 1), pos=(-2,10,2), scale=(.2,.2,.2))
                    frame.vars[2][0] = txt
                    frame.PC += 1  # bump forward a step

                case 1:
                    print("testObj3 Stream 1 case 1")
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


    class testCompiledPar:
        mode = Wye.mode.PARALLEL
        parTermType = Wye.parTermType.FIRST_FAIL
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("obj", Wye.dType.OBJECT, None),                # 0
                    ("file", Wye.dType.STRING, "flyer_01.glb"),     # 1
                    ("objId", Wye.dType.STRING, ""),                # 2
                    ("obj", Wye.dType.OBJECT, None),                # 3
                    ("file", Wye.dType.STRING, "flyer_01.glb"),     # 4
                    ("objId", Wye.dType.STRING, ""),                # 5
                    ("count", Wye.dType.INTEGER, 1))                # 6

        # two parallel code streams
        codeDescr = (
            (
                ("WyeCore.libs.WyeLib.loadModel", (None, "frame.vars[0]"), (None, "frame.vars[1]")),
                ("WyeCore.libs.WyeLib.makePickable", (None, "frame.vars[2]"), (None, 'frame.vars[0]')),
                ("WyeCore.libs.WyeLib.showModel", (None, "frame.vars[0]"),
                 ("WyeCore.libs.TestLib.makeVec", (None, "[]"), (None, "[-3]"), (None, "[15]"), (None, "[0]")),
                 (None, "(.5,.5,.5)")),
                ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[0]"), (None, "(1,0,0,1)")),
                #(None, "print('TestCompiledPar stream0 zero Wait For Click case ',frame.PC)"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars[2]")),
                #(None, "print('TestCompiledPar stream0 one case ',frame.PC)"),
                ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[0]"), (None, "(0,1,0,1)")),
                #(None, "print('TestCompiledPar stream0 set color (0,1,0,1)')"),
                (None, "frame.status = Wye.status.SUCCESS")   # trap execution here in loop
            ),
            (
                ("WyeCore.libs.WyeLib.loadModel", (None, "frame.vars[3]"), (None, "frame.vars[4]")),
                ("WyeCore.libs.WyeLib.makePickable", (None, "frame.vars[5]"), (None, 'frame.vars[3]')),
                ("WyeCore.libs.WyeLib.showModel", (None, "frame.vars[3]"), (None, "(-2,15,0)"), (None, "(.5,.5,.5)")),
                #(None, "print('TestCompiledPar stream1 zero Wait For Click case ',frame.PC)"),
                ("Label", "Reset"),
                #(None, "print('TestCompiledPar stream1 start color sequence')"),
                ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[3]"), (None, "(1,1,0,1)")),

                ("Label", "DoClick"),
                ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars[5]")),
                #(None, "print('TestCompiledPar stream1 one case ',frame.PC, ' loopVar', frame.vars[6][0])"),
                (None, "frame.vars[6][0] += 1"),

                ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[3]"), (None, "(frame.vars[6][0]*(1/10),1,0,1)")),
                #(None, "print('TestCompiledPar stream1 set color', (frame.vars[6][0]*(1/10),1,0,1))"),

                ("IfGoTo", "frame.vars[6][0] < 10", "DoClick"),
                ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[3]"), (None, "(1,1,1,1)")),
                #(None, "print('TestCompiledPar stream1 done')"),
                (None, "frame.vars[6][0] = 1"),
                ("GoTo", "Reset"),
                ("Label", "Done")

            )
                     )
        code = None

        def build():
            #print("Testlib2 build testCompiledPar")
            return WyeCore.Utils.buildParallelText("TestLib2", "testCompiledPar", TestLib2.testCompiledPar.codeDescr)

        def start(stack):
            return TestLib2.TestLib2_rt.testCompiledPar_start_rt(stack)        # run compiled start code to build parallel code stacks

        def run(frame):
            frame.runParallel()      # run compiled run code


    class testMCycle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("obj", Wye.dType.OBJECT, None),                # 0
                    ("file", Wye.dType.STRING, "flyer_01.glb"),     # 1
                    ("objId", Wye.dType.STRING, ""),                # 2
                    ("obj", Wye.dType.OBJECT, None),                # 3
                    ("file", Wye.dType.STRING, "flyer_01.glb"),     # 4
                    ("objId", Wye.dType.STRING, ""))                # 5
        codeDescr = (
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.vars[0]"), (None, "frame.vars[1]")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.vars[2]"), (None, 'frame.vars[0]')),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.vars[0]"),
                                              #(None, "(1,15,0)"),
                                              ("WyeCore.libs.TestLib.makeVec", (None, "[]"), (None, "[-1]"),(None, "[15]"),(None, "[0]")),
                                              (None, "(.5,.5,.5)")),

            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.vars[3]"), (None, "frame.vars[4]")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.vars[5]"), (None, 'frame.vars[3]')),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.vars[3]"), (None, "(1,15,0)"), (None, "(.5,.5,.5)")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[3]"), (None, "(0,1,1,1)")),

            #(None, "print('testMCycle zero Wait For Click case ',frame.PC)"),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars[2]")),
            #(None, "print('testMCycle one case ',frame.PC)"),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[0]"), (None, "(0,1,0,1)")),

            #(None, "print('testMCycle vars=',frame.vars)"),

            ("TestLib2.testMCycle2", (None, "frame.vars[3]"), (None, "frame.vars[5]")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[3]"), (None, "(0,1,0,1)"))
        )

        def build():
            #print("Testlib2 build testMCycle")
            return WyeCore.Utils.buildCodeText("testMCycle", TestLib2.testMCycle.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib2.testMCycle, stack)

        def run(frame):
            TestLib2.TestLib2_rt.testMCycle_run_rt(frame)


    class testMCycle2:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE), ("objTag", Wye.dType.STRING, Wye.access.REFERENCE))
        varDescr = (("obj", Wye.dType.OBJECT, None),                # 0
                    ("file", Wye.dType.STRING, "flyer_01.glb"),     # 1
                    ("objId", Wye.dType.STRING, ""))                # 2
        codeDescr = (
            (None, "frame.vars[0][0] = frame.params[0][0]"),
            (None, "frame.vars[2][0] = frame.params[1][0]"),
            #(None, "print('testMCycle2 tag=',frame.vars[2][0])"),

            #(None, "print('testMCycle2 zero Wait For Click case ',frame.PC)"),
            ("WyeCore.libs.WyeLib.waitClick", (None, "frame.vars[2]")),
            #(None, "print('testMCycle2 one case ',frame.PC)"),
        )

        def build():
            #print("Testlib2 build testMCycle2")
            return WyeCore.Utils.buildCodeText("testMCycle2", TestLib2.testMCycle2.codeDescr)

        def start(stack):
            return Wye.codeFrame(TestLib2.testMCycle2, stack)

        def run(frame):
            TestLib2.TestLib2_rt.testMCycle2_run_rt(frame)


    class testMObj:
        cType = Wye.cType.OBJECT
        autoStart = True
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = () 
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib2.testMObj, stack)
        
        def run(frame):
            match(frame.PC):
                case 0:
                    #print("testMObj: case 0, Start TestCompiledPar, get frame")
                    f = TestLib2.testCompiledPar.start(frame.SP)
                    frame.SP.append(f)
                    frame.PC += 1
                case 1:
                    #print("testMObj: case 1, TestCompiledPar runtime done, pop frame")
                    f = frame.SP.pop()

                    frame.PC += 1
                case 2:
                    pass
                    