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

class WyeUI(Wye.staticObj):


    # Build run_rt methods on each class
    def build():
        print("Hi from WyeLib")
        WyeCore.Utils.buildLib(WyeUI)


    # 3d positioned clickable text
    # There are 3 parts, the text node (shows text, not clickable, the card (background, clickable), and the 3d position
    # Changing the text requires regenerating the card and 3d node
    class Label3d:
        def __init__(self, text="", color=(1,1,1,1), pos=(0,0,0), scale=(1,1,1), bg=(0,0,0,1)):
            self.marginL = .1
            self.marginR = .2
            self.marginB = .1
            self.marginT = .1
            #
            self.__genTextObj(text, color)
            self.__genCardObj()
            self.__gen3dTextObj((-.5, 17, 2), (.2, .2, .2), (0, 0, 0, 1))
            # txtNode.setAlign(TextNode.ACenter)
            # txtNode.setFrameColor(0, 0, 1, 1)
            # txtNode.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)

        def setAlign(self, ctr):
            self.text.setAlign(ctr)

        # update the frame color
        def setFrameColor(self, color):
            self.Label3d.setColor(color)

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
            self.Label3d.setPos(val)

        def setColor(self, val):
            self.Label3d.setColor(val)

        def setScale(self, val):
            self.Label3d.setScale(val)

        def setWordWrap(self):
            return self.text.getWordwrap()

        def getText(self):
            return self.text.getText()

        def getPos(self):
            return self.Label3d.getPos()

        def getColor(self):
            return self.Label3d.getColor()

        def getScale(self):
            return self.Label3d.getScale()

        def getWordWrap(self):
            return self.text.setWordwrap()

        def getTag(self):
            return self.text.name

        def getAlign(self):
            return self.text.getAlign()

        def getFrameColor(self):
            return self.Label3d.getColor()

        # update the margin spacing
        def getFrameAsMargin(self):
            return (self.marginL, self.marginR, self.marginB, self.marginT)

        # rebuild card and path for updated text object
        def __regen3d(self):
            bg = self.Label3d.getColor()
            pos = self.Label3d.getPos()
            scale = self.Label3d.getScale()
            self.__genCardObj()                     # generate new card obj for updated text object
            self.Label3d.detachNode()                # detach 3d node path to old card
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
            self.Label3d = NodePath(self.card.generate())     # ,generate() makes clickable geometry but won't resize when frame dimensions change
            self.Label3d.attachNewNode(self.text)
            self.Label3d.setEffect(DecalEffect.make())        # glue text onto card
            self.Label3d.reparentTo(render)
            WyeCore.picker.makePickable(self.Label3d)         # make selectable
            self.Label3d.setTag("wyeTag", self.text.name)       # section tag: use unique name from text object
            self.Label3d.setPos(pos)
            self.Label3d.setScale(scale)

            self.Label3d.setBillboardPointWorld(0.)           # always face the camera
            self.Label3d.setLightOff()                        # unaffected by world lighting
            self.Label3d.setColor(bg)

