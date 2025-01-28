# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *
from panda3d.core import LVector3f
#from functools import partial
#import traceback
#import sys
#from sys import exit

#for 3d geometry (input cursor)
#from direct.showbase.ShowBase import ShowBase

from functools import partial

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MouseButton

# from https://github.com/Epihaius/procedural_panda3d_model_primitives
from sphere import SphereMaker

#import pygame.midi
#import time


# 3d UI element library
class WyeUI(Wye.staticObj):
    LINE_HEIGHT = 1.25
    TEXT_SCALE = (.2,.2,.2)

    dragFrame = None    # not currently dragging anything
    dragOffset = (0,0,0)   # mouse position at drag downclick

    class _ball:
        def __init__(self, radius, pos=[0,0,0]):
            # see https: // github.com / Epihaius / procedural_panda3d_model_primitives
            self.radius = radius
            ballBuilder = SphereMaker(radius=radius)
            self.node = ballBuilder.generate()
            if self.node:
                self.path = render.attachNewNode(self.node)
                self.path.setPos(pos[0], pos[1], pos[2])
            else:
                print("WyeUI _ball: SphereMaker didn't")

        def removeNode(self):
            self._nodePath.removeNode()

        def setColor(self, val):
            self._nodePath.setColor(val)

        def setScale(self, val):
            self._nodePath.setScale(val)

        def setPos(self, val):
            self._nodePath.setPos(val)

        def setTag(self, tag):
            self.node.setTag("wyeTag", tag)

        def getColor(self):
            return self._nodePath.getColor()

        def getNodePath(self):
            return self._nodePath

        def getPos(self):
            return self._nodePath.getPos()

        def getScale(self):
            return self._nodePath.getScale()

        def getTag(self):
            return self.node.getTag()

        def getHeight(self):
            return self.radius

        def getWidth(self):
            return self.radius


        def show(self):
            self._nodePath.show()
        def hide(self):
            self._nodePath.hide()

    # create a scaled rectangular prism
    # (primarily used for InputText cursor)
    # NOTE: this class gets instantiated
    class _box:

        def __init__(self, size, pos=[0,0,0], parent=None):
            # Instantiate a vertex buffer
            # https://stackoverflow.com/questions/75774821/how-to-create-three-dimensional-geometric-shapes-in-panda3d-in-python
            # https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-vertex-data
            format = GeomVertexFormat.getV3c4()
            format = GeomVertexFormat.registerFormat(format)
            vdata = GeomVertexData("name", format, Geom.UHStatic)
            vertex = GeomVertexWriter(vdata, "vertex")
            color = GeomVertexWriter(vdata, "color")
            self.size = size

            # Add vertices and colors
            vertex.addData3f(-1*size[0], -1*size[1], -1*size[2])
            color.addData4f(0, 0, 0, 1)

            vertex.addData3f(-1*size[0], -1*size[1], 1*size[2])
            color.addData4f(0, 0, 1, 1)

            vertex.addData3f(-1*size[0], 1*size[1], -1*size[2])
            color.addData4f(0, 1, 0, 1)

            vertex.addData3f(-1*size[0], 1*size[1], 1*size[2])
            color.addData4f(0, 1, 1, 1)

            vertex.addData3f(1*size[0], -1*size[1], -1*size[2])
            color.addData4f(1, 0, 0, 1)

            vertex.addData3f(1*size[0], -1*size[1], 1*size[2])
            color.addData4f(1, 0, 1, 1)

            vertex.addData3f(1*size[0], 1*size[1], -1*size[2])
            color.addData4f(1, 0, 1, 1)

            vertex.addData3f(1*size[0], 1*size[1], 1*size[2])
            color.addData4f(1, 1, 1, 1)

            # Create the triangles (2 per face)
            # https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-primitives
            prim = GeomTriangles(Geom.UHStatic)
            prim.addVertices(0, 1, 2)
            prim.addVertices(2, 1, 3)
            prim.addVertices(2, 3, 6)
            prim.addVertices(6, 3, 7)
            prim.addVertices(6, 7, 4)
            prim.addVertices(4, 7, 5)
            prim.addVertices(4, 5, 0)
            prim.addVertices(0, 5, 1)
            prim.addVertices(1, 5, 3)
            prim.addVertices(3, 5, 7)
            prim.addVertices(6, 4, 2)
            prim.addVertices(2, 4, 0)

            geom = Geom(vdata)
            geom.addPrimitive(prim)
            self.node = GeomNode("node")
            self.node.addGeom(geom)

            self._nodePath = render.attachNewNode(self.node)
            if parent:
                self._nodePath.reparentTo(parent)
            self._nodePath.setPos(pos[0], pos[1], pos[2])


        def removeNode(self):
            self._nodePath.removeNode()

        def setColor(self, val):
            self._nodePath.setColor(val)

        def setScale(self, val):
            self._nodePath.setScale(val)

        def setPos(self, *args):
            self._nodePath.setPos(args)

        def setTag(self, tag):
            return self.node.setTag("wyeTag", tag)

        def show(self):
            self._nodePath.show()
        def hide(self):
            self._nodePath.hide()

        def getColor(self):
            return self._nodePath.getColor()

        def getNodePath(self):
            return self._nodePath

        def getPos(self):
            return self._nodePath.getPos()

        def getScale(self):
            return self._nodePath.getScale()

        def getTag(self):
            return self.text.name

        def getHeight(self):
            return self.size[2]

        def getTag(self):
            return self.node.getTag()

        def getWidth(self):
            return self.size[0]

    # create a scaled surface from a point grid
    # NOTE: this class gets instantiated
    class _surf:

        def __init__(self, data, size, pos=[0,0,0], colorFn=None):
            # Instantiate a vertex buffer
            format = GeomVertexFormat.getV3c4()
            format = GeomVertexFormat.registerFormat(format)
            vdata = GeomVertexData("name", format, Geom.UHStatic)
            vertex = GeomVertexWriter(vdata, "vertex")
            color = GeomVertexWriter(vdata, "color")

            self.colorFn = colorFn

            vtxColors = (
            (0, 0, 0, 1),
            (0, 0, 1, 1),
            (0, 1, 0, 1),
            (0, 1, 1, 1),
            (1, 0, 0, 1),
            (1, 0, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 1, 1),
            )

            # Add vertices and colors
            cIx = 0     # vertex color index
            xLen = len(data)
            yLen = len(data[0])
            #print("gen surface xLen", xLen, " by yLen", yLen)

            #for yy in range(yLen):
            #    print(data[yy])

            dMin = 100000
            dMax = -100000
            for yy in range(yLen):
                for xx in range(xLen):
                    if data[yy][xx] < dMin:
                        dMin = data[yy][xx]
                    if data[yy][xx] > dMax:
                        dMax = data[yy][xx]
            dRange = dMax - dMin
            colorStep = 1 / dRange
            #print("data min", dMin, " max", dMax, " range", dRange, " step", colorStep)
            # gen points
            for yy in range( yLen):
                for xx in range(xLen):
                    #print("data[",yy,"][",xx,"]", data[yy][xx])
                    vertex.addData3f(xx*size[0], yy*size[1], data[yy][xx]*size[2])
                    if True: #colorFn:
                        #r, g, b, a = colorFn(xx, yy, data[yy][xx]*size[2])
                        a = 1
                        g = b = 0
                        r = (data[yy][xx] - dMin) * colorStep
                        #print("data[", yy, "][", xx, "]", data[yy][xx], " color", r)
                        color.addData4f(r, g, b, a)
                    else:
                        color.addData4f(vtxColors[cIx][0], vtxColors[cIx][1], vtxColors[cIx][2], vtxColors[cIx][3])
                    cIx += 1
                    cIx = cIx % 8

            # gen triangles
            prim = GeomTriangles(Geom.UHStatic)
            for yy in range(yLen - 1):
                for xx0 in range(xLen - 1):
                    xx1 = xx0+1
                    yy0 = yy*xLen
                    yy1 = (yy+1)*xLen
                    #print("xx0", xx0, " xx1", xx1, " yy0", yy0, " yy1", yy1)
                    prim.addVertices(xx0 + yy0, xx1 + yy0, xx1 + yy1)
                    prim.addVertices(xx0 + yy0, xx1 + yy1, xx0 + yy1)

            geom = Geom(vdata)
            geom.addPrimitive(prim)
            node = GeomNode("node")
            node.addGeom(geom)

            self.node = node

            self.path = render.attachNewNode(self.node)
            self.path.setPos(pos[0], pos[1], pos[2])


        def removeNode(self):
            self._nodePath.removeNode()

        def show(self):
            self._nodePath.show()

        def hide(self):
            self._nodePath.hide()

    # Build run_rt methods on each class in library
    def build():
        WyeCore.Utils.buildLib(WyeUI)

            
    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class _3dText:
        global render

        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1), parent=None, tag=""):
            if parent is None:
                self.parent = render
            else:
                self.parent = parent
            self.tag = tag          # if caller supplied, else will auto-gen unique tag
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.text = None
            self.card = None
            self._nodePath = None
            self.gFrame = None
            #
            self._genTextObj(text, color)
            #self._genCardObj()
            self._gen3dTextObj(pos, scale, bg)

            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameColor(0, 0, 1, 1)
            # txtNode.setFrameMargin(0.2, 0.2, 0.1, 0.1)

        ## setters

        def setAlign(self, ctr):
            self.text.setAlign(ctr)

        def setColor(self, color):
            self.text.setTextColor(color)
            self._regen3d()

        # update the frame color
        def setFrameColor(self, color):
            self._nodePath.setColor(color)

        # update the margin spacing
        def setFrameMargin(self, marginL, marginR, marginB, marginT):
            self.marginL = marginL
            self.marginR = marginR
            self.marginB = marginB
            self.marginT = marginT
            self._regen3d()

        def setPos(self, val):
            self._nodePath.setPos(val)

        def setScale(self, val):
            self._nodePath.setScale(val)

        # changing the text requires regenerating the background card and the 3d node
        def setText(self, text):
            self.text.setText(text)
            self._regen3d()

        def setWordWrap(self):
            return self.text.getWordwrap()

        ## getters

        def getAlign(self):
            return self.text.getAlign()

        def getColor(self):
            return self._nodePath.getColor()

        def getFrame(self):
            return self.gFrame

        def getHeight(self):
            return self.gFrame[3] - self.gFrame[2]

        def getFrameColor(self):
            return self._nodePath.getColor()

        # update the margin spacing
        def getFrameMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        def getNodePath(self):
            return self._nodePath

        def getPos(self):
            return self._nodePath.getPos()

        def getScale(self):
            return self._nodePath.getScale()

        def getTag(self):
            return self.text.name

        def getText(self):
            return self.text.getText()

        def getWidth(self):
            return self.gFrame[1] - self.gFrame[0]

        def getWordWrap(self):
            return self.text.setWordwrap()

        ## methods

        def show(self):
            self._nodePath.show()
        def hide(self):
            self._nodePath.hide()

        # rebuild card and path for updated text object
        def _regen3d(self):
            bg = self._nodePath.getColor()
            pos = self._nodePath.getPos()
            scale = self._nodePath.getScale()
            #self._genCardObj()                     # generate new card obj for updated text object
            self._nodePath.detachNode()            # detach 3d node path from old card
            self._gen3dTextObj(pos, scale, bg)     # make new 3d node path to new card

        # internal rtn to gen text object with unique wyeTag name
        def _genTextObj(self, text, color=(1,1,1,1)):
            if not self.tag:
                self.tag = "txt"+str(WyeCore.Utils.getId())
            self.text = TextNode(self.tag)
            if len(text) == 0:
                text = ' '
            self.text.setText(text)
            self.text.setTextColor(color)

        # internal rtn to gen 3d Card clickable background object
        #def _genCardObj(self):
        #    #print("initial txtNode frame ", self.text.getFrameActual())
        #    self.card = CardMaker("Txt Card")
        #    self.gFrame = self.text.getFrameActual()
        #    if self.gFrame[1] == 0:      # if empty frame
        #        self.gFrame[1] = 1
        #        self.gFrame[3] = 1
        #    #print("self.gFrame", self.gFrame)
        #    self.gFrame[0] -= self.marginL
        #    self.gFrame[1] += self.marginR
        #    self.gFrame[2] -= self.marginB
        #    self.gFrame[3] += self.marginT
        #    #print("initial adjusted self.gFrame", self.gFrame)
        #    self.card.setFrame(self.gFrame)

        # internal rtn to generate 3d (path) object to position, etc. the text
        def _gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self._nodePath = NodePath(self.text.generate())
            #self._nodePath = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            #self._nodePath.attachNewNode(self.text)
            #self._nodePath.setEffect(DecalEffect.make())        # glue text onto card
            self._nodePath.reparentTo(self.parent)


            WyeCore.picker.makePickable(self._nodePath)         # make selectable
            self._nodePath.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self._nodePath.setPos(pos[0], pos[1], pos[2])
            self._nodePath.setScale(scale)

     #       self._nodePath.setBillboardPointWorld(0.)           # always face the camera
     #       self._nodePath.setBillboardAxis()
            self._nodePath.setLightOff()                        # unaffected by world lighting
            self._nodePath.setColor(bg)

            if not self.gFrame:
                self.gFrame = self.text.getFrameActual()
                if self.gFrame[1] == 0:  # if empty frame
                    self.gFrame[1] = 1
                    self.gFrame[3] = 1
                # print("self.gFrame", self.gFrame)
                self.gFrame[0] -= self.marginL
                self.gFrame[1] += self.marginR
                self.gFrame[2] -= self.marginB
                self.gFrame[3] += self.marginT

        def removeNode(self):
            self._nodePath.removeNode()


    # text entry verb
    # todo - finish this
    class text3d:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.NUMBER
        paramDescr = (
            ("text", Wye.dType.STRING, Wye.access.REFERENCE),       # 0 - caller var updated with curr text
            ("pos", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE),  # 1 - position to put text3d at
            ("color", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 - color
            ("scale", Wye.dType.NUMBER_LIST, Wye.access.REFERENCE)  # 3 - scale
        )
        varDescr = (
            ("label", Wye.dType.OBJECT, None),          # 0 - label showing text
            ("labelID", Wye.dType.STRING, None),        # 1 - id of label for setting selected
            ("pos", Wye.dType.INTEGER_LIST, [0,0,0]),   # 2 - pos?
            ("text", Wye.dType.STRING, "---"),          # 3
            ("graphicID", Wye.dType.OBJECT, None)       # 4
           )   # var 4

        # np=loader.loadModel("jack") #load a model
        # #... do something
        # np.removeNode() #unload the model
        # loader.unloadModel(path)


        #def __init__(self, text="", color=(1, 1, 1, 1), pos=(0, 0, 0), scale=(1, 1, 1), bg=(0, 0, 0, 1)):
        #    label = WyeUI._3dText(text, color, pos, scale, bg)

    # This does more than camera control, it also triggers debugger and editor
    class CameraControl(DirectObject):
        def __init__(self):
            self.m1Down = False     # state
            self.m2Down = False
            self.m3Down = False

            self.shift = False
            self.ctl = False
            self.alt = False

            self.m1Pressed = False  # edge
            self.m2Pressed = False
            self.m3Pressed = False

            self.shiftPressed = False
            self.ctlPressed = False
            self.altPressed = False

            self.walk = False       # start off flying [not currently implemented]
            self.viewDir = (0, 1, 0)
            self.shift = False

            self.speed = .25
            self.rotRate = .5


        def mouseMove(self, x, y):
            global base

            self.m1Pressed = False  # edge
            self.m2Pressed = False
            self.m3Pressed = False

            self.shiftPressed = False
            self.ctlPressed = False
            self.altPressed = False

            # get mouse buttons and mouse-down start pos
            if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                if not self.m1Down:
                    self.m1Down = True
                    self.m1DownPos = (x, y)
                    self.m1DownRot = base.camera.getHpr()
                    self.m1Pressed = True
            else:
                self.m1Down = False
            if base.mouseWatcherNode.isButtonDown(MouseButton.two()):
                if not self.m2Down:
                    self.m2Down = True
                    self.m2DownPos = (x, y)
                    self.m2DownRot = base.camera.getHpr()
                    self.m2Pressed = True
            else:
                self.m2Down = False
            if base.mouseWatcherNode.isButtonDown(MouseButton.three()):
                if not self.m3Down:
                    self.m3Down = True
                    self.m3DownPos = (x, y)
                    self.m3DownRot = base.camera.getHpr()
                    self.m3Pressed = True
            else:
                self.m3Down = False

            # if anyone wants to know a mouse button was pressed
            if (self.m1Pressed or self.m2Pressed or self.m3Pressed) and len(WyeCore.World.mouseCallbacks) > 0:
                for callback in WyeCore.World.mouseCallbacks:
                    callback()

            # get shift key
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.shift()):
                if not self.shift:
                    self.shift = True
                    self.shiftPressed = True
            else:
                self.shift = False
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt()):
                if not self.alt:
                    self.alt = True
                    self.altPressed = True
            else:
                self.alt = False
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                if not self.ctl:
                    self.ctl = True
                    self.ctlPressed = True
            else:
                self.ctl = False

            if self.m1Pressed and self.ctl and self.alt:
                if not WyeCore.World.mainMenu:
                    WyeCore.World.mainMenu = WyeCore.World.startActiveObject(WyeCore.libs.WyeUI.MainMenuDialog)
                else:
                    print("Already have Wye Main Menu")

            # if don't have the edit menu and the user wants it, start it
            elif self.m1Pressed and self.shift and self.ctl:
                if not WyeCore.World.editMenu:
                    WyeCore.World.editMenu = WyeCore.World.startActiveObject(WyeCore.libs.WyeUI.EditMainDialog)
                    WyeCore.World.editMenu.eventData = ("", (0))
                else:
                    print("Already have editor")

            # if don't have the debug menu and the user wants it, start it
            elif self.m1Pressed and self.shift and self.alt:
                if not WyeCore.World.debugger:
                    WyeCore.World.debugger = WyeCore.World.startActiveObject(WyeCore.libs.WyeUI.DebugMainDialog)
                else:
                    print("Already have debugger")

            # if not dragging then moving
            # mouseY is fwd/back
            # mouseX is rotate left/right
            # shift mouseY is up/down
            # shift mouseX is slide left/right
            elif not Wye.dragging:

                # motion
                if self.m1Down:
                    # regular motion
                    if not self.shift:
                        # walk fwd/back (mouseY), turning l/r (mouseX)
                        camRot = base.camera.getHpr()
                        dx = -(x - self.m1DownPos[0]) * self.rotRate
                        base.camera.setHpr(camRot[0] + dx, camRot[1], camRot[2])

                        quaternion = base.camera.getQuat()
                        fwd = quaternion.getForward()

                        #fwd = LVector3f(fwd[0], fwd[1], 0)
                        quat = Quat()
                        quat.setFromAxisAngle(-90, LVector3f.up())
                        right = quat.xform(fwd)

                        base.camera.setPos(base.camera.getPos() + fwd * (y - self.m1DownPos[1]) * self.speed) # + right * (x - self.m1DownPos[0]) * self.speed)

                    else:
                        # tilt up/down (mouseY), slide left/right (mouseX)
                        camRot = base.camera.getHpr()
                        dy = (y - self.m1DownPos[1]) * self.rotRate
                        base.camera.setHpr(camRot[0], camRot[1] + dy, camRot[2])

                        quaternion = base.camera.getQuat()
                        fwd = quaternion.getForward()
                        fwd = LVector3f(fwd[0], fwd[1], 0)      # no roll
                        quat = Quat()
                        quat.setFromAxisAngle(-90, LVector3f.up())
                        right = quat.xform(fwd)

                        #up = LVector3f(0, 0, 1)
                        #base.camera.setPos(base.camera.getPos() + up * (y - self.m1DownPos[1]) * self.speed + right * (x - self.m1DownPos[0]) * self.speed)
                        base.camera.setPos(base.camera.getPos() + right * (x - self.m1DownPos[0]) * self.speed)


                # reset viewpoint
                elif self.m2Down:
                    if not self.shift:
                        base.camera.setPos(Wye.startPos[0], Wye.startPos[1], Wye.startPos[2])
                    base.camera.setHpr(0,0,0)


                # slide sideways and up
                elif self.m3Down:
                    #quaternion = base.camera.getQuat()
                    #fwd = quaternion.getForward()
                    #fwd = LVector3f(fwd[0], fwd[1], 0)  # no roll
                    #quat = Quat()
                    #quat.setFromAxisAngle(-90, LVector3f.up())
                    #right = quat.xform(fwd)
                    right = LVector3f(1,0,0)

                    up = LVector3f(0, 0, 1)
                    #base.camera.setPos(base.camera.getPos() + up * (y - self.m3DownPos[1]) * self.speed + right * (x - self.m3DownPos[0]) * self.speed)
                    base.camera.setPos(base.camera, up * (y - self.m3DownPos[1]) * self.speed + right * (x - self.m3DownPos[0]) * self.speed)


#                # rotate viewpoint
#                if self.m3Down:
#                    #print("CameraControl mouseMove: m1Down")
#                    camRot = base.camera.getHpr()
#                    dx = -(x - self.m3DownPos[0]) * self.rotRate
#                    if self.shift:
#                        dx = 0  # don't rotate while tilting
#                        dy = 0
#                        dz = (x - self.m3DownPos[0]) * self.rotRate
#                    else:
#                        dy = (y - self.m3DownPos[1]) * self.rotRate
#                        dz = 0
#                    base.camera.setHpr(camRot[0]+dx, camRot[1]+dy, camRot[2]+dz)
#
#
#                # move viewpoint
#                # Walk flat (mouse up = fwd, mouse l/r = slide sideways).  Elevator up and down
#                elif self.m1Down:
#                    # move viewpoint
#                    #print("CameraControl mouseMove: m3Down")
#
#                    quaternion = base.camera.getQuat()
#                    fwd = quaternion.getForward()
#
#                    # shift -> only up/down
#                    if self.shift:
#                        fwd = LVector3f(0, 0, 1)
#                        right = LVector3f.zero()
#                    # else walk flat
#                    else:
#                        fwd = LVector3f(fwd[0], fwd[1], 0)
#                        quat = Quat()
#                        quat.setFromAxisAngle(-90, LVector3f.up())
#                        right = quat.xform(fwd)
#
#                    base.camera.setPos(base.camera.getPos() + fwd * (y - self.m1DownPos[1]) * self.speed + right * (x - self.m1DownPos[0]) * self.speed)

            # dragging dialog
            else:
                if self.m1Down:
                    # camera forward vec
                    quaternion = base.camera.getQuat()
                    fwd = quaternion.getForward()

                    # plane at obj pos perpendicular to view direction
                    objPath = WyeCore.libs.WyeUI.dragFrame.vars.dragObj[0]._nodePath
                    objPlane = LPlanef(fwd, objPath.getPos())

                    # mouse position on that plane
                    mpos = base.mouseWatcherNode.getMouse()
                    newPos = Point3(0,0,0)
                    nearPoint = Point3()
                    farPoint = Point3()
                    # generate ray from camera through mouse xy
                    base.camLens.extrude(mpos, nearPoint, farPoint)
                    # get intersection of mouse point ray with object plane
                    if objPlane.intersectsLine(newPos,
                                                 render.getRelativePoint(base.camera, nearPoint),
                                                 render.getRelativePoint(base.camera, farPoint)):
                        # Move dialog to that location, taking into account offset
                        # from where user clicked rel to position of dialog
                        tgtPos = newPos - WyeCore.libs.WyeUI.dragOffset
                        objPath.setPos(tgtPos)
                        if hasattr(WyeCore.libs.WyeUI.dragFrame.params, "position"):
                            WyeCore.libs.WyeUI.dragFrame.params.position[0] = tgtPos

                else:
                    Wye.dragging = False
                    WyeCore.libs.WyeUI.dragFrame = None

        # stub
        def setFly(self, doFly):
            self.fly = doFly

    # Widget focus manager singleton
    # Maintains a list of dialog hierarchies where the most recently added member of each hierarchy is the only one
    # whose widgets can accept focus
    # Only one widget in all of them can have focus (if any have)
    #
    # Note: in theory this should turn on event handling when there's a dialog up and
    # shut it off when
    #
    # Note: event management is rudimentary.
    # Optimization might be to switch off key and drag events when an input doesn't have
    # focus.  For now, simplicity wins over optimization
    #
    class FocusManager:

        _dialogHierarchies = []          # list of open dialog hierarchies (dialog frame lists)
        #_mouseHandler = None

        _shiftDown = False
        _ctlDown = False

        _activeDialog = None
        _mouseHandler = None

        class MouseHandler(DirectObject):
            def __init__(self):
                #print("FocusManager create MouseHandler")
                self.accept('wheel_up', partial(self.mouseWheel, 1))
                self.accept('wheel_down', partial(self.mouseWheel, -1))

                ## reference - events
                # "escape", "f" + "1-12"(e.g.
                # "f1", "f2", ...
                # "f12"), "print_screen",
                # "scroll_lock", "backspace", "insert", "home", "page_up", "num_lock",
                # "tab", "delete", "end", "page_down", "caps_lock", "enter", "arrow_left",
                # "arrow_up", "arrow_down", "arrow_right", "shift", "lshift", "rshift",
                # "control", "alt", "lcontrol", "lalt", "space", "ralt", "rcontrol"
                ## end reference

            # if there's an active dialog, pass it mousewheel events
            def mouseWheel(self, dir):
                #print("mouseWheel", dir)
                if WyeUI.FocusManager._activeDialog:
                    #print("MouseHandler: mouseWheel", dir)
                    WyeUI.FocusManager._activeDialog.verb.doWheel(dir)


        # find dialogFrame in leaf nodes of dialog hierarchies
        def findDialogHier(dialogFrame):
            retHier = None
            for hier in WyeUI.FocusManager._dialogHierarchies:
                # if found it, add to hierarchy list
                if len(hier) > 0 and hier[-1] == dialogFrame:
                    retHier = hier
                    break  # found it, break out of loop

            if retHier is None:
                print("Error: WyeUI FocusManager findDialogHier - dialog not found")
                print("  dialog title", dialogFrame.params.title[0])
            return retHier


        # User is adding a dialog to the display
        # If it has a parent dialog, it is now the leaf of the hierarchy and
        # its inputs get any incoming events
        def openDialog(dialogFrame, parentFrame):
            # if no focus manager set to catch selected objects, fix that
            if WyeCore.Utils.getFocusManager() is None:
                WyeCore.Utils.setFocusManager(WyeUI.FocusManager)

            # also set up to handle mouse events
            if WyeUI.FocusManager._mouseHandler is None:
                WyeUI.FocusManager._mouseHandler = WyeUI.FocusManager.MouseHandler()

            # connect to parent frame
            dialogFrame.parentFrame = parentFrame

            # if starting new dialog hierarchy
            if parentFrame is None:
                WyeUI.FocusManager._dialogHierarchies.append([dialogFrame])
                #print("Wye UI FocusManager openDialog: no parent, add dialog", dialogFrame," to hierarchy list", WyeUI.FocusManager._dialogHierarchies)

            # if has parent then add it to the parent's hierarchy
            else:
                #print("WyeUI FocusManager openDialog find parentFrame ", parentFrame)
                hier = WyeUI.FocusManager.findDialogHier(parentFrame)
                if not hier is None:
                    hier.append(dialogFrame)
                else:
                    print("Error: WyeUI FocusManager openDialog - did not find parent dialog", parentFrame, " in", WyeUI.FocusManager._dialogHierarchies)

            # if there's an active dialog, deactivate it and activate this one
            if not WyeUI.FocusManager._activeDialog is None:
                WyeUI.Dialog.select(WyeUI.FocusManager._activeDialog, False)

            WyeUI.Dialog.select(dialogFrame, True)
            #print("FocusManager openDialog", WyeUI.FocusManager._dialogHierarchies)


        # Remove the given dialog from the display hierarchy
        def closeDialog(dialogFrame):
            #print("FocusManager closeDialog", dialogFrame)
            hier = WyeUI.FocusManager.findDialogHier(dialogFrame)
            #print("FocusManager closeDialog remove", dialogFrame, " from len", len(hier), ", hier", hier)
            del hier[-1]    # remove dialog from hierarchy
            if len(hier) == 0:  # if that was the last dialog, remove hierarchy too
                #print(" hier now empty, remove it")
                WyeUI.FocusManager._dialogHierarchies.remove(hier)
            #print("FocusManager closeDialog complete: hierarchies", WyeUI.FocusManager._dialogHierarchies)
            if dialogFrame == WyeUI.FocusManager._activeDialog:
                if len(hier) > 0:
                    WyeUI.Dialog.select(hier[-1], True)
                else:
                    WyeUI.FocusManager._activeDialog = None

        # User clicked on object, it might be a dialog field.
        # call each leaf dialog to see if tag belongs to it.
        # If so, return True (we used it)
        # else return False (not ours, someone else can use it)
        def doSelect(id):
            status = False
            WyeUI.Dialog.hideCursor()
            # if there is an active dialog, deactivate it
            #if WyeUI.FocusManager._activeDialog:
            #    WyeUI.Dialog.select(WyeUI.FocusManager._activeDialog, False)
            #    WyeUI.FocusManager._activeDialog = None
            # loop through all the dialog hierarchies checking leaf dialogs to see if one wants this tag
            for hier in WyeUI.FocusManager._dialogHierarchies:       # loop through them all to be sure only one dialog has field selected
                #print("FocusManager doSelect hier=", hier)
                if len(hier) > 0:
                    frm = hier[-1]
                    #print("FocusManager doSelect", frm, ",", frm.params.title[0], ",", id)
                    # if dialog uses the tag, mark it active
                    if frm.verb.doSelect(frm, id):
                        #print("doSelect: Active dialog", WyeUI.FocusManager._activeDialog.params.title)
                        WyeUI.Dialog.select(frm, True)
                        break   # Found user of tag. Done with loop

            return status

        # process keys and controls (shift, ctl)
        def doKey(key):
            # handle control codes.
            # if key, apply case
            match key:
                # check for control codes
                case Wye.ctlKeys.CTL_DOWN:
                    WyeUI.FocusManager._ctlDown = True
                    return True
                case Wye.ctlKeys.CTL_UP:
                    WyeUI.FocusManager._ctlDown = False
                    return True
                case Wye.ctlKeys.SHIFT_DOWN:
                    WyeUI.FocusManager._shiftDown = True
                    return True
                case Wye.ctlKeys.SHIFT_UP:
                    WyeUI.FocusManager._shiftDown = True
                    return True
                # any other key
                case _:
                    if isinstance(key, str) and 'a' <= key and key <= 'z' and WyeUI.FocusManager._shiftDown:
                        key = key.upper()
                    # pass key to next lowest (?) in every dialog hierarchy
                    # key will be handled by the one that currently has focus
                    for hier in WyeUI.FocusManager._dialogHierarchies:
                        if len(hier) > 0:
                            frm = hier[-1]
                            #print("FocusManager doKey", frm, " ,", key)
                            if hasattr(frm, "parentFrame") and not frm.parentFrame is None:
                                if frm.parentFrame.verb.doKey(frm, key):
                                    return True
                            else:
                                if frm.verb.doKey(frm, key):
                                    return True

                    return False # if get this far, didn't use the character



    # Input field classes
    # Each input run method just returns its frame as p0.
    # Since the input is a parameter and is run before the dialog runs, the input's run cannot do any graphic setup
    #
    # When the dialog runs it calls the input's display method to do the actual graphical layout.
    #
    # Effectively each input is a factory generating an input object frame for dialog to use

    # label field
    # Technically not an input, but is treated as one for layout
    class InputLabel:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),                 # parent dialog/dropdown
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),
                   )  # 0

        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputLabel, stack)
            frame.vars.gWidgetStack[0] = []
            frame.vars.tags[0] = []     # no clickable tags
            return frame

        def run(frame):
            frame.params.frame[0] = frame  # self referential!
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]

            lbl = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())
            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # update dialog pos to next free space downward

            pos[2] -= lbl.getHeight()           # update to next position

            return []       # no clickable object tags

        def redisplay(frame):
            pass

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)


    # text input field
    class InputText:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None),                    # input cursor graphic widget
                    ("callback", Wye.dType.OBJECT, None),  # verb to call
                    ("optData", Wye.dType.ANY, None),
                    )
        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputText, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def run(frame):
            #print("InputText label", frame.params.label, " value=", frame.params.value)
            frame.vars.currVal[0] = frame.params.value[0]
            frame.params.frame[0] = frame  # self referential!
            frame.vars.callback = frame.params.callback
            frame.vars.optData = frame.params.optData

            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]


            gTags = []      # clickable graphic object tags assoc with this input
            lbl = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + .5
            txt = WyeUI._3dText(frame.vars.currVal[0], Wye.color.TEXT_COLOR,
                                pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath())
            #txt.setColor(WyeUI.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            gTags.append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt
            frame.vars.tags[0] = gTags

            # update dialog pos to next free space downward
            pos[2] -= txt.getHeight()           # update to next position

            return gTags

        def redisplay(inFrm):
            inWidg = inFrm.vars.gWidget[0]
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(inFrm.vars.currVal[0])

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, text):
            frame.vars.gWidget[0].setText(text)
            frame.vars.currVal[0] = text

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setCurrentPos(frame, index):
            frame.vars.currPos[0] = index       # TODO needs validating!

    class InputInteger(InputText):

        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.INTEGER, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),                  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("Cursor", Wye.dType.OBJECT, None),                    # input cursor graphic widget
                    ("callback", Wye.dType.OBJECT, None),               # verb to call
                    ("optData", Wye.dType.ANY, None),
                    )

        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputInteger, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]


            gTags = []      # clickable graphic object tags assoc with this input
            lbl = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + .5
            txt = WyeUI._3dText(str(frame.vars.currVal[0]), Wye.color.LABEL_COLOR,
                                pos=(width, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath())
            txt.setColor(Wye.color.TEXT_COLOR)
            # print("    Dialog inWdg", txt)
            gTags.append(txt.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(txt)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = txt

            frame.vars.tags[0] = gTags

            # update dialog pos to next free space downward
            pos[2] -= txt.getHeight()  # update to next position

            return gTags

        def redisplay(inFrm):
            inWidg = inFrm.vars.gWidget[0]
            # print("  set text", txt," ix", ix, " txtWidget", inWidg)
            inWidg.setText(str(inFrm.vars.currVal[0]))

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, int):
            frame.vars.gWidget[1].setText(str(int))
            frame.vars.currVal[0] = str(int)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

    # text input field
    class InputButton:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # 0 return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # 1 user supplied label for field
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE),   # 2 verb to call when button clicked
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),   # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # 0 list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("gWidget", Wye.dType.OBJECT, None),                  # 1 associated graphic widget
                    ("callback", Wye.dType.OBJECT, None),                     # 2 verb to call
                    ("clickCount", Wye.dType.INTEGER, 0),                 # 3 button depressed count
                    ("verbStack", Wye.dType.OBJECT_LIST, None),           # 4 verb callback stack
                    ("optData", Wye.dType.ANY, None),
                    )

        def start(stack):
            frm = Wye.codeFrame(WyeUI.InputButton, stack)
            frm.vars.gWidgetStack[0] = []
            frm.vars.verbStack[0] = []
            return frm

        def run(frame):
            #print("InputButton frame", frame.tostring())
            #print("  frame.params.frame=",frame.params.frame)
            frame.params.frame[0] = frame  # self referential!
            #print("InputButton ", frame.params.label, " params.callback", frame.params.callback)
            frame.vars.callback = frame.params.callback  # save verb to call
            frame.vars.optData = frame.params.optData
            #print("InputButton optData", frame.vars.optData)
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]

            btn = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())
            frame.vars.gWidgetStack[0].append(btn)  # save for deleting on dialog close
            frame.vars.gWidget[0] = btn  # stash graphic obj in input's frame
            tags = [btn.getTag()]
            frame.vars.tags[0] = tags

            # update dialog pos to next free space downward
            pos[2] -= btn.getHeight()  # update to next position

            return tags

        def redisplay(frame):
            pass

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidget[0].setText(text)
            frame.params.label[0] = text

        def setColor(frame, color):
            frame.vars.gWidget[0].setColor(color)

    # checkbox
    class InputCheckbox:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),  # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied label for field
                      ("value", Wye.dType.STRING, Wye.access.REFERENCE),  # user supplied var to return value in
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),           # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("currPos", Wye.dType.INTEGER, 0),                    # 3d pos
                    ("currVal", Wye.dType.STRING, ""),                    # current string value
                    ("currInsPt", Wye.dType.INTEGER, 0),                  # text insertion point
                    ("gWidget", Wye.dType.OBJECT, None),                  # stashed graphic widget
                    ("callback", Wye.dType.OBJECT, None),  # verb to call
                    ("optData", Wye.dType.ANY, None),
                    ("userCallback", Wye.dType.OBJECT, None),  # user verb to call when done
                    ("userOptData", Wye.dType.ANY, None),
                    )
        def start(stack):
            frame = Wye.codeFrame(WyeUI.InputCheckbox, stack)
            frame.vars.gWidgetStack[0] = []
            return frame

        def run(frame):
            #print("InputText label", frame.params.label, " value=", frame.params.value)
            frame.vars.currVal[0] = frame.params.value[0]
            frame.params.frame[0] = frame  # self referential!
            frame.vars.callback[0] = WyeUI.InputCheckbox.InputCheckboxCallback       # save verb to call
            frame.vars.optData[0] = (frame,)       # don't know position yet
            frame.vars.userCallback[0] = frame.params.callback[0]
            frame.vars.userOptData = frame.params.optData

            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]


            gTags = []      # clickable graphic object tags assoc with this input
            lbl = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            lblGFrm = lbl.text.getFrameActual()
            width = (lblGFrm[1] - lblGFrm[0]) + .5

            check = WyeCore.libs.WyeUI._box(size=[.5, .05, .5], pos=[pos[0]+width+.5, pos[1], pos[2]+.25], parent=dlgHeader.getNodePath())
            tag = "wyeTag" + str(WyeCore.Utils.getId())  # generate unique tag for object
            check.setTag(tag)
            gTags.append(tag)  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(check)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = check

            # set checkbox color to match data
            #print("InputCheckbox display: init value to", frame.params.value[0])
            frame.verb.setValue(frame, frame.params.value[0])

            frame.vars.tags[0] = gTags
            #print("InputCheckbox tags", gTags)

            # update dialog pos to next free space downward
            pos[2] -= max(lbl.getHeight(), check.getHeight())           # update to next position

            return gTags

        def redisplay(frame):
            frame.verb.setValue(frame, frame.params.value[0])

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, isOn):
            print("InputCheckbox setValue", isOn, " color", Wye.color.TRUE_COLOR if isOn else Wye.color.FALSE_COLOR)
            frame.vars.gWidget[0].setColor(Wye.color.TRUE_COLOR if isOn else Wye.color.FALSE_COLOR)

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        def setCurrentPos(frame, index):
            frame.vars.currPos[0] = index       # TODO needs validating!


        # User clicked input, generate the DropDown
        class InputCheckboxCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("retStat", Wye.dType.INTEGER, -1),
                        ("rowFrm", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                # print("InputDropdownCallback started")
                return Wye.codeFrame(WyeUI.InputCheckbox.InputCheckboxCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("InputDropdownCallback run: data", data)
                rowFrm = data[1][0]
                print("InputCheckboxCallback run: rowFrm", rowFrm.params.label[0], " ", rowFrm.verb.__name__)

                # toggle value
                rowFrm.vars.currVal[0] = not rowFrm.vars.currVal[0]     # toggle value
                rowFrm.verb.setValue(rowFrm, rowFrm.vars.currVal[0])    # make graphic match value state

                # if the user supplied a callback, call it
                if rowFrm.vars.userCallback[0]:
                    # put user's callback info in std callback location, call doCallback, put our callback data back
                    tmpCallback = rowFrm.vars.callback[0]
                    tmpOptData = rowFrm.vars.optData[0]
                    rowFrm.vars.callback[0] = rowFrm.vars.userCallback[0]
                    rowFrm.vars.optData[0] = rowFrm.vars.userOptData[0]
                    WyeCore.libs.WyeUI.Dialog.doCallback(rowFrm, rowFrm, "none")
                    rowFrm.vars.callback[0] = tmpCallback
                    rowFrm.vars.optData[0] = tmpOptData




    # dropdown input field
    class InputDropdown:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("frame", Wye.dType.STRING, Wye.access.REFERENCE),    # return own frame
                      ("label", Wye.dType.STRING, Wye.access.REFERENCE),    # user supplied label for field
                      ("list", Wye.dType.STRING, Wye.access.REFERENCE),     # text list of entries
                      ("selectionIx", Wye.dType.INTEGER, Wye.access.REFERENCE), # current selection index
                      ("color", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE, Wye.color.LABEL_COLOR),
                      ("callback", Wye.dType.STRING, Wye.access.REFERENCE, None),  # 2 verb to call when number changes
                      ("optData", Wye.dType.ANY, Wye.access.REFERENCE),  # 3 optional data
                      )
        varDescr = (("position", Wye.dType.INTEGER_LIST, (0,0,0)),      # position rel to parent
                    ("size", Wye.dType.INTEGER_LIST, (0, 0, 0)),        # size
                    ("parent", Wye.dType.OBJECT, None),
                    ("gWidgetStack", Wye.dType.OBJECT_LIST, None),        # list of objects to delete on exit
                    ("tags", Wye.dType.STRING_LIST, None),  # assigned tags
                    ("gWidget", Wye.dType.OBJECT, None),                  # associated graphic widget
                    ("callback", Wye.dType.OBJECT, None),                 # internal verb to call when done
                    ("optData", Wye.dType.ANY, None),
                    ("userCallback", Wye.dType.OBJECT, None),             # user verb to call when done
                    ("userOptData", Wye.dType.ANY, None),
                    ("clickCount", Wye.dType.INTEGER, 0),                 # button depressed count
                    ("list", Wye.dType.OBJECT_LIST, None),                # local copy of dropdown values
                    )

        def start(stack):
            frm = Wye.codeFrame(WyeUI.InputDropdown, stack)
            frm.vars.gWidgetStack[0] = []
            frm.vars.list[0] = []
            return frm

        def run(frame):
            #print("  frame.params.frame=",frame.params.frame)
            frame.vars.callback[0] = WyeUI.InputDropdown.InputDropdownCallback       # save verb to call
            frame.vars.optData[0] = (frame,)       # don't know position yet
            frame.vars.userCallback[0] = frame.params.callback[0]
            frame.vars.userOptData = frame.params.optData
            frame.params.frame[0] = frame  # self referential!
            #print("InputDropdown optData", frame.params.optData, " manufactured optData", frame.vars.optData)

            #print("InputDropdown run: callback=", frame.vars.callback)

            # copy the list over for later
            frame.vars.list[0] = frame.params.list[0][:]
            # return frame and success, caller dialog will use frame as placeholder for input
            frame.status = Wye.status.SUCCESS

        def display(frame, dlgFrm, pos):
            frame.vars.position[0] = (pos[0], pos[1], pos[2])  # save this position

            dlgHeader = dlgFrm.vars.dragObj[0]

            gTags = []  # clickable graphic object tags assoc with this input
            lbl = WyeUI._3dText(frame.params.label[0], frame.params.color[0], pos=tuple(pos),
                                scale=(1, 1, 1), parent=dlgHeader.getNodePath())

            frame.vars.gWidgetStack[0].append(lbl)  # save graphic widget for deleting on close

            # add tag, input index to dictionary
            gTags.append(lbl.getTag())  # tag => inp index dictionary (both label and entry fields point to inp frm)
            # offset 3d input field right past end of 3d label
            btn = WyeUI._3dText(frame.params.list[0][frame.params.selectionIx[0]], Wye.color.LABEL_COLOR,
                                pos=(lbl.getWidth() + .5, 0, 0), scale=(1, 1, 1), parent=lbl.getNodePath())
            btn.setColor(Wye.color.TEXT_COLOR)
            # print("    Dialog inWdg", btn)
            gTags.append(btn.getTag())  # save graphic widget for deleting on dialog close
            frame.vars.gWidgetStack[0].append(btn)  # save graphic widget for deleting on close
            frame.vars.gWidget[0] = btn
            frame.vars.tags[0] = gTags

            # update dialog pos to next free space downward
            pos[2] -= btn.getHeight()  # update to next position

            return gTags

        def redisplay(frame):
            frame.verb.setValue(frame, frame.params.selectionIx[0])

        def setList(frame, newList, newIndex):
            print("frame", frame.verb.__name__, " setList: newList", newList, " newIndex", newIndex)
            frame.vars.list[0] = newList
            frame.verb.setValue(frame, newIndex)
            frame.params.selectionIx[0] = newIndex

        def close(frame):
            for gObj in frame.vars.gWidgetStack[0]:
                gObj.removeNode()

        def setLabel(frame, text):
            frame.vars.gWidgetStack[0][0].setText(text)

        def setValue(frame, index):
            # todo Range check index!
            print("InputDropdown setValue. Label", frame.params.label, " index", index, " vars", frame.varsToStringV())
            frame.vars.gWidget[0].setText(frame.vars.list[0][index])
            frame.params.selectionIx[0] = index

        def setColor(frame, color):
            frame.vars.gWidgetStack[0][0].setColor(color)
            frame.vars.gWidget[0].setColor(color)

        # User clicked input, generate the DropDown
        class InputDropdownCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("retStat", Wye.dType.INTEGER, -1),
                        ("rowFrm", Wye.dType.OBJECT, None),
                        )

            def start(stack):
                # print("InputDropdownCallback started")
                return Wye.codeFrame(WyeUI.InputDropdown.InputDropdownCallback, stack)

            def run(frame):
                data = frame.eventData
                #print("InputDropdownCallback run: data", data)
                rowFrm = data[1][0]

                match (frame.PC):
                    case 0:
                        #print("InputDropdownCallback parentFrm", parentFrm.params.title[0], ":", parentFrm.tostring())
                        #print(" objFrm", objFrm.tostring())

                        pos = [rowFrm.vars.position[0][0], rowFrm.vars.position[0][1], rowFrm.vars.position[0][2]]
                        pos[1] -= .5

                        dlgFrm = WyeCore.libs.WyeUI.DropDown.start([])
                        dlgFrm.params.retVal = frame.vars.retStat
                        dlgFrm.params.title = ["Data Type"]
                        dlgFrm.params.position = [[pos[0], pos[1], pos[2]],]
                        dlgFrm.params.parent = [rowFrm.parentFrame]

                        # build dialog frame params list of input frames
                        attrIx = 0
                        for rowTxt in rowFrm.vars.list[0]:
                            # print("lib", lib.__name__, " verb", verb.__name__)
                            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [rowFrm]  # return value
                            btnFrm.params.parent = [dlgFrm]
                            btnFrm.params.label = [rowTxt]  # button label is currently selected value
                            # note: dropdown doesn't do per-row callbacks
                            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                            attrIx += 1

                        # WyeUI.Dialog.run(dlgFrm)
                        frame.SP.append(dlgFrm)     # push dialog so it runs next cycle

                        frame.PC += 1               # on return from dialog, run next case

                    case 1:
                        dlgFrm = frame.SP.pop()
                        #print("InputDropdownCallback run case1: dlgFrm", dlgFrm.verb.__name__, " status", \
                        #      Wye.status.tostring(frame.status), " selIx", dlgFrm.vars.currInp[0], \
                        #      " retStat", frame.vars.retStat[0])
                        if frame.vars.retStat[0] == Wye.status.SUCCESS:
                            #print("InputDropdownCallback done, success, set row label to", dlgFrm.vars.currInp[0])
                            rowFrm.verb.setValue(rowFrm, dlgFrm.vars.currInp[0])

                            #print("parentFrm", rowFrm.verb.__name__, " callback", rowFrm.params.callback)
                            if rowFrm.vars.userCallback[0]:
                                # put user's callback info in std callback location, call doCallback, put our callback data back
                                tmpCallback = rowFrm.vars.callback[0]
                                tmpOptData = rowFrm.vars.optData[0]
                                rowFrm.vars.callback[0] = rowFrm.vars.userCallback[0]
                                rowFrm.vars.optData[0] = rowFrm.vars.userOptData[0]
                                WyeCore.libs.WyeUI.Dialog.doCallback(rowFrm, rowFrm, "none")
                                rowFrm.vars.callback[0] = tmpCallback
                                rowFrm.vars.optData[0] = tmpOptData

                        frame.status = dlgFrm.status


    # Dialog object.
    # Display dialog and fields
    # Update fields on events
    class Dialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.OBJECT
        paramDescr = (("retVal", Wye.dType.INTEGER, Wye.access.REFERENCE),    # 0 ok/cancel or other status (if dropdown)
                      ("title", Wye.dType.STRING, Wye.access.REFERENCE),    # 1 user supplied title for dialog
                      ("position", Wye.dType.INTEGER_LIST, Wye.access.REFERENCE), # 2 user supplied position
                      ("parent", Wye.dType.STRING, Wye.access.REFERENCE),   # 3 parent dialog frame, if any
                      ("inputs", Wye.dType.VARIABLE, Wye.access.REFERENCE)) # 5+ variable length list of input control frames
                      # input widgets go here (Input fields, Buttons, and who knows what all cool stuff that may come

        varDescr = (("position", Wye.dType.FLOAT_LIST, (0,0,0)),            # 0 pos copy  *** REQUIRED ***
                    ("dlgWidgets", Wye.dType.OBJECT_LIST, None),            # 1 standard dialog widgets
                    ("dlgTags", Wye.dType.STRING_LIST, None),               # 2 OK, Cancel widget tags
                    ("inpTags", Wye.dType.OBJECT, None),                    # 3 dictionary return param ix of input by graphic tag
                    ("currInp", Wye.dType.INTEGER, -1),                     # 4 index to current focus widget, if any
                    ("clickedBtns", Wye.dType.OBJECT_LIST, None),           # 5 list of buttons that need to be unclicked
                    ("dragObj", Wye.dType.OBJECT, None),                    # 6 path to top graphic obj *** REF'D BY CHILDREN ***
                    ("topTag", Wye.dType.STRING, ""),                       # 6 Wye tag for top object (used for dragging)
                    ("bgndGObj", Wye.dType.OBJECT, None),                   # 7 background card
                    )

        _cursor = None      # 3d TextInput cursor
        _activeInputInteger = None  # used for wheel up/down events

        def start(stack):
            frame = Wye.codeFrame(WyeUI.Dialog, stack)
            # give frame unique lists
            frame.vars.dlgWidgets[0] = []      # standard widgets common to all Dialogs
            frame.vars.dlgTags[0] = []         # tags for OK, Cancel buttons
            frame.vars.inpTags[0] = {}         # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []     # clicked button(s) being "flashed" (so user sees they were clicked)

            # If there isn't a text input cursor, make it
            if WyeUI.Dialog._cursor is None:
                WyeUI.Dialog._cursor = WyeCore.libs.WyeUI._box([.05, .05, .6], [0, 0, 0])
                WyeUI.Dialog._cursor.hide()
            return frame

        # first time through run, draw dialog and all its fields
        # after that, process any buttons being flashed to show user they were clicked on
        def run(frame):
            match frame.PC:
                case 0:     # Start up case - set up all the fields
                    #print("Dialog run: frame", frame.verb.__name__, " params", frame.paramsToStringV())
                    frame.params.retVal[0] = Wye.status.CONTINUE        # return value: 0 running, 1 OK, 2 Cancel
                    parent = frame.params.parent[0]

                    #print("Dialog put frame in param[0][0]", frame)
                    frame.vars.position[0] = (frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2])      # save display position
                    # return frame

                    #print("Dialog display: pos=frame.params.position", frame.params.position)
                    if parent is None:
                        #print("  params.inputs", frame.params.inputs)
                        dlgHeader = WyeUI._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0], scale=(.2, .2, .2))
                    else:
                        dlgHeader = WyeUI._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0],
                                                  scale=(1,1,1), parent=parent.vars.dragObj[0].getNodePath())
                    frame.vars.topTag[0] = dlgHeader.getTag()   # save tag for drag checking
                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.dragObj[0] = dlgHeader        # save graphic for parenting sub dialogs


                    #print("Dialog run: params.position",frame.params.position[0])
                    # row position rel to parent, not global
                    pos = [0,0,-dlgHeader.getHeight()] #[x for x in frame.params.position[0]]    # copy position

                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = len(frame.params.inputs[0])
                    # draw user- supplied label and text inputs
                    for ii in range(nInputs):
                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]
                        #print("    inFrm", inFrm)
                        #print("    Dialog input ", ii, " inFrm", inFrm)
                        #print("       inFrm.params.title", inFrm.params.title)
                        #print("")

                        setattr(inFrm, "parentFrame", frame)

                        # display inputs
                        # Note: each Input's display function updates draw "pos" downward
                        # stash returned display obj tags in lookup dict to detect what user clicked on
                        #print("Build dialog", frame.params.title[0])
                        if hasattr(inFrm.verb, "display"):
                            for lbl in inFrm.verb.display(inFrm, frame, pos):  # displays label, updates pos, returns selection tags
                                frame.vars.inpTags[0][lbl] = ii
                        else:
                            print("Dialog: Error. Unknown input verb", inFrm.verb.__name__)

                    #print("Dialog has input widgets", frame.vars.inpTags[0])

                    # display OK, Cancel buttons
                    pos[1] -= .1  # hack fwd just a tad in case text overran the dialog space and covered the ok/cancel
                    txt = WyeUI._3dText("OK", color=(Wye.color.HEADER_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                        parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())
                    pos[0] += 2.5       # shove Cancel to the right of OK
                    #print("Dialog Cancel btn at", pos)
                    txt = WyeUI._3dText("Cancel", color=(Wye.color.HEADER_COLOR), pos=tuple(pos), scale=(1, 1, 1),
                                        parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())
                    # done setup, go to next case to process events
                    frame.PC += 1

                    # make a background for entire dialog
                    if parent is None:
                        scMult = 5
                    else:
                        scMult = 1
                    dlgNodePath = frame.vars.dragObj[0].getNodePath()
                    dlgNodePath.setPos(frame.vars.position[0][0], frame.vars.position[0][1], frame.vars.position[0][2])
                    dlgBounds = dlgNodePath.getTightBounds()
                    card = CardMaker("Dlg Bgnd")
                    gFrame = LVecBase4f(0, 0, 0, 0)
                    # print("gFrame", gFrame)
                    ht = (dlgBounds[1][2] - dlgBounds[0][2]) * scMult + 1
                    wd = (dlgBounds[1][0] - dlgBounds[0][0]) * scMult + 1
                    gFrame[0] = 0                                  # marginL
                    gFrame[1] = wd  # marginR
                    gFrame[2] = 0  # marginB
                    gFrame[3] = ht # marginT
                    # print("initial adjusted gFrame", gFrame)
                    card.setFrame(gFrame)
                    cardPath = NodePath(card.generate())
                    cardPath.reparentTo(dlgNodePath)
                    cardPath.setPos((-.5, .1, 1.2 - ht))

                    # background outline
                    oCard = CardMaker("Dlg Bgnd Outline")
                    # print("gFrame", gFrame)
                    gFrame[0] = -.1    # marginL
                    gFrame[1] = wd+.3  # marginR
                    gFrame[2] = -.1    # marginB
                    gFrame[3] = ht+.3  # marginT
                    # print("initial adjusted gFrame", gFrame)
                    oCard.setFrame(gFrame)
                    oCardPath = NodePath(oCard.generate())
                    oCardPath.reparentTo(dlgNodePath)
                    oCardPath.setPos((-.6, .2, 1.1 - ht))
                    frame.vars.bgndGObj[0] = oCardPath

                    # Add dialog to known dialogs
                    WyeUI.FocusManager.openDialog(frame, parent)        # pass parent, if any

                case 1:
                    # do click-flash count down and end-flash color reset for buttons user clicked
                    delLst = []
                    # decrement flash count.  if zero, turn off button highlight
                    for btnFrm in frame.vars.clickedBtns[0]:
                        #print("button", btnFrm.verb.__name__, " count ", btnFrm.vars.clickCount[0])
                        btnFrm.vars.clickCount[0] -= 1
                        if btnFrm.vars.clickCount[0] <= 0:
                            #print("Dialog run: Done click flash for button ", btnFrm.verb.__name__, ". Set color", Wye.color.BACKGROUND_COLOR)
                            delLst.append(btnFrm)
                            btnFrm.vars.gWidget[0].setColor(btnFrm.params.color[0])
                    # remove any buttons whose count is finished
                    for btnFrm in delLst:
                        #print("Dialog run: Remove clicked btn frame", btnFrm.verb.__name__)
                        frame.vars.clickedBtns[0].remove(btnFrm)

        def doCallback(frame, inFrm, tag):
            # if something to call
            callVerb = inFrm.vars.callback[0]
            if callVerb:
                # print("Dialog doSelect: clicked btn, verb ", callVerb.__name__)
                # start the verb
                verbFrm = callVerb.start(frame.SP)
                # handle user data
                if len(inFrm.vars.optData) > 0:
                    # print("Button callback", callVerb.__name__, " user data", inFrm.vars.optData)
                    data = inFrm.vars.optData[0]
                else:
                    data = None
                # if not single cycle, then put up as parallel path
                if callVerb.mode != Wye.mode.SINGLE_CYCLE:
                    # queue to be called every display cycle
                    WyeCore.World.setRepeatEventCallback("Display", verbFrm, data)
                else:
                    # call this once
                    verbFrm.eventData = (tag, data, inFrm)  # pass along user supplied event data, if any
                    if Wye.debugOn:
                        Wye.debug(verbFrm,"Dialog doSelect: call single cycle verb " + verbFrm.verb.__name__ + " data" + str(verbFrm.eventData))
                    else:
                        # print("doSelect run", verbFrm.verb.__name__)
                        verbFrm.verb.run(verbFrm)

        # User clicked on a tag. It might belong to a field in our dialog.
        # Figure out what dialog field it belongs to, if any, and do the appropriate thing
        def doSelect(frame, tag):
            #print("Dialog doSelect: ", frame.verb, " tag", tag)
            prevSel = frame.vars.currInp[0]      # get current selection
            # if tag is input field in this dialog, select it
            closing = False
            WyeUI.Dialog._activeInputInteger = None
            retStat = False     # haven't used the tag (yet)

            # if clicked header for dragging
            if tag == frame.vars.topTag[0]:
                if not Wye.dragging:
                    Wye.dragging = True
                    WyeCore.libs.WyeUI.dragFrame = frame
                    #frame.vars.dragObj[0]._nodePath.wrtReparentTo(base.camera)

                    # todo - clean this up!
                    objPath = frame.vars.dragObj[0]._nodePath
                    quaternion = base.camera.getQuat()
                    fwd = quaternion.getForward()
                    objPlane = LPlanef(fwd, objPath.getPos())
                    mpos = base.mouseWatcherNode.getMouse()
                    newPos = Point3(0,0,0)
                    nearPoint = Point3()
                    farPoint = Point3()
                    base.camLens.extrude(mpos, nearPoint, farPoint)
                    if objPlane.intersectsLine(newPos,
                                                 render.getRelativePoint(base.camera, nearPoint),
                                                 render.getRelativePoint(base.camera, farPoint)):
                        objPosInPlane = objPlane.project(objPath.getPos())
                        WyeCore.libs.WyeUI.dragOffset = newPos - objPosInPlane

                    retStat = True  # used up the tag

            # if clicked on input field
            if tag in frame.vars.inpTags[0]:        # do we have a matching tag?
                #print("doSelect: clicked on input tag", tag, " frame", frame.verb.__name__)

                ix = frame.vars.inpTags[0][tag]     # Yes
                retStat = True

                # handle dialog inputs
                if frame.verb is WyeUI.Dialog:
                    inFrm = frame.params.inputs[0][ix][0]

                    # if is text input make it selected
                    if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputInteger:
                        inWidg = inFrm.vars.gWidget[0]
                        #print("  found ix", ix, " inWdg", inWidg, " Set selected color")
                        inWidg.setColor(Wye.color.SELECTED_COLOR)        # set input background to "has focus" color
                        WyeUI.Dialog.drawCursor(inFrm)
                        frame.vars.currInp[0] = ix           # save as current input focus

                        if inFrm.verb is WyeUI.InputInteger:
                            WyeUI.Dialog._activeInputInteger = inFrm

                    # button callback
                    elif inFrm.verb is WyeUI.InputButton:
                        #print("Dialog", frame.params.title[0], " doSelect: clicked on", inFrm.verb.__name__, " label", inFrm.params.label[0])

                        inFrm.vars.gWidget[0].setColor(Wye.color.SELECTED_COLOR) # set button color pressed
                        #print("gWidget", inFrm.vars.gWidget[0])
                        #print("set button", inFrm.params.label[0], " selected color", Wye.color.SELECTED_COLOR,". click count", inFrm.vars.clickCount[0])
                        if inFrm.vars.clickCount[0] <= 0:     # if not in an upclick count, process click
                            #print("Dialog doSelect: Start clicked countdown for", inFrm.verb.__name__)
                            inFrm.vars.clickCount[0] = 10       # start flash countdown (in display frames)
                            frame.vars.clickedBtns[0].append(inFrm)  # stash button for flash countdown

                            if inFrm.params.callback:
                                # note: call inFrm.vars.callback, not infrm.params.callback
                                # so special inputs like dropdown can have internal callback that is called before the
                                # user's param callback
                                WyeCore.libs.WyeUI.Dialog.doCallback(frame, inFrm, tag)

                        frame.vars.currInp[0] = -1       # no input has focus

                    elif inFrm.verb is WyeUI.InputCheckbox or inFrm.verb is WyeUI.InputDropdown:
                        if inFrm.params.callback:
                            # note: call inFrm.vars.callback, not infrm.params.callback
                            # so special inputs like dropdown can have internal callback that is called before the
                            # user's param callback
                            WyeCore.libs.WyeUI.Dialog.doCallback(frame, inFrm, tag)

                        frame.vars.currInp[0] = -1       # no input has focus

                # if dropdown, currInp is dropdown index
                elif frame.verb is WyeUI.DropDown:
                    #print("Dropdown selected line ", ix)
                    frame.vars.currInp[0] = ix
                    frame.params.retVal[0] = Wye.status.SUCCESS
                    closing = True
                    # Done with dialog
                    WyeCore.libs.WyeUI.Dialog.closeDialog(frame)

            # if clicked on OK or Cancel
            elif tag in frame.vars.dlgTags[0]:
                # if is Cancel button
                if tag == frame.vars.dlgTags[0][-1]:    # if cancel button
                    frame.params.retVal[0] = Wye.status.FAIL
                    #print("Dialog", frame.params.title[0], " Cancel Button pressed, return status", frame.params.retVal)
                    retStat = True

                # else is OK button
                else:
                    #print("Dialog", frame.params[1][0], " OK Button pressed")
                    nInputs = (len(frame.params.inputs[0]))
                    #print("dialog ok: nInputs",nInputs," inputs",frame.params.inputs[0])
                    for ii in range(nInputs):
                        inFrm = frame.params.inputs[0][ii][0]
                        # for any text inputs, copy working string to return string
                        if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputCheckbox:
                            #print("input", ii, " frame", inFrm, "\n", WyeCore.Utils.frameToString(inFrm))
                            #print("input old val '"+ inFrm.params[2][0]+ "' replaced with '"+ inFrm.vars[1][0]+"'")
                            inFrm.params.value[0] = inFrm.vars.currVal[0]
                        elif inFrm.verb is WyeUI.InputInteger:
                            inFrm.params.value[0] = int(inFrm.vars.currVal[0])

                    frame.params.retVal[0] = Wye.status.SUCCESS
                    #print("doSelect OK button, return status", frame.params.retVal)
                    retStat = True

                # Done with dialog
                WyeCore.libs.WyeUI.Dialog.closeDialog(frame)

                closing = True
                #print("Closing dialog.  Status", frame.status)

            # selected graphic tag not recognized as a control in this dialog
            else:
                frame.vars.currInp[0] = -1   # no currInp

            # If there was a diff selection before, fix that
            # (if closing dialog, nevermind)
            if prevSel > -1 and prevSel != frame.vars.currInp[0] and not closing:
                inFrm =frame.params.inputs[0][prevSel][0]
                if inFrm.verb in [WyeUI.InputText, WyeUI.InputInteger, WyeUI.InputButton]:
                    inWidg = inFrm.vars.gWidget[0]
                    inWidg.setColor(Wye.color.TEXT_COLOR)

            #print("Dialog retStat", retStat)
            return retStat      # return true if we used the tag

        def closeDialog(frame):
            frame.status = Wye.status.SUCCESS

            # remove dialog from active dialog list
            WyeUI.FocusManager.closeDialog(frame)

            # delete any graphic objects associated with the inputs
            nInputs = (len(frame.params.inputs[0]))
            for ii in range(nInputs):
                inFrm = frame.params.inputs[0][ii][0]
                inFrm.verb.close(inFrm)

            # delete the graphic widgets associated with the dialog
            for wdg in frame.vars.dlgWidgets[0]:
                # print("del ctl ", wdg.text.name)
                wdg.removeNode()

        # mark dialog selected/unselected
        def select(frame, setOn):
            if setOn:
                # if there's already an active dialog, deactivate it
                if WyeUI.FocusManager._activeDialog:
                    WyeUI.Dialog.select(WyeUI.FocusManager._activeDialog, False)
                # make this the currently active dialog
                WyeUI.FocusManager._activeDialog = frame
                frame.vars.bgndGObj[0].setColor(Wye.color.SELECTED_COLOR)
                #print("Dialog '"+frame.params.title[0]+ "' Selected")

            else:
                frame.vars.bgndGObj[0].setColor(Wye.color.OUTLINE_COLOR)
                #print("Dialog '"+frame.params.title[0]+ "' Unselected")


        # inc/dec InputInteger on wheel event
        def doWheel(dir):
            #print("doWheel")
            if WyeUI.Dialog._activeInputInteger:
                #print("doWheel update input")
                inFrm = WyeUI.Dialog._activeInputInteger
                if isinstance(inFrm.vars.currVal[0], str):
                    inFrm.vars.currVal[0] = str(int(inFrm.vars.currVal[0]) + dir)
                else:
                    inFrm.vars.currVal[0] += dir

                txt = str(inFrm.vars.currVal[0])
                inWidg = inFrm.vars.gWidget[0]
                inWidg.setText(txt)
                WyeUI.Dialog.drawCursor(inFrm)

                # if the user supplied a callback
                if inFrm.vars.callback[0]:
                    WyeCore.libs.WyeUI.Dialog.doCallback(inFrm.parentFrame, inFrm, "none")

        # update InputText/InputInteger on key event
        def doKey(frame, key):
            #print("Dialog doKey: key", key)
            # if we have an input with focus
            ix = frame.vars.currInp[0]
            if ix >= 0:
                inFrm = frame.params.inputs[0][ix][0]
                if inFrm.verb is WyeUI.InputText or inFrm.verb is WyeUI.InputInteger:

                    txt = str(inFrm.vars.currVal[0])    # handle either text or integer
                    insPt = inFrm.vars.currInsPt[0]
                    preTxt = txt[:insPt]
                    postTxt = txt[insPt:]
                    # delete key
                    if key == '\x08':  # backspace delete key
                        if insPt > 0:
                            preTxt = preTxt[:-1]
                            insPt -= 1
                            inFrm.vars.currInsPt[0] = insPt
                        txt = preTxt + postTxt
                    if key == -9:  # delete (forward) key
                        if insPt < len(txt):
                            postTxt = postTxt[1:]
                        txt = preTxt + postTxt
                    # arrow keys
                    elif key == Wye.ctlKeys.LEFT:   # arrow keys
                        if insPt > 0:
                            insPt -= 1
                            inFrm.vars.currInsPt[0] = insPt
                        # place insert cursor
                        WyeUI.Dialog.drawCursor(inFrm)
                        return
                    elif key == Wye.ctlKeys.RIGHT:
                        if insPt < len(txt):
                            insPt += 1
                            inFrm.vars.currInsPt[0] = insPt
                        # place insert cursor
                        WyeUI.Dialog.drawCursor(inFrm)
                        return
                    # not special control, if printable char, insert it in the string
                    else:
                        if isinstance(key,str):
                            #print("verb is", inFrm.verb.__name__)
                            # For int input, only allow ints
                            if inFrm.verb is WyeUI.InputInteger:
                                if key in "-0123456789":
                                    if key != '-' or insPt == 0:
                                        txt = preTxt + key + postTxt
                                        insPt += 1
                                        inFrm.vars.currInsPt[0] = insPt  # set text insert point after new char

                            # else general text
                            elif key.isprintable():
                                txt = preTxt + key + postTxt
                                insPt += 1
                                inFrm.vars.currInsPt[0] = insPt        # set text insert point after new char

                    if inFrm.verb is WyeUI.InputInteger and len(txt) == 0 or txt == "-":
                        txt = '0'
                    inFrm.vars.currVal[0] = txt

                    # if the user supplied a callback
                    # note: callback can change currVal and result will be displayed
                    if inFrm.vars.callback[0]:
                        WyeCore.libs.WyeUI.Dialog.doCallback(inFrm.parentFrame, inFrm, "none")

                    inWidg = inFrm.vars.gWidget[0]
                    #print("  set text", txt," ix", ix, " txtWidget", inWidg)
                    inWidg.setText(txt)
                    # place insert cursor
                    WyeUI.Dialog.drawCursor(inFrm)

        # draw text cursor at InputText frame's currInsPt
        def drawCursor(inFrm):
            insPt = inFrm.vars.currInsPt[0]

            inWidg = inFrm.vars.gWidget[0]
            #wPos = inWidg.getPos()
            xOff = 0
            WyeUI.Dialog._cursor._nodePath.reparentTo(inWidg._nodePath)
            WyeUI.Dialog._cursor.setColor(Wye.color.CURSOR_COLOR)
            # If cursor not at beginning of text in widget,
            # get length of text before insert pt by generating temp text obj
            # with just pre-insert chars and getting its width
            if insPt > 0:
                txt = inWidg.getText()
                tmp = TextNode("tempNode")
                tmp.setText(txt[0:insPt]+'.')  # '.' - hack to force trailing spaces to be included
                tFrm = tmp.getFrameActual()
                xOff = tFrm[1] - tFrm[0] - .2  # get width of text. Subtract off trailing period hack
            # put cursor after current character
            WyeUI.Dialog._cursor.setPos(xOff + .01, -.1, .3)
            WyeUI.Dialog._cursor.show()

        def hideCursor():
            WyeUI.Dialog._cursor.hide()

    # dropdown menu
    # subclass of Dialog so FocusManager can handle focus properly
    # Returns index of selected line or -1
    class DropDown(Dialog):
        def start(stack):
            frame = Wye.codeFrame(WyeUI.DropDown, stack)
            frame.vars.dlgWidgets[0] = []      # standard widgets common to all Dialogs
            frame.vars.dlgTags[0] = []         # not used
            frame.vars.inpTags[0] = {}         # map input widget to input sequence number
            frame.vars.clickedBtns[0] = []     # clicked button(s) being "flashed"

            # If we don't have a text input cursor, make one
            #if WyeUI.Dialog._cursor is None:
            #    WyeUI.Dialog._cursor = WyeCore.libs.WyeUI._geom3d([.05, .05, .6], [0, 0, 0])
            #    WyeUI.Dialog._cursor.hide()
            return frame

        def run(frame):
            match frame.PC:
                case 0:  # Start up case - set up all the fields
                    frame.params.retVal[0] = -1           # set default return value
                    parent = frame.params.parent[0]

                    # print("DropDown put frame in param[0][0]", frame)
                    frame.vars.position[0] = (frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2])  # save display position
                    # return frame

                    # handle scale and parent obj, if any
                    if parent is None:
                        dlgHeader = WyeUI._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0], scale=(.2, .2, .2))
                    else:
                        #print("dropdown parent", parent.verb.__name__)
                        dlgHeader = WyeUI._3dText(text=frame.params.title[0], color=(Wye.color.HEADER_COLOR), pos=frame.params.position[0],
                                                  scale=(1,1,1), parent=parent.vars.dragObj[0].getNodePath())

                    frame.vars.dlgWidgets[0].append(dlgHeader)  # save graphic for dialog delete
                    frame.vars.dragObj[0] = dlgHeader        # save graphic for parenting sub dialogs

                    pos = [0,0,-dlgHeader.getHeight()] #[x for x in frame.params.position[0]]    # copy position


                    # do user inputs
                    # Note that input returns its frame as parameter value
                    nInputs = len(frame.params.inputs[0])
                    # draw user-supplied label and text inputs
                    for ii in range(nInputs):
                        #print("  Dialog input", ii, " frame", frame.params.inputs[0][ii])
                        inFrm = frame.params.inputs[0][ii][0]

                        setattr(inFrm, "parentFrame", frame)

                        # tell input to display itself.  Collect returned objects to close when dlg closes
                        # Note: each Input's display function updates pos downward
                        if inFrm.verb in [WyeUI.InputLabel, WyeUI.InputButton]:
                            for lbl in inFrm.verb.display(inFrm, frame, pos):  # displays label, updates pos, returns selection tags
                                frame.vars.inpTags[0][lbl] = ii

                        else:
                            print("Dialog: Error. Only Label and Button allowed in dropdown", inFrm.verb.__class__)

                    # Cancel button

                    #print("Dialog Cancel btn at", pos)
                    txt = WyeUI._3dText("Cancel", color=(Wye.color.HEADER_COLOR), pos=tuple(pos),
                                        scale=(1,1,1), parent=dlgHeader.getNodePath())
                    frame.vars.dlgWidgets[0].append(txt)
                    frame.vars.dlgTags[0].append(txt.getTag())

                    # make a background for entire DropDown
                    if parent is None:
                        scMult = 5  # no parent, everything has been scaled by .2
                    else:
                        scMult = 1  # have parent, already scaled by parent
                    dlgNodePath = dlgHeader.getNodePath()
                    dlgBounds = dlgNodePath.getTightBounds()
                    card = CardMaker("Dlg Bgnd")
                    gFrame = LVecBase4f(0, 0, 0, 0)
                    # print("gFrame", gFrame)
                    ht = (dlgBounds[1][2] - dlgBounds[0][2]) * scMult + 1
                    wd = (dlgBounds[1][0] - dlgBounds[0][0]) * scMult + 1
                    gFrame[0] = 0  # marginL
                    gFrame[1] = wd  # marginR
                    gFrame[2] = 0  # marginB
                    gFrame[3] = ht  # marginT
                    # print("initial adjusted gFrame", gFrame)
                    card.setFrame(gFrame)
                    cardPath = NodePath(card.generate())
                    cardPath.reparentTo(dlgNodePath)
                    cardPath.setPos((-.5, .1, 1.2 - ht))

                    # background outline
                    oCard = CardMaker("Dlg Bgnd Outline")
                    # print("gFrame", gFrame)
                    gFrame[0] = -.1    # marginL
                    gFrame[1] = wd+.3  # marginR
                    gFrame[2] = -.1    # marginB
                    gFrame[3] = ht+.3  # marginT
                    # print("initial adjusted gFrame", gFrame)
                    oCard.setFrame(gFrame)
                    oCardPath = NodePath(oCard.generate())
                    oCardPath.reparentTo(dlgNodePath)
                    oCardPath.setPos((-.6, .2, 1.1 - ht))
                    frame.vars.bgndGObj[0] = oCardPath
                    WyeUI.FocusManager.openDialog(frame, parent)  # pass parent, if any

                    frame.PC += 1

                case 1:
                    #print("DropDown case 1")
                    # if click event, callback set status to selected row, clean up dialog
                    if frame.vars.currInp[0] > -1:
                        #print("DropDown got click event.  CurrInp", frame.vars.currInp[0], " ")
                        frame.params.retVal[0] = frame.vars.currInp[0]
                        # remove dialog from active dialog list
                        WyeUI.FocusManager.closeDialog(frame)
                        # delete the graphic widgets associated with the dialog
                        for wdg in frame.vars.dlgWidgets[0]:
                            # print("del ctl ", wdg.text.name)
                            wdg.removeNode()
                        frame.status = Wye.status.SUCCESS

    # Button callback for each dropdown row
    class DropdownCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            print("DropdownCallback start")
            return Wye.codeFrame(WyeUI.DropdownCallback, stack)

        def run(frame):
            print("DropdownCallback run: event data", frame.eventData)
            rowIx = frame.eventData[1][0]
            dlgFrm = frame.eventData[1][1]
            # return dropdown index in dropdown dialog's first param
            lst = getattr(dlgFrm.params, dlgFrm.firstParamName())
            lst[0] = rowIx
            # print("DropdownCallback data=", frame.eventData, " index = ", frame.eventData[1])


    # Wye main menu - user settings n stuff
    class MainMenuDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    )

        # global list of libs being edited
        activeFrames = {}

        def start(stack):
            return Wye.codeFrame(WyeUI.MainMenuDialog, stack)

        def run(frame):
            match(frame.PC):
                case 0:
                    # create top level edit dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Wye Main Menu"]
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,10,0))
                    pos = point.getPos()
                    point.removeNode()
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]

                    # Settings
                    settingsLblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    settingsLblFrm.params.frame = [None]  # return value
                    settingsLblFrm.params.parent = [None]
                    settingsLblFrm.params.label = ["Settings"]
                    settingsLblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(settingsLblFrm)
                    dlgFrm.params.inputs[0].append([settingsLblFrm])

                    sndChkFrm = WyeCore.libs.WyeUI.InputCheckbox.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([sndChkFrm])
                    sndChkFrm.params.frame = [None]
                    sndChkFrm.params.parent = [None]
                    sndChkFrm.params.value = [True]
                    sndChkFrm.params.label = ["3D Sound On"]
                    sndChkFrm.params.callback = [WyeCore.libs.WyeUI.MainMenuDialog.SoundCheckCallback]  # button callback
                    sndChkFrm.params.optData = [sndChkFrm]
                    sndChkFrm.verb.run(sndChkFrm)

                    #
                    # Test
                    #

                    testLblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    testLblFrm.params.frame = [None]  # return value
                    testLblFrm.params.parent = [None]
                    testLblFrm.params.label = ["Test"]
                    testLblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(testLblFrm)
                    dlgFrm.params.inputs[0].append([testLblFrm])

                    obj2ChkFrm = WyeCore.libs.WyeUI.InputCheckbox.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([obj2ChkFrm])
                    obj2ChkFrm.params.frame = [None]
                    obj2ChkFrm.params.parent = [None]
                    obj2ChkFrm.params.value = [True]
                    obj2ChkFrm.params.label = ["Show Test Fish"]
                    obj2ChkFrm.params.callback = [WyeCore.libs.WyeUI.MainMenuDialog.Obj2CheckCallback]  # button callback
                    obj2ChkFrm.params.optData = [obj2ChkFrm]
                    obj2ChkFrm.verb.run(obj2ChkFrm)

                    btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([btnFrm])
                    btnFrm.params.frame = [None]
                    btnFrm.params.parent = [None]
                    btnFrm.params.label = ["Test Create Lib"]
                    btnFrm.params.callback = [WyeCore.libs.WyeUI.MainMenuDialog.TestButtonCallback]  # button callback
                    #btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb)]  # button row, dialog frame
                    WyeCore.libs.WyeUI.InputButton.run(btnFrm)


                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done
                    print("MainMenuDialog: Done")

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.mainMenu)
                    WyeCore.World.mainMenu = None


        # turn sound on/off
        class SoundCheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("SoundCheckCallback started")
                return Wye.codeFrame(WyeUI.MainMenuDialog.SoundCheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                Wye.soundOn = rowFrm.vars.currVal[0]
                print("3D Sound On", Wye.soundOn)


        #
        # test callbacks
        #

        class Obj2CheckCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("Obj2CheckCallback started")
                return Wye.codeFrame(WyeUI.MainMenuDialog.Obj2CheckCallback, stack)


            def run(frame):
                data = frame.eventData
                rowFrm = data[1]
                showObj = rowFrm.vars.currVal[0]
                testObj2 = WyeCore.World.findActiveObj('testObj2')
                testText = WyeCore.World.findActiveObj('showFishDialog')
                if showObj:
                    testObj2.vars.gObj[0].show()
                    testText.vars.dlgButton[0].show()
                else:
                    testObj2.vars.gObj[0].hide()
                    testText.vars.dlgButton[0].hide()


        class TestButtonCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                # print("TestButtonCallback started")
                return Wye.codeFrame(WyeUI.MainMenuDialog.TestButtonCallback, stack)

            def run(frame):
                print("createLibrary test")
                WyeCore.Utils.createLib("TemplateTestLib")
                print("Run test from TestButtonCallback")
                WyeCore.libs.TemplateTestLib.test()
                print("Known libs")
                for libName in dir(WyeCore.libs):
                    if not libName.startswith("__"):
                        print("  ", libName)

    # Create dialog showing loaded libraries so user can edit them
    class EditMainDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    )

        # global list of libs being edited
        activeFrames = {}

        def start(stack):
            return Wye.codeFrame(WyeUI.EditMainDialog, stack)

        def run(frame):
            match(frame.PC):
                case 0:
                    # create top level edit dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Select Library to Edit"]
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,10,0))
                    pos = point.getPos()
                    point.removeNode()
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]

                    # build dialog

                    attrIx = [0]
                    rowIx = [0]

                    for lib in WyeCore.World.libList:
                        # make the dialog row
                        btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                        dlgFrm.params.inputs[0].append([btnFrm])
                        btnFrm.params.frame = [None]  # return value
                        btnFrm.params.parent = [None]
                        btnFrm.params.label = [
                            "  Library " + str(attrIx[0]) + ":" + lib.__name__]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditLibCallback]  # button callback
                        btnFrm.params.optData = [
                            (rowIx[0], btnFrm, dlgFrm, lib, frame)]  # button row, row frame, dialog frame, obj frame
                        WyeCore.libs.WyeUI.InputButton.run(btnFrm)
                        rowIx[0] += 1
                        attrIx[0] += 1

                    # if no libs loaded
                    if attrIx == 0:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["<no libraries loaded>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])


                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done
                    print("EditMainDialog: Done")

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.editMenu)
                    WyeCore.World.editMenu = None

    # put up dialog showing verbs in given library
    class EditLibCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.OBJECT, None),
                    ("selVerb", Wye.dType.OBJECT, None),
                    ("coord", Wye.dType.FLOAT_LIST, (0.,0.,0.)),
                    ("vrbStat", Wye.dType.INTEGER, -1),
                    )

        def start(stack):
            # print("EditLibCallback started")
            return Wye.codeFrame(WyeUI.EditLibCallback, stack)


        def run(frame):
            match (frame.PC):
                case 0:
                    data = frame.eventData
                    #print("EditLibCallback data=", data)
                    libRow = data[1][0]
                    btnFrm = data[1][1]
                    parentDlgFrm = data[1][2]
                    lib = data[1][3]
                    libLstDlgFrm = data[1][4]
                    #print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)

                    #print("EditLibCallback called, library row", libRow, " name", lib.__name__)
                    #print("parentDlg '"+ parentDlgFrm.params.title[0] +"'")
                    #print("parentDlgFrm", parentDlgFrm)
                    frame.vars.coord[0] = (.5, -.5, -.5 + btnFrm.vars.position[0][2]) # position rel to parent dlg

                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start(parentDlgFrm.SP)

                    dlgFrm.params.retVal = frame.vars.vrbStat
                    dlgFrm.params.title = ["Library" + lib.__name__ + " Select Verb to Edit"]
                    dlgFrm.params.position = [[frame.vars.coord[0][0], frame.vars.coord[0][1], frame.vars.coord[0][2]],]
                    dlgFrm.params.parent = [parentDlgFrm]

                    # create a row for each verb in the library
                    attrIx = 0
                    # print("_displayLib: process library", lib.__name__)
                    for attr in dir(lib):
                        if attr != "__class__":
                            verb = getattr(lib, attr)
                            if inspect.isclass(verb):
                                if hasattr(verb, "codeDescr"):
                                    # print("lib", lib.__name__, " verb", verb.__name__)
                                    btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                                    txt = "  " + lib.__name__ + "." + verb.__name__
                                    btnFrm.params.frame = [None]  # return value
                                    btnFrm.params.parent = [dlgFrm]
                                    btnFrm.params.label = [txt]  # button label is verb name
                                    btnFrm.params.callback = [WyeCore.libs.WyeUI.EditLibCallback.EditLibaryVerbCallback]  # button callback
                                    btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb)]  # button data - offset to button
                                    WyeCore.libs.WyeUI.InputButton.run(btnFrm)
                                    dlgFrm.params.inputs[0].append([btnFrm])
                                else:
                                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                                    lblFrm.params.frame = [None]
                                    lblFrm.params.parent = [None]
                                    txt = "  " + lib.__name__ + "." + verb.__name__
                                    lblFrm.params.label = [txt]
                                    lblFrm.params.color = [Wye.color.DISABLED_COLOR]
                                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                                    dlgFrm.params.inputs[0].append([lblFrm])

                                attrIx += 1

                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)     # push dialog so it runs next cycle

                    frame.PC += 1


                case 1:
                    dlgFrm = frame.SP.pop()  # remove dialog frame from stack

                    print("EditLibCallback case 1: popped frame", dlgFrm.verb.__name__, " ", dlgFrm.params.title[0])
                    # hang here forever?  that's not good
                    frame.status = Wye.status.SUCCESS

        # edit verb in lib
        class EditLibaryVerbCallback:
            mode = Wye.mode.MULTI_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = (("count", Wye.dType.INTEGER, 0),)

            def start(stack):
                #print("EditLibaryVerbCallback start")
                return Wye.codeFrame(WyeUI.EditLibCallback.EditLibaryVerbCallback, stack)

            def run(frame):
                data = frame.eventData
                rowIx = data[1][0]
                btnFrm = data[1][1]
                dlgFrm = data[1][2]
                verb = data[1][3]
                match(frame.PC):
                    case 0:
                        #print("EditLibaryVerbCallback run: event data", frame.eventData)
                        #print("EditLibaryVerbCallback data=", frame.eventData, " index = ", frame.eventData[1][0])

                        # open object editor
                        edFrm = WyeCore.libs.WyeUI.EditVerb.start(frame.SP)
                        edFrm.params.verb = [verb]
                        edFrm.params.parent = [dlgFrm]
                        edFrm.params.position = [(.5, -1.3, -.5 + btnFrm.vars.position[0][2]),]

                        frame.SP.append(edFrm)
                        frame.PC += 1

                    case 1:
                        edFrm = frame.SP.pop()  # remove dialog frame from stack
                        print("EditLibraryVerbCallback case 1: popped frame", edFrm.verb.__name__)
                        frame.status = Wye.status.SUCCESS  # done


    # class instance is called when user clicks on a graphic object that has a WyeID tag
    # fires up Wye's ObjEditor object with the given object to edit
    class ObjEditCtl(DirectObject):
        def __init__(self):
            self.currObj = None

        # User clicked on object.  It alt key down and it's editable, open the editor
        # note: all object frames must have a "position" variable with the object's position in it
        # for edit and debug dialog's to be positioned near
        def tagClicked(self, wyeID, pos):
            status = False      # assume we won't use this tag
            #print("ObjEditCtl tagClicked")
            if base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.control()):
                frm = WyeCore.World.getRegisteredObj(wyeID)
                if not frm is None:
                    #print("wyeID", wyeID, " Is registered")
                    #print("ObjEditCtl: Edit object", frm.verb.__name__)

                    # fire up object editor with given frame
                    #print("ObjEditorCtl: Create ObjEditor")
                    edFrm = WyeCore.World.startActiveObject(WyeCore.libs.WyeUI.EditVerb)
                    edFrm.params.position = [(frm.vars.position[0][0], frm.vars.position[0][1], frm.vars.position[0][2]),]
                    edFrm.params.parent = [None]
                    #print("ObjEditorCtl: Fill in ObjEditor objFrm param")

                    # if this is one subframe of a parallel stream, edit the parent
                    if frm.verb is WyeCore.ParallelStream:
                        #print(frm.verb.__name__, " is parallel stream, get parent", frm.parentFrame.verb.__name__)
                        frm = frm.parentFrame
                    edFrm.params.verb = [frm.verb]

                    status = True     # tell caller we used the tag

            # if alt key down then debug
            elif base.mouseWatcherNode.getModifierButtons().isDown(KeyboardButton.alt()):
                #print("ObjEditCtl tag Clicked: Alt held down, is wyeID registered?")
                frm = WyeCore.World.getRegisteredObj(wyeID)
                if not frm is None:
                    #print("wyeID", wyeID, " Is registered")
                    #print("ObjEditCtl: Edit object", frm.verb.__name__)

                    # set up object to be put on active list
                    #print("ObjEditorCtl: Create ObjDebugger")
                    stk = []            # create stack to run object on
                    dbgFrm = WyeCore.libs.WyeUI.ObjectDebugger.start(stk)  # start obj debugger and get its stack frame
                    dbgFrm.params.objFrm = [frm]  # put object to edit in editor frame
                    dbgFrm.params.position = [[frm.vars.position[0][0], frm.vars.position[0][1], frm.vars.position[0][2]],]
                    stk.append(dbgFrm)  # put obj debugger on its stack

                    # put object frame on active list
                    WyeCore.World.startActiveFrame(dbgFrm)
                    #print("ObjEditorCtl: Fill in ObjEditor objFrm param")

                    status = True     # tell caller we used the tag

            # return status true if used tag, false if someone else can have it
            return status

    # put up object dialog for given object
    class EditVerb:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("verb", Wye.dType.OBJECT, Wye.access.REFERENCE),     # library verb to edit
                      ("parent", Wye.dType.OBJECT, Wye.access.REFERENCE),   # parent dialog, if any
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE))  # object frame to edit
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("paramInpLst", Wye.dType.OBJECT_LIST, None),   # Inputs showing params
                    ("varInpLst", Wye.dType.OBJECT_LIST, None),     # Inputs showing vars
                    ("newParamDesc", Wye.dType.OBJECT_LIST, None),  # Build new verb params here
                    ("newVarDesc", Wye.dType.OBJECT_LIST, None),    # Build new verb vars here
                    ("newCodeDesc", Wye.dType.OBJECT_LIST, None),   # Build new verb code here
                    )

        # global list of frames being edited
        activeVerbs = {}

        def start(stack):
            #print("EditVerb start")
            f = Wye.codeFrame(WyeUI.EditVerb, stack)
            f.vars.paramInpLst[0] = []
            f.vars.varInpLst[0] = []
            f.vars.newParamDesc = []
            f.vars.newVarDesc = []
            f.vars.newCodeDesc = []
            return f

        def run(frame):
            verb = frame.params.verb[0]  # shorthand
            match(frame.PC):
                case 0:
                    #print("EditVerb run case 0")

                    # test midi player
                    #pygame.midi.init()
                    #player = pygame.midi.Output(0)
                    #for ins in range(127):
                    #    print("Midi Instrument", ins)
                    #    player.set_instrument(ins)
                    #    player.note_on(64, 64)
                    #    time.sleep(1)
                    #    player.note_off(64, 64)
                    #del player
                    #pygame.midi.quit()

                    # only edit frame once
                    if verb in WyeUI.EditVerb.activeVerbs:
                        print("Already editing this library", verb.library.__name__, " verb", verb.__name__)
                        # take self off active object list
                        WyeCore.World.stopActiveObject(frame)
                        frame.status = Wye.status.FAIL
                        return

                    # mark this frame actively being edited
                    WyeUI.EditVerb.activeVerbs[verb] = True

                    # create object dialog
                    #dlgFrm = WyeCore.libs.WyeUI.DropDown.start([])
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Edit Object " + verb.__name__]
                    #print("Edit object", verb.__name__)
                    dlgFrm.params.position = [[frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2]],]
                    dlgFrm.params.parent = frame.params.parent


                    # build dialog

                    # params
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Parameters:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if len(verb.paramDescr) > 0:     # if we have params, list them

                        attrIx = 0

                        for param in verb.paramDescr:
                            # make the dialog row
                            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [None]
                            btnFrm.params.parent = [None]
                            btnFrm.params.label = ["  '"+param[0] + "' "+Wye.dType.tostring(param[1]) + " call by:"+Wye.access.tostring(param[2])]
                            btnFrm.params.callback = [WyeCore.libs.WyeUI.EditParamCallback]  # button callback
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb)]  # button row, dialog frame
                            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                            attrIx += 1

                    # else no params to edit
                    else:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <no parameters>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])

                    # vars
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Variables:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if len(verb.varDescr) > 0:
                        attrIx = 0

                        for var in verb.varDescr:
                            # make the dialog row
                            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [None]
                            btnFrm.params.parent = [None]
                            btnFrm.params.label = ["  '"+var[0] + "' "+Wye.dType.tostring(var[1]) + " = "+str(var[2])]
                            btnFrm.params.callback = [WyeCore.libs.WyeUI.EditVarCallback]  # button callback
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb)]  # button row, dialog frame
                            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                            attrIx += 1


                    # else no vars to edit
                    else:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <no variables>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])


                    # code
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Wye Code:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if hasattr(verb, "codeDescr") and len(verb.codeDescr) > 0:
                        # If it's parallel code blocks
                        if verb.mode == Wye.mode.PARALLEL:
                                lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                                lblFrm.params.frame = [None]  # return value
                                lblFrm.params.parent = [None]
                                lblFrm.params.label = ["  <TODO - Parallel Code>"]
                                WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                                dlgFrm.params.inputs[0].append([lblFrm])
                        # regular boring normal single stream code
                        else:
                            level = 2       # starting indent for nesting tuple data
                            attrIx = 0      # This level code row
                            row = [0]       # dialog row, including recursively displayed tuple data
                            for tuple in verb.codeDescr:
                                WyeCore.libs.WyeUI.EditVerb.displayTuple(tuple, level, verb, attrIx, row, dlgFrm)

                                attrIx += 1

                    # no code to edit
                    else:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <no editable code>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])

                    # Test edited code
                    tstLblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    tstLblFrm.params.frame = [None]
                    tstLblFrm.params.parent = [None]
                    tstLblFrm.params.label = ["Test:"]
                    tstLblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(tstLblFrm)
                    dlgFrm.params.inputs[0].append([tstLblFrm])

                    tstBtnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([tstBtnFrm])
                    tstBtnFrm.params.frame = [None]
                    tstBtnFrm.params.parent = [None]
                    tstBtnFrm.params.label = ["  Check Code"]
                    tstBtnFrm.params.callback = [WyeCore.libs.WyeUI.TestCodeCallback]  # button callback
                    tstBtnFrm.params.optData = [(tstBtnFrm, dlgFrm, verb)]  # button row, dialog frame
                    WyeCore.libs.WyeUI.InputButton.run(tstBtnFrm)

                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    frame.SP.pop()  # remove dialog frame from stack
                    WyeUI.EditVerb.activeVerbs.pop(verb)
                    #print("ObjEditor: returned status", frame.vars.dlgStat[0])  # Wye.status.tostring(frame.))
                    frame.status = Wye.status.SUCCESS  # done


        # make the object editor dialog code row recursively
        # level is the recursion level (starting at 2)
        # verb is the verb being edited
        # attrIx is the row within the verb's codeDescr
        # row is the dialog row (since recursion expands the codeDescr rows)
        # dlgFrm is the dialog being added to
        def displayTuple(tuple, level, verb, attrIx, row, dlgFrm):
            indent = "".join(["    " for l in range(level)])      # indent by recursion depth
            #print("level", level, " indent '"+indent+"' tuple", tuple)

            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
            dlgFrm.params.inputs[0].append([btnFrm])
            btnFrm.params.frame = [None]
            btnFrm.params.parent = [None]

            # fill in text and callback based on code row type
            if not tuple[0] is None and "." in tuple[0]:
                vStr = str(tuple[0])
                if vStr.startswith("WyeCore.libs."):
                    vStr = vStr[13:]
                btnFrm.params.label = [indent + "Verb: " + vStr]
                btnFrm.params.callback = [WyeCore.libs.WyeUI.EditVerbCallback]  # button callback

                # display verb's params (if any)
                if len(tuple) > 1:
                    for paramTuple in tuple[1:]:
                        row[0] += 1
                        WyeCore.libs.WyeUI.EditVerb.displayTuple(paramTuple, level+1, verb, attrIx, row, dlgFrm)
            else:
                match tuple[0]:
                    case "Code" | None:  # raw Python
                        btnFrm.params.label = [indent + "Code: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback
                    case "CodeBlock":  # multi-line raw Python
                        btnFrm.params.label = [indent + "CodeBLock: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback
                    case "Expr":
                        btnFrm.params.label = [indent + "Expression: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback
                    case "Const":
                        btnFrm.params.label = [indent + "Constant: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback

                    case "Var":
                        btnFrm.params.label = [indent + "Variable: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback

                    case "Var=":
                        btnFrm.params.label = [indent + "Variable=: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditCodeCallback]  # button callback

                    case "GoTo":
                        btnFrm.params.label = [indent + " GoTo: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditSpecialCallback]  # button callback

                    case "Label":
                        btnFrm.params.label = [indent + "Label: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditSpecialCallback]  # button callback

                    case "IfGoTo":
                        btnFrm.params.label = [indent + "If GoTo: " + tuple[1]]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.EditSpecialCallback]  # button callback

            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, verb, tuple)]  # button row, dialog frame
            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

    ######################
    # VerbEditor Button Callback classes
    # Callback gets passed eventData = (buttonTag, optUserData, buttonFrm)
    ######################


    # put up code edit dialog for given verb
    # put up dropdown to select other verb from library - or other library
    class EditVerbCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("verb", Wye.dType.OBJECT, Wye.access.REFERENCE),)  # object frame to edit
        varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),  # object dialog frame
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    ("libName", Wye.dType.STRING, ""),
                    ("libNames", Wye.dType.STRING_LIST, []),
                    ("verbName", Wye.dType.STRING, ""),
                    ("verbNames", Wye.dType.STRING_LIST, []),
                    )

        # global list of frames being edited
        activeVerbs = {}

        tempLib = None      # lib holding new version of verb

        noneSelected = "<none selected>"

        def start(stack):
            return Wye.codeFrame(WyeUI.EditVerbCallback, stack)

        def run(frame):
            data = frame.eventData
            # print("EditVerbCallback data='" + str(data) + "'")
            varIx = data[1][0]      # offset to parameter in object's paramDescr list
            btnFrm = data[1][1]
            parentFrame = data[1][2]
            verb = data[1][3]
            match (frame.PC):
                case 0:
                    # build verb select/edit dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.position = [(.5, -.5, -.5 + btnFrm.vars.position[0][2]),]
                    dlgFrm.params.parent = [parentFrame]
                    dlgFrm.params.title = ["Select Library and Verb"]

                    # split verb into lib, verb dropowns

                    # build lib list for dropdown
                    attrIx = [0]
                    rowIx = [0]

                    libName, verbName = btnFrm.params.label[0].split(".")
                    libName = libName.split(":")[1].strip()
                    verbName = verbName.strip()
                    frame.vars.libName[0] = libName

                    #print("lib", libName, " verb", verbName, " from ", btnFrm.params.label[0])

                    # do this here so can ref it in lib callback data
                    verbFrm = WyeCore.libs.WyeUI.InputDropdown.start(dlgFrm.SP)


                    libFrm = WyeCore.libs.WyeUI.InputDropdown.start(dlgFrm.SP)
                    libFrm.params.frame = [None]
                    libFrm.params.parent = [None]
                    libFrm.params.label = ["Library"]
                    frame.vars.libNames[0] = [lib.__name__ for lib in WyeCore.World.libList]
                    frame.vars.libName[0] = libName
                    libFrm.params.list = frame.vars.libNames
                    libFrm.params.selectionIx = [frame.vars.libNames[0].index(libName)]
                    libFrm.params.callback = [WyeCore.libs.WyeUI.EditVerbCallback.SelectLibCallback]
                    libFrm.params.optData = ((varIx, libFrm, dlgFrm, verb, frame.vars.libName, verbFrm),)
                    libFrm.verb.run(libFrm)
                    dlgFrm.params.inputs[0].append([libFrm])


                    # build verb list for 2nd dropdown

                    frame.vars.verbNames[0] = frame.verb.buildVerbList(libName)

                    # fill in rest of verb drop down
                    verbFrm.params.frame = [None]
                    btnFrm.params.parent = [None]
                    verbFrm.params.label = ["Verb"]
                    verbFrm.params.list = frame.vars.verbNames
                    frame.vars.verbName[0] = verbName
                    #print("find verName", verbName, " in ", frame.vars.verbNames)
                    verbFrm.params.selectionIx = [frame.vars.verbNames[0].index(verbName)]
                    verbFrm.params.callback = [WyeCore.libs.WyeUI.EditVerbCallback.SelectVerbCallback]
                    verbFrm.params.optData = ((varIx, verbFrm, dlgFrm, verb, frame.vars.verbName),)
                    verbFrm.verb.run(verbFrm)
                    dlgFrm.params.inputs[0].append([verbFrm])


                    frame.SP.append(dlgFrm)
                    # (if change lib, then have to rebuild verb dropdown)

                    frame.PC += 1
                case 1:
                    dlgFrm = frame.SP.pop()
                    if frame.vars.dlgStat[0] == Wye.status.SUCCESS:
                        # print("InputDropdownCallback done, success, set row label to", dlgFrm.vars.currInp[0])
                        print("EditVerbCallback Success: lib", frame.vars.libName[0], " verb", frame.vars.verbName[0])
                        if frame.vars.verbName[0] == WyeCore.libs.WyeUI.EditVerbCallback.noneSelected:
                            print("no valid verb")


                    frame.status = dlgFrm.status

        # given the name of a library, get the list of verb names in the library
        def buildVerbList(libName):
            #print("libName", libName)
            verbLst = []
            lib = WyeCore.World.libDict[libName]
            for attr in dir(lib):
                if attr != "__class__":
                    libVerb = getattr(lib, attr)
                    if inspect.isclass(libVerb):
                        verbLst.append(libVerb.__name__)
            return verbLst

        class SelectLibCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                #print("SelectLibCallback started")
                return Wye.codeFrame(WyeUI.EditVerbCallback.SelectLibCallback, stack)

            def run(frame):
                data = frame.eventData
                varIx = data[1][0]  # offset to parameter in object's paramDescr list
                btnFrm = data[1][1]
                parentFrame = data[1][2]
                verb = data[1][3]
                libNameLst = data[1][4]
                verbFrm = data[1][5]

                # if lib changed, invalidate verb dropdown
                newLib = btnFrm.vars.list[0][btnFrm.params.selectionIx[0]]
                #print("SelectLibCallback old lib", libNameLst[0], " new lib", newLib)
                if libNameLst[0] != newLib:
                    libNameLst[0] = newLib
                    verbLst = WyeCore.libs.WyeUI.EditVerbCallback.buildVerbList(libNameLst[0])
                    verbLst.append(WyeCore.libs.WyeUI.EditVerbCallback.noneSelected)
                    verbFrm.verb.setList(verbFrm,verbLst, len(verbLst)-1)

                    # jam <none selected> into current verb"
                    # todo - uggly - better to just use the index everywhere
                    verbFrm.params.optData[0][4][0] = verbFrm.vars.list[0][len(verbLst)-1]



        class SelectVerbCallback:
            mode = Wye.mode.SINGLE_CYCLE
            dataType = Wye.dType.STRING
            paramDescr = ()
            varDescr = ()

            def start(stack):
                #print("SelectVerbCallback started")
                return Wye.codeFrame(WyeUI.EditVerbCallback.SelectVerbCallback, stack)

            def run(frame):
                data = frame.eventData
                varIx = data[1][0]  # offset to parameter in object's paramDescr list
                btnFrm = data[1][1]
                parentFrame = data[1][2]
                verb = data[1][3]
                verbNameLst = data[1][4]

                #print("SelectVerbCallback data='" + str(frame.eventData) + "'")
                newVerb = btnFrm.vars.list[0][btnFrm.params.selectionIx[0]]
                #print("SelectLibCallback old verb", verbNameLst[0], " new verb", newVerb)
                verbNameLst[0] = newVerb


    class EditCodeCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("tuple", Wye.dType.OBJECT, None),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    )

        def start(stack):
            #print("EditCodeCallback started")
            return Wye.codeFrame(WyeUI.EditCodeCallback, stack)

        def run(frame):
            data = frame.eventData
            rowIx = data[1][0]  # offset to parameter in object's paramDescr list
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            verb = data[1][3]
            tuple = data[1][4]

            match (frame.PC):
                case 0:
                    print("EditCodeCallback data='" + str(frame.eventData) + "'")

                    # build code dialog
                    # TODO - build this out to handle all diff code types
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    frame.vars.tuple[0] = tuple

                    if verb.mode == Wye.mode.PARALLEL:
                        print("Don't know how to edit parallel code yet")
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Editing parallel code not supported yet"]
                        dlgFrm.params.parent = [dlgFrm]
                        dlgFrm.params.position = [(.5, -.3, -.5 + btnFrm.vars.position[0][2]), ]

                    else:
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Edit Code"]
                        dlgFrm.params.parent = [parentFrm]
                        dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                        # Code type
                        verbType = verb.codeDescr[rowIx][0]
                        if verbType is None:
                            verbType = "Code"

                        # verb type/name
                        verbNameFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                        verbNameFrm.params.frame = [None]        # placeholder
                        verbNameFrm.params.label = ["Op:"]
                        verbNameFrm.params.value = [verbType]
                        WyeCore.libs.WyeUI.InputText.run(verbNameFrm)
                        dlgFrm.params.inputs[0].append([verbNameFrm])

                        # Code
                        codeFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                        codeFrm.params.frame = [None]        # placeholder
                        codeFrm.params.label = ["Expr:"]
                        codeFrm.params.value = [tuple[1]]
                        WyeCore.libs.WyeUI.InputText.run(codeFrm)
                        dlgFrm.params.inputs[0].append([codeFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1

                case 1:
                    dlgFrm = frame.SP.pop()
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        # save back to code
                        pass

                    frame.status = dlgFrm.status

    class EditSpecialCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),
                    ("tuple", Wye.dType.OBJECT, None),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                   )

        def start(stack):
            return Wye.codeFrame(WyeUI.EditSpecialCallback, stack)

        def run(frame):
            data = frame.eventData
            rowIx = data[1][0]  # offset to parameter in object's paramDescr list
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            verb = data[1][3]
            tuple = data[1][4]

            match (frame.PC):
                case 0:
                    print("EditSpecialCallback data='" + str(frame.eventData) + "'")

                    # build code dialog
                    # TODO - build this out to handle all diff code types
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    frame.vars.tuple[0] = tuple

                    if verb.mode == Wye.mode.PARALLEL:
                        print("Don't know how to edit parallel code yet")
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Editing parallel code not supported yet"]
                        dlgFrm.params.parent = [dlgFrm]
                        dlgFrm.params.position = [(.5, -.3, -.5 + btnFrm.vars.position[0][2]), ]

                    else:
                        dlgFrm.params.retVal = frame.vars.dlgStat
                        dlgFrm.params.title = ["Edit Code"]
                        dlgFrm.params.parent = [parentFrm]
                        dlgFrm.params.position = [(.5, -.3, -.5 + btnFrm.vars.position[0][2]), ]

                        # Code type
                        verbType = verb.codeDescr[rowIx][0]

                        # verb type/name
                        verbNameFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                        verbNameFrm.params.frame = [None]  # placeholder
                        verbNameFrm.params.label = ["Op:"]
                        verbNameFrm.params.value = [verbType]
                        WyeCore.libs.WyeUI.InputText.run(verbNameFrm)
                        dlgFrm.params.inputs[0].append([verbNameFrm])

                        # Code
                        codeFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                        codeFrm.params.frame = [None]  # placeholder
                        codeFrm.params.label = ["Expr:"]
                        codeFrm.params.value = [tuple[1]]
                        WyeCore.libs.WyeUI.InputText.run(codeFrm)
                        dlgFrm.params.inputs[0].append([codeFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1

                case 1:
                    dlgFrm = frame.SP.pop()
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        # save back to code
                        pass

                    frame.status = dlgFrm.status


    class EditParamCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("paramName", Wye.dType.STRING, "<name>"),
                    ("paramType", Wye.dType.STRING, "<type>"),
                    ("paramAccess", Wye.dType.STRING, "<access>"),
                    )

        def start(stack):
            #print("EditParamCallback started")
            return Wye.codeFrame(WyeUI.EditParamCallback, stack)

        def run(frame):
            data = frame.eventData
            paramIx = data[1][0]
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            verb = data[1][3]
            #print("param ix", data[1][0], " parentFrm", parentFrm.verb.__name__, " verb", verb.__name__)

            match (frame.PC):
                case 0:
                    #print("EditParamCallback data='" + str(data) + "'")
                    # build param dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    nParams = len(verb.paramDescr)

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Edit Parameter"]
                    dlgFrm.params.parent = [parentFrm]
                    #print("EditParamCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                    dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                    # param name
                    frame.vars.paramName[0] = verb.paramDescr[paramIx][0]
                    paramNameFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    paramNameFrm.params.frame = [None]        # placeholder
                    paramNameFrm.params.label = ["Name: "]
                    paramNameFrm.params.value = frame.vars.paramName
                    WyeCore.libs.WyeUI.InputText.run(paramNameFrm)
                    dlgFrm.params.inputs[0].append([paramNameFrm])

                    # param type
                    frame.vars.paramType[0] = verb.paramDescr[paramIx][1]
                    paramTypeFrm = WyeCore.libs.WyeUI.InputDropdown.start(dlgFrm.SP)
                    paramTypeFrm.params.frame = [None]
                    paramTypeFrm.params.label = ["Type: "]
                    paramTypeFrm.params.list = [[Wye.dType.tostring(x) for x in Wye.dType.dTypeList]]
                    paramTypeFrm.params.selectionIx = [Wye.dType.dTypeList.index(frame.vars.paramType[0])]
                    paramTypeFrm.params.callback = [WyeCore.libs.WyeUI.EditParamTypeCallback]
                    paramTypeFrm.params.optData = ((paramIx, paramTypeFrm, dlgFrm, verb, frame.vars.paramType[0]),)    # var to return chosen type in
                    paramTypeFrm.verb.run(paramTypeFrm)
                    dlgFrm.params.inputs[0].append([paramTypeFrm])

                    # param access method
                    frame.vars.paramAccess[0] = Wye.access.tostring(verb.paramDescr[paramIx][2])
                    paramAccessFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    paramAccessFrm.params.frame = [None]
                    paramAccessFrm.params.label = ["Access: "]
                    paramAccessFrm.params.value = frame.vars.paramAccess
                    WyeCore.libs.WyeUI.InputText.run(paramAccessFrm)
                    dlgFrm.params.inputs[0].append([paramAccessFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1
                case 1:
                    dlgFrm = frame.SP.pop()
                    # check status to see if values should be used
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        label = dlgFrm.params.inputs[0][0][0].params.value[0]
                        typeIx = dlgFrm.params.inputs[0][1][0].params.selectionIx[0]
                        wType = Wye.dType.dTypeList[typeIx]
                        accessVal = dlgFrm.params.inputs[0][2][0].params.value[0]
                        accessCode = Wye.access.REFERENCE    # default
                        accessStr = "REFERENCE"
                        match(accessVal.upper()):
                            case "VALUE":
                                accessStr = "VALUE"
                                accessCode = Wye.access.VALUE
                            case "REFERENCE":
                                accessStr = "REFERENCE"
                                accessCode = Wye.access.REFERENCE

                        # param descriptions are constants so have to rebuild the whole thing
                        preDescr = verb.paramDescr[:paramIx]
                        postDescr = verb.paramDescr[paramIx+1:]
                        descr = ((label, wType, accessCode), )
                        verb.paramDescr = preDescr + descr + postDescr

                        rowTxt = "  '" + label + "' " + Wye.dType.tostring(wType) + " call by:" + accessStr
                        #print("new row", rowTxt)
                        btnFrm.verb.setLabel(btnFrm, rowTxt)

                    frame.status = Wye.status.SUCCESS


    # Param edit type button callback: put up dropdown for variable type
    class EditParamTypeCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            #print("EditParamTypeCallback started")
            return Wye.codeFrame(WyeUI.EditParamTypeCallback, stack)

        def run(frame):
            #print("EditParamTypeCallback")
            match (frame.PC):
                case 0:
                    data = frame.eventData
                    #print("EditParamTypeCallback data='" + str(data) + "'")
                    frm = data[1][1]
                    #print("param ix", data[1][0], " data frame", frm.verb.__name__)
                    frame.PC += 1
                case 1:
                    pass


    # Object variable callback: put up variable edit dialog
    class EditVarCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("varName", Wye.dType.STRING, "<name>"),
                    ("varType", Wye.dType.STRING, "<type>"),
                    ("varVal", Wye.dType.STRING, "<val>"),
                    )

        def start(stack):
            #print("EditVarCallback started")
            return Wye.codeFrame(WyeUI.EditVarCallback, stack)

        def run(frame):
            data = frame.eventData
            # print("EditVarCallback data='" + str(data) + "'")
            varIx = data[1][0]      # offset to parameter in object's paramDescr list
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            verb = data[1][3]
            #print("param ix", data[1][0], " parentFrm", parentFrm.verb.__name__, " verb", verb.__name__)

            match (frame.PC):
                case 0:
                    # build var dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    nParams = len(verb.paramDescr)
                    nVars = len(verb.varDescr)

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Edit Variable"]
                    dlgFrm.params.parent = [parentFrm]
                    #print("EditVarCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                    dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                    # Var name
                    frame.vars.varName[0] = verb.varDescr[varIx][0]
                    varNameFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    varNameFrm.params.frame = [None]        # placeholder
                    varNameFrm.params.label = ["Name: "]
                    varNameFrm.params.value = frame.vars.varName
                    WyeCore.libs.WyeUI.InputText.run(varNameFrm)
                    dlgFrm.params.inputs[0].append([varNameFrm])

                    # Var type
                    frame.vars.varType[0] = verb.varDescr[varIx][1]
                    varTypeFrm = WyeCore.libs.WyeUI.InputDropdown.start(dlgFrm.SP)
                    varTypeFrm.params.frame = [None]
                    varTypeFrm.params.label = ["Type: "]
                    varTypeFrm.params.list = [[Wye.dType.tostring(x) for x in Wye.dType.dTypeList]]
                    varTypeFrm.params.selectionIx = [Wye.dType.dTypeList.index(frame.vars.varType[0])]
                    varTypeFrm.params.callback = [WyeCore.libs.WyeUI.EditVarTypeCallback]
                    varTypeFrm.params.optData = ((varIx, varTypeFrm, dlgFrm, verb, frame.vars.varType[0]),)    # var to return chosen type in
                    varTypeFrm.verb.run(varTypeFrm)
                    dlgFrm.params.inputs[0].append([varTypeFrm])

                    # Var initial value
                    frame.vars.varVal[0] = str(verb.varDescr[varIx][2])
                    varValFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    varValFrm.params.frame = [None]
                    varValFrm.params.label = ["Value: "]
                    varValFrm.params.value = frame.vars.varVal
                    WyeCore.libs.WyeUI.InputText.run(varValFrm)
                    dlgFrm.params.inputs[0].append([varValFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1

                case 1:
                    dlgFrm = frame.SP.pop()
                    # check status to see if values should be used
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        label = dlgFrm.params.inputs[0][0][0].params.value[0]
                        typeIx = dlgFrm.params.inputs[0][1][0].params.selectionIx[0]
                        wType = Wye.dType.dTypeList[typeIx]
                        initVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                        # convert initVal to appropriate type
                        initVal = Wye.dType.convertType(initVal, wType)

                        # var descriptions are constants so have to rebuild the whole thing
                        preDescr = verb.varDescr[:varIx]
                        postDescr = verb.varDescr[varIx+1:]
                        descr = ((label, wType, initVal), )
                        verb.varDescr = preDescr + descr + postDescr

                        rowTxt = "  '" + label + "' " + Wye.dType.tostring(wType) + " = " + str(initVal)
                        #print("new row", rowTxt)
                        btnFrm.verb.setLabel(btnFrm, rowTxt)

                    # either way, we're done
                    frame.status = Wye.status.SUCCESS

    # Var edit type button callback: put up dropdown for variable type
    class EditVarTypeCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            #print("EditVarTypeCallback started")
            return Wye.codeFrame(WyeUI.EditVarTypeCallback, stack)

        def run(frame):
            #print("EditVarTypeCallback")

            data = frame.eventData
            print("EditVarTypeCallback data='" + str(data) + "'")
            frm = data[1][1]
            print("param ix", data[1][0], " data frame", frm.verb.__name__)

    # check code for compile errors and highlight anything that needs fixing
    class TestCodeCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = ()

        def start(stack):
            #print("TestCodeCallback started")
            return Wye.codeFrame(WyeUI.TestCodeCallback, stack)

        def run(frame):
            data = frame.eventData
            print("TestCodeCallback data='" + str(data) + "'")
            btnFrm = data[1][0]
            parentFrm = data[1][1]
            verb = data[1][2]
            #print("param ix", data[1][0], " parentFrm", parentFrm.verb.__name__, " verb", verb.__name__)



    # show active objects (currently running object stacks)
    # so user can debug them
    class DebugMainDialog:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("objFrm", Wye.dType.OBJECT, Wye.access.REFERENCE),)  # object frame to edit
        varDescr = (("dlgFrm", Wye.dType.OBJECT, None),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    )

        # global list of frames being edited
        activeFrames = {}

        def start(stack):
            return Wye.codeFrame(WyeUI.DebugMainDialog, stack)


        def run(frame):
            match(frame.PC):
                case 0:
                    # create top level debug dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])
                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Wye Debugger"]
                    point = NodePath("point")
                    point.reparentTo(render)
                    point.setPos(base.camera, (0,10,0))
                    pos = point.getPos()
                    point.removeNode()
                    dlgFrm.params.position = [(pos[0], pos[1], pos[2]),]
                    dlgFrm.params.parent = [None]


                    # build dialog

                    # running objects
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]  # return value
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Active Objects:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    attrIx = [0]
                    row = [0]

                    for stack in WyeCore.World.objStacks:
                        WyeCore.libs.WyeUI.DebugMainDialog.listStack(stack, dlgFrm, row, attrIx, frame, 0)
                        attrIx[0] += 1

                    # if nothing running
                    if attrIx == 0:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["<no active objects>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])


                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    frame.SP.pop()  # remove dialog frame from stack
                    frame.status = Wye.status.SUCCESS  # done

                    # stop ourselves
                    WyeCore.World.stopActiveObject(WyeCore.World.debugger)
                    WyeCore.World.debugger = None

        def listStack(stack, dlgFrm, rowIx, attrIx, frame, level):
            indent = "".join(["  " for l in range(level)])      # indent by recursion depth
            sLen = len(stack)
            if sLen > 0:  # if there's something on the stack
                offset = 0
                for objFrm in stack:

                    # make the dialog row
                    btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                    dlgFrm.params.inputs[0].append([btnFrm])
                    btnFrm.params.frame = [None]  # return value
                    btnFrm.params.parent = [None]
                    if offset == 0:
                        btnFrm.params.label = [
                            indent + "  stack " + str(attrIx[0]) + " depth " + str(offset) + ":" + objFrm.verb.__name__]
                    else:
                        btnFrm.params.label = [indent + "                depth " + str(offset) + ":" + objFrm.verb.__name__]
                    btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugFrameCallback]  # button callback
                    btnFrm.params.optData = [
                        (rowIx[0], btnFrm, dlgFrm, objFrm, frame)]  # button row, row frame, dialog frame, obj frame
                    WyeCore.libs.WyeUI.InputButton.run(btnFrm)
                    offset += 1
                    rowIx[0] += 1

                # if bottom frame is a parallel frame, do all its stacks
                lastFrm = stack[-1]
                if isinstance(lastFrm, Wye.parallelFrame):
                    pAttrIx = [0]
                    for pStack in lastFrm.stacks:
                        WyeCore.libs.WyeUI.DebugMainDialog.listStack(pStack, dlgFrm, rowIx, pAttrIx, frame, level + 1)
                        pAttrIx[0] += 1
                        rowIx[0] += 1


    # User selected an object, open its frame in the debugger
    class DebugFrameCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                    ("dlgStat", Wye.dType.INTEGER, -1),

                    )

        def start(stack):
            # print("DebugFrameCallback started")
            return Wye.codeFrame(WyeUI.DebugFrameCallback, stack)


        def run(frame):
            match (frame.PC):
                case 0:
                    data = frame.eventData
                    #print("DebugFrameCallback data='" + str(data) + "'")
                    objRow = data[1][0]
                    parentFrame = data[1][2]
                    objFrm = data[1][3]
                    mainDbgFrm = data[1][4]
                    #print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)


                    objOffset = (objRow + 2) * .3
                    objPos = (2, -.5, -objOffset)
                    dbgFrm = WyeCore.libs.WyeUI.ObjectDebugger.start(frame.SP)
                    dbgFrm.params.objFrm = [objFrm]
                    dbgFrm.params.position = [[objPos[0], objPos[1], objPos[2]]]
                    dbgFrm.params.parent = [parentFrame]
                    frame.SP.append(dbgFrm)
                    frame.PC += 1
                case 1:
                    dbgFrm = frame.SP.pop()
                    # todo - if success then update object
                    frame.status = Wye.status.SUCCESS



    # Open up an object and debug it
    class ObjectDebugger:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        autoStart = False
        paramDescr = (("objFrm", Wye.dType.OBJECT, Wye.access.REFERENCE),  # object frame to edit
                      ("position", Wye.dType.FLOAT_LIST, Wye.access.REFERENCE),  # object position
                      ("parent", Wye.dType.OBJECT, Wye.access.REFERENCE),  # object parent
                      )
        varDescr = (("dlgFrm", Wye.dType.INTEGER, -1),
                    ("dlgStat", Wye.dType.INTEGER, -1),
                    ("paramInpLst", Wye.dType.OBJECT_LIST, None),
                    ("varInpLst", Wye.dType.OBJECT_LIST, None),
                    ("breakLst", Wye.dType.OBJECT_LIST, None),
                    )

        def start(stack):
            # print("EditVarTypeCallback started")
            f = Wye.codeFrame(WyeUI.ObjectDebugger, stack)
            f.vars.paramInpLst[0] = []
            f.vars.varInpLst[0] = []
            f.vars.breakLst[0] = []
            return f

        def run(frame):
            match (frame.PC):
                case 0:
                    objFrm = frame.params.objFrm[0]

                    # print("param ix", data[1][0], " debug frame", objFrm) # objFrm.verb.__name__)

                    # Display contents of frame in a dialog

                    # If parallel subframe, get parent frame data
                    # todo - debugging shd add dbg on/off.  For now, automatically set break point
                    if objFrm.verb is WyeCore.ParallelStream:
                        paramDescr = objFrm.parentFrame.verb.paramDescr
                        varDescr = objFrm.parentFrame.verb.varDescr
                        name = objFrm.parentFrame.verb.__name__
                        objFrm.parentFrame.breakpt = True
                        Wye.debugOn += 1  # make sure debugging is happening
                        #print("ObjectDebugger: set parallel parent breakpt on", objFrm.parentFrame.verb.__name__," debugOn to", Wye.debugOn)
                        #print(">>>>>>1 Set parallel breakpt true for ", objFrm.verb.__name__)
                    else:
                        paramDescr = objFrm.verb.paramDescr
                        varDescr = objFrm.verb.varDescr
                        name = objFrm.verb.__name__
                        objFrm.breakpt = True
                        Wye.debugOn += 1  # make sure debugging is happening
                        #print("ObjectDebugger: set breakpt on", objFrm.verb.__name__," debugOn to", Wye.debugOn)
                        #print(">>>>>>2 Set breakpt true for ", objFrm.verb.__name__)

                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Debug " + name]
                    dlgFrm.params.position = [[frame.params.position[0][0], frame.params.position[0][1], frame.params.position[0][2]],]
                    #print("ObjectDebugger frame.params.parent[0]", frame.params.parent[0])
                    if len(frame.params.parent) == 0 or isinstance(frame.params.parent[0], list):
                        dlgFrm.params.parent = [None]
                    else:
                        dlgFrm.params.parent = frame.params.parent

                    #print("ObjectDebugger objFrm", objFrm.tostring())
                    # params
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]  # return value
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Parameters:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    if len(paramDescr) > 0:     # if we have params, list them

                        attrIx = 0

                        for param in paramDescr:
                            # make the dialog row
                            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            btnFrm.params.frame = [None]  # return value
                            btnFrm.params.parent = [None]
                            paramVal = getattr(objFrm.params, param[0])
                            btnFrm.params.label = ["  '" + param[0] + "' " + Wye.dType.tostring(
                                param[1]) + " = " + str(paramVal)]
                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugParamCallback]  # button callback
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm)]  # button row, dialog frame
                            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                            attrIx += 1

                    # else nothing to do here
                    else:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <no parameters>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])

                    # vars
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]  # return value
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Variables:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])


                    if len(varDescr) > 0:       # if we have variables, list them

                        attrIx = 0

                        for var in varDescr:
                            # make the dialog row
                            btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                            dlgFrm.params.inputs[0].append([btnFrm])
                            frame.vars.varInpLst[0].append(btnFrm)
                            
                            btnFrm.params.frame = [None]  # return value
                            btnFrm.params.parent = [None]
                            varVal = getattr(objFrm.vars, var[0])
                            btnFrm.params.label = [
                                "  '" + var[0] + "' " + Wye.dType.tostring(var[1]) + " = " + str(varVal[0])]
                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugVarCallback]  # button callback
                            btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm)]  # button row, dialog frame
                            WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                            attrIx += 1
                            
                        # refresh
                        btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                        dlgFrm.params.inputs[0].append([btnFrm])
                        btnFrm.params.frame = [None]  # return value
                        btnFrm.params.parent = [None]
                        btnFrm.params.label = ["  Refresh Values"]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugRefreshVarCallback]  # button callback
                        btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm, frame)]  # button row, dialog frame
                        btnFrm.params.color = [(1,1,0,1)]
                        WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                        # Step
                        btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                        dlgFrm.params.inputs[0].append([btnFrm])
                        btnFrm.params.frame = [None]  # return value
                        btnFrm.params.parent = [None]
                        btnFrm.params.label = ["  Step"]
                        btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugStepCallback]  # button callback
                        btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm, frame)]  # button row, dialog frame
                        btnFrm.params.color = [(1,1,0,1)]
                        WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                    # else nothing to do here
                    else:
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <no variables>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])

                    # build dialog frame params list of input frames
                    lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    lblFrm.params.frame = [None]
                    lblFrm.params.parent = [None]
                    lblFrm.params.label = ["Wye Code:"]
                    lblFrm.params.color = [Wye.color.SUBHDR_COLOR]
                    WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                    dlgFrm.params.inputs[0].append([lblFrm])

                    attrIx = 0

                    # Need meta layer to display parallel code blocks
                    if isinstance(objFrm, Wye.parallelFrame):
                        lblFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                        lblFrm.params.frame = [None]  # return value
                        lblFrm.params.parent = [None]
                        lblFrm.params.label = ["  <TODO - Parallel Code>"]
                        WyeCore.libs.WyeUI.InputLabel.run(lblFrm)
                        dlgFrm.params.inputs[0].append([lblFrm])
                    # regular boring normal single stream code
                    else:
                        if hasattr(objFrm, "codeDescr"):
                            for tuple in objFrm.verb.codeDescr:
                                print("  do tuple ", tuple)
                                # make the dialog row
                                btnFrm = WyeCore.libs.WyeUI.InputButton.start(dlgFrm.SP)
                                dlgFrm.params.inputs[0].append([btnFrm])
                                btnFrm.params.frame = [None]  # return value
                                btnFrm.params.parent = [None]

                                # fill in text and callback based on code row type
                                if tuple[0] is None:
                                    btnFrm.params.label = ["  Code: " + tuple[1]]
                                    btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback
                                elif "." in tuple[0]:
                                    vStr = str(tuple[0])
                                    if vStr.startswith("WyeCore.libs."):
                                        vStr = vStr[13:]
                                    btnFrm.params.label = ["  Verb: " + vStr + ", " + str(tuple[1])]
                                    btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugVerbCallback]  # button callback
                                else:
                                    match tuple[0]:
                                        case "Code":         # raw Python
                                            btnFrm.params.label = ["  Code: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback
                                        case "CodeBlock":    # multi-line raw Python
                                            btnFrm.params.label = ["  CodeBLock: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback
                                        case "Expr":
                                            btnFrm.params.label = ["  Expression: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback
                                        case "Const":
                                            btnFrm.params.label = ["  Constant: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback

                                        case "Var":
                                            btnFrm.params.label = ["  Variable: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback

                                        case "Var=":
                                            btnFrm.params.label = ["  Variable=: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugCodeCallback]  # button callback

                                        case "GoTo":
                                            btnFrm.params.label = ["  GoTo: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugSpecialCallback]  # button callback

                                        case "Label":
                                            btnFrm.params.label = ["  Label: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugSpecialCallback]  # button callback

                                        case "IfGoTo":
                                            btnFrm.params.label = ["  If GoTo: " + tuple[1]]
                                            btnFrm.params.callback = [WyeCore.libs.WyeUI.DebugSpecialCallback]  # button callback

                                btnFrm.params.optData = [(attrIx, btnFrm, dlgFrm, objFrm, tuple)]  # button row, dialog frame
                                WyeCore.libs.WyeUI.InputButton.run(btnFrm)

                    # WyeUI.Dialog.run(dlgFrm)
                    frame.SP.append(dlgFrm)  # push dialog so it runs next cycle

                    frame.PC += 1  # on return from dialog, run next case

                case 1:
                    frame.SP.pop()  # remove dialog frame from stack
                    # print("ObjDebugger: returned status", frame.vars.dlgStat[0])  # Wye.status.tostring(frame.))
                    frame.status = Wye.status.SUCCESS  # done

                    # turn obj breakpt off
                    objFrm = frame.params.objFrm[0]
                    if objFrm.verb is WyeCore.ParallelStream:
                        objFrm.parentFrame.breakpt = False
                        Wye.debugOn -= 1
                        #print("ObjectDebugger remove breakpt on", objFrm.parentFrame.verb.__name__," reduce debugOn to", Wye.debugOn)
                        if hasattr(objFrm.parentFrame, "prevStatus"):
                            objFrm.status = objFrm.parentFrame.prevStatus
                    else:
                        objFrm.breakpt = False
                        Wye.debugOn -= 1
                        #print("ObjectDebugger remove breakpt on", objFrm.verb.__name__," reduce debugOn to", Wye.debugOn)
                        if hasattr(objFrm, "prevStatus"):
                            objFrm.status = objFrm.prevStatus

        def refresh(frame):
            objFrm = frame.params.objFrm[0]
            if objFrm.verb is WyeCore.ParallelStream:
                varDescr = objFrm.parentFrame.verb.varDescr
            else:
                varDescr = objFrm.verb.varDescr

            attrIx = 0
            for btnFrm in frame.vars.varInpLst[0]:
                # update the given input
                var = varDescr[attrIx]
                varVal = getattr(objFrm.vars, var[0])
                btnFrm.verb.setLabel(btnFrm, "  '" + var[0] + "' " + Wye.dType.tostring(var[1]) + " = " + str(varVal[0]))

                attrIx += 1

    # Debug parameter callback: put up parameter edit dialog
    # TODO - finish this
    class DebugParamCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("paramName", Wye.dType.STRING, "<name>"),
                    ("paramType", Wye.dType.STRING, "<type>"),
                    ("paramVal", Wye.dType.STRING, "<val>"),
                    )

        def start(stack):
            #print("DebugParamCallback started")
            return Wye.codeFrame(WyeUI.DebugParamCallback, stack)

        def run(frame):
            data = frame.eventData
            # print("DebugParamCallback data='" + str(data) + "'")
            paramIx = data[1][0]      # offset to paramiable in object's paramDescr list
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            objFrm = data[1][3]
            if objFrm.verb is WyeCore.ParallelStream:
                paramDescr = objFrm.parentFrame.verb.paramDescr
            else:
                paramDescr = objFrm.verb.paramDescr

            match (frame.PC):
                case 0:
                    #print("param ix", data[1][0], " data frame", parentFrm.verb.__name__)

                    # build param dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    nParams = min(len(objFrm.verb.paramDescr), 1)
                    nParams = len(paramDescr)
                    paramIx = data[1][0]

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Edit Parameter"]
                    dlgFrm.params.parent = [parentFrm]
                    #print("DebugParamCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                    dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                    # Param name
                    frame.vars.paramName[0] = paramDescr[paramIx][0]
                    paramNameFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    paramNameFrm.params.frame = [None]        # placeholder
                    paramNameFrm.params.label = ["Name: "+frame.vars.paramName[0]]
                    WyeCore.libs.WyeUI.InputLabel.run(paramNameFrm)
                    dlgFrm.params.inputs[0].append([paramNameFrm])

                    # Param type
                    frame.vars.paramType[0] = paramDescr[paramIx][1]
                    paramTypeFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    paramTypeFrm.params.frame = [None]
                    paramTypeFrm.params.label = ["Type: "+Wye.dType.tostring(frame.vars.paramType[0])]
                    paramTypeFrm.verb.run(paramTypeFrm)
                    dlgFrm.params.inputs[0].append([paramTypeFrm])

                    # Param current value
                    print("DebugParamCallback get param", frame.vars.paramName[0])
                    frame.vars.paramVal[0] = getattr(objFrm.params, frame.vars.paramName[0])[0]
                    #print("paramVal[0]", frame.vars.paramVal[0])
                    paramValFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    paramValFrm.params.frame = [None]
                    paramValFrm.params.label = ["Value: "]
                    paramValFrm.params.value = [str(frame.vars.paramVal[0])]
                    WyeCore.libs.WyeUI.InputText.run(paramValFrm)
                    dlgFrm.params.inputs[0].append([paramValFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1

                case 1:
                    dlgFrm = frame.SP.pop()
                    # check status to see if values should be used
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        strVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                        # convert val to appropriate type
                        val = Wye.dType.convertType(strVal, frame.vars.paramType[0])

                        # if value has changed, update it
                        if val != frame.vars.paramVal[0]:
                            getattr(objFrm.params, frame.vars.paramName[0])[0] = val

                        rowStr = "  '" + frame.vars.paramName[0] + "' " + Wye.dType.tostring(frame.vars.paramType[0]) + " = " + str(val)
                        btnFrm.verb.setLabel(btnFrm, str(rowStr))

                    # either way, we're done
                    frame.status = Wye.status.SUCCESS


    # Debug variable callback: put up variable edit dialog
    class DebugVarCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                    ("varName", Wye.dType.STRING, "<name>"),
                    ("varType", Wye.dType.STRING, "<type>"),
                    ("varVal", Wye.dType.STRING, "<val>"),
                    )

        def start(stack):
            #print("DebugVarCallback started")
            return Wye.codeFrame(WyeUI.DebugVarCallback, stack)

        def run(frame):
            data = frame.eventData
            # print("DebugVarCallback data='" + str(data) + "'")
            varIx = data[1][0]      # offset to variable in object's varDescr list
            btnFrm = data[1][1]
            parentFrm = data[1][2]
            objFrm = data[1][3]
            if objFrm.verb is WyeCore.ParallelStream:
                varDescr = objFrm.parentFrame.verb.varDescr
            else:
                varDescr = objFrm.verb.varDescr

            match (frame.PC):
                case 0:
                    #print("param ix", data[1][0], " data frame", parentFrm.verb.__name__)

                    # build var dialog
                    dlgFrm = WyeCore.libs.WyeUI.Dialog.start([])

                    nParams = min(len(objFrm.verb.paramDescr), 1)
                    nVars = len(varDescr)
                    varIx = data[1][0]

                    dlgFrm.params.retVal = frame.vars.dlgStat
                    dlgFrm.params.title = ["Edit Variable"]
                    dlgFrm.params.parent = [parentFrm]
                    #print("DebugVarCallback title", dlgFrm.params.title, " dlgFrm.params.parent", dlgFrm.params.parent)
                    dlgFrm.params.position = [(.5,-.3, -.5 + btnFrm.vars.position[0][2]),]

                    # Var name
                    frame.vars.varName[0] = varDescr[varIx][0]
                    varNameFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    varNameFrm.params.frame = [None]        # placeholder
                    varNameFrm.params.label = ["Name: "+frame.vars.varName[0]]
                    WyeCore.libs.WyeUI.InputLabel.run(varNameFrm)
                    dlgFrm.params.inputs[0].append([varNameFrm])

                    # Var type
                    frame.vars.varType[0] = varDescr[varIx][1]
                    varTypeFrm = WyeCore.libs.WyeUI.InputLabel.start(dlgFrm.SP)
                    varTypeFrm.params.frame = [None]
                    varTypeFrm.params.label = ["Type: "+Wye.dType.tostring(frame.vars.varType[0])]
                    varTypeFrm.verb.run(varTypeFrm)
                    dlgFrm.params.inputs[0].append([varTypeFrm])

                    # Var current value
                    frame.vars.varVal[0] = getattr(objFrm.vars, frame.vars.varName[0])[0]
                    #print("varVal[0]", frame.vars.varVal[0])
                    varValFrm = WyeCore.libs.WyeUI.InputText.start(dlgFrm.SP)
                    varValFrm.params.frame = [None]
                    varValFrm.params.label = ["Value: "]
                    varValFrm.params.value = [str(frame.vars.varVal[0])]
                    WyeCore.libs.WyeUI.InputText.run(varValFrm)
                    dlgFrm.params.inputs[0].append([varValFrm])

                    frame.SP.append(dlgFrm)
                    frame.PC += 1

                case 1:
                    dlgFrm = frame.SP.pop()
                    # check status to see if values should be used
                    if dlgFrm.params.retVal[0] == Wye.status.SUCCESS:
                        strVal = dlgFrm.params.inputs[0][2][0].params.value[0]

                        # convert initVal to appropriate type
                        val = Wye.dType.convertType(strVal, frame.vars.varType[0])
                        #print("DebugVarCallback strVal", strVal, " type", Wye.dType.tostring(frame.vars.varType[0]), "converted type", type(val), " value", val)

                        # if value has changed, update it
                        if val != frame.vars.varVal[0]:
                            getattr(objFrm.vars, frame.vars.varName[0])[0] = val

                        rowStr = "  '" + frame.vars.varName[0] + "' " + Wye.dType.tostring(frame.vars.varType[0]) + " = " + str(val)
                        btnFrm.verb.setLabel(btnFrm, str(rowStr))

                    # either way, we're done
                    frame.status = Wye.status.SUCCESS

    class DebugRefreshVarCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = ()

        def start(stack):
            #print("DebugRefreshVarCallback started")
            return Wye.codeFrame(WyeUI.DebugRefreshVarCallback, stack)

        def run(frame):
            data = frame.eventData
            #print("DebugRefreshVarCallback data='" + str(data) + "'")

            dbgFrm = data[1][4]
            
            WyeCore.libs.WyeUI.ObjectDebugger.refresh(dbgFrm)

    class DebugStepCallback:
        mode = Wye.mode.MULTI_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = (("count", Wye.dType.INTEGER, 0),)

        def start(stack):
            #print("DebugStepCallback started")
            return Wye.codeFrame(WyeUI.DebugStepCallback, stack)

        def run(frame):
            data = frame.eventData

            objFrm = data[1][3]
            dbgFrm = data[1][4]
            # if parallel, set flag on actual object frame (parent of this frame)
            if objFrm.verb is WyeCore.ParallelStream:
                objFrm = objFrm.parentFrame

            match frame.PC:
                case 0:
                    objFrm.breakCt += 1     # step object once
                    #print("DebugStepCallback increment breakCt to", objFrm.breakCt," on objFrm", objFrm.verb.__name__)
                    frame.PC += 1

                case 1:
                    # note - do after the objFrm has cycled once
                    WyeCore.libs.WyeUI.ObjectDebugger.refresh(dbgFrm)
                    frame.status = Wye.status.SUCCESS






