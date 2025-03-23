# Wye TestLib

from Wye import Wye
from WyeCore import WyeCore
from panda3d.core import *

import inspect
#import partial
import traceback
import sys
from sys import exit
from direct.showbase import Audio3DManager

'''
Wye Overview

libList and words are static
All refs to a lib or word within a lib or word have to be 3rd person (lib.word.xxx) rather than self.
because there is no instantiated class so there is no self.
All context (local variables, parameters passed in, and PC (which is used by multi-pass word) is in the 
stack frame that is returned by word.start.

Basic concept for executing a word in a library:
    wordFrame =  word.start(stack)
        The frame holds the local storage for this exec of word.  The most used attributes are the
        calling params and local variable values.
        
        if a word uses local variables the word's frame.vars is built automatically from the
        word's varDescr.  
        
        Each variable is a separate list so it can be passed to another word in that word's 
        stackframe.params and the var can be updated by that word.
        All vars are filled in with initial values by the frame on instantiation.
        example: wordFrame.vars = [[0],[1],["two"]]
    wordFrame.params.xxx
        If the word being called requires any params passed in, the caller has to set them up
        as attributes on frames.params
        Each parameter is wrapped in a list so that its value can be changed
        functions return their value in the first parameter (as defined in the verb's paramDescr list)
    word.run(wordFrame)
        If the word is a function, the return value is in wordFrame.params[0][0]
        
Compiling 
    Two stages, first translating Wye code to Python code, and then compiling Python code to runtime code.  This is 
    done on library load so the overhead of compiling is done once.  
    
    If there is a codeDescr = (..wye-code..) then the code will be translated to Python.
    
    Wye code is in nested tuples in the form ("lib.word", (..param..), (..param..)) where the param list can be
    zero or more params.  Note that a tuple or list with just one entry must end with a comma (entry,) or python will 
    optimize the tuple or list away.
    (..param..) can be either (None, a-constant) or ("lib.word", (..param..)) to recurse to a function that will
    supply the parameter.
    
    The Python output is put in a string under code.
    
    All code attributes found in classes in the library are compiled to methods under the dynamically created 
    class libName_rt.  Each word's runtime is def'd as wordName_run_rt.  
    
    The word itself has a run method that calls libName_rt.wordName_run_rt(frame)
    
    Note: there is the risk that the string holding the
    Python code will get too long (the internal limit is not clearly defined).  If that happens then the compile loop
    could compile each word's code individually, but that would be much slower.  Or it could process words in chunks
    that are small enough to fit within the string limit.
    
    Note: a runtime optimization would be to reparent the rt attributes back to each word so there was no indirection
    on the call.
'''


class TestLib:

    # Build run_rt methods on each class
    def build(rowRef):
        WyeCore.Utils.buildLib(TestLib)


    # print params passed in, followed by a crlf
    class wyePrint:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()     # takes arbitrary number of params.  Need to create a way to specify that
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib.wyePrint, stack)

        def run(frame):
            for param in frame.params:
                print(param[0], end="")
            print("\n")

    # test operations on local variables
    class testAddInPlace:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NUMBER
        paramDescr = (
        ("_ret_", Wye.dType.NUMBER, Wye.access.REFERENCE), ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE),
        ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE))
        varDescr = ()  # ("a", Wye.dType.NUMBER, 10), ("b", Wye.dType.NUMBER, 20), ("c", Wye.dType.NUMBER, 30))
        codeString = '''
 def testAddInPlace_run_rt(frame):
  # add var 1 and var 2 and put in var3.  Return var 3 in param 0
  frame.vars[0][0] = frame.vars[1][0] + frame.vars[2][0]
  frame.params[0][0] = frame.vars[0][0]
'''
        code = None

        def build(rowRef):
            # string will be added to TestLib_rt.testAddInPlace_rt
            return TestLib.testAddInPlace.codeString, ""

        def start(stack):
            return Wye.codeFrame(TestLib.testAddInPlace, stack)

        def run(frame):
            TestLib.TestLib_rt.testAddInPlace_run_rt(frame)
            pass

    # manual code test - show how reading and writing params
    # Takes 3 params, ret, p1, p2.
    # adds p1 to p2 and return in ret
    class testAdd:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NUMBER
        paramDescr = (("_ret_", Wye.dType.NUMBER, Wye.access.REFERENCE), ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE),
                  ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE))
        varDescr = () #("a", Wye.dType.NUMBER, 10), ("b", Wye.dType.NUMBER, 20), ("c", Wye.dType.NUMBER, 30))
        codeString = '''
 def testAdd_run_rt(frame):
  # add param 1 to param 2 and return in param 0
  frame.params[0][0] = frame.params[1][0] + frame.params[2][0]
  #print("testAdd_run_rt: add  ", frame.params[1], " + ", frame.params[2], " to get ", frame.params[0])
'''
        code = None

        def build(rowRef):
            # string will be added to TestLib_rt.testAdd_rt
            #print("Called testAdd.build(rowref)")
            return TestLib.testAdd.codeString, ""

        def start(stack):
            return Wye.codeFrame(TestLib.testAdd, stack)

        def run(frame):
            TestLib.TestLib_rt.testAdd_run_rt(frame)
            pass

    # test autogenerated code
    class testAdd2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NUMBER
        paramDescr = (("_ret_", Wye.dType.NUMBER, Wye.access.REFERENCE), ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE),
                  ("p1", Wye.dType.NUMBER, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = (
            ("TestLib.testAdd", (None, "frame.params[0]"), (None, "frame.params[1]"), (None, "frame.params[2]")),
        )
        code = None

        def build(rowRef):
            return WyeCore.Utils.buildCodeText("testAdd2", TestLib.testAdd2.codeDescr, rowRef)

        def start(stack):
            return Wye.codeFrame(TestLib.testAdd2, stack)

        def run(frame):
            TestLib.TestLib_rt.testAdd2_run_rt(frame)
            pass

    class makeVec:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.FLOAT_LIST
        paramDescr = (("_ret_", Wye.dType.NUMBER, Wye.access.REFERENCE), ("x", Wye.dType.NUMBER, Wye.access.REFERENCE),
            ("y", Wye.dType.NUMBER, Wye.access.REFERENCE),("z", Wye.dType.NUMBER, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib.makeVec, stack)

        def run(frame):
            retList = [frame.params[1][0], frame.params[2][0], frame.params[3][0]]
            #print("TestLib makeVec: return ", retList)
            frame.params[0] = retList

    class testWord2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.INTEGER  # i.e function returning integer in p1
        paramDescr = (("_ret_", Wye.dType.INTEGER, Wye.access.REFERENCE)),
        varDescr = (("a", Wye.dType.NUMBER, 10), ("b", Wye.dType.NUMBER, 20))

        def start(stack):
            frame = Wye.codeFrame(TestLib.testWord2, stack)
            #print("testWord2 start: frame params ", frame.params)
            #print("testWord2 start: frame vars ", frame.vars)
            return frame

        def run(frame):
            frame.params[0][0] = frame.vars[0][0] + frame.vars[1][0]
            #print("testWord2 run param 0 ", frame.params[0][0], " var 0 ", frame.vars[0][0], " + var 1 ",
            #      frame.vars[1][0], " = ", frame.params[0][0])
            pass


    # spin object back and forth
    class spin:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),)
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.spin, stack)

        # TODO - make multi-cycle
        def run(frame):
            #print('execute spin, params', frame.params, ' vars', frame.vars)

            gObj = frame.params[0][0]
            vec = gObj.getHpr()
            axis = frame.params[1][0]
            #print("Current HPR ", vec)
            match frame.PC:
                case 0:
                    vec[axis] += 5
                    #print("spin (pos) obj", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if frame.vars[0][0] < 4:  # wiggle this many times, then exit
                        if vec[axis] > 45:  # end of swing this way
                            frame.vars[0][0] += 1  # count cycles
                            frame.PC += 1   # go to next state
                    else:   # last spin cycle, stop at zero
                        #print("spin: done")
                        if vec[axis] >= 0:  # end of swing this way
                            frame.PC = -1  # undefined case value so will go to default to exit


                    frame.status = Wye.status.CONTINUE

                case 1:
                    vec[axis] -= 5
                    #print("spin (neg) obj ", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] < -45:    # end of swing other way
                        frame.PC -= 1   # go to previous state

                    frame.status = Wye.status.CONTINUE

                case _:
                    frame.status = Wye.status.SUCCESS


    # repeat clickWiggle a bunch of times
    class repClickWiggle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE), ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("repCt", Wye.dType.INTEGER, 0),("repFrm", Wye.dType.OBJECT, None))
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.repClickWiggle, stack)

        def run(frame):
            #print('execute spin, params', frame.params, ' vars', frame.vars)

            gObj = frame.params[0][0]
            tag = frame.params[1][0]
            match frame.PC:
                case 0:
                    # create a single shot event
                    #print("repClickWiggle: start clickWiggle")
                    f = TestLib.clickWiggle.start(frame.SP)
                    f.params = [frame.params[0], frame.params[1], frame.params[2]]  # obj, obj tag
                    frame.SP.append(f)  # push clickWiggle stack frame so it execs until done
                    frame.PC += 1

                case 1:
                    #print("repClickWiggle: done clickWiggle")
                    frame.SP.pop()
                    frame.vars[0][0] += 1
                    if frame.vars[0][0] < 2:        # stop rep event after this many wiggles
                        #print("repClickWIggle ct ", frame.vars[0][0], " <5, do it again")
                        # go back to do it again
                        frame.PC -= 1
                    # done repeats, finished with repeated event
                    else:
                        #print("repClickWiggle ct ", frame.vars[0][0], " >=5, done")
                        f = WyeCore.libs.WyeLib.setObjMaterialColor.start(frame.SP)
                        f.params = [frame.params[0], (1,1,1,1)]
                        f.verb.run(f)
                        frame.status = Wye.status.SUCCESS  # yeah, we're done

                case _:
                    print("repClickWiggle ct ", frame.vars[0][0], " unexpected PC ", frame.PC, " ERROR EXIT")

                    frame.status = Wye.status.FAIL

    # when clicked, spin object back and forth
    class clickWiggle:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE), ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("axis", Wye.dType.INTEGER, Wye.access.REFERENCE))
        varDescr = (("rotCt", Wye.dType.INTEGER, 0),("sound", Wye.dType.OBJECT, None))
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(TestLib.clickWiggle, stack)

        def run(frame):
            global base
            #print('execute spin, params', frame.params, ' vars', frame.vars)

            gObj = frame.params[0][0]
            vec = gObj.getHpr()
            axis = frame.params[2][0]
            #print("Current HPR ", vec)
            match frame.PC:
                case 0:
                    WyeCore.World.setEventCallback("click", frame.params[1][0], frame)
                    # frame.vars[1][0] = Wye.audio3d.kiadSfx("WyePop.wav")
                    audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
                    frame.vars[1][0] = audio3d.loadSfx("WyePop.wav")
                    audio3d.attachSoundToObject(frame.vars[1][0], frame.params[0][0])
                    frame.PC += 1
                    #print("clickWiggle waiting for event 'click' on tag ", frame.params[1][0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    frame.vars[1][0].play()
                    frame.PC += 1

                case 3:
                    vec[axis] += 5
                    #print("spin (pos) obj", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] > 45:   # end of swing this way
                        frame.PC += 1  # go to next state

                case 4:
                    vec[axis] -= 5
                    #print("spin (neg) obj ", gObj, "to", vec)
                    gObj.setHpr(vec[0], vec[1], vec[2])
                    if vec[axis] < -45:    # end of swing other way
                        frame.PC += 1   # go to next state

                case 5:
                    frame.vars[0][0] += 1  # count cycles
                    if frame.vars[0][0] < 2:  # wiggle this many times, then exit
                        frame.PC = 3    # go do another wiggle
                    else:
                        # finish by coming back to zero
                        vec[axis] += 5
                        #print("spin (neg) obj ", gObj, "to", vec)
                        gObj.setHpr(vec[0], vec[1], vec[2])
                        if vec[axis] >= 0:    # end of swing other way
                            #print("clickWiggle: done")
                            frame.status = Wye.status.SUCCESS


                case _:
                    frame.status = Wye.status.SUCCESS

    # hand written code
    class testLoader:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = ()
        varDescr = (("obj", Wye.dType.OBJECT, None), ("file", Wye.dType.STRING, "flyer_01.glb"))

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader, stack)

        def run(frame):
            #print("testLoader")
            f = WyeCore.libs.WyeLib.loadModel.start(frame.SP)
            #print("testLoader run: load model ", f.vars[1][0])
            f.params.append(frame.vars.obj)
            f.params.append(frame.vars[1])
            WyeCore.libs.WyeLib.loadModel.run(f)
            if f.status != Wye.status.SUCCESS:
                frame.status = f.status
                return

            #print("testLoader run: loadModel returned ", f.params[0])

            obj = frame.vars[0][0]
            tag = "wyeTag" + str(WyeCore.Utils.getId())
            #print("TestLib testLoader: set tag ", tag, " on obj ", obj)
            obj.setTag(tag, "true")
            WyeCore.picker.makePickable(obj)

            f2 = WyeCore.libs.WyeLib.showModel.start(frame.SP)
            f2.params.append(frame.vars[0])
            f2.params.append([1,15,1])
            f2.params.append([.75,.75,.75])
            #f2.params.append(["o1"])
            WyeCore.libs.WyeLib.showModel.run(f2)
            #print("testLoader run: done displayed model")


    # generated code
    class testLoader2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),("tag", Wye.dType.STRING, Wye.access.REFERENCE))
        varDescr = (("obj", Wye.dType.OBJECT, None), ("file", Wye.dType.STRING, "flyer_01.glb"),
                    ("posVec", Wye.dType.INTEGER_LIST, [0,0,0]))
        codeDescr = (
            # call loadModel with testLoader2 var0 and var1 as params
            #hi from testLoader2')")),
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.vars[0]"), (None, "frame.vars[1]")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params[1]"), (None, "frame.vars[0]")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.vars[0]"), (None, "[1.,0.,0.,1.]")),
            # call showModel with testLoader2 var0 and constantw for pos, scale, tag
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.vars[0]"),
                ("TestLib.makeVec", (None, "[]"), (None, "[-4]"), (None, "[15]"), (None, "[1]")),
                (None, "[.75,.75,.75]")),
            (None, "frame.params[0][0] = frame.vars[0][0]")
            )
        code = None

        def build(rowRef):
            return WyeCore.Utils.buildCodeText("testLoader2", TestLib.testLoader2.codeDescr, rowRef)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader2, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader2_run_rt(frame)


    # generated code for
    # load model passed in at loc, scale passed in
    class testLoader3:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE

        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("file", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),
                      ("scaleVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("colorVec", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = (
            #(None, "print('test inline code')"),
            # call loadModel with testLoader3 params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.params.obj"), (None, "frame.params.file")),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params.tag"), (None, "frame.params.obj")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params.obj"), (None, "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.params.obj"), (None, "frame.params.posVec"), (None, "frame.params.scaleVec"))
        )
        code = None

        def build(rowRef):
            return WyeCore.Utils.buildCodeText("testLoader3", TestLib.testLoader3.codeDescr, rowRef)

        def start(stack):
            return Wye.codeFrame(TestLib.testLoader3, stack)

        def run(frame):
            TestLib.TestLib_rt.testLoader3_run_rt(frame)




    # Runtime object
    # test compiled code
    class testObj:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = (("_ret_", Wye.dType.INTEGER, Wye.access.REFERENCE),)    # gotta have a ret param
        #varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("obj1", Wye.dType.OBJECT, None),("obj2", Wye.dType.OBJECT, None),
                    ("obj1Tag", Wye.dType.STRING, ""), ("obj2Tag", Wye.dType.STRING, ""),
                    ("repEvtID", Wye.dType.OBJECT, None), ("repEvtFrm", Wye.dType.OBJECT, None))

        # print("testObj code: frame.params ", frame.params, " frame.debug '", frame.debug, "'")
        # chFrame = TestLib.testWord2.start(frame.SP)
        # print("testObj code: a chFrame.params = ", chFrame.params)
        # print("testObj code: frame.vars = ", frame.vars)
        # chFrame.params.append(frame.vars[0])
        # print("testObj code: b len chFrame.params = ", len(chFrame.params))
        # print("testObj code: frame.vars[0] (result) = ", frame.vars[0][0])
        # TestLib.testWord2.run(chFrame)
        # print("testObj code: c chFrame.params = ", chFrame.params," result = ", frame.vars[0][0])
        ##frame.params[0][0] = chFrame.vars[0][0]
        # print("")
        # f = TestLib.testAdd.start(frame.SP)
        # f.params = [frame.params[0], frame.vars[1], frame.vars[2]]
        # TestLib.testAdd.run(f)
        # print("testAdd returned ", frame.params[0])

        #print("test testAdd ret in param")
        #f = TestLib.testAdd.start(frame.SP)
        #f.params = [frame.params[0], frame.vars[3], frame.vars[4]]
        #TestLib.testAdd.run(f)
        #print("testAdd returned ", frame.params[0])

        #print("test testAdd ret in var")
        #f = TestLib.testAdd.start(frame.SP)
        #print("test testAdd ret in parent var")
        #f.params = [frame.vars[2], frame.vars[3], frame.vars[4]]
        #TestLib.testAdd.run(f)
        #print("testAdd var contains ", frame.vars[2])

        codeString = '''
def f():
  match frame.PC:
    case 0:
        #print("testObj: testLoader 2 and 3")
        
        # create object1 from verb's local variables
        #print("testObj start: frame.vars ", frame.vars)
        f = TestLib.testLoader2.start(frame.SP)
        f.params = [frame.vars[0],frame.vars[2]]
        TestLib.testLoader2.run(f)
        #print("testObj vars after testLoader2: ", frame.vars)
        
        # create object2 from parameters
        f1 = TestLib.testLoader3.start(frame.SP)
        # position doesn't matter 'cause set pos below
        f1.params = [frame.vars[1], ["flyer_01.glb"], [0,0,0], [.75,.75,.75], frame.vars[3], [1,1,0,1]]
        TestLib.testLoader3.run(f1)
        if f1.status != Wye.status.SUCCESS:
            print("Exit testObj code on file load error")
            frame.status = f1.status
            return
            
        #print("testObj vars after testLoader3: ", frame.vars)
        
        # move 2nd object
        f2 = WyeCore.libs.WyeLib.setObjPos.start(frame.SP)
        f2.params = [frame.vars[1], [2.5,10,1]]
        WyeCore.libs.WyeLib.setObjPos.run(f2)

        # set angle of 1st object
        f3 = WyeCore.libs.WyeLib.setObjAngle.start(frame.SP)
        f3.params = [frame.vars[0],[45, 0, 0]]
        WyeCore.libs.WyeLib.setObjAngle.run(f3)
        
        # set angle of 2nd object
        f3 = WyeCore.libs.WyeLib.setObjAngle.start(frame.SP)
        f3.params = [frame.vars[1],[-45, 0, 0]]
        WyeCore.libs.WyeLib.setObjAngle.run(f3)
                        
        # create a repeated event on obj 1
        fRep = TestLib.repClickWiggle.start(frame.SP)
        fRep.params = [frame.vars[0], frame.vars[2],[0]]       #obj 1, obj 1 tag, spin axis
        fTag = WyeCore.World.setRepeatEventCallback("click", fRep)
        frame.vars[4] = [fTag]                          # save rep event tag so can cancel it
        frame.vars[5] = [fRep]
        
        frame.PC += 1
        
    case 1:
        # create a single shot event
        #print("testObj: push clickWiggle")
        f = TestLib.clickWiggle.start(frame.SP)
        f.params = [frame.vars[1], frame.vars[3], [2]]       #obj 2, obj 2 tag, spin axis
        frame.SP.append(f)               #push clickWiggle stack frame so it execs until done
        frame.PC += 1                                   #inc to next state, which will run when clickWiggle done

    case 2:
        #print("testObj: done clickWiggle on obj 2")
        # pop stack and go back to do it again (never ending loop)
        frame.SP.pop()
        
        # if repClickWiggle on obj 1 is done, make another one
        oldEvtFrm = frame.vars[5][0]
        if oldEvtFrm.status != Wye.status.CONTINUE:         # if repClickWiggle is done, Start over.            
            axis = oldEvtFrm.params[2][0]
            axis = (axis + 1) %3                            # progress through axes
            #print("Start another repClickWiggle")
            fRep = TestLib.repClickWiggle.start(frame.SP)
            fRep.params = [frame.vars[0], frame.vars[2], [axis]]       #obj 1, obj 1 tag, spin axis
            fTag = WyeCore.World.setRepeatEventCallback("click", fRep)
            frame.vars[4][0] = fTag                          # save rep event tag so can cancel it
            frame.vars[5][0] = fRep
        
            f = WyeCore.libs.WyeLib.setObjMaterialColor.start(frame.SP)
            color = [0,0,0,1]
            color[axis] = 1
            f.params = [frame.vars[0], color]
            f.verb.run(f)
        
        frame.PC -= 1
    
    case _:
        # return a value for testing purposes
        frame.status = Wye.status.SUCCESS       # yeah, we're done
        frame.params[0][0] = 1
f()
'''
        code = None

        def start(stack):
            if not TestLib.testObj.code:        # if object not compiled, compile it
                #print("testObj compile codeString:"+TestLib.testObj.codeString)
                TestLib.testObj.code = compile(TestLib.testObj.codeString, "<string>", "exec")
            return Wye.codeFrame(TestLib.testObj, stack)

        def run(frame):
            #print("testObj run frame ",frame, " frame params ", frame.params)
            #print("testObj codeString ", TestLib.testObj.code)
            #print("testObj exec code")
            try:
                exec(TestLib.testObj.code, {"TestLib":TestLib, "frame":frame, "Wye":Wye, "WyeCore":WyeCore,
                                            "WyeLib":WyeCore.libs.WyeLib, "WyeUILib":WyeCore.libs.WyeUILib,
                                            "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
                                            "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib})

            except:
                #print("testObj run error:")
                frame.status = Wye.status.FAIL
                ex = sys.exception()
                traceback.print_exception(ex)
                #exit(1)


    class testObj2:
        mode = Wye.mode.MULTI_CYCLE
        autoStart = True
        dataType = Wye.dType.INTEGER
        paramDescr = (("_ret_", Wye.dType.INTEGER, Wye.access.REFERENCE),)    # gotta have a ret param
        #varDescr = (("a", Wye.dType.NUMBER, 0), ("b", Wye.dType.NUMBER, 1), ("c", Wye.dType.NUMBER, 2))
        varDescr = (("obj1", Wye.dType.OBJECT, None),("obj2", Wye.dType.OBJECT, None),
                    ("obj1Tag", Wye.dType.STRING, "obj1Tag"), ("obj2Tag", Wye.dType.STRING, "obj2Tag"),
                    ("sound", Wye.dType.OBJECT, None))   # var 4

        codeString = '''
def f():
  match frame.PC:
    case 0:
        #print("testObj2 case 0: start - set up object")

        # create object from parameters
        f1 = TestLib.testLoader3.start(frame.SP)
        # position doesn't matter - explicitly set, below
        f1.params = [frame.vars[0], ["flyer_01.glb"], [0,0,0], [.75,.75,.75], frame.vars[2], [0,1,0,1]]
        TestLib.testLoader3.run(f1)
        if f1.status != Wye.status.SUCCESS:
            print("Exit testObj2 code on file load error")
            frame.status = f1.status
            return
        #print("testObj2 after 2nd testLoader3: frame.vars ", frame.vars)

        # move object
        f2 = WyeCore.libs.WyeLib.setObjPos.start(frame.SP)
        f2.params = [frame.vars[0], [0,5,-.5]]
        WyeCore.libs.WyeLib.setObjPos.run(f2)
        
        # load click sound
        frame.vars[4][0] = Wye.audio3d.kiadSfx("WyePew.wav")
        #audio3d = base.Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
        #frame.vars[4][0] = audio3d.loadSfx("WyePop.wav")
        #audio3d.attachSoundToObject(frame.vars[4][0], frame.params[0][0])
        #audio3d.attachSoundToObject(frame.vars[4][0], frame.params[1][0])

        frame.PC += 1
        
    case 1:
        #print("testObj2 case 1: start spin")        
        f4 = TestLib.spin.start(frame.SP)       # create multi-cycle verb (frame default status is CONTINUE
        f4.params = [frame.vars[0], [1]]    # pass obj, rotation axis to spin
        frame.SP.append(f4)             # note2:  put its frame on the stack.  Execution will continue in spin until it's done
        #print("testObj2, frame.SP", frame.SP)
        #print("testObj2, stack contains ", frame.stackToString(frame.SP))
        
        frame.PC = 3 # jump over delay to waitClick                    # bump forward a step - when spin completes we'll pick up at the next case
        
    case 2:
        #print("testObj2 case 2: done spin")
        # we won't get here until spin completes
        # spin's frame is at the bottom of the stack
        f = frame.SP.pop()
        #print("testObj2: spin returned p0 ", frame.params[0][0], " status ", WyeCore.status.tostring(f.params.retVal[0]))
        #frame.status = Wye.status.SUCCESS   # we're done

        #print("testObj2 case 2 start delay")
        f = WyeCore.libs.WyeLib.delay.start(frame.SP)
        f.params = [[200]]
        frame.SP.append(f)
        # when we get back here after delay, we'll pick up at case 3
        frame.PC += 1       # when delay done, go pop frame
        
    case 3:
        frame.SP.pop()  # remove delay frame
        
        f = WyeCore.libs.WyeLib.waitClick.start(frame.SP)       # create multi-cycle verb (frame default status is CONTINUE
        f.params = [frame.vars[2],]    # pass tag to waitClick
        frame.SP.append(f)             # note2:  put its frame on the stack.  Execution will continue in spin until it's done
        #print("tstObj2 Obj waiting for click")
        frame.PC += 1                   # bump forward a step - when event happens we'll pick up at the next case
        
    case 4:
        # get here when waitClick detects event
        frame.vars[4][0].play()
        f = frame.SP.pop()  # remove event frame
        #print("tstObj2: got click on obj ", f.eventData[0])
        frame.PC = 1   # Set PC back so next cycle we do it all again

  #print("testObj2 cycle")
  # return a value for testing purposes
  frame.params[0][0] = 1
f()
        '''
        code = None
        def start(stack):
            if not TestLib.testObj2.code:        # if object not compiled, compile it
                #print("testObj2 compile codeString:"+TestLib.testObj.codeString)
                TestLib.testObj2.code = compile(TestLib.testObj2.codeString, "<string>", "exec")
            return Wye.codeFrame(TestLib.testObj2, stack)

        def run(frame):
            #print("testObj2 run frame ",frame, " frame params ", frame.params, " debug '", frame.debug, "'")
            #print("testObj2 codeString ", TestLib.testObj.code)
            #print("testObj2 exec code")
            try:
                exec(TestLib.testObj2.code, {"TestLib":TestLib, "frame":frame, "Wye":Wye, "WyeCore":WyeCore,
                                            "WyeLib":WyeCore.libs.WyeLib, "WyeUILib":WyeCore.libs.WyeUILib,
                                            "WyeUIUtilsLib": WyeCore.libs.WyeUIUtilsLib,
                                            "Wye3dObjsLib": WyeCore.libs.Wye3dObjsLib})
            except:
                #print("testObj2 run error:")
                frame.status = Wye.status.FAIL
                ex = sys.exception()
                traceback.print_exception(ex)
                #exit(1)
