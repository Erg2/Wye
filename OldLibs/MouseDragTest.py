#snatched time ago from chombee's code
#
#import direct.directbase.DirectStart
from panda3d.core import *
from direct.task import Task
import sys
import random

# Collision mask worn by all draggable objects.
dragMask = BitMask32.bit(1)
# Collision mask worn by all droppable objects.
dropMask = BitMask32.bit(1)

highlight = VBase4(.3,.3,.3,1)

class objectMangerClass:
  def __init__( self ):
    self.objectIdCounter = 0
    self.objectDict = dict()

  def tag( self, objectNp, objectClass ):
    self.objectIdCounter += 1
    objectTag = str(self.objectIdCounter)
    objectNp.setTag( 'objectId', objectTag )
    self.objectDict[objectTag] = objectClass

  def get( self, objectTag ):
    if objectTag in self.objectDict:
      return self.objectDict[objectTag]
    return None
objectManger = objectMangerClass()

class dragDropObjectClass:
  def __init__( self, np ):
    self.model = np
    self.previousParent = None
    self.model.setCollideMask(dragMask)
    objectManger.tag( self.model, self )

  def onPress( self, mouseNp ):
    self.previousParent = self.model.getParent()
    self.model.wrtReparentTo( mouseNp )
    self.model.setCollideMask(BitMask32.allOff())

  def onRelease( self ):
    self.model.wrtReparentTo( self.previousParent )
    self.model.setCollideMask(dragMask)

  def onCombine( self, otherObj ):
    self.model.setPos( otherObj.model.getPos() )

class mouseCollisionClass:
  def __init__(self):
    global base

    base.accept("escape",sys.exit)
    base.accept('mouse1',self.onPress)
    base.accept('mouse1-up',self.onRelease)
    self.draggedObj = None
    self.setupCollision()

    taskMgr.add( self.mouseMoverTask, 'mouseMoverTask' )

  def setupCollision( self ):
    # Initialise the collision ray that is used to detect which draggable
    # object the mouse pointer is over.
    cn = CollisionNode('')
    cn.addSolid( CollisionRay(0,-100,0, 0,1,0) )
    cn.setFromCollideMask(dragMask)
    cn.setIntoCollideMask(BitMask32.allOff())
    self.cnp = aspect2d.attachNewNode(cn)
    self.ctrav = CollisionTraverser()
    self.queue = CollisionHandlerQueue()
    self.ctrav.addCollider(self.cnp,self.queue)
    self.cnp.show()

  def mouseMoverTask( self, task ):
    if base.mouseWatcherNode.hasMouse():
      mpos = base.mouseWatcherNode.getMouse()
      self.cnp.setPos(render2d,mpos[0],0,mpos[1])
    return task.cont

  def collisionCheck( self ):
    self.ctrav.traverse(aspect2d)
    self.queue.sortEntries()
    if self.queue.getNumEntries():
      np = self.queue.getEntry( self.queue.getNumEntries()-1 ).getIntoNodePath()
      objectId = np.getTag( 'objectId' )
      if objectId is None:
        objectId = np.findNetTag( 'objectId' )
      if objectId is not None:
        object = objectManger.get( objectId )
        return object
    return None

  def onPress( self ):
    obj = self.collisionCheck()
    if obj is not None:
      self.draggedObj = obj
      obj.onPress( self.cnp )

  def onRelease( self ):
    obj = self.collisionCheck()
    self.draggedObj.onRelease() # self.cnp )
    if obj is not None:
      self.draggedObj.onCombine( obj )

if __name__ == '__main__':
  cm = CardMaker('cm')
  left,right,bottom,top = 0,2,0,-2
  width = right - left
  height = top - bottom
  cm.setFrame(left,right,bottom,top)
  node = aspect2d.attachNewNode('')
  node.setPos(-1.2,0,0.9)
  cards = []

  for i in range(3):
    for j in range(3):
      card = node.attachNewNode(cm.generate())
      card.setScale(.2)
      card.setPos(i/2.0,0,-j/2.0)
      card.setColor(random.random(),random.random(),random.random())
      draggable = dragDropObjectClass(card)
      cards.append(card)

  mouseCollision = mouseCollisionClass()
  run()