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
        WyeCore.Utils.buildLib(WyeLib)


    # Wait for click on graphic object
    # caller puts wyeTag of graphic obj in waitClick param[0]
    # caller pushes waitClick frame on stack and updates frame.PC to state it wants to go to when click happens
    # When click event happens, caller must pop waitClick frame off stack
    class waitClick:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("tag", Wye.dType.STRING, Wye.access.REFERENCE),)
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
                    #print("waitClick: clicked on obj ", frame.eventData[0])
                    frame.status = Wye.status.SUCCESS



    # load Panda3d model
    # p0 - returned model
    # p1 - file path to model
    class loadModel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("loadedObject", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("objectFileName", Wye.dType.STRING, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.loadModel, stack)

        def run(frame):
            global base

            filepath = frame.params[1][0]
            # full path minus drive letter
            path = WyeCore.Utils.resourcePath(filepath)[2:]
            #path = filepath
            #path = "C/Users/ebeng/PycharmProjects/Wye/flyer_01.glb"
            try:
                #print("Load graphic model ", path)
                model = base.loader.loadModel(path)
                if model:
                    frame.params[0][0] = model
                else:
                    frame.status = Wye.status.FAIL
            except:
                print("WyeLib loadModel: failed to load model ", path)
                frame.status = Wye.status.FAIL
                #ex = sys.exception()
                #traceback.print_exception(ex)

    # make this object pickable
    class makePickable:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.INTEGER
        paramDescr = (("returnId", Wye.dType.STRING, 0), ("loadedObject", Wye.dType.OBJECT, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.makePickable, stack)

        def run(frame):
            global base

            obj = frame.params[1][0]
            # if the object already has a tag, we're done, return it
            tag = obj.getTag('wyeTag')
            # if no tag, then create one and make the object pickable
            if not tag:
                tag = "wyeTag" + str(WyeCore.Utils.getId())     # generate unique tag for object
                obj.setTag("wyeTag", tag)
            WyeCore.picker.makePickable(obj)                # just be sure it's pickable
            frame.params[0][0] = tag                        # return tag to caller

    class showModel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("object", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE),
                      ("scale", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE),
                     # ("tag", Wye.dType.STRING, Wye.access.REFERENCE)
                      )
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.showModel, stack)

        def run(frame):
            global render     # panda3d base

            model = frame.params[0][0]
            pos = frame.params[1]
            scale = frame.params[2]
            #tag = frame.params[3][0]
            #print("showModel pos ", pos, " scale ", scale) #, " tag ", tag)
            model.reparentTo(render)
            model.setScale(scale[0], scale[1], scale[2])
            model.setPos(pos[0], pos[1], pos[2])
            #model.setTag('wyeTag', tag)

    # set model pos
    class setObjPos:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                    ("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjPos, stack)

        def run(frame):
            #print("setObjPos run: params ", frame.params)
            gObj = frame.params[0][0]
            vec = frame.params[1]
            #print("setObjPos set obj", gObj, "to", vec)
            gObj.setPos(vec[0], vec[1], vec[2])

    # set object to given angle
    class setObjAngle:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),("angle", Wye.dType.FLOAT_LIST, [0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjAngle, stack)

        # TODO - make multi-cycle
        def run(frame):
            #print('execute setObjAngle, params', frame.params, ' vars', frame.vars)

            gObj = frame.params[0][0]
            vec = frame.params[1]

            #hpr = frame.params[0][0].getHpr()
            #print("Current HPR ", hpr)

            #print("setObjAngle obj", gObj, "to", vec)
            gObj.setHpr(vec[0], vec[1], vec[2])

            hpr = frame.params[0][0].getHpr()
            #print("New HPR ", hpr)


    # set object to given color (r,g,b,a, values 0..1.0)
    class setObjColor:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),("color", Wye.dType.FLOAT_LIST, [0,0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjColor, stack)

        def run(frame):
            gObj = frame.params[0][0]
            color = frame.params[1]
            #print("setColor obj", gObj, "to", color)
            gObj.setColor(color[0], color[1], color[2], color[3])



    # set object wityh material to given color (r,g,b,a, values 0..1.0)
    class setObjMaterialColor:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),("color", Wye.dType.FLOAT_LIST, [0,0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjMaterialColor, stack)

        def run(frame):
            gObj = frame.params[0][0]
            color = frame.params[1]
            #print("setMaterialColor obj", gObj, "to", color)
            mat = Material()
            mat.setShininess(5.0)  # Make this material shiny
            mat.setAmbient((color[0], color[1], color[2], color[3]))  # Make this material blue
            mat.setDiffuse((color[0], color[1], color[2], color[3]))  # Make this material blue
            gObj.setMaterial(mat, 1)


    class delay:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("startCt", Wye.dType.INTEGER),)
        varDescr = (("delayCt", Wye.dType.INTEGER, 0),)
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.delay, stack)

        # TODO - make multi-cycle
        def run(frame):
            match frame.PC:
                case 0:
                    #print('execute delay, params', frame.params, ' vars', frame.vars)
                    frame.vars[0][0] = frame.params[0][0]   # set start count
                    frame.PC += 1

                case 1:
                    if frame.vars[0][0] > 0:
                        frame.vars[0][0] -= 1
                    else:
                        #print("delay done")
                        frame.status = Wye.status.SUCCESS


