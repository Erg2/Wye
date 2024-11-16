
# Wye globals

# static Wye object (not instantiated)
# contains constants (static classes)
#    structures (regular classes)
#    and factories (lib, obj)

# import collections

# Wye container class that holds Wye classes
class Wye:

    debugOn = False          # true if exec should check debug flags
    trace = True           # true if tracing
    step = False            # true if single stepping
    breakList = []          # list of frames to break on

    version = "0.3"


    # if debugging is on, check for what to do on run()
    def debug(frame, msg):
        if Wye.trace:
            print("trace frame", frame.verb.__name__, ":", msg)



    #############################################
    #
    #  Static Wye Classes
    #
    #  The following classes hold static code.  They are never instantiated
    #  Typically they are holders for constants
    #
    #  (let's not get into a discussion of Python not having constants so the values COULD change at runtime
    #  because in that direction lies madness.  No legal Wye code is going to mess with the constant values.)
    #
    #############################################

    # base class for static python objects (libList, objs, verbs)
    # Only reason for existing it to complain if someone tries to instantiate the object!!
    class staticObj:
        def __init__(self):
            print("Wye Error - staticObj: attempting to instantiate a static object!")
            # if this happens a lot, maybe do an exit(1)
            # it would be cool to put code in every child object to identify which obj is being instantiated - once
            # the editor is fully running.
# Unused
#
#   # convenient library holder
#   class libList:
#       pass

    # Constants

    # status values returned by multi-cycle verbs
    class status:
        CONTINUE = 0
        SUCCESS = 1
        FAIL = -1

        def tostring(status):        # static print function
            match status:
                case Wye.status.CONTINUE:
                    return "CONTINUE"
                case Wye.status.SUCCESS:
                    return "SUCCESS"
                case Wye.status.FAIL:
                    return "FAIL"
                case _:
                    return "--unknown status value " + str(status) + "--"

    class pType:
        REQUIRED = 0        # default
        OPTIONAL = 1

        def tostring(pType):
            match pType:
                case Wye.status.REQUIRED:
                    return "REQUIRED"

                case Wye.status.OPTIONAL:
                    return "OPTIONAL"

                case _:
                    return "unknown pType "+str(pType)


    # Wye cType - verb, object, function verb
    class cType:
        FUNCTION = "F"      # Function that immediately returns a value of given dType (see dType)
        OBJECT = "O"        # multi-cycle object that has a "runnable" test and returns status (above) on each cycle
        VERB = "V"          # regular verb (default)
        
        def tostring(val):            # static print function
            match val:
                case Wye.mode.FUNCTION:
                    return "FUNCTION"
                case Wye.mode.OBJECT:
                    return "OBJECT"
                case Wye.mode.VERB:
                    return "VERB"

                case _:
                    return "--unknown cType value " + str(val) + "--"
            
    # verb modes
    class mode:
        SINGLE_CYCLE = "S"  # single cycle subroutine runs immediately and doesn't return a value
        MULTI_CYCLE = "M"   # multi-cycle subroutine that returns status (see above) on each cycle
        PARALLEL = "P"      # parallel processing of parameters


        def tostring(mode):            # static print function
            match mode:
                case Wye.mode.PARALLEL:
                    return "PARALLEL"
                case Wye.mode.SINGLE_CYCLE:
                    return "SINGLE_CYCLE"
                case Wye.mode.MULTI_CYCLE:
                    return "MULTI_CYCLE"
                case _:
                    return "--unknown mode value " + str(mode) + "--"

    # parallel completion requirement
    class parTermType:
        FIRST_FAIL = "F"        # done when any fails or all succeed
        FIRST_SUCCESS = "S"     # done when any succeeds or all fail
        FIRST_ANY = "A"         # done on first non-CONTINUE (i.e don on succeed or fail)

    # Data types
    class dType:
        NONE =          "Z"
        ANY =           "A"
        NUMBER =        "N"
        INTEGER =       "I"
        FLOAT =         "F"
        BOOL =          "B"
        OBJECT =        "O"
        STRING =        "S"
        ANY_LIST =      "AL"
        NUMBER_LIST =   "NL"
        INTEGER_LIST =  "IL"
        FLOAT_LIST =    "FL"
        BOOL_LIST =     "BL"
        OBJECT_LIST =   "OL"
        STRING_LIST =   "SL"
        VARIABLE =      "V"

        dTypeList = [
            NONE,
            ANY,
            NUMBER,
            INTEGER,
            FLOAT,
            BOOL,
            OBJECT,
            STRING,
            ANY_LIST,
            ANY_LIST,
            INTEGER_LIST,
            FLOAT_LIST,
            BOOL_LIST,
            OBJECT_LIST,
            STRING_LIST,
            VARIABLE,
        ]

        def tostring(dataType):            # static print function
            match dataType:
                case Wye.dType.NONE:
                    return "NONE"
                case Wye.dType.ANY:
                    return "ANY"
                case Wye.dType.NUMBER:
                    return "NUMBER"
                case Wye.dType.INTEGER:
                    return "INTEGER"
                case Wye.dType.FLOAT:
                    return "FLOAT"
                case Wye.dType.BOOL:
                    return "BOOL"
                case Wye.dType.OBJECT:
                    return "OBJECT"
                case Wye.dType.STRING:
                    return "STRING"
                case Wye.dType.ANY_LIST:
                    return "NUMBER_LIST"
                case Wye.dType.ANY_LIST:
                    return "NUMBER_LIST"
                case Wye.dType.INTEGER_LIST:
                    return "INTEGER_LIST"
                case Wye.dType.FLOAT_LIST:
                    return "FLOAT_LIST"
                case Wye.dType.BOOL_LIST:
                    return "BOOL_LIST"
                case Wye.dType.OBJECT_LIST:
                    return "OBJECT_LIST"
                case Wye.dType.STRING_LIST:
                    return "STRING_LIST"
                case Wye.dType.VARIABLE:
                    return "VARIABLE"

                case _:
                    return "--unknown data dType value " + str(dataType) + "--"

    # parameter access (how parameter is passed)
    class access:
        VALUE = 0
        REFERENCE = 1
        # decide if worth doing OUT = 2

        def tostring(access):            # static print function
            match access:
                case Wye.access.VALUE:
                    return "VALUE"
                case Wye.access.REFERENCE:
                    return "REFERENCE"
                #case Wye.dType.OUT:
                #    return "OUT"
                case _:
                    return "--unknown access value " + str(access) + "--"

    # known event types that a word can wait for
    class event:
        PICK = 1

    class ctlKeys:
        RIGHT = -1
        LEFT = -2
        UP = -3
        DOWN = -4
        CTL_DOWN = -5
        CTL_UP = -6
        SHIFT_DOWN = -7
        SHIFT_UP = -8

        def tostring(key):
            match key:
                case Wye.ctlKyes.RIGHT:
                    return "RIGHT"
                case Wye.ctlKyes.LEFT:
                    return "LEFT"
                case Wye.ctlKyes.UP:
                    return "UP"
                case Wye.ctlKyes.DOWN:
                    return "DOWN"
                case Wye.ctlKyes.CTL_DOWN:
                    return "CTL_DOWN"
                case Wye.ctlKyes.CTL_UP:
                    return "CTL_UP"
                case Wye.ctlKyes.SHIFT_DOWN:
                    return "SHIFT_DOWN"
                case Wye.ctlKyes.SHIFT_UP:
                    return "SHIFT_UP"

    ###########################################################################
    #
    # Dynamic Wye Classes
    #
    # (instantiated like any normal class)
    #
    ###########################################################################

    # minimal classes to hang all the params and vars on
    class params:
        pass
    class vars:
        pass


    # Code frame - for any verb defined by WyeCode rather than compiled Python
    # note: each variable is wrapped in its own list so that it can be passed
    # as a parameter by reference
    # Frame creates a params attribute for each param in paramDescr with value set to an empty list
    # Frame creates a vars attribute for each var in varDescr with the value being the varDescr value in a list
    # Wrapping each param and var value in a list allows it to be passed by reference
    class codeFrame:      # Used by any verb with Wye code
        def __init__(self, verb, stack):
            self.verb = verb    # the static verb that we're holding runtime data for
            self.params = Wye.params()  # caller will fill in params
            self.vars = Wye.vars()

            #print("code frame for verb ", verb.__name__)
            if hasattr(verb, "varDescr"):
                for varDef in verb.varDescr:
                    if len(varDef) > 1:
                        #print("  vars attr ", varDef[0], "=", varDef[2])
                        setattr(self.vars, varDef[0], [varDef[2]])
                        #print("  set vars '", varDef[0], "' to '", str(getattr(self.vars, varDef[0])))
            #else:
            #    print("verb",verb, " has no varDescr")
            if hasattr(verb, "paramDescr"):
                for paramDef in verb.paramDescr:
                    if len(paramDef) > 1:
                        #print("  params attr ", paramDef[0])
                        if paramDef[1] != Wye.dType.VARIABLE:
                            setattr(self.params, paramDef[0], [])
                        else:
                            setattr(self.params, paramDef[0], [[]])

            self.PC = 0         # used by async verbs to track location in executing code
            self.SP = stack      # points to stack list this frame is on
            if verb.mode == Wye.mode.MULTI_CYCLE or verb.mode == Wye.mode.PARALLEL:
                self.status = Wye.status.CONTINUE   # assume stay running
            else:
                self.status = Wye.status.SUCCESS    # assume good things
            self.debug = ""
            # print("codeFrame for verb", verb, " verb.varDescr =", verb.varDescr, " vars =", self.vars)

        def firstParamName(self):
            if hasattr(self.verb, "paramDescr") and len(self.verb.paramDescr) > 0:
                name = self.verb.paramDescr[0][0]
                return name
            else:
                print("Wye.codeFrame.firstParamName: Warning: verb ", self.verb.__name__, " does not have a first param")
                return None

        # go through the gyrations required to find the first parameter and get its value
        def firstParamVal(self):
            if hasattr(self.verb, "paramDescr") and len(self.verb.paramDescr) > 0:
                name = self.verb.paramDescr[0][0]
                val = getattr(self.params, name)
                return val
            # don't have one
            else:
                print("Wye.codeFrame.firstParamVal: Warning: verb ", self.verb.__name__, " does not have a first param")
                return 0

        def tostring(frame):
            fStr = ""
            fStr += "frame: "+str(frame)+"\n"
            if hasattr(frame, "verb"):
                if hasattr(frame.verb, "__name__"):
                    fStr += "  verb "+frame.verb.__name__+"\n"
                else:
                    fStr += "  verb has no name"+"\n"
            else:
                fStr += "  frame has no verb"+"\n"
            if hasattr(frame, "PC"):
                fStr += "  PC="+str(frame.PC)+"\n"
            else:
                fStr += "  <no PC>"+"\n"
            if hasattr(frame, "SP"):
                fStr += "  SP len: " + str(len(frame.SP)) + ", stack:"+frame.frameListSummary(frame.SP)+"\n"
            else:
                fStr += "  <no SP>"+"\n"
            if hasattr(frame, "status"):
                fStr += "  status:" + Wye.status.tostring(frame.status) + "\n"
            else:
                fStr += "  <no status>\n"
            fStr += "  params:" + frame.paramsToString()+"\n"
            fStr += "  vars:" + frame.varsToString()

            return fStr

        def frameListSummary(self, lst):
            pStr = ""
            if len(lst) > 0:
                for ii in range(len(lst)):
                    frm = lst[ii]
                    pStr += str(frm.verb.__name__)
                    if ii < len(lst)-1:
                        pStr += ", "
            else:
                pStr = "<empty>"
            return pStr

        def listToString(self, lst):
            #print("listToString lst:", lst)
            pStr = ""
            if len(lst) > 0:
                for ii in range(len(lst)):
                    pStr += str(lst[ii])
                    if ii < len(lst)-1:
                        pStr += ", "
            else:
                pStr = "<empty>"
            return pStr

        def attribToString(self, obj):
            return ",".join([x for x in dir(obj) if x[0] != '_'])

        # return params concatenated
        def paramsToString(frame):
            return frame.attribToString(frame.params)

        # verbose version that lists values
        def paramsToStringV(frame):
            # name from verb paramDescr, value from frame parameter
            if hasattr(frame, "verb") and hasattr(frame.verb, "paramDescr"):
                return ",".join([ desc[0] + "=" + str(getattr(frame.params, desc[0])) for desc in frame.verb.paramDescr])
            else:
                return Wye.codeFrame.paramsToString(frame)

        # return vars concanated
        def varsToString(frame):
            return frame.attribToString(frame.vars)

        def varsToStringV(frame):
            # name from verb varDescr, value from frame var
            if hasattr(frame, "verb") and hasattr(frame.verb, "varDescr"):
                return ",".join([ desc[0] + "=" + str(getattr(frame.vars, desc[0])) for desc in frame.verb.varDescr])
            else:
                return Wye.codeFrame.varsToString(frame)

        # return stack in reverse order
        def stackToString(stack):
            sLen = len(stack)
            stkStr = "\n stack len=" + str(sLen)
            if sLen > 0:
                for ix in range(sLen-1, -1, -1):
                    frame = stack[ix]
                    stkStr += "\n  ["+str(ix)+"] verb=" + frame.verb.__name__ + " status " + Wye.status.tostring(frame.status) + \
                              " PC=" + str(frame.PC) + " params: " + str(frame.params)
            return stkStr


    # used by verbs that run parallel streams
    class parallelFrame(codeFrame): # used by any object with parallel execution (multiple stacks)

        def __init__(self, verb, stack):
            super().__init__(verb, stack)
            #print("parallelFrame init: verb", verb.__name__," stack", stack)
            self.stacks = []        # callee must fill in empty lists for appropriate number of stacks

        # run the top of each parallel stack once
        def runParallel(self):
            dbgIx = 0
            status = Wye.status.CONTINUE  # assume we'll keep going
            foundFail = False
            foundSuccess = False
            foundContinue = False

            # DEBUG: print out all the stacks
            # print("parallel run: frame.stacks:")
            # for sIx in range(len(frame.stacks)):
            # print(" stack:", sIx, WyeCore.Utils.stackToString(frame.stacks[sIx]))

            # Each parallel code block (aka stream) has its own stack.
            # For each stack, process frame at end of stack.
            # When stacks complete (single remaining frame generates a non-CONTINUE status),
            # handle termination based on condition in parallel verb's parTermType.
            delLst = []
            dbgStkNum = 0
            for stack in self.stacks:
                #print("runParallel stack", dbgStkNum)
                # if there's a frame, there's something to do
                if len(stack) > 0:
                    f = stack[-1]  # grab the bottom frame

                    # if it's still running, run it again
                    if f.status == Wye.status.CONTINUE:
                        if Wye.debugOn:
                            Wye.debug(f, "runParallel: run frame "+ f.verb.__name__+ " status CONTINUE, PC " + str(f.PC)+ " run frame")
                        f.verb.run(f)
                        foundContinue = True

                    # if it terminated, if there's a parent, call it to clean up completed child
                    else:
                        #print("  frame", f.verb.__name__," status", Wye.status.tostring(f.status), ", PC", f.PC)
                        # have a parent on stack
                        if len(stack) > 1:
                            fp = stack[-2]
                            if Wye.debugOn:
                                Wye.debug(fp, "runParallel: run parent " + fp.verb.__name__)
                            fp.verb.run(fp)  # run parent (will test child status, remove from stack, and continue)
                            foundContinue = True  # technically we haven't checked, but we will next time
                        # no parent, atatus not CONTINUE, we're done with stream
                        else:
                            #print("    no parent, process status and remove stack")
                            if f.status == Wye.status.FAIL:
                                foundFail = True
                            elif f.status == Wye.status.SUCCESS:
                                foundSuccess = True
                            else:
                                foundContinue = True
                            if (foundFail and self.verb.parTermType == Wye.parTermType.FIRST_FAIL) or \
                                    (foundSuccess and self.verb.parTermType == Wye.parTermType.FIRST_SUCCESS) or \
                                    ((
                                             foundFail or foundSuccess) and self.verb.parTermType == Wye.parTermType.FIRST_ANY):
                                #print("stream complete with status ", f.status)
                                status = f.status
                                break
                            # we're done with this stack, remove it
                            delLst.append(stack)
                    dbgIx += 1
                # remove empty stack
                else:
                    #print("  stack depth 0, remove stack")
                    delLst.append(stack)

                dbgStkNum += 1

            # if there are completed streams, remove their stacks
            for stack in delLst:
                self.stacks.remove(stack)

            # If we're done, figure out whether we succeeded or failed
            if status == Wye.status.CONTINUE and not foundContinue:  # all streams completed without triggering an exit
                if self.verb.parTermType == Wye.parTermType.FIRST_FAIL:
                    #print("stream done, all succeeded")
                    status = Wye.status.SUCCESS  # FIRST_FAIL didn't have any failures - yay!
                else:
                    #print("stream done, all failed")
                    status = Wye.status.FAIL  # FIRST_SUCCESS and didn't have any successes - boo :-(
            self.status = status  # return whatever status we have

        # create additional parallel stream at runtime
        def addStream(self, frame):
            sp = [frame]
            frame.SP = sp
            self.stacks.append(sp)

        # remove parallel stream
        # NOTE: can't do it here 'cause prolly running from runParallel loop, above
        # so queue for deleting at end of run
        def removeStream(self, frame):
            self.delLst.append(frame.SP)

    # object template class for editing new Wye objects
    # note that this object will be used as the template for creating a new
    # class object in the library currently being edited
    class WyeObjTemplate:
        def __init__(self):
            self.library = None
            self.mode = Wye.mode.OBJECT
            self.dType = ""
            self.params = ()
            self.vars = ()


    ###########################################################################
    # The main Wye class
    # -- not used, static class and all, right??? ---
    ###########################################################################
    def __init__(self):
        print("Wye.py Execution can't get here so you don't see this!!!")
        #self.currWorld = None  # the universe
        #self.picker = None  # 3d object picker
        #self.textBgnd = None  # Text background geom reffed by all text

# if Wye UI is not already running, start it?