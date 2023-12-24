
# Wye globals

# static Wye object (not instantiated)
# contains constants (static classes)
#    structures (regular classes)
#    and factories (lib, obj)

# Wye container class that holds Wye classes
class Wye:

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

    # base class for static python objects (libs, objs, verbs)
    # Only reason for existing it to complain if someone tries to instantiate the object!!
    class staticObj:
        def __init__(self):
            print("Wye Error - attempting to instantiate a static object!")
            # if this happens a lot, maybe do an exit(1)
            # it would be cool to put code in every child object to identify which obj is being instantiated - once
            # the editor is fully running.

    # convenient library holder
    class libs:
        pass

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

    # verb modes
    class mode:
        FUNCTION = "F"      # single cycle function that immediately returns a value of a predefined type (see type)
        SINGLE_CYCLE = "S"  # single cycle subroutine runs immediately and doesn't return a value
        MULTI_CYCLE = "M"   # multi-cycle subroutine that returns status (see above) on each cycle
        OBJECT = "O"        # multi-cycle object that has a "runnable" test and returns status (above) on each cycle


        def tostring(mode):            # static print function
            match(mode):
                case Wye.mode.FUNCTION:
                    return "FUNCTION"
                case Wye.mode.SINGLE_CYCLE:
                    return "SINGLE_CYCLE"
                case Wye.mode.MULTI_CYCLE:
                    return "MULTI_CYCLE"
                case Wye.mode.OBJECT:
                    return "OBJECT"
                case _:
                    return "--unknown mode value " + str(mode) + "--"

    # Data types
    class type:
        NONE = "Z"
        ANY = "A"
        NUMBER = "N"
        INTEGER = "I"
        FLOAT = "F"
        BOOL = "B"
        OBJECT = "O"
        STRING = "S"
        ANY_LIST = "AL"
        NUMBER_LIST = "NL"
        INTEGER_LIST = "IL"
        FLOAT_LIST = "FL"
        BOOL_LIST = "BL"
        OBJECT_LIST = "OL"
        STRING_LIST = "SL"

        def tostring(dataType):            # static print function
            match(dataType):
                case Wye.type.NONE:
                    return "NONE"
                case Wye.type.ANY:
                    return "ANY"
                case Wye.type.NUMBER:
                    return "NUMBER"
                case Wye.type.INTEGER:
                    return "INTEGER"
                case Wye.type.FLOAT:
                    return "FLOAT"
                case Wye.type.BOOL:
                    return "BOOL"
                case Wye.type.OBJECT:
                    return "OBJECT"
                case Wye.type.STRING:
                    return "STRING"
                case Wye.type.ANY_LIST:
                    return "NUMBER_LIST"
                case Wye.type.ANY_LIST:
                    return "NUMBER_LIST"
                case Wye.type.INTEGER_LIST:
                    return "INTEGER_LIST"
                case Wye.type.FLOAT_LIST:
                    return "FLOAT_LIST"
                case Wye.type.BOOL_LIST:
                    return "BOOL_LIST"
                case Wye.type.OBJECT_LIST:
                    return "OBJECT_LIST"
                case Wye.type.STRING_LIST:
                    return "STRING_LIST"

                case _:
                    return "--unknown data type value " + str(dataType) + "--"

    # parameter access (how parameter is passed)
    class access:
        VALUE = 0
        REFERENCE = 1
        # decide if worth doing OUT = 2

        def tostring(access):            # static print function
            match(access):
                case Wye.type.VALUE:
                    return "VALUE"
                case Wye.type.REFERENCE:
                    return "REFERENCE"
                #case Wye.type.OUT:
                #    return "OUT"
                case _:
                    return "--unknown access value " + str(access) + "--"


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
            self.stack = stack  # exec stack
            self.verb = verb    # the static verb that we're holding runtime data for
            self.params = []  # caller will fill in params
            self.vars = [[varDef[2]] for varDef in verb.varDescr]  # create vars and fill with initial values
            self.PC = 0        # used by async verbs to track location in executing code
            self.debug = ""
            # print("codeFrame for verb", verb, " verb.varDescr =", verb.varDescr, " vars =", self.vars)

    class objFrame(codeFrame):   # Used by any object with its own exec
        def __init__(self, verb):
            super().__init__(verb)
            self.stack = []

    class parallelFrame(codeFrame): # used by any object with parallel execution (multiple stacks)
        def __init__(self, verb):
            super().__init__(verb)
            self.stacks = []        # callee must fill in empty lists for appropriate number of stacks

    # object template class for editing new Wye objects
    # note that this object will be used as the template for creating a new
    # class object in the library currently being edited
    class WyeObjTemplate:
        def __init__(self):
            self.library = None
            self.mode = Wye.mode.OBJECT
            self.type = ""
            self.params = ()
            self.vars = ()


    ###########################################################################
    #
    # Static Parameter Functions
    #
    ###########################################################################

    # return the next item in the code stream
    def getImmediate(frame, code):
        frame.PC += 1
        return code[frame.PC]

    def getParamConstVal(code):
        pass

    def getParamVarArrayVal(code):
        pass

    ###########################################################################
    # The main Wye class
    # fill in global objects
    ###########################################################################
    def __init__(self):
        self.currWorld = None  # the universe
        self.picker = None  # 3d object picker
        self.textBgnd = None  # Text background geom reffed by all text



# if Wye UI is not already running, start it?