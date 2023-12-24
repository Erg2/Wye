# Wye testLib

from Wye import Wye
from WyeCore import WyeCore
import inspect

'''
Wye Overview

Libs and words are static
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
    wordFrame.params.append( [p1], .. )
        If the word being called requires any params passed in, the caller has to set them up.
        Each parameter is wrapped in a list so that its value can be changed
        functions return their value in the first parameter
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


class testLib:

    # TODO - move this to WyeCore
    # Build run_rt methods on each class
    def build():
        codeStr = "class testLib_rt:\n"
        # check all the classes in the lib for build functions.
        for attr in dir(testLib):
            val = getattr(testLib, attr)
            if inspect.isclass(val):
                # if the class has a build function then call it to generate Python source code for its runtime method
                if hasattr(val, "build"):
                    #print("class ", attr, " has build method.  attr is ", type(attr), " val is ", type(val))
                    build = getattr(val, "build")   # get child's build method
                    # call the build function to get the "run" code string
                    bldStr = build()                # call it to get child's runtime code string(s)
                    lines = bldStr.splitlines(True) # break the code into lines
                    # start runtime function for class
                    codeStr += " def " + attr + "_run_rt(frame):\n" # define a runtime method containing the code lines
                    # DEBUG
                    codeStr += "   print('execute "+attr+"_run_rt(frame) params', frame.params, ' vars', frame.vars)\n"
                    # End DEBUG
                    for line in lines:      # put child's code in rt method at required indent
                        if not line.isspace():
                            codeStr += "   " + line
                    codeStr += "   print('end of "+attr+"_run_rt(frame) params', frame.params, ' vars', frame.vars)\n"

        #codeStr += "print('testLib is ', testLib)\n"        # DEBUG

        # All classes in this library defined by Wye-code generate their runtime methods as methods of the library's dynamically added testLib_rt class
        # This allows the compile to be done once when the library is loaded instead of piecemeal for each class.
        #
        codeStr += 'setattr(testLib, "testLib_rt", testLib_rt)\n'

        # DEBUG - print out code string for Python to compile
        lineNum = 1
        print("testLib code string:")
        for line in codeStr.split("\n"):
            if line[0:3] == "   ":
                print("%-3d " % lineNum, line)
                lineNum += 1
            else:
                lineNum = 1
                print("    ", line)
        # End DEBUG

        # Compile the runtime Wye code
        code = compile(codeStr, "<string>", "exec")
        exec(code, {"testLib":testLib})

        ## DEBUG vvv Check that testLib_rt class was created and has testAdd_run_rt method
        ##print("testLib attrs after exec:\n", dir(testLib))
        #if hasattr(testLib, "testLib_rt"):
        #    tLib_rt = getattr(testLib, "testLib_rt")
        #    if hasattr(tLib_rt, "testAdd_run_rt"):
        #        print("testLib.testLib_rt.testAdd_run_rt found!")
        #    else:
        #        print("testLib.testLib_rt does not have testAdd_run_rt")
        #else:
        #    print("testLib does not have testLib_rt")
        ## End DEBUG ^^^


    # print as many params as passed in, followed by a crlf
    class printParams:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()     # takes arbitrary number of params.  Need to create a way to specify that
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.printParams, stack)

        def run(frame):
            print(inspect.stack()[1].function, "params: ", end="")
            pIx = 0
            for param in frame.params:
                print(" param[%d] =" % pIx, param, end="")
                pIx += 1
            print("")

    # print as many params as passed in, followed by a crlf
    class wyePrint:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()     # takes arbitrary number of params.  Need to create a way to specify that
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.wyePrint, stack)

        def run(frame):
            #print(inspect.stack()[1].function, "params: ", end="")
            for param in frame.params:
                print(param, end="")
            print("")

    # test operations on local variables
    class testAddInPlace:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NUMBER
        paramDescr = (
        ("_ret_", Wye.type.NUMBER, Wye.access.REFERENCE), ("p1", Wye.type.NUMBER, Wye.access.REFERENCE),
        ("p1", Wye.type.NUMBER, Wye.access.REFERENCE))
        varDescr = ()  # ("a", Wye.type.NUMBER, 10), ("b", Wye.type.NUMBER, 20), ("c", Wye.type.NUMBER, 30))
        codeString = '''
# add var 1 and var 2 and put in var3.  Return var 3 in param 0
frame.vars[0][0] = frame.vars[1][0] + frame.vars[2][0]
frame.params[0][0] = frame.vars[0][0]
'''
        code = None

        def build():
            # string will be added to testLib_rt.testAddInPlace_rt
            print("Called testAddInPlace.build()")
            return testLib.testAddInPlace.codeString

        def start(stack):
            return Wye.codeFrame(testLib.testAddInPlace, stack)

        def run(frame):
            testLib.testLib_rt.testAddInPlace_run_rt(frame)
            pass

    # manual code test - show how reading and writing params
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

    # test autogenerated code
    class testAdd2:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NUMBER
        paramDescr = (("_ret_", Wye.type.NUMBER, Wye.access.REFERENCE), ("p1", Wye.type.NUMBER, Wye.access.REFERENCE),
                  ("p1", Wye.type.NUMBER, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = (
            ("testLib.testAdd", (None, "frame.params[0]"), (None, "frame.params[1]"), (None, "frame.params[2]")),
        )
        code = None

        def build():
            return WyeCore.utils.buildCodeText(testLib.testAdd2.codeDescr)

        def start(stack):
            return Wye.codeFrame(testLib.testAdd2, stack)

        def run(frame):
            testLib.testLib_rt.testAdd2_run_rt(frame)
            pass

    class makeVec:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("_ret_", Wye.type.NUMBER, Wye.access.REFERENCE), ("x", Wye.type.NUMBER, Wye.access.REFERENCE),
            ("y", Wye.type.NUMBER, Wye.access.REFERENCE),("z", Wye.type.NUMBER, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(testLib.makeVec, stack)

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

            filepath = frame.params[1][0]
            model = base.loader.loadModel(filepath)
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
            print("showModel pos ", pos, " scale ", scale)
            model.reparentTo(render)
            model.setScale(scale[0], scale[1], scale[2])
            model.setPos(pos[0], pos[1], pos[2])
            model.setTag('wyeTag', tag)

    # set model pos
    class setObjPos:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("obj", Wye.type.OBJECT, Wye.access.REFERENCE),
                    ("posVec", Wye.type.INTEGER_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(testLib.setObjPos, stack)

        def run(frame):
            #print("setObjPos run: params ", frame.params)
            gObj = frame.params[0][0]
            vec = frame.params[1]
            print("setObjPos set obj", gObj, "to", vec)
            gObj.setPos(vec[0], vec[1], vec[2])

    # hand written code
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
            print("testLoader run: done displayed model")


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
            ("testLib.showModel", (None, "frame.vars[0]"),
                ("testLib.makeVec", (None, "[]"), (None, "[-1]"), (None, "[15]"), (None, "[1]")),
                (None, "[.75,.75,.75]"),
                (None, "'o1'")),
            (None, "frame.params[0][0] = frame.vars[0][0]")
            )
        code = None

        def build():
            return WyeCore.utils.buildCodeText(testLib.testLoader2.codeDescr)

        def start(stack):
            return Wye.codeFrame(testLib.testLoader2, stack)

        def run(frame):
            testLib.testLib_rt.testLoader2_run_rt(frame)


    # generated code for
    # load model passed in at loc, scale passed in
    class testLoader3:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE

        paramDescr = (("obj", Wye.type.OBJECT, Wye.access.REFERENCE), ("file", Wye.type.STRING, Wye.access.REFERENCE),
                    ("posVec", Wye.type.INTEGER_LIST, Wye.access.REFERENCE),
                    ("scaleVec", Wye.type.INTEGER_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = (
            ("testLib.wyePrint", (None, "'testLoader3 first line'")),
            (None, "print('test inline code')"),
            # call loadModel with testLoader3 params 0 and 1
            ("testLib.loadModel", (None, "frame.params[0]"), (None, "frame.params[1]")),
            # call showModel with testLoader3 on passed in params
            ("testLib.printParams", (None, "frame.params[0]"),(None, "frame.params[2]"), (None, "frame.params[3]")),
            ("testLib.showModel", (None, "frame.params[0]"),(None, "frame.params[2]"), (None, "frame.params[3]"),
             (None, "'o1'")) # need to set up global object name list
        )
        code = None

        def build():
            return WyeCore.utils.buildCodeText(testLib.testLoader3.codeDescr)

        def start(stack):
            return Wye.codeFrame(testLib.testLoader3, stack)

        def run(frame):
            testLib.testLib_rt.testLoader3_run_rt(frame)



    # compiled code
    # testObj calls testWord2 and passes it testObj's var as testWord2's return param
    # then testObj puts the value from var into it's return param
    class testObj:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.INTEGER
        paramDescr = (("_ret_", Wye.type.INTEGER, Wye.access.REFERENCE),)    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("obj1", Wye.type.OBJECT, {}),("obj2", Wye.type.OBJECT, {}),
                    ("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))

        tokens=[]

        # print("testObj code: frame.params ", frame.params, " frame.debug '", frame.debug, "'")
        # chFrame = testLib.testWord2.start(frame.stack)
        # print("testObj code: a chFrame.params = ", chFrame.params)
        # print("testObj code: frame.vars = ", frame.vars)
        # chFrame.params.append(frame.vars[0])
        # print("testObj code: b len chFrame.params = ", len(chFrame.params))
        # print("testObj code: frame.vars[0] (result) = ", frame.vars[0][0])
        # testLib.testWord2.run(chFrame)
        # print("testObj code: c chFrame.params = ", chFrame.params," result = ", frame.vars[0][0])
        ##frame.params[0][0] = chFrame.vars[0][0]
        # print("")
        # f = testLib.testAdd.start(frame.stack)
        # f.params = [frame.params[0], frame.vars[1], frame.vars[2]]
        # testLib.testAdd.run(f)
        # print("testAdd returned ", frame.params[0])

        #print("test testAdd ret in param")
        #f = testLib.testAdd.start(frame.stack)
        #f.params = [frame.params[0], frame.vars[3], frame.vars[4]]
        #testLib.testAdd.run(f)
        #print("testAdd returned ", frame.params[0])

        #print("test testAdd ret in var")
        #f = testLib.testAdd.start(frame.stack)
        #print("test testAdd ret in parent var")
        #f.params = [frame.vars[2], frame.vars[3], frame.vars[4]]
        #testLib.testAdd.run(f)
        #print("testAdd var contains ", frame.vars[2])

        codeString = '''
#print("testObj: test testAdd2 ret in var")
#f = testLib.testAdd2.start(frame.stack)
#f.params = [frame.vars[2], frame.vars[3], frame.vars[4]]
#testLib.testAdd2.run(f)
#print("testObj: post testAdd2 var contains ", frame.vars[2])

# create object from verb's local variables
print("testObj start: frame.vars ", frame.vars)
f = testLib.testLoader2.start(frame.stack)
f.params = [frame.vars[0],]
testLib.testLoader2.run(f)
print("testObj after testLoader2: frame.vars ", frame.vars)

# create object from parameters
f1 = testLib.testLoader3.start(frame.stack)
f1.params = [frame.vars[1], ["flyer_01.glb"], [-1,15,-1], [.75,.75,.75]]
testLib.testLoader3.run(f1)
print("testObj after 2nd testLoader3: frame.vars ", frame.vars)

# move 2nd object
f2 = testLib.setObjPos.start(frame.stack)
f2.params = [frame.vars[1], [1,10,1]]
testLib.setObjPos.run(f2)
frame.params[0][0] = 1
'''
        code = None

        def start(stack):
            if not testLib.testObj.code:        # if object not compiled, compile it
                print("testObj compile codeString")
                testLib.testObj.code = compile(testLib.testObj.codeString, "<string>", "exec")
            return Wye.codeFrame(testLib.testObj, stack)    # run compiled object

        def run(frame):
            #print("testObj run frame ",frame, " frame stack ", frame.stack, " frame params ", frame.params, " debug '", frame.debug, "'")
            #print("testObj codeString ", testLib.testObj.code)
            print("testObj exec code")
            exec(testLib.testObj.code, {"testLib":testLib, "frame":frame})

