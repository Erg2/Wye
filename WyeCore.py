# Wye Core
# static single class lib
#
# license: We don't need no stinking license
#

from Wye import Wye
import inspect      # for debugging

# WyeCore class is a static container for the core Wye Classes that is never instantiated

# Building it this way prevents the editor from accidentally writing over the core because
# editing one of the contained libs will create an external file for just that lib.
# Incorporating the result requires external editing.
class WyeCore(Wye.staticObj):

    # The UI lib enables editing world objects in-world
    # As of now, it's a static Wye object
    # That could change if it's just too hard to bootstrap this way
    class uiLib(Wye.staticObj):

        # all object instantiations that have contents that can be listed have the same structure
        class listObjs(object):
            library = None
            # mode - F function S single cycle subroutine MC multi-cycle subroutine O multi-cycle object
            mode = Wye.mode.SINGLE_CYCLE
            type = Wye.type.STRING_LIST
            # params - tuple of (name, type) tuples
            params = (("param1", Wye.type.INTEGER, Wye.access.VALUE), ("param2", Wye.type.INTEGER, Wye.access.VALUE))  # param definition
            # vars - tuple of (name, type, defaultVal) tuples
            vars = (("var1", Wye.type.INTEGER, 0), ("var2", Wye.type.OBJECT, None))  # var definition

            def start():
                frame = Wye.codeFrame(WyeCore.uiLib.listObjs)
                return frame

    class utils(Wye.staticObj):

        # Take a Wye code description tuple and return compilable Python code
        # Resulting code pushes all the params to the frame, then runs the function
        # Recurses to handle nested param tuples
        def parseWyeTuple(wyeTuple, fNum):
            # Wye verb
            if wyeTuple[0]:
                eff = "f"+str(fNum)         # eff is frame var.  fNum keeps frame var names unique in nested code
                codeText = eff+" = " + wyeTuple[0] + ".start()\n"
                #print("parseWyeTuple: 1 codeText =", codeText[0])
                if len(wyeTuple) > 1:
                    for paramIx in range(1, len(wyeTuple)):
                        #print("parseWyeTuple: 2a paramIx ", paramIx, " out of ", len(wyeTuple)-1)
                        paramDesc = wyeTuple[paramIx]
                        #print("parseWyeTuple: 2 parse paramDesc ", paramDesc)
                        if paramDesc[0] is None:        # constant/var (leaf node)
                            #print("parseWyeTuple: 3a add paramDesc[1]=", paramDesc[1])
                            codeText += eff+".params.append(" + paramDesc[1] + ")\n"
                            #print("parseWyeTuple: 3 codeText=", codeText[0])
                        else:                           # recurse to parse nested code tuple
                            #print("parseWyeTuple: 4 - Can't get here")
                            codeText += WyeCore.utils.parseWyeTuple(paramDesc, fNum+1) + "\n" + eff+".params.append(" + \
                                "f"+str(fNum+1)+".params[0])\n"
                codeText += wyeTuple[0] + ".run("+eff+")\n"
            # Raw Python code
            else:
                if len(wyeTuple) > 1:
                    codeText = wyeTuple[1]+"\n"
                else:
                    print("Wye Warning - parseTuple null verb but no raw code supplied")

            return codeText

        def buildCodeText(codeDescr):
            codeText = [""]
            #print("WyeCore buildCodeText compile code=", codeDescr)

            for wyeTuple in codeDescr:
                # DEBUG start vvv
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                print('WyeCore buildCodeText caller:', calframe[1][3])
                print('WyeCore buildCodeText caller:', calframe[1][3])
                print("WyeCore buildCodeText: compile tuple=", wyeTuple)
                # DEBUG end ^^^^
                codeText[0] += WyeCore.utils.parseWyeTuple(wyeTuple, 0)

            print("buildCodeText complete.  codeText=\n", codeText[0])
            return codeText[0]

        # Take Python code for a Wye word and return compiled code
        def compileCodeText(codeText):
            print("WyeCore.compileCodeText: compile ", codeText)
            code = compile(codeText, "<string>", "exec")
            if code:
                print("WyeCore.compileCodeText: Compiled successfully")
            return code


        def printStatus(stat):
            match stat:
                case Wye.status.CONTINUE:
                    return "CONTINUE"
                case Wye.status.SUCCESS:
                    return "SUCCESS"
                case Wye.status.FAIL:
                    return "FAIL"

        def printStack(stack):
            stkStr = "\n stack len=" + str(len(stack))
            for frame in stack:
                stkStr += "\n  verb=" + frame.verb.__name__ + " status " + WyeCore.utils.printStatus(frame.status) + \
                          " params: " + str(frame.params)
            return stkStr
