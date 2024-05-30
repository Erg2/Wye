# Wye dialog classes
#
# Basic dialog objects - dialog framework, label, text input, button

from Wye import Wye
from WyeCore import WyeCore
import inspect      # for debugging
from panda3d.core import *

#import partial
import traceback
import sys
from sys import exit
from direct.showbase import Audio3DManager

from direct.showbase.DirectObject import DirectObject

# 3d UI element library
class WyeUI(Wye.staticObj):


    # Build run_rt methods on each class
    def build():
        WyeCore.Utils.buildLib(WyeUI)

    def displayLib(lib, coord, elements=None):
        yy =0
        for attr in dir(lib):
            if attr != "__class__":
                val = getattr(lib, attr)
                if inspect.isclass(val) and hasattr(val, "mode"):
                    print("lib", lib.__name__, " verb", val.__name__)
                    txt = lib.__name__ + "." +val.__name__
                    txtCoord = list(coord)
                    txtCoord[2] +=yy
                    #elements.append(WyeCore.libs.WyeUI.label3d("Stream 0", color=(0, 1, 0, 1), pos=(0, 10, yy), scale=(.2, .2, .2)))
                    WyeCore.libs.WyeUI.label3d(txt, color=(0, 1, 0, 1), pos=(txtCoord[0], txtCoord[1], txtCoord[2]), scale=(.2, .2, .2))
                    yy += -.25


    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class label3d:
        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.text = None
            self.card = None
            self.label3d = None
            #
            self.__genTextObj(text, color)
            self.__genCardObj()
            self.__gen3dTextObj(pos, scale, bg)
            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameColor(0, 0, 1, 1)
            # txtNode.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

        def setAlign(self, ctr):
            self.text.setAlign(ctr)

        # update the frame color
        def setFrameColor(self, color):
            self.label3d.setColor(color)

        # update the margin spacing
        def setFrameAsMargin(self, marginL, marginR, marginB, marginT):
            self.marginL = marginL
            self.marginR = marginR
            self.marginB = marginB
            self.marginT = marginT
            self.__regen3d()

        # changing the text requires regenerating the background card and the 3d node
        def setText(self, text):
            self.text.setText(text)
            self.__regen3d()

        def setPos(self, val):
            self.label3d.setPos(val)

        def setColor(self, val):
            self.label3d.setColor(val)

        def setScale(self, val):
            self.label3d.setScale(val)

        def setWordWrap(self):
            return self.text.getWordwrap()

        def getText(self):
            return self.text.getText()

        def getPos(self):
            return self.label3d.getPos()

        def getColor(self):
            return self.label3d.getColor()

        def getScale(self):
            return self.label3d.getScale()

        def getWordWrap(self):
            return self.text.setWordwrap()

        def getTag(self):
            return self.text.name

        def getAlign(self):
            return self.text.getAlign()

        def getFrameColor(self):
            return self.label3d.getColor()

        # update the margin spacing
        def getFrameAsMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        # rebuild card and path for updated text object
        def __regen3d(self):
            bg = self.label3d.getColor()
            pos = self.label3d.getPos()
            scale = self.label3d.getScale()
            self.__genCardObj()                     # generate new card obj for updated text object
            self.label3d.detachNode()                # detach 3d node path to old card
            self.__gen3dTextObj(pos, scale, bg)     # make new 3d node path to new card

        # internal rtn to gen text object with unique wyeTag name
        def __genTextObj(self, text, color=(1,1,1,1)):
            tag = "txt"+str(WyeCore.Utils.getId())
            self.text = TextNode(tag)
            self.text.setText(text)
            self.text.setTextColor(color)

        # internal rtn to gen 3d Card clickable background object
        def __genCardObj(self):
            #print("initial txtNode frame ", self.text.getFrameActual())
            self.card = CardMaker("My Card")
            frame = self.text.getFrameActual()
            #print("frame", frame)
            frame[0] -= self.marginL
            frame[1] += self.marginR
            frame[2] -= self.marginB
            frame[3] += self.marginT
            #print("initial adjusted frame", frame)
            self.card.setFrame(frame)

        # internal rtn to generate 3d (path) object to position, etc. the text
        def __gen3dTextObj(self, pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            global render

            self.label3d = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            self.label3d.attachNewNode(self.text)
            self.label3d.setEffect(DecalEffect.make())        # glue text onto card
            self.label3d.reparentTo(render)
            WyeCore.picker.makePickable(self.label3d)         # make selectable
            self.label3d.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self.label3d.setPos(pos)
            self.label3d.setScale(scale)

            self.label3d.setBillboardPointWorld(0.)           # always face the camera
            self.label3d.setLightOff()                        # unaffected by world lighting
            self.label3d.setColor(bg)


