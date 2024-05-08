# Wye TestLib2

from Wye import Wye
from WyeCore import WyeCore
from panda3d.core import *
from WyeUI import WyeUI
import inspect
#import partial
import traceback
import sys
from sys import exit
from direct.showbase import Audio3DManager

from direct.showbase.DirectObject import DirectObject

# test loading code from another library

class TestLib2:

    # Build run_rt methods on each class
    def build():
        WyeCore.Utils.buildLib(TestLib2)

    class crossCall:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.type.NONE
        paramDescr = ()     # takes arbitrary number of params.  Need to create a way to specify that
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(TestLib2.crossCall, stack)

        def run(frame):
            lib = WyeCore.World.libDict["TestLib"]
            f = lib.printParams.start()
            f.params = [["one"], [2], ["C"]]
            lib.printParams.run(f)


    class testObj3():
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.type.INTEGER
        paramDescr = ()    # gotta have a ret param
        #varDescr = (("a", Wye.type.NUMBER, 0), ("b", Wye.type.NUMBER, 1), ("c", Wye.type.NUMBER, 2))
        varDescr = (("txtObj", Wye.type.OBJECT, None),("3dTxtObj", Wye.type.OBJECT, None),
                    ("val", Wye.type.INTEGER, 0))

        class testObj3Callback:
            pass

        def start(stack):
            return Wye.codeFrame(TestLib2.testObj3, stack)

        def run(frame):
            global base
            global render

            match frame.PC:
                case 0:
                    # cross call to other library
                    ll = WyeCore.World.libObj
                    f = ll.TestLib.wyePrint.start(frame.SP)
                    f.params = [["The number two="], [2], [". Cool, huh?"]]
                    f.verb.run(f)

                    print(WyeCore.Utils.paramsToString(f))

                    txt = WyeCore.Utils.genTextObj("Text String 1", (1,0,0,1))

                    txt.setText("Text String 2")

                    #txt.setTextColor(1,0,0,1)
                    frame.vars[0][0] = txt

                    #txt3d = render.attach_new_node(txt)
                    #txt3d = WyeCore.Utils.gen3dTextObj(txt)     # this kills the ability to change text

                    txt3d = WyeCore.Utils.gen3dTextObj(txt, (-.5, 17, 2), (.2, .2, .2))
                    frame.vars[1][0] = txt3d

                    # get text node from path and set text
                    txt3d.node().setText("Text String 3")

                    #txtFroPath = txt3d.node()
                    #print("txtFroPath == txt", txtFroPath == txt)
                    #txtFroPath.setText("How about this one?")

                    #txt3d.reparentTo(render)
                    #txt3d.setScale(.2, .2, .2)

                    #txt.setText("Text String 4")

                    #txt3d.setPos(-.5, 17, 2)

                    #txt.setText("Text String 5n 5 5 5")

                    txt3d.setBillboardPointWorld(0.)

                    #WyeCore.picker.makePickable(txt3d)
                    #tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
                    #txt3d.setTag("wyeTag", tag)

                    print("testObj3 go to case 1")

                    frame.PC += 1

                case 1:
                    text = frame.vars[0][0]
                    text3d = frame.vars[1][0]

                    print("testObj3 case 1")
                    #text.setText("Text String 6")
                    frame.vars[2][0] += 1

                    frame.PC += 1

                case 2:


                    pass

        def keyFunc(keyName):
            print("keyFunc: key ", keyName)