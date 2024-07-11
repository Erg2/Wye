
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
                    self.vars.append([varDef[2]])
            except:
                print("ERROR Wye codeFrame: verb ",verb.__name__," varDef failed to parse:", varDef, " in ", verb.varDescr)
            self.PC = 0         # used by async verbs to track location in executing code
            self.SP = stack      # points to stack list this frame is on
            if verb.mode == Wye.mode.MULTI_CYCLE or verb.mode == Wye.mode.PARALLEL:
                self.status = Wye.status.CONTINUE   # assume stay running
            else:
                self.status = Wye.status.SUCCESS    # assume good things
            self.debug = ""
            # print("codeFrame for verb", verb, " verb.varDescr =", verb.varDescr, " vars =", self.vars)

    class parallelFrame(codeFrame): # used by any object with parallel execution (multiple stacks)
        def __init__(self, verb, stack):
            super().__init__(verb, stack)
            self.stacks = []        # callee must fill in empty lists for appropriate number of stacks

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