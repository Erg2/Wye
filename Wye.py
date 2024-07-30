
# Wye globals

# static Wye object (not instantiated)
# contains constants (static classes)
#    structures (regular classes)
#    and factories (lib, obj)

# Wye container class that holds Wye classes
class Wye:

    version = "0.2"
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
        FAIL = 2

        def tostring(status):        # static print function
            match(status):
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
            match(pType):
                case Wye.status.REQUIRED:
                    return "REQUIRED"

                case Wye.status.OPTIONAL:
                    return "OPTIONAL"

                case _:
                    return "unknown pType "+str(pType)


    # Wye dType - verb, object, function verb
    class cType:
        FUNCTION = "F"      # Function that immediately returns a value of given dType (see dType)
        OBJECT = "O"        # multi-cycle object that has a "runnable" test and returns status (above) on each cycle
        VERB = "V"          # regular verb (default)
        
        def tostring(val):            # static print function
            match(val):
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
            match(mode):
                case Wye.mode.PARALLEL:
                    return "PARALLEL"
                case Wye.mode.SINGLE_CYCLE:
                    return "SINGLE_CYCLE"
                case Wye.mode.MULTI_CYCLE:
                    return "MULTI_CYCLE"
                case _:
                    return "--unknown mode value " + str(mode) + "--"

    # parallel completion rquirement
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

        def tostring(dataType):            # static print function
            match(dataType):
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

                case _:
                    return "--unknown data dType value " + str(dataType) + "--"

    # parameter access (how parameter is passed)
    class access:
        VALUE = 0
        REFERENCE = 1
        # decide if worth doing OUT = 2

        def tostring(access):            # static print function
            match(access):
                case Wye.dType.VALUE:
                    return "VALUE"
                case Wye.dType.REFERENCE:
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
            match(key):
                case Wye.ctlKyes.RIGHT:
                    return("RIGHT")
                case Wye.ctlKyes.LEFT:
                    return("LEFT")
                case Wye.ctlKyes.UP:
                    return("UP")
                case Wye.ctlKyes.DOWN:
                    return("DOWN")
                case Wye.ctlKyes.CTL_DOWN:
                    return("CTL_DOWN")
                case Wye.ctlKyes.CTL_UP:
                    return("CTL_UP")
                case Wye.ctlKyes.SHIFT_DOWN:
                    return("SHIFT_DOWN")
                case Wye.ctlKyes.SHIFT_UP:
                    return("SHIFT_UP")

    ###########################################################################
    #
    # Dynamic Wye Classes
    #
    # (instantiated like any normal class)
    #
    ###########################################################################

    # Code frame - for any verb defined by WyeCode rather than compiled Python
    # note: each variable is wrapped in its own list so that it can be passed
    # as a parameter by reference
    class codeFrame:      # Used by any verb with Wye code
        def __init__(self, verb, stack):
            self.verb = verb    # the static verb that we're holding runtime data for
            #print("codeFrame ", self, " for verb ", verb.__name__)
            self.params = []  # caller will fill in params
            try:
                if not hasattr(verb, "varDescr"):
                    print("verb",verb, " has no varDescr")
                #self.vars = [[varDef[2]] for varDef in verb.varDescr]  # create vars and fill with initial values
                self.vars = []
                for varDef in verb.varDescr:
                    if len(varDef) > 1:
                        self.vars.append([varDef[2]])
            except:
                print("ERROR Wye codeFrame: verb ", verb.__name__, " varDef failed to parse:", varDef, " in ", verb.varDescr)
            self.PC = 0         # used by async verbs to track location in executing code
            self.SP = stack      # points to stack list this frame is on
            if verb.mode == Wye.mode.MULTI_CYCLE or verb.mode == Wye.mode.PARALLEL:
                self.status = Wye.status.CONTINUE   # assume stay running
            else:
                self.status = Wye.status.SUCCESS    # assume good things
            self.debug = ""
            # print("codeFrame for verb", verb, " verb.varDescr =", verb.varDescr, " vars =", self.vars)

    # used by verbs that run parallel streams
    class parallelFrame(codeFrame): # used by any object with parallel execution (multiple stacks)
        def __init__(self, verb, stack):
            super().__init__(verb, stack)
            self.stacks = []        # callee must fill in empty lists for appropriate number of stacks

        # run the top of each parallel stack
        def runParallel(frame):
            dbgIx = 0
            status = Wye.status.CONTINUE  # assume we'll keep going
            foundFail = False
            foundSuccess = False
            foundContinue = False

            # DEBUG: print out all the stacks
            # print("parallel run: frame.stacks:")
            # for sIx in range(len(frame.stacks)):
            # print(" stack:", sIx, WyeCore.Utils.stackToString(frame.stacks[sIx]))

            # Each parallel code block has its own stack
            # Loop through each stack until termination conditions met (based on parTermType for parallel verb)
            delLst = []
            for stack in frame.stacks:

                # if there's a frame, there's something to do
                if len(stack) > 0:
                    f = stack[-1]  # grab the bottom frame

                    # if it's still running, run it again
                    if f.status == Wye.status.CONTINUE:
                        f.verb.run(f)
                        foundContinue = True

                    # if it terminated, if there's a parent, call it to clean up completed child
                    else:
                        # have a parent
                        if len(stack) > 1:
                            f = stack[-2]
                            f.verb.run(f)  # run parent (will test child status, remove from stack, and continue)
                            foundContinue = True  # technically we haven't checked, but we will next time
                        # no parent, atatus not CONTINUE, we're done with stream
                        else:
                            if f.status == Wye.status.FAIL:
                                foundFail = True
                            elif f.status == Wye.status.SUCCESS:
                                foundSuccess = True
                            else:
                                foundContinue = True
                            if (foundFail and frame.verb.parTermType == Wye.parTermType.FIRST_FAIL) or \
                                    (foundSuccess and frame.verb.parTermType == Wye.parTermType.FIRST_SUCCESS) or \
                                    ((
                                             foundFail or foundSuccess) and frame.verb.parTermType == Wye.parTermType.FIRST_ANY):
                                #print("stream complete with status ", f.status)
                                status = f.status
                                break;
                            # we're done with this stack, remove it
                            delLst.append(stack)
                    dbgIx += 1
                # remove empty stack
                else:
                    delLst.append(stack)
            # if there are completed streams, remove their stacks
            for stack in delLst:
                frame.stacks.remove(stack)

            # If we're done, figure out whether we succeeded or failed
            if status == Wye.status.CONTINUE and not foundContinue:  # all streams completed without triggering an exit
                if frame.verb.parTermType == Wye.parTermType.FIRST_FAIL:
                    #print("stream done, all succeeded")
                    status = Wye.status.SUCCESS  # FIRST_FAIL didn't have any failures - yay!
                else:
                    #print("stream done, all failed")
                    status = Wye.status.FAIL  # FIRST_SUCCESS and didn't have any successes - boo :-(
            frame.status = status  # return whatever status we have

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