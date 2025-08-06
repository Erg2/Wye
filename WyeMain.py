# Building up direct compiled version of Wye
# consolidating compiled code into one block
#
# license: We don't need no stinking license
# This is prototype code.  If it blows up your nuclear reactor, that is your dumb fault.
#


from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr   # needed to run world task in sync with panda3d
from panda3d.core import *
#from direct.showbase.DirectObject import DirectObject
#import traceback
from WyeCore import WyeCore
from Wye import Wye
import sys


############# run the world
#
# Note: Wye's static class structure means we need this instantiated class
# to derive from ShowBase to access all the Panda3d runstime stuff
class WorldRunner(ShowBase):
    global base
    global render

    def __init__(self):
        #ConfigVariableBool('fullscreen').setValue(1)

        ShowBase.__init__(self)     # Init Panda3d

        ## set screen size
        #WyeCore.Utils.setScreenSize(Wye.windowSize)


        #myFog = Fog("Fog Name")
        #myFog.setColor(0, 0, 0)
        #myFog.setExpDensity(0.001)
        #base.render.setFog(myFog)

        taskMgr.add(WyeCore.World.worldRun)
        WyeCore.base = self      # world needs this to do panda3d stuff


        #props = WindowProperties()
        #props.setTitle("Wye V" + version)
        #WyeCore.base.win.requestProperties(props)



# main program, set up and run the world

#print("Start")
#loadPrcFileData("", "fullscreen 1")  # Set to 1 for fullscreen
#loadPrcFileData("", "win-origin 10 10")
#loadPrcFileData("", "win-fixed-size 0")

loadPrcFileData('', 'win-size 1200 800')           # set size of window
loadPrcFileData('', 'show-frame-rate-meter #t')    # turn on frame rate display
loadPrcFileData('', 'window-title Wye V'+Wye.version)

#ConfigVariableBool('fullscreen').setValue(1)


# if the user supplied a list of libList and or start objs
if len(sys.argv) > 1:
    for ix in range(1, len(sys.argv), 2):
        sw = sys.argv[ix]
        val = sys.argv[ix+1]
        match sw:
            case "-l":
                #print("cmd line lib ", val)
                WyeCore.libLoadList.append(val)

# No parameters, load default libs and start default objs
else:
    WyeCore.libLoadList.extend(["TestLib.py", "WyeUserLibraries/FlockingFishLib.py", "WyeUserLibraries/FishLib.py", "WyeUserLibraries/WyeTestLib.py", "WyeUserLibraries/VoiceTestLib.py"])



pandaRunner = WorldRunner()
#print("Started, now run")
pandaRunner.run()
#print("Done")

