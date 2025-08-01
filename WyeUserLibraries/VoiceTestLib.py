from Wye import Wye
from WyeCore import WyeCore
from panda3d.core import NodePath

import sys

# VOSK example
# from Real-TIme Speech Recognition With Your Microphone by Dataquest
#https://www.youtube.com/watch?v=2kSPbH4jWME

#VOSK Model list
#This is the list of models compatible with Vosk-API.
#
#To add a new model here create an issue on Github.
#
#Model	Size	Word error rate/Speed	Notes	License
#English
# Lightweight wideband model for Android and RPi	Apache 2.0
#    vosk-model-small-en-us-0.15	   40M	  9.85  (librispeech test-clean) 10.38 (tedlium)
# Accurate generic US English model	Apache 2.0
#    vosk-model-en-us-0.22	           1.8G	  5.69  (librispeech test-clean) 6.05 (tedlium) 29.78(callcenter)
# Big US English model with dynamic graph	Apache 2.0
#    vosk-model-en-us-0.22-lgraph	   128M	  7.82  (librispeech) 8.20 (tedlium)
# Accurate generic US English model trained by Kaldi on Gigaspeech. Mostly for podcasts, not for telephony	Apache 2.0
#    vosk-model-en-us-0.42-gigaspeech  2.3G	  5.64  (librispeech test-clean) 6.24 (tedlium) 30.17 (callcenter)

from threading import Thread
from queue import Queue

# list input devices
import pyaudio
from direct.showbase.DirectObject import DirectObject

######################
CHANNELS = 1
FRAME_RATE=16000
RECORD_SECONDS = 1
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
INPUT_DEV = 3

import json
from vosk import Model, KaldiRecognizer
from functools import partial
from queue import Queue

# global comm queues
messages = Queue()
recordings = Queue()


class VoiceCmds:
    initialized = False

    def moveFwd(vMgrFrm):
        print("VoiceTestLib moveFwd")
        return False

    def move(vMgrFrm):
        if vMgrFrm.vars.currCmd[0] == None:
            print("VoiceTestLib start move")
            vMgrFrm.vars.currCmd[0] = VoiceCmds.move

        else:
            while len(vMgrFrm.vars.cmdText[0]) > 0:
                word = vMgrFrm.vars.cmdText[0].pop()
                if word == "why":
                    return False

                print(" VoiceTestLib do move ", word)
                moveFrm = vMgrFrm.vars.moveFrm[0]
                match word:
                    case "forward":
                        moveFrm.vars.forward[0] += moveFrm.vars.inc[0]

                    case "back":
                        moveFrm.vars.forward[0] -= moveFrm.vars.inc[0]

                    case "left":
                        moveFrm.vars.right[0] -= moveFrm.vars.inc[0]

                    case "right":
                        moveFrm.vars.right[0] += moveFrm.vars.inc[0]

                    case "up":
                        moveFrm.vars.up[0] += moveFrm.vars.inc[0]

                    case "down":
                        moveFrm.vars.up[0] -= moveFrm.vars.inc[0]

                    case "turn":
                        vMgrFrm.vars.currCmd[0] = VoiceCmds.turn

                    case "stop":
                        moveFrm.vars.forward[0] = 0
                        moveFrm.vars.right[0] = 0
                        moveFrm.vars.up[0] = 0
                        moveFrm.vars.rotRight[0] = 0
                        moveFrm.vars.rotUp[0] = 0

                    case _:
                        pass

        # keep going
        return True

    def turn(vMgrFrm):
        if vMgrFrm.vars.currCmd[0] == None:
            print("VoiceTestLib start move")
            vMgrFrm.vars.currCmd[0] = VoiceCmds.move

        else:
            while len(vMgrFrm.vars.cmdText[0]) > 0:
                word = vMgrFrm.vars.cmdText[0].pop()
                if word == "why":
                    return False

                print(" VoiceTestLib do move ", word)
                moveFrm = vMgrFrm.vars.moveFrm[0]
                match word:
                    case "left":
                        moveFrm.vars.rotRight[0] += moveFrm.vars.inc[0]

                    case "right":
                        moveFrm.vars.rotRight[0] -= moveFrm.vars.inc[0]

                    case "up":
                        moveFrm.vars.rotUp[0] += moveFrm.vars.inc[0]

                    case "down":
                        moveFrm.vars.rotUp[0] -= moveFrm.vars.inc[0]

                    case "move":
                        vMgrFrm.vars.currCmd[0] = VoiceCmds.move

                    case "stop":
                        moveFrm.vars.forward[0] = 0
                        moveFrm.vars.right[0] = 0
                        moveFrm.vars.up[0] = 0
                        moveFrm.vars.rotRight[0] = 0
                        moveFrm.vars.rotUp[0] = 0

                    case _:
                        pass

        # keep going
        return True


    def stop(vMgrFrm):
        print("VoiceTestLib Stop")
        moveFrm = vMgrFrm.vars.moveFrm[0]
        moveFrm.vars.forward[0] = 0
        moveFrm.vars.right[0] = 0
        moveFrm.vars.up[0] = 0
        moveFrm.vars.rotRight[0] = 0
        moveFrm.vars.rotUp[0] = 0
        return False

class VoiceTestLib:
  def _build():
    WyeCore.Utils.buildLib(VoiceTestLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class VoiceTestLib_rt:
   pass #1

  # Move with momentum
  class MoveViewpoint(DirectObject):
      mode = Wye.mode.MULTI_CYCLE
      dataType = Wye.dType.NONE
      autoStart = False
      paramDescr = (("vMgrFrm", Wye.dType.OBJECT, None),
                    )
      varDescr = (("momentum", Wye.dType.FLOAT, 0.),
                  ("inc", Wye.dType.FLOAT, 0.01),
                  ("right", Wye.dType.FLOAT, 0.0),
                  ("up", Wye.dType.FLOAT, 0.0),
                  ("rotRight", Wye.dType.FLOAT, 0.0),
                  ("rotUp", Wye.dType.FLOAT, 0.0),
                  ("forward", Wye.dType.FLOAT, 0.0),
                  ("drag", Wye.dType.FLOAT, 0.01),
                  )

      def start(stack):
          # print("MoveViewpoint: Start")
          f = Wye.codeFrame(VoiceTestLib.MoveViewpoint,
                            stack)  # not stopped by breakAll or debugger debugger
          f.systemObject = True
          return f

      def run(frame):
          global base

          # print("MoveViewpoint: run")
          base.camera.setPos(base.camera, frame.vars.right[0], frame.vars.forward[0], frame.vars.up[0])
          camRot = base.camera.getHpr()
          base.camera.setHpr(camRot[0] + frame.vars.rotRight[0], camRot[1], camRot[2])


  # Wye voice input
  class VoiceDialog:
    mode = Wye.mode.MULTI_CYCLE
    dataType = Wye.dType.NONE
    autoStart = True
    paramDescr = ()
    varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                ("dlgFrm", Wye.dType.OBJECT, None),
                ("listCode", Wye.dType.BOOL, False),
                ("inputFrm", Wye.dType.OBJECT, None),
                ("textFrm", Wye.dType.OBJECT, None),
                ("cmdFrm", Wye.dType.OBJECT, None),
                ("startStopFrm", Wye.dType.OBJECT, None),
                ("loadLbl", Wye.dType.OBJECT, None),
                ("moveFrm", Wye.dType.OBJECT, None),
                ("record", Wye.dType.OBJECT, None),
                ("transcribe", Wye.dType.OBJECT, None),
                ("load", Wye.dType.OBJECT, None),
                ("input", Wye.dType.INTEGER, -1),
                ("rate", Wye.dType.FLOAT, -1),
                ("rec", Wye.dType.OBJECT, None),
                ("model", Wye.dType.OBJECT, None),
                ("currCmd", Wye.dType.OBJECT, None),
                ("cmdLst", Wye.dType.STRING_LIST, []),
                ("cmdText", Wye.dType.STRING_LIST, []),
                ("shutdownCallback", Wye.dType.OBJECT, None),
                )

    def stopVoiceInput(frame):
        print("VoiceDialog stopVoiceInput: stop recording")
        frame.verb.stopRecording(frame)
        print("VoiceDialog close any open threads")
        if frame.vars.load[0]:
            print("Wait for dictionary load thread to finish", flush=True)
            frame.vars.load[0].join()
            frame.vars.load[0] = None
        if frame.vars.record[0]:
            print("Wait for mic input thread to finish", flush=True)
            frame.vars.record[0].join()
            frame.vars.record[0] = None
        if frame.vars.transcribe[0]:
            print("Wait for transcribe thread to finish", flush=True)
            frame.vars.transcribe[0].join()
            frame.vars.transcribe[0] = None


    # command -> action lookup table
    commands = [
        (VoiceCmds.move, ["why", "move"]),
        (VoiceCmds.turn, ["why", "turn"]),
        (VoiceCmds.moveFwd, ["why", "forward"]),
        (VoiceCmds.stop, ["why", "stop"]),
    ]               # Global commands
    currContext = None          # class handling current context

    def start(stack):
        f = Wye.codeFrame(VoiceTestLib.VoiceDialog, stack)
        f.systemObject = True
        return f

    def run(frame):
        global render
        global base
        global INPUT_DEV
        global FRAME_RATE

        match (frame.PC):
            case 0:
                # start the move class
                frame.vars.moveFrm[0] = WyeCore.World.startActiveObject(WyeCore.libs.VoiceTestLib.MoveViewpoint)

                # create top level edit dialog
                #dlgFrm = WyeCore.libs.WyeUILib.Dialog.start(frame.SP)
                dlgFrm = WyeCore.libs.WyeUIUtilsLib.doHUDDialog("Voice Input Manager", formatLst=["NO_CANCEL"],
                                                                okOnCr=False,
                                                                position=(-11.3, Wye.UI.NOTIFICATION_OFFSET, -4))
                frame.vars.dlgFrm[0] = dlgFrm

                p = pyaudio.PyAudio()
                inpList = []
                inIx = 0
                selIx = 0
                for ii in range(p.get_device_count()):
                    info = p.get_device_info_by_index(ii)
                    #print("info", p.get_device_info_by_index(ii))
                    if frame.vars.input[0] < 0 and "Microphone" in str(info["name"]):
                        frame.vars.input[0] = ii    # ix in list of I/O devices
                        INPUT_DEV = ii
                        FRAME_RATE = int(float(info["defaultSampleRate"]))
                        selIx = inIx                # ix in list of input devices
                        sep = ", *"
                    else:
                        sep = ",   "
                    if info["maxInputChannels"] > 0:
                        inpList.append(str(info["index"]) + ", " + str(info["defaultSampleRate"]) + sep + info["name"])
                        inIx += 1

                p.terminate()
                frame.vars.inputFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputDropdown(dlgFrm, "Select Audio Input", [inpList],
                                    [selIx], callback=VoiceTestLib.VoiceDialog.SetInputCallback, optData=(frame))

                frame.vars.loadLbl[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Loading language model.  Please Wait.")

                #WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  Set Window Size (F11)", color=Wye.color.NORMAL_COLOR)
                frame.vars.startStopFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Disable Voice Input",
                                               [True], VoiceTestLib.VoiceDialog.StartStopCallback,
                                               (frame), hidden=True)

                frame.vars.textFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Input Text:", hidden=True)
                frame.vars.cmdFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Wye Cmd:", hidden=True)

                print("VoiceTestLib start speech model load thread")
                frame.vars.load[0] = Thread(target=VoiceTestLib.VoiceDialog.speechRecognition_load, args=(frame,))
                frame.vars.load[0].start()

                frame.SP.append(dlgFrm)  # push dialog so it runs next cycle
                frame.PC += 1  # on return from dialog, run next case


            case 1:
                dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                frame.verb.stopVoiceInput(frame)

                WyeCore.World.stopActiveObject(frame.vars.moveFrm)

                # delay a frame
                frame.PC += 1

            case 2:
                frame.status = Wye.status.SUCCESS  # done

                # stop ourselves
                WyeCore.World.stopActiveObject(frame)

    def startRecording(frame):
        messages.put(True)

        frame.vars.record[0] = Thread(target=VoiceTestLib.VoiceDialog.recordFroMicrophone, args=(frame, 1024))
        frame.vars.record[0].start()

        frame.vars.transcribe[0] = Thread(target=VoiceTestLib.VoiceDialog.speechRecognition, args=(frame,))
        frame.vars.transcribe[0].start()

    def stopRecording(frame):
        # pump queue dry
        try:
            while messages.get(block=False):
                pass
        except:
            pass
        print("stopRecording: messages emptied")

    # microphone input thread
    # Runs when speech-to-text is active
    # Reads data from mic stream and puts on frames queue
    # Note messages queue is used to start/stop thread
    def recordFroMicrophone(vMgrFrm, chunk=1024):
        global CHANNELS
        global FRAME_RATE
        global INPUT_DEV

        print("recordFroMicrophone: thread started, chan", CHANNELS, " rate", FRAME_RATE, " input", INPUT_DEV)
        vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Disable Voice Input")

        p = pyaudio.PyAudio()
        stream = p.open(format=AUDIO_FORMAT,
                        channels=CHANNELS,
                        rate=FRAME_RATE,
                        input=True,
                        input_device_index=INPUT_DEV,  # 3 laptop mic 4 headset mic
                        frames_per_buffer=chunk
                        )
        frames = []

        # wait for input to start
        while not vMgrFrm.vars.rec[0]:
            pass

        print("recordFroMicrophone: speech rec started, start recording")

        # while main wants us to run
        while not messages.empty():
            data = stream.read(chunk)
            #print("rec: data len", len(data), " data", *data[0:20])
            frames.append(data)

            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                #print("rec: write", len(frames))
                recordings.put(frames.copy())
                frames = []

        print("recordFroMicrophone: Done recording")
        recordings.put([])

        stream.stop_stream()
        stream.close()
        p.terminate()
        vMgrFrm.vars.record[0] = None
        print("Recording thread done")

    # Load speech recognition model thread
    # Runs at start to load speech->text model
    def speechRecognition_load(vMgrFrm):
        print("speechRecognition_load thread started")
        if not vMgrFrm.vars.model[0]:
            vMgrFrm.vars.model[0] = Model(model_path=WyeCore.Utils.userLibPath() + "vosk-model-en-us-0.22")
            vMgrFrm.vars.rec[0] = KaldiRecognizer(vMgrFrm.vars.model[0], FRAME_RATE)
            vMgrFrm.vars.rec[0].SetWords(True)

        print("speechRecognition_load model loaded, show start/stop")
        vMgrFrm.vars.loadLbl[0].verb.setLabel(vMgrFrm.vars.loadLbl[0], "VOSK US English Loaded.  Voice Input ready")
        vMgrFrm.vars.startStopFrm[0].verb.show(vMgrFrm.vars.startStopFrm[0])
        vMgrFrm.vars.textFrm[0].verb.show(vMgrFrm.vars.textFrm[0])
        vMgrFrm.vars.cmdFrm[0].verb.show(vMgrFrm.vars.cmdFrm[0])
        vMgrFrm.vars.load[0] = None

        # start recording
        # todo - call fn instead of setting everything
        vMgrFrm.verb.startRecording(vMgrFrm)
        vMgrFrm.vars.shutdownCallback[0] = partial(vMgrFrm.verb.stopVoiceInput, vMgrFrm)
        WyeCore.World.shutdownCallbacks.append(vMgrFrm.vars.shutdownCallback[0])

        print("Loading speech model thread done")

    # Display current command text in dialog
    def displayCommandText(vMgrFrm):
        txt = "Input Text: "
        for s in vMgrFrm.vars.cmdText[0]:
            if s == "why":
                s = "Wye"
            txt += s + " "

        vMgrFrm.vars.textFrm[0].verb.setLabel(vMgrFrm.vars.textFrm[0], txt)

    def displayCommand(vMgrFrm, cmdLst):
        txt = "Wye Cmd: "
        if vMgrFrm.vars.currCmd[0]:
            txt += " " + vMgrFrm.vars.currCmd[0].__name__ + ": "
        for s in cmdLst:
            if s == "why":
                s = "Wye"
            txt += s + " "

        vMgrFrm.vars.cmdFrm[0].verb.setLabel(vMgrFrm.vars.cmdFrm[0], txt)

    # clear buffer up to "Wye"
    # If found, return True, else return False (and an empty buffer)
    def flushToWye(vMgrFrm):
        while len(vMgrFrm.vars.cmdText[0]) > 0 and vMgrFrm.vars.cmdText[0][0] != "why":
            vMgrFrm.vars.cmdText[0] = vMgrFrm.vars.cmdText[0][1:]
        return len(vMgrFrm.vars.cmdText[0]) > 0 and vMgrFrm.vars.cmdText[0][0] == "why"

    # convert data to text thread
    # Runs while speech-to-text is active
    # Reads from audio frames queue.  Converts to text.  Parses text for Wye commands.
    #  There are two parallel loops, one translating sound buffs to text and one parsing the text into Wye commands.
    #  Some commands are one-shot operations.  Others start running and continue to take words from the input stream
    #  until the user starts a new Wye command.
    # Aggregated input stream is stored in cmdText variable (vMgrFrm.vars.currCmd[0])
    # Note messages queue is used to start/stop thread
    def speechRecognition(vMgrFrm):
        print("speechRecognition thread started")

        # text input loop states
        BUF_EMPTY = 0           # nothing here
        BUF_BUILD_CMD = 1       # building a command (doesn't match known cmd)
        BUF_PROCESS_CMD = 2     # running a command
        bufferState = BUF_EMPTY

        # command processing loop states
        PROC_WAITING = 0
        PROC_BUILDING_CMD = 1
        PROC_RUNNING_CMD = 2

        procState = PROC_WAITING

        # while main wants us to run
        while not messages.empty():
            #print("Get recording")
            frames = recordings.get()
            print(">>> speechRecognition: Top of loop. Got", len(frames)," audio frames")
            if len(frames):
                # process sound into words
                vMgrFrm.vars.rec[0].AcceptWaveform(b''.join(frames))
                result = vMgrFrm.vars.rec[0].Result()
                #print("speechRecognition result", result)
                newText = json.loads(result)["text"]
                print("speechRecognition: frames => text", newText)

                # if we got words, process them
                if len(newText) > 0:
                    # no input generates a "the"
                    if newText == "the":   # ignore solitary "the" which seems to be what silence generates
                        # nothing to do here
                        # if building command (i.e. current cmd not match any known cmds) then fail building that cmd and clear buffer
                        if procState == PROC_BUILDING_CMD:
                            vMgrFrm.vars.cmdText[0] = []
                            print(" speechRecognition: got 'the', clear building command buffer to:", vMgrFrm.vars.cmdText[0])
                            procState = PROC_WAITING

                        vMgrFrm.verb.displayCommandText(vMgrFrm)
                        vMgrFrm.verb.displayCommand(vMgrFrm, [" "])

                        # else waiting or running -> just go back for more input

                    # something to parse in buffer
                    else:
                        # Split into words
                        textList = newText.split(" ")
                        print(" speechRecognition: New textList:", textList)
                        print(" existing text:", vMgrFrm.vars.cmdText[0])

                        # add to existing text
                        vMgrFrm.vars.cmdText[0].extend(textList)
                        print(" combined text:", vMgrFrm.vars.cmdText[0])

                        # loop while there's text to process
                        moreToDo = True
                        while len(vMgrFrm.vars.cmdText[0]) > 0 and moreToDo:
                            # if starting new command
                            if vMgrFrm.vars.cmdText[0][0] == "why":
                                procState = PROC_BUILDING_CMD

                            vMgrFrm.verb.displayCommandText(vMgrFrm)
                            vMgrFrm.verb.displayCommand(vMgrFrm, [" "])

                            if procState == PROC_WAITING:
                                if vMgrFrm.verb.flushToWye(vMgrFrm):
                                    # there's a command in the buffer, drop through to  process it
                                    print("  speechRecognition: Run cmd shift to PROC_BUILDING_CMD")
                                    procState = PROC_BUILDING_CMD
                                # else no cmd found in buff and now buff's empty -> exit loop
                                else:
                                    print("  speechRecognition: Run cmd shift to PROC_WAITING. Wait for more input. buff", vMgrFrm.vars.cmdText[0])
                                    moreToDo = False

                            # if there's a command wanting input, call it
                            if procState == PROC_RUNNING_CMD:
                                print("  speechRecognition text loop: PROC_RUNNING_CMD")
                                # call cmd.  If returns False, done command
                                # note: cmd removes any text it uses from the buffer
                                print("  speechRecognition: Running ", vMgrFrm.vars.currCmd[0].__name__)
                                if not vMgrFrm.vars.currCmd[0](vMgrFrm):
                                    # cmd ret False -> finished command, clear text up to next command, if any

                                    if vMgrFrm.verb.flushToWye(vMgrFrm):
                                        # there's another command in the buffer, loop to process it
                                        print("  speechRecognition: Run cmd shift to PROC_BUILDING_CMD. buff", vMgrFrm.vars.cmdText[0])
                                        procState = PROC_BUILDING_CMD
                                    # else done, buff's empty, exit loop
                                    else:

                                        print("  speechRecognition: Run cmd shift to PROC_WAITING. Wait for more input. buff", vMgrFrm.vars.cmdText[0])
                                        procState = PROC_WAITING
                                        moreToDo = False

                                # else cmd ret True -> continue PROC_RUNNING_CMD (curr cmd waiting for input)
                                else:
                                    print("  speechRecognition: Run", vMgrFrm.vars.currCmd[0], " continues. buff", vMgrFrm.vars.cmdText[0])

                            # if we're building a command, see if it's complete
                            # (note, this is after PROC_RUNNING_CMD 'cause there might be another cmd in buffer)
                            if procState == PROC_BUILDING_CMD:
                                print("  speechRecognition text loop: PROC_BUILDING_CMD")
                                # look up command.  Returns True if it found cmd (also removes cmd text from buff)
                                if vMgrFrm.verb.parse(vMgrFrm):
                                    # if found command and it wants to keep processing input
                                    if vMgrFrm.vars.currCmd[0]:
                                        # it wants more input so it put ptr to itself in vMgrFrm.vars.currCmd[0]
                                        print("  speechRecognition: Build found, ran cmd.  Shift to PROC_RUNNING_CMD. buff", vMgrFrm.vars.cmdText[0])
                                        procState = PROC_RUNNING_CMD
                                    # else finished command, go back to wait state.  If more in buffer, keep looping
                                    else:
                                        procState = PROC_WAITING
                                        moreToDo = len(vMgrFrm.vars.cmdText[0]) > 0
                                        if moreToDo:
                                            print("  speechRecognition: Build found, ran cmd. cmd is done. Shift to PROC_WAITING and process more buffer. buff",
                                                  vMgrFrm.vars.cmdText[0])
                                        else:
                                            print("  speechRecognition: Build found, ran cmd. cmd is done. Shift to PROC_WAITING.  Buff is empty.",
                                                  vMgrFrm.vars.cmdText[0])

                                # did not find matching command, exit loop to wait for more text in case that helps
                                else:
                                    print("  speechRecognition: Build din't find matching cmd. Wait for more input. buff", vMgrFrm.vars.cmdText[0])
                                    moreToDo = False

                        print("speechRecognition: Done processing text input. ", end="")
                        match procState:
                            case 0: #PROC_WAITING:
                                print("procState == PROC_WAITING")
                            case 1: #PROC_BUILDING_CMD:
                                print("procState == PROC_BUILDING_CMD")
                            case 2: #PROC_RUNNING_CMD:
                                print("procState == PROC_RUNNING_CMD")

                else:
                    print("speechRecognition: Nothing parsed from mic input")
            else:
                print("speechRecognition: No mic input")

        print("speechRecognition: messages empty, stopped recognition")


        vMgrFrm.vars.transcribe[0] = None
        print("speechRecognition thread Done")

    # parse for cmd in ouputText starting at txtIx
    # return true if found command
    def parse(frame):
        print("voiceDialog parse:", frame.vars.cmdText[0])
        txtLen = len(frame.vars.cmdText[0])
        # look for match in prebuilt commands
        for cmd in frame.verb.commands:
            cmdLen = len(cmd[1])

            # if there's enough input text to do compare
            if cmdLen <= txtLen:
                # check text after the initial "why"
                print("  Compare input to", cmd[1])
                cmdMatched = True   # assume success
                for wdIx in range(1,cmdLen):
                    # if fail to match, kick out to try the next word
                    if frame.vars.cmdText[0][wdIx] != cmd[1][wdIx]:
                        print("   this cmd not a match")
                        cmdMatched = False
                        break;

                # if matched
                if cmdMatched:
                    print("parse: Call command", cmd[1])
                    frame.verb.displayCommand(frame, cmd[1])
                    # call command.  Will return True if it wants to keep processing input
                    cmdContinues = cmd[0](frame)
                    # trim text used by command off input buffer
                    frame.vars.cmdText[0] = frame.vars.cmdText[cmdLen:]
                    print("parse: trim cmd", cmd[1], " off cmdText", frame.vars.cmdText[0])
                    # if command wants to keep processing input, stash ptr to it
                    if cmdContinues:
                        print(" parse: command wants to keep processing input")
                        frame.vars.currCmd[0] = cmd[0]     # cmd wants to process more text,

                    # else make sure no continuing command
                    else:
                        print(" parse: command done")
                        frame.vars.currCmd[0] = None

                    # found command
                    return True

        # get this far then did not match command
        frame.verb.displayCommand(frame, [" "])
        return False

    # set input source
    class SetInputCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = ()

        def start(stack):
            # print("SetInputCallback started")
            return Wye.codeFrame(VoiceTestLib.VoiceDialog.SetInputCallback, stack)

        def run(frame):
            global INPUT_DEV
            global FRAME_RATE

            data = frame.eventData
            #print("SetInputCallback data", data)
            vMgrFrm = data[1]
            ix = vMgrFrm.vars.inputFrm[0].params.selectedIx[0]
            entry = vMgrFrm.vars.inputFrm[0].vars.list[0][ix]
            segStr = entry.split(",")
            input = int(segStr[0])
            rate = int(float(segStr[1]))
            #print("Selected entry", ix, " =", entry)
            #print("  input", input, " rate", rate)
            INPUT_DEV = input
            FRAME_RATE = rate
            vMgrFrm.vars.input[0] = input
            vMgrFrm.vars.rate[0] = rate


    # turn sound on/off
    class StartStopCallback:
        mode = Wye.mode.SINGLE_CYCLE
        dataType = Wye.dType.STRING
        paramDescr = ()
        varDescr = ()

        def start(stack):
            # print("SetScrnCallback started")
            return Wye.codeFrame(VoiceTestLib.VoiceDialog.StartStopCallback, stack)

        def run(frame):
            data = frame.eventData
            #print("StartStopCallback data", data)
            vMgrFrm = data[1]
            #print("vMgrFrm", vMgrFrm.verb.__name__)

            if vMgrFrm.vars.startStopFrm[0].vars.currVal[0]:
                #vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Loading English Model")
                vMgrFrm.verb.startRecording(vMgrFrm)
                vMgrFrm.vars.shutdownCallback[0] = partial(vMgrFrm.verb.stopVoiceInput, vMgrFrm)
                WyeCore.World.shutdownCallbacks.append(vMgrFrm.vars.shutdownCallback[0])


            else:
                vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Enable Voice Input")
                vMgrFrm.verb.stopRecording(vMgrFrm)
                #print("StartStopCallback Stopped recording (maybe)")
                if vMgrFrm.vars.shutdownCallback[0] and vMgrFrm.vars.shutdownCallback[0] in WyeCore.World.shutdownCallbacks:
                    WyeCore.World.shutdownCallbacks.remove(vMgrFrm.vars.shutdownCallback[0])
                    vMgrFrm.vars.shutdownCallback[0] = None

