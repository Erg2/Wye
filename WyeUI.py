# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging

class WyeUI(Wye.staticObj):

    # dialog framework
    # success = OK button, fail = Cancel button
    class wyeDialog(Wye.staticObj):
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()
        varDescr = (("gObj", Wye.type.OBJECT, None),
                    ("children", Wye.type.ANY_LIST, []),    # list of child frames
                    ("callbacks", Wye.type.ANY_LIST, []))   # list of

        def start(stack):
            return Wye.codeFrame(WyeUI.wyeDialog, stack)
            # TODO create graphic object billboard

        # set position of our dialog object
        def setPos(frame, pos):
            frame.vars[0][0].setPos(pos[0], pos[1], pos[2])

        # add child to our dialog at [x,y]
        def addChild(frame, childFrame, xyOffset):
            pass

        def run(frame):
            pass
