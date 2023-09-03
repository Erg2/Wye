# Wye testLib

from Wye import Wye
from WyeCore import WyeCore
import inspect

'''
Libs and words are static
All refs to a lib or word within a lib or word have to be 3rd person (lib.word.xxx) rather than self.
because there is no instantiated class so there is no self.
All context (local variables, parameters passed in, and PC (which is used by multi-pass word) is in the 
stack frame that is created on word.start.

Basic concept for executing a word in a library:
    wordFrame =  word.start(stack)
        The frame holds the local storage for this exec of word.  The most used attributes are the
        calling params and local variable values.
        Note: if word uses local variables the list wordFrame.vars is built automatically from the
              wordFrame.varDescr.  
              Each variable is a separate list so it can be passed to another word in that word's 
              stackframe.params and the var can be updated by that word.
              All vars are filled in with initial values by the frame on instantiation.
              example: wordFrame.vars = [[0],[1],["two"]]
    wordFrame.params.append( [p1], .. )
        If the word being called requires any params passed in, the caller has to set them up.
        Note: Each parameter is wrapped in a list so that its value can be changed
        Note: functions return their value in the first parameter
    word.run(wordFrame)
        Note: if the word is a function, the return value is in wordFrame.params[0][0]
'''


class testLib:

    # TODO - move this to WyeCore
    # Build run_rt methods on each class
    def build():
        codeStr = "class testLib_rt:\n"
        # check all the classes in the lib for build functions.
        for attr in dir(testLib):
            val = getattr(testLib, attr)
            if inspect.isclass(val):
                # if the class has a build function then call it
                if hasattr(val, "build"):
                    #print("class ", attr, " has build method.  attr is ", type(attr), " val is ", type(val))
                    build = getattr(val, "build")
                    # call the build function to get the "run" code string
                    bldStr = build()
                    lines = bldStr.splitlines(True)
                    codeStr += " def " + attr + "_run_rt(frame):\n"
                    for line in lines:
                        if not line.isspace():
                            codeStr += "   " + line

        codeStr += "print('testLib is ', testLib)\n"
        codeStr += 'setattr(testLib, "testLib_rt", testLib_rt)\n'

        print("testLib code string:\n", codeStr)

        code = compile(codeStr, "<string>", "exec")
        exec(code, {"testLib":testLib})

        #print("testLib attrs after exec:\n", dir(testLib))
        if hasattr(testLib, "testLib_rt"):
            tLib_rt = getattr(testLib, "testLib_rt")
            if hasattr(tLib_rt, "testAdd_run_rt"):
                print("testLib.testLib_rt.testAdd_run_rt found!")
            else:
                print("testLib.testLib_rt does not have testAdd_run_rt")
        else:
            print("testLib does not have testLib_rt")


    # Takes 3 params, ret, p1, p2.
    # adds p1 to p2 and return in ret
    class testAdd:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NUMBER
        paramDescr = (("_ret_", Wye.type.NUMBER, Wye.access.REFERENCE), ("p1", Wye.type.NUMBER, Wye.access.REFERENCE),
                  ("p1", Wye.type.NUMBER, Wye.access.REFERENCE))
        varDescr = () #("a", Wye.type.NUMBER, 10), ("b", Wye.type.NUMBER, 20), ("c", Wye.type.NUMBER, 30))
        codeString = '''
# add param 1 to param 2 and return in param 0
frame.params[0][0] = frame.params[1][0] + frame.params[2][0]
print("testAdd_run_rt: add  ", frame.params[1], " + ", frame.params[2], " to get ", frame.params[0])
'''
        code = None

        def build():
            # string will be added to testLib_rt.testAdd_rt
            print("Called testAdd.build()")
            return testLib.testAdd.codeString

        def start(stack):
            return Wye.codeFrame(testLib.testAdd, stack)

        def run(frame):
            testLib.testLib_rt.testAdd_run_rt(frame)
            pass

    class makeVec:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("_ret_", Wye.type.NUMBER, Wye.access.REFERENCE), ("x", Wye.type.NUMBER, Wye.access.REFERENCE),
            ("y", Wye.type.NUMBER, Wye.access.REFERENCE),("z", Wye.type.NUMBER, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.testLoader2, stack)

        def run(frame):
            retList = [frame.params[1][0], frame.params[2][0], frame.params[3][0]]
            print("testLib makeVec: return ", retList)
            frame.params[0] = retList


    class testWord2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.INTEGER  # i.e function returning integer in p1
        paramDescr = (("_ret_", Wye.type.INTEGER, Wye.access.REFERENCE)),
        varDescr = (("a", Wye.type.NUMBER, 10), ("b", Wye.type.NUMBER, 20))

        def start(stack):
            frame = Wye.codeFrame(testLib.testWord2, stack)
            #frame.params = [0,0,0]
            print("testWord2 start: frame params ", frame.params)
            print("testWord2 start: frame vars ", frame.vars)
            return frame

        def run(frame):
            frame.params[0][0] = frame.vars[0][0] + frame.vars[1][0]
            print("testWord2 run param 0 ", frame.params[0][0], " var 0 ", frame.vars[0][0], " + var 1 ",
                  frame.vars[1][0], " = ", frame.params[0][0])
            pass


    # load Panda3d model
    # p0 - returned model
    # p1 - file path to model
    class loadModel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("loadedObject", Wye.type.OBJECT, Wye.access.REFERENCE),
                      ("objectFileName", Wye.type.STRING, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.loadModel, stack)

        def run(frame):
            global base

            path = frame.params[1][0]
            model = base.loader.loadModel(path)
            frame.params[0][0] = model

    class showModel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("object", Wye.type.OBJECT, Wye.access.REFERENCE),
                      ("position", Wye.type.FLOAT_LIST, Wye.access.REFERENCE),
                      ("scale", Wye.type.FLOAT_LIST, Wye.access.REFERENCE),
                      ("tag", Wye.type.STRING, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.showModel, stack)

        def run(frame):
            global render     # panda3d base

            model = frame.params[0][0]
            pos = frame.params[1]
            scale = frame.params[2]
            tag = frame.params[3][0]
            model.reparentTo(render)
            model.setScale(scale[0], scale[1], scale[2])
            model.setPos(pos[0], pos[1], pos[2])
            model.setTag('wyeTag', tag)

    class testLoader:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = (("obj", Wye.type.OBJECT, None), ("file", Wye.type.STRING, "flyer_01.glb"))

        def start(stack):
            return Wye.codeFrame(testLib.testLoader, stack)

        def run(frame):
            print("testLoader run: load model")
            f = testLib.loadModel.start(frame.stack)
            f.params.append(frame.vars[0])
            f.params.append(frame.vars[1])
            testLib.loadModel.run(f)
            print("testLoader run: loadModel returned ", f.params[0])
            f2 = testLib.showModel.start(frame.stack)
            f2.params.append(frame.vars[0])
            f2.params.append([1,15,1])
            f2.params.append([.75,.75,.75])
            f2.params.append(["o1"])
            testLib.showModel.run(f2)
            print("testLoader run: displayed model")


    # generated code
    class testLoader2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = (("obj", Wye.type.OBJECT, None), ("file", Wye.type.STRING, "flyer_01.glb"),
                    ("posVec", Wye.type.INTEGER_LIST, [0,0,0]))
        codeDescr = (
            # call loadModel with testLoader2 var0 and var1 as params
            ("testLib.loadModel", (None, "frame.vars[0]"), (None, "frame.vars[1]")),
            # call showModel with testLoader2 var0 and constantw for pos, scale, tag
#            ("testLib.showModel", (None, "frame.vars[0]"), (None, "[-1,15,1]"), (None, "[.75,.75,.75]"), (None, "'o1'"))
            ("testLib.showModel", (None, "frame.vars[0]"), ("testLib.makeVec", (None, "frame.vars[2]"), (None, "[-1]"), (None, "[15]"), (None, "[1]")), (None, "[.75,.75,.75]"), (None, "'o1'"))
            )
        code = None

        def build():
            return WyeCore.utils.buildCodeText(testLib.testLoader2.codeDescr)

        def start(stack):
            return Wye.codeFrame(testLib.testLoader2, stack)

        def run(frame):
            testLib.testLib_rt.testLoader2_run_rt(frame)
            print("testLoader2 run: exec code")


    # compiled code
    # testObj calls testWord2 and passes it testObj's var as testWord2's return param
    # then testObj puts the value from var into it's return param
    class testObj:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.INTEGER
        paramDescr = (("_ret_", Wye.type.INTEGER, Wye.access.REFERENCE))
        varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))

        tokens=[]
        codeString = '''
#print("testObj code: frame.params ", frame.params, " frame.debug '", frame.debug, "'")
#chFrame = testLib.testWord2.start(frame.stack)
#print("testObj code: a chFrame.params = ", chFrame.params)
#print("testObj code: frame.vars = ", frame.vars)
#chFrame.params.append(frame.vars[0])
#print("testObj code: b len chFrame.params = ", len(chFrame.params))
#print("testObj code: frame.vars[0] (result) = ", frame.vars[0][0])
#testLib.testWord2.run(chFrame)
#print("testObj code: c chFrame.params = ", chFrame.params," result = ", frame.vars[0][0])
##frame.params[0][0] = chFrame.vars[0][0]
#print("")
f = testLib.testAdd.start(frame.stack)
f.params = [frame.params[0], frame.vars[1], frame.vars[2]]
testLib.testAdd.run(f)
print("testAdd returned ", frame.params[0])
'''
        code = None

        def start(stack):
            if not testLib.testObj.code:
                testLib.testObj.code = compile(testLib.testObj.codeString, "<string>", "exec")
            return Wye.codeFrame(testLib.testObj, stack)

        def run(frame):
            #print("testObj run frame ",frame, " frame stack ", frame.stack, " frame params ", frame.params, " debug '", frame.debug, "'")
            exec(testLib.testObj.code, {"testLib":testLib, "frame":frame})

