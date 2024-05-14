# Wye WyeLib
# Base Weye word dictionary

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


class WyeLib:

    # Build run_rt methods on each class
    def build():
        print("Hi from WyeLib")
        WyeCore.Utils.buildLib(WyeLib)


    class parallelFailAny:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = (("stackList", Wye.type.OBJECT, []),)        # stacks used by parallel words
        codeDescr = ()
        code = None

        def start(stack):
            f = Wye.codeFrame(WyeLib.parallelFailAny, stack)

            return f

        # TODO - make multi-cycle
        def run(frame):
            pass

    # Wait for click on graphic object
    # caller puts wyeTag of graphic obj in waitClick param[0]
    # caller pushes waitClick frame on stack and updates frame.PC to state it wants to go to when click happens
    # When click event happens, caller must pop waitClick frame off stack
    class waitClick:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.NONE
        paramDescr = (("obj", Wye.type.OBJECT, Wye.access.REFERENCE),)
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.waitClick, stack)

        # TODO - make multi-cycle
        def run(frame):
            #print('execute spin, params', frame.params, ' vars', frame.vars)
            match frame.PC:
                case 0:
                    #print("waitClick: set event for tag ", frame.params[0][0])
                    WyeCore.World.setEventCallback("click", frame.params[0][0], frame)
                    frame.PC += 1
                    #print("waitClick: waiting for event 'click' tag ", frame.params[0][0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    #print("waitClick: click on obj ", frame.eventData[0])
                    frame.status = Wye.status.SUCCESS

