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
            match frame.PC:
                case 0:
                    #print("waitClick: set event for tag ", frame.params.tag[0])
                    WyeCore.World.setEventCallback("click", frame.params.tag[0], frame)
                    frame.PC += 1
                    #print("waitClick: waiting for event 'click' tag ", frame.params.tag[0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    #print("waitClick: clicked on obj ", frame.eventData[0])
                    frame.status = Wye.status.SUCCESS


    # Wait for user to type a character
    # caller puts unique wyeTag waitChar param[0]
    # caller pushes waitChar frame on stack and updates frame.PC to state it wants to go to when click happens
    # When click event happens, caller must pop waitChar frame off stack
    # char is returned as function value
    class waitChar:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("char", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),)
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.waitChar, stack)

        # TODO - make multi-cycle
        def run(frame):
            match frame.PC:
                case 0:
                    #print("waitChar: set event for tag ", frame.params.tag[0])
                    WyeCore.World.setEventCallback("key", frame.params.tag[0], frame)
                    frame.PC += 1
                    #print("waitChar: waiting for event 'key' tag ", frame.params.tag[0])
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    #print("waitChar: clicked on obj tag ", frame.eventData[0], " returned ", frame.eventData[1])
                    getattr(frame.params, frame.firstParamName())[0] = frame.eventData[1]     # return character
                    frame.status = Wye.status.SUCCESS



    # Wait for user to type a character
    # caller puts unique wyeTag waitChar param[0]
    # caller pushes waitChar frame on stack and updates frame.PC to state it wants to go to when click happens
    # When click event happens, caller must pop waitChar frame off stack
    # char is returned as function value
    class waitText:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("ret", Wye.dType.STRING, Wye.access.REFERENCE),
                      ("tag", Wye.dType.STRING, Wye.access.REFERENCE),)
        varDescr = (("cursorPos", Wye.dType.INTEGER, 0),)
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.waitChar, stack)

        # TODO - make multi-cycle
        def run(frame):
            match frame.PC:
                case 0:
                    frame.PC = 2    # go start the wait loop
                case 1:
                    pass
                    # do nothing until event occurs

                case 2:
                    #print("waitChar: clicked on obj tag ", frame.eventData[0], " returned ", frame.eventData[1])
                    if hasattr(frame, "eventData"):     # skip first time through
                        getattr(frame.params, frame.firstParamName())[0][frame.vars.cursorPos[0]] = frame.eventData[1]
                        frame.vars.cursorPos[0] += 1

                        # eventually want to check for delete key (remove previous char), left/right arrow keys, and return (done)

                    # start waiting for a char
                    frame.PC = 1        # go back for another character
                    WyeCore.World.setEventCallback("key", frame.params.tag[0], frame)
                    #frame.status = Wye.status.SUCCESS


    # load model passed in at loc, scale passed in
    class loadObject:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("objFrm", Wye.dType.OBJECT, Wye.access.REFERENCE),       # parent frame to associate obj with
                      ("gObj", Wye.dType.OBJECT, Wye.access.REFERENCE),         # graphic object returned
                      ("file", Wye.dType.STRING, Wye.access.REFERENCE),         # file to load graphic from
                      ("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # position to place graphic
                      ("rotVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # YPR angles to orient graphic
                      ("scaleVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # scale to apply to object
                      ("tag", Wye.dType.STRING_LIST, Wye.access.REFERENCE),     # returned tag assigned to graphic object
                      ("colorVec", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE)) # color to assign to object
        varDescr = ()
        codeDescr = (
            #(None, "print('test inline code')"),
            # call loadModel with testLoader params 0 and 1
            ("WyeCore.libs.WyeLib.loadModel", (None, "frame.params.gObj"), (None, "frame.params.file")),
            #(None, "print('loadObject frame.params.gObj', frame.params.gObj)"),
            ("WyeCore.libs.WyeLib.makePickable", (None, "frame.params.tag"), (None, "frame.params.gObj")),
            (None, "WyeCore.World.registerObjTag(frame.params.tag[0], frame.params.objFrm[0])"),
            ("WyeCore.libs.WyeLib.setObjAngle", (None, "frame.params.gObj"), (None, "frame.params.rotVec")),
            ("WyeCore.libs.WyeLib.setObjMaterialColor", (None, "frame.params.gObj"), (None, "frame.params.colorVec")),
            ("WyeCore.libs.WyeLib.showModel", (None, "frame.params.gObj"), (None, "frame.params.posVec"), (None, "frame.params.scaleVec"))
        )

        def build():
            return WyeCore.Utils.buildCodeText("loadObject", WyeLib.loadObject.codeDescr)

        def start(stack):
            return Wye.codeFrame(WyeLib.loadObject, stack)

        def run(frame):
            WyeLib.WyeLib_rt.loadObject_run_rt(frame)


    # load Panda3d model
    # p0 - returned model
    # p1 - file path to model
    class loadModel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),      # return param
                      ("objectFileName", Wye.dType.STRING, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.loadModel, stack)

        def run(frame):
            global base

            filepath = frame.params.objectFileName[0]
            # full path minus drive letter
            path = WyeCore.Utils.resourcePath(filepath)[2:]
            #path = filepath
            #path = "C/Users/ebeng/PycharmProjects/Wye/flyer_01.glb"
            try:
                #print("Load graphic model ", path)
                model = base.loader.loadModel(path)
                if model:
                    getattr(frame.params, frame.firstParamName())[0] = model
                else:
                    frame.status = Wye.status.FAIL
            except:
                print("WyeLib loadModel: failed to load model ", path)
                frame.status = Wye.status.FAIL
                #ex = sys.exception()
                #traceback.print_exception(ex)

    # make this object pickable
    # return object id string
    class makePickable:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.INTEGER
        paramDescr = (("id", Wye.dType.STRING, 0),     # return object id string
                      ("loadedObject", Wye.dType.OBJECT, Wye.access.REFERENCE))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.makePickable, stack)

        def run(frame):
            global base

            obj = frame.params.loadedObject[0]
            # if the object already has a tag, we're done, return it
            tag = obj.getTag('wyeTag')
            # if no tag, then create one and make the object pickable
            if not tag:
                tag = "wyeTag" + str(WyeCore.Utils.getId())     # generate unique tag for object
                obj.setTag("wyeTag", tag)
            WyeCore.picker.makePickable(obj)                # just be sure it's pickable
            frame.params.id[0] = tag                        # return tag to caller

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

            model = frame.params.object[0]
            pos = frame.params.position[0]
            scale = frame.params.scale[0]
            #tag = frame.params.tag[0]
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
            gObj = frame.params.obj[0]
            vec = frame.params.posVec[0]

            #print("setObjPos set obj", gObj, "to", vec)
            gObj.setPos(vec[0], vec[1], vec[2])

    # set model pos rel to model orientation
    class setObjRelPos:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                     ("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjRelPos, stack)

        def run(frame):
            #print("setObjRelPos run: params ", frame.params)
            gObj = frame.params.obj[0]
            vec = frame.params.posVec[0]
            #print("setObjRelPos set obj", gObj, "to", vec)
            gObj.setPos(gObj, vec[0], vec[1], vec[2])

    # get model pos
    class getObjPos:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("posVec", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),
                      ("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                    )
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjPos, stack)

        def run(frame):
            #print("getObjPos run: params ", frame.params)
            gObj = frame.params.obj[0]
            pos = gObj.getPos()
            #print("getObjPos get obj pos", gObj, " ", pos)

            frame.params.posVec = [[pos[0], pos[1], pos[2] ]]


    # set object to given angle
    class setObjAngle:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("angle", Wye.dType.FLOAT_LIST, [0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjAngle, stack)

        # TODO - make multi-cycle
        def run(frame):
            #print('execute setObjAngle, params', frame.params, ' vars', frame.vars)

            gObj = frame.params.obj[0]
            vec = frame.params.angle[0]

            #hpr = frame.params.obj[0].getHpr()
            #print("Current HPR ", hpr)

            gObj.setHpr(vec[0], vec[1], vec[2])

            hpr = frame.params.obj[0].getHpr()
            #print("New HPR ", hpr)

        # set object to given angle

    class setObjRelAngle:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("angle", Wye.dType.FLOAT_LIST, [0, 0, 0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjRelAngle, stack)

        # TODO - make multi-cycle
        def run(frame):
            # print('execute setObjRelAngle, params', frame.params, ' vars', frame.vars)

            gObj = frame.params.obj[0]
            vec = frame.params.angle[0]

            # hpr = frame.params.obj[0].getHpr()
            # print("Current HPR ", hpr)

            #print("setObjRelAngle obj", gObj, "to", vec)
            gObj.setHpr(gObj, vec[0], vec[1], vec[2])

            hpr = frame.params.obj[0].getHpr()
            # print("New HPR ", hpr)



    # return object current angle
    class getObjAngle:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("angle", Wye.dType.FLOAT_LIST, [0,0,0]),
                      ("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      )
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.getObjAngle, stack)

        # TODO - make multi-cycle
        def run(frame):
            #print('execute getObjAngle, params', frame.params, ' vars', frame.vars)

            gObj = frame.params.obj[0]
            angle = gObj.getHpr()
            frame.params.angle = [[angle[0], angle[1], angle[2]]]

            #hpr = frame.params.obj[0].getHpr()
            #print("getObjAngle: HPR", hpr)

    # set object to given color (r,g,b,a, values 0..1.0)
    class setObjColor:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("color", Wye.dType.FLOAT_LIST, [0,0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjColor, stack)

        def run(frame):
            gObj = frame.params.obj[0]
            color = frame.params.color[0]
            #print("setObjColor: setColor obj", gObj, "to", color)
            gObj.setColor(color[0], color[1], color[2], color[3])



    # set object wityh material to given color (r,g,b,a, values 0..1.0)
    class setObjMaterialColor:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("obj", Wye.dType.OBJECT, Wye.access.REFERENCE),
                      ("color", Wye.dType.FLOAT_LIST, [0,0,0,0]))
        varDescr = ()
        codeDescr = ()
        code = None

        def start(stack):
            return Wye.codeFrame(WyeLib.setObjMaterialColor, stack)

        def run(frame):
            gObj = frame.params.obj[0]
            color = frame.params.color[0]
            #print("setObjMaterialColor obj", gObj, "to", color)
            mat = Material()
            mat.setShininess(5.0)  # Make this material shiny
            mat.setAmbient((color[0], color[1], color[2], color[3]))  # Make this material blue
            mat.setDiffuse((color[0], color[1], color[2], color[3]))  # Make this material blue
            gObj.setMaterial(mat, 1)


    class delay:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.NONE
        paramDescr = (("startCt", Wye.dType.INTEGER), Wye.access.REFERENCE)
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
                    frame.vars.delayCt[0] = frame.params.startCt[0]   # set start count
                    frame.PC += 1

                case 1:
                    if frame.vars.delayCt[0] > 0:
                        frame.vars.delayCt[0] -= 1
                    else:
                        #print("delay done")
                        frame.status = Wye.status.SUCCESS

    # put value into var
    class setEqual:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.ANY
        paramDescr = (("var", Wye.dType.ANY, Wye.access.REFERENCE),
                      ("value", Wye.dType.ANY, None))
        varDescr = ()

        def start(stack):
            return Wye.codeFrame(WyeLib.setEqual, stack)

        def run(frame):
            frame.params.var[0] = frame.params.value[0]

