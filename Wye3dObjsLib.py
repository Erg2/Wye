# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *
from panda3d.core import LVector3f
#from functools import partial
import traceback
import sys
#from sys import exit
import math
import sys, os
#for 3d geometry (input cursor)
#from direct.showbase.ShowBase import ShowBase
from importlib.machinery import SourceFileLoader    # to load library from file

from functools import partial

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MouseButton

# from https://github.com/Epihaius/procedural_panda3d_model_primitives
from sphere import SphereMaker

import inspect

#import pygame.midi
#import time


# 3d UI element library
class Wye3dObjsLib(Wye.staticObj):
    systemLib = True        # prevent overwriting
    modified = False  # no changes
    canSave = False

    # Build run_rt methods on each class in library
    def _build():
        WyeCore.Utils.buildLib(Wye3dObjsLib)


    #
    # 3D object classes
    #

    class _ball:
        def __init__(self, radius, pos=[0,0,0]):
            # see https: // github.com / Epihaius / procedural_panda3d_model_primitives
            self.radius = radius
            ballBuilder = SphereMaker(radius=radius)
            self.node = ballBuilder.generate()
            self._path = None
            if self.node:
                self._path = render.attachNewNode(self.node)
                self._path.setPos(pos[0], pos[1], pos[2])
            else:
                print("WyeUILib _ball: SphereMaker didn't")

        def removeNode(self):
            self._path.removeNode()

        def setColor(self, val):
            self._path.setColor(val)

        def setScale(self, val):
            self._path.setScale(val)

        def setPos(self, *args):
            self._path.setPos(args)

        def getHpr(self):
            return self._path.getHpr()

        def setHpr(self, *args):
            self._path.setHpr(args)

        def setTag(self, tag):
            self.node.setTag("wyeTag", tag)

        def getColor(self):
            return self._path.getColor()

        def getNodePath(self):
            return self._path

        def getPos(self):
            return self._path.getPos()

        def getScale(self):
            return self._path.getScale()

        def getTag(self):
            return self.node.getTag('wyeTag')

        def getHeight(self):
            return self.radius

        def getWidth(self):
            return self.radius

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

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

            self._path = render.attachNewNode(self.node)
            if parent:
                self._path.reparentTo(parent)
            self.setPos(pos[0], pos[1], pos[2])


        def removeNode(self):
            self._path.removeNode()

        def setColor(self, val):
            self._path.setColor(val)

        def setScale(self, val):
            self._path.setScale(val)

        def setPos(self, *args):
            self._path.setPos(args)

        def getHpr(self):
            return self._path.getHpr()

        def setHpr(self, *args):
            self._path.setHpr(args)

        def setTag(self, tag):
            return self.node.setTag("wyeTag", tag)

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

        def getColor(self):
            return self._path.getColor()

        def getNodePath(self):
            return self._path

        def getPos(self):
            return self._path.getPos()

        def getScale(self):
            return self._path.getScale()

        def getHeight(self):
            return self.size[2]

        def getTag(self):
            return self.node.getTag('wyeTag')

        def getWidth(self):
            return self.size[0]

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)


    # create a scaled triangle for playback cursor
    class _pointer:

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
            #vertex.addData3f(-1*size[0], -1*size[1], -1*size[2])
            vertex.addData3f(0*size[0], -1*size[1], 0*size[2])          # llb - 0
            color.addData4f(0, 0, 0, 1)

            #vertex.addData3f(-1*size[0], -1*size[1], 1*size[2])
            vertex.addData3f(-1*size[0], -1*size[1], -.1*size[2])       # llt - 1
            color.addData4f(0, 0, 1, 1)

            #vertex.addData3f(-1*size[0], 1*size[1], -1*size[2])
            vertex.addData3f(0*size[0], 1*size[1], 0*size[2])          # ulb - 2
            color.addData4f(0, 1, 0, 1)

            #vertex.addData3f(-1*size[0], 1*size[1], 1*size[2])
            vertex.addData3f(-1*size[0], 1*size[1], -.1*size[2])       # ult - 3
            color.addData4f(0, 1, 1, 1)

            #vertex.addData3f(1*size[0], -1*size[1], -1*size[2])
            vertex.addData3f(-.1*size[0], -1*size[1], -1*size[2])       # lrb - 4
            color.addData4f(1, 0, 0, 1)

            #vertex.addData3f(1*size[0], -1*size[1], 1*size[2])
            vertex.addData3f(1*size[0], -1*size[1], 1*size[2])          # lrt - 5
            color.addData4f(1, 0, 1, 1)

            #vertex.addData3f(1*size[0], 1*size[1], -1*size[2])
            vertex.addData3f(-.1*size[0], 1*size[1], -1*size[2])       # urb - 6
            color.addData4f(1, 0, 1, 1)

            #vertex.addData3f(1*size[0], 1*size[1], 1*size[2])
            vertex.addData3f(1*size[0], 1*size[1], 1*size[2])          # urt - 7
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

            self._path = render.attachNewNode(self.node)
            if parent:
                self._path.reparentTo(parent)
            self.setPos(pos[0], pos[1], pos[2])


        def removeNode(self):
            self._path.removeNode()

        def setColor(self, val):
            self._path.setColor(val)

        def setScale(self, val):
            self._path.setScale(val)

        def setPos(self, *args):        # use args so can set abs or obj-relative path
            #print("_pointer setPos", args)
            self._path.setPos(args)

        def getHpr(self):
            return self._path.getHpr()

        def setHpr(self, *args):
            #print("_pointer setHpr", args)
            self._path.setHpr(args)

        def setTag(self, tag):
            return self.node.setTag("wyeTag", tag)

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

        def getColor(self):
            return self._path.getColor()

        def getNodePath(self):
            return self._path

        def getPos(self):
            return self._path.getPos()

        def getScale(self):
            return self._path.getScale()

        def getHeight(self):
            return self.size[2]

        def getTag(self):
            return self.node.getTag('wyeTag')

        def getWidth(self):
            return self.size[0]

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)


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

            self._path = render.attachNewNode(self.node)
            self._path.setPos(pos[0], pos[1], pos[2])


        def removeNode(self):
            self._path.removeNode()

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

        def setScale(self, val):
            self._path.setScale(val)

        def getScale(self):
            return self._path.getScale()

        def setPos(self, *args):
            self._path.setPos(args)

        def getPos(self):
            return self._path.getPos()

        def getHpr(self):
            return self._path.getHpr()

        def setHpr(self, *args):
            self._path.setHpr(args)

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

        def setTag(self, tag):
            WyeCore.picker.makePickable(self._path)  # make selectable
            return self.node.setTag("wyeTag", tag)

        def getTag(self):
            return self.node.getTag('wyeTag')

        def setColor(self, val):
            self._path.setColor(val)

        def getColor(self):
            return self._path.getColor()

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class _3dText:
        global render

        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,0), parent=None, tag="", doTag=True):
            #print("_3dText '"+text+"' at", pos)
            #curframe = inspect.currentframe()
            #callframe = inspect.getouterframes(curframe, 2)
            #print('  caller name:', callframe[1][3])
            if len(text) == 0:
                text = ' '
            self.text = text
            if parent is None:
                self.parent = render
            else:
                self.parent = parent
            self.tag = tag          # if caller supplied, else will auto-gen unique tag
            self.doTag = doTag      # false if caller doesn't want a tag
            self.color = color
            self.pos = pos
            self.scale = scale
            self.bg = bg
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.textNode = None
            self.card = None
            self._path = None
            self._txtPath = None
            self.gFrame = None
            #
            self._genTextObj(text, color)
            if self.bg[3] > 0:
                self._genCardObj(bg)
            self._gen3dTextObj(pos, scale, color)

            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameMargin(0.2, 0.2, 0.1, 0.1)

        ## setters

        def setAlign(self, ctr):
            self.textNode.setAlign(ctr)

        def setColor(self, color):
            self.color = color
            self.textNode.setTextColor(color)
            self._regen3d()

        def setBackgroundColor(self, bg):
            self.bg = bg
            if self.bg[3] > 0:
                self._genCardObj(self.bg)
            self._regen3d()

        # update the margin spacing
        def setFrameMargin(self, marginL, marginR, marginB, marginT):
            self.marginL = marginL
            self.marginR = marginR
            self.marginB = marginB
            self.marginT = marginT
            self._regen3d()

        def setPos(self, *args):
            self._path.setPos(*args)
            self.pos = self._path.getPos()

        def getHpr(self):
            return self._path.getHpr()

        def setHpr(self, *args):
            self._path.setHpr(*args)

        def setScale(self, val):
            self._path.setScale(val)
            self.scale = val

        # changing the text requires regenerating the background card and the 3d node
        def setText(self, text):
            if len(text) == 0:
                text = ' '
            self.textNode.setText(text)
            self.text = text
            self._regen3d()

        def setWordWrap(self):
            return self.textNode.getWordwrap()

        ## getters

        def getAlign(self):
            return self.textNode.getAlign()

        def getColor(self):
            return self.color

        def getFrame(self):
            return self.gFrame

        def getHeight(self):
            return self.gFrame[3] - self.gFrame[2]

        def getFrameColor(self):
            return self.color

        # update the margin spacing
        def getFrameMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        def getNodePath(self):
            return self._path

        def getPos(self):
            return self.pos

        def getScale(self):
            return self.scale

        def getTag(self):
            return self.tag

        def getText(self):
            return self.text

        def getWidth(self):
            return self.gFrame[1] - self.gFrame[0]

        def getWordWrap(self):
            return self.textNode.setWordwrap()

        ## methods

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)

        # rebuild card and path for updated text object
        def _regen3d(self):
            self.textNode = TextNode(self.tag)
            self.textNode.setText(self.text)
            self.textNode.setTextColor(self.color)
            if self.bg[3] > 0:
                self._genCardObj(self.bg)
            self._gen3dTextObj(self.pos, self.scale, self.color)

        # internal rtn to gen text object with unique wyeTag name
        def _genTextObj(self, text, color=(1,1,1,1)):
            if self.doTag and not self.tag:
                self.tag = "txt"+str(WyeCore.Utils.getId())
                #print("_3dTxt", self.text, " tag", self.tag, " doTag", self.doTag)
            self.textNode = TextNode(self.tag)
            if len(text) == 0:
                text = ' '
            self.textNode.setText(text)
            self.textNode.setTextColor(color)

        ## internal rtn to gen 3d Card clickable background object
        # only used when background color set
        def _genCardObj(self, bg=(0,0,0,0)):
            self.textNode.set_card_as_margin(.1,.1,.1,.1)
            self.textNode.set_card_color(bg[0], bg[1], bg[2], bg[3])
            self.textNode.setCardDecal(True)        # force card behind text so can read it!!!
            #print("initial txtNode frame ", self.textNode.getFrameActual())
            #self.card = CardMaker("Txt Card")
            #self.card.set_color(bg[0], bg[1], bg[2], bg[3])    # set background color
            #self.gFrame = self.textNode.getFrameActual()
            #if self.gFrame[1] == 0:      # if empty frame
            #    self.gFrame[1] = 1
            #    self.gFrame[3] = 1
            ##print("self.gFrame", self.gFrame)
            #self.gFrame[0] -= self.marginL
            #self.gFrame[1] += self.marginR
            #self.gFrame[2] -= self.marginB
            #self.gFrame[3] += self.marginT
            ##print("initial adjusted self.gFrame", self.gFrame)
            #self.card.setFrame(self.gFrame)

        # internal rtn to generate/update 3d path object to position, etc. the text
        def _gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), color=(0,0,0,1), genNodePath = True):
            #print("_gen3dTextObj keep old node path for", self.text)
            if self._path:  # if we already have a path, keep using it
                #print("Update text node", self.text, " re-use node path")
                self._txtPath.removeNode()
                self._txtPath = NodePath(self.textNode.generate())
                self._txtPath.reparentTo(self._path)
            else:   # first time, create new path0
                #print("New text node", self.text, " gen node path")
                self._path = NodePath(self.tag)
                self._txtPath = NodePath(self.textNode.generate())
                self._txtPath.reparentTo(self._path)
                # stick text path into scene
                self._path.reparentTo(self.parent)

                if self.doTag:
                    WyeCore.picker.makePickable(self._path)  # make selectable
                    self._path.setTag("wyeTag", self.textNode.name)  # section tag: use unique name from text object
            #if self.bg[3] > 0:      # if visible background color, gen background card
            #    self._path.attachNewNode(self.card.generate())  # ,generate() makes clickable geometry but won't resize when frame dimensions change
            #    self._path.setEffect(DecalEffect.make())        # glue text onto card


            self._path.setPos(pos[0], pos[1], pos[2])
            self._path.setScale(scale)

            self._path.setLightOff()                        # unaffected by world lighting
            #print(" set new path to color", color)
            self._path.setColor(color)
            self.textNode.setText(self.text)

            self.gFrame = self.textNode.getFrameActual()
            if self.gFrame[1] == 0:  # if empty frame
                print("_3dText _gen3dTextObj: Warning", self.text,": empty gFrame")
                self.gFrame[1] = 1
                self.gFrame[3] = 1
            # print("self.gFrame", self.gFrame)
            self.gFrame[0] -= self.marginL
            self.gFrame[1] += self.marginR
            self.gFrame[2] -= self.marginB
            self.gFrame[3] += self.marginT

        def removeNode(self):
            self._path.removeNode()

        def show(self):
            self._path.show()
            WyeCore.picker.makePickable(self._path)

        def hide(self):
            self._path.hide()
            WyeCore.picker.makeNotPickable(self._path)
            #print("_3tTxt ", self.text, " made not pickable. tag 'pickable'=", self._path.getTag('pickable'))
