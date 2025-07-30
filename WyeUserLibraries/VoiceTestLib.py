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

######################
CHANNELS = 1
FRAME_RATE=16000
RECORD_SECONDS = 2
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
        pass


class VoiceTestLib:
  def _build():
    WyeCore.Utils.buildLib(VoiceTestLib)
  canSave = True  # all verbs can be saved with the library
  modified = False  # no changes
  class VoiceTestLib_rt:
   pass #1




  # Wye main menu - user settings n stuff
  class VoiceDialog:
    mode = Wye.mode.MULTI_CYCLE
    dataType = Wye.dType.STRING
    autoStart = True
    paramDescr = ()
    varDescr = (("dlgStat", Wye.dType.INTEGER, -1),
                ("dlgFrm", Wye.dType.OBJECT, None),
                ("listCode", Wye.dType.BOOL, False),
                ("inputFrm", Wye.dType.OBJECT, None),
                ("textFrm", Wye.dType.OBJECT, None),
                ("startStopFrm", Wye.dType.OBJECT, None),
                ("loadLbl", Wye.dType.OBJECT, None),
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
        frame.verb.stop_recording(frame)
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


    # Audio command - word list to match and function to call
    class cmd:
        def __init__(self, action=None, *args):
            self.words = [*args]
            self.action = action

        # look for matching word(s) in inList starting at ix
        def stmtMatch(self, inList):
            nWords = len(self.words)
            if len(inList) < nWords:
                return False
            for ix in range(nWords):
                wd = inList[ix]
                if not wd in self.words[ix]:
                    return False

            # if get here, have match, call action
            self.action(inList[ix:])
            return True

    # command -> action lookup table
    commands = [
        (VoiceCmds.moveFwd, ["why", "forward"]),
    ]               # Global commands
    currContext = None          # class handling current context

    def start(stack):
        f = Wye.codeFrame(VoiceTestLib.VoiceDialog, stack)
        return f

    def run(frame):
        global render
        global base
        global INPUT_DEV
        global FRAME_RATE

        match (frame.PC):
            case 0:
                # create top level edit dialog
                dlgFrm = WyeCore.libs.WyeUILib.Dialog.start(frame.SP)
                dlgFrm.params.retVal = frame.vars.dlgStat
                dlgFrm.params.title = ["Voice Input Manager"]
                point = NodePath("point")
                point.reparentTo(render)
                point.setPos(base.camera, Wye.UI.NICE_DIALOG_POS)
                pos = point.getPos()
                point.removeNode()
                dlgFrm.params.position = [(pos[0], pos[1]-.5, pos[2]), ]
                dlgFrm.params.parent = [None]
                dlgFrm.params.format = [["NO_CANCEL"]]
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
                frame.vars.startStopFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Enable Voice Input",
                                               [Wye.windowSize == 0], VoiceTestLib.VoiceDialog.StartStopCallback,
                                               (frame), hidden=True)

                frame.vars.textFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Text:", hidden=True)

                print("VoiceTestLib start speech model load thread")
                frame.vars.load[0] = Thread(target=VoiceTestLib.VoiceDialog.speech_recognition_load, args=(frame,))
                frame.vars.load[0].start()

                frame.SP.append(dlgFrm)  # push dialog so it runs next cycle
                frame.PC += 1  # on return from dialog, run next case


            case 1:
                dlgFrm = frame.SP.pop()  # remove dialog frame from stack
                frame.verb.stopVoiceInput(frame)

                # delay a frame
                frame.PC += 1

            case 2:
                frame.status = Wye.status.SUCCESS  # done

                # stop ourselves
                WyeCore.World.stopActiveObject(frame)

    def start_recording(frame):
        messages.put(True)

        frame.vars.record[0] = Thread(target=VoiceTestLib.VoiceDialog.record_microphone, args=(frame,1024))
        frame.vars.record[0].start()

        frame.vars.transcribe[0] = Thread(target=VoiceTestLib.VoiceDialog.speech_recognition, args=(frame,))
        frame.vars.transcribe[0].start()

    def stop_recording(frame):
        # pump queue dry
        try:
            while messages.get(block=False):
                pass
        except:
            pass
        print("stop_recording: messages emptied")

    # microphone input thread
    # Runs when speech-to-text is active
    # Reads data from mic stream and puts on frames queue
    # Note messages queue is used to start/stop thread
    def record_microphone(vMgrFrm, chunk=1024):
        global CHANNELS
        global FRAME_RATE
        global INPUT_DEV

        print("record_microphone: thread started, chan", CHANNELS, " rate", FRAME_RATE, " input", INPUT_DEV)
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

        while not vMgrFrm.vars.rec[0]:
            pass

        print("record_microphone: speech rec started, start recording")

        # while main wants us to run
        while not messages.empty():
            data = stream.read(chunk)
            #print("rec: data len", len(data), " data", *data[0:20])
            frames.append(data)

            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                #print("rec: write", len(frames))
                recordings.put(frames.copy())
                frames = []

        print("record_microphone: Done recording")
        recordings.put([])

        stream.stop_stream()
        stream.close()
        p.terminate()
        vMgrFrm.vars.record[0] = None
        print("Recording thread done")

    # Load speech recognition model thread
    # Runs at start to load speech->text model
    def speech_recognition_load(vMgrFrm):
        print("speech_recognition_load thread started")
        if not vMgrFrm.vars.model[0]:
            vMgrFrm.vars.model[0] = Model(model_path=WyeCore.Utils.userLibPath() + "vosk-model-en-us-0.22")
            vMgrFrm.vars.rec[0] = KaldiRecognizer(vMgrFrm.vars.model[0], FRAME_RATE)
            vMgrFrm.vars.rec[0].SetWords(True)

        print("speech_recognition_load model loaded, show start/stop")
        vMgrFrm.vars.loadLbl[0].verb.setLabel(vMgrFrm.vars.loadLbl[0], "VOSK US English Loaded.  Voice Input ready")
        vMgrFrm.vars.startStopFrm[0].verb.show(vMgrFrm.vars.startStopFrm[0])
        vMgrFrm.vars.textFrm[0].verb.show(vMgrFrm.vars.textFrm[0])
        vMgrFrm.vars.load[0] = None
        print("Loading speech model thread done")

    # convert data to text thread
    # Runs while speech-to-text is active
    # Reads from audio frames queue.  Converts to text.  Parses text for Wye commands.
    #  There are two parallel loops, one translating sound buffs to text and one parsing the text into Wye commands.
    #  Some commands are one-shot operations.  Others start running and continue to take words from the input stream
    #  until the user starts a new Wye command.
    # Aggregated input stream is stored in cmdText variable (vMgrFrm.vars.currCmd[0])
    # Note messages queue is used to start/stop thread
    def speech_recognition(vMgrFrm):
        print("speech_recognition thread started")

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
            print("Got", len(frames)," audio frames")
            if len(frames):
                # process sound into words
                vMgrFrm.vars.rec[0].AcceptWaveform(b''.join(frames))
                result = vMgrFrm.vars.rec[0].Result()
                #print("speech_recognition result", result)
                newText = json.loads(result)["text"]
                #print("speech", newText)

                # if we got words, process them
                if len(newText) > 0:
                    if newText == "the":   # ignore solitary "the" which seems to be what silence generates
                        # nothing to do here
                        # if building command (i.e. current cmd not match any known cmds) then fail building that cmd and clear buffer
                        if procState == PROC_BUILDING_CMD:
                            vMgrFrm.vars.cmdText[0] = []
                            print(" got 'the', clear building command buffer to:", vMgrFrm.vars.cmdText[0])
                            procState = PROC_WAITING

                    else:
                        # Split into words
                        textList = newText.split(" ")
                        print(" New textList:", textList)
                        print(" existing text:", vMgrFrm.vars.cmdText[0])

                        # if start new command clear any existing string
                        if textList[0] == "why":
                            # building command
                            procState = PROC_BUILDING_CMD

                            # flush command buffer and load new command
                            vMgrFrm.vars.cmdText[0] = [x for x in textList]
                            print("Start Wye command:", vMgrFrm.vars.cmdText[0])

                        # else add to current command string
                        else:
                            vMgrFrm.vars.cmdText[0].extend(textList)
                            print("Continue Wye command:", vMgrFrm.vars.cmdText[0])

                        txt = ""
                        for s in vMgrFrm.vars.cmdText[0]:
                            if s == "why":
                                s = "Wye"
                            txt += s + " "
                        vMgrFrm.vars.textFrm[0].verb.setLabel(vMgrFrm.vars.textFrm[0], txt)


                        # If we have Wye commands, process them

                        # continue command loop
                        haveCmd = True
                        while haveCmd:
                            print("haveCmd True, cmdText:", vMgrFrm.vars.cmdText[0])
                            # if we're building a command (trying to recognize current command string - may not be complete yet)
                            if procState == PROC_BUILDING_CMD:
                                txtLen = len(vMgrFrm.vars.cmdText[0])
                                if txtLen:
                                    # try to find current command in known commands
                                    # if found it will run and will remove any words it uses from the input buffer.
                                    # if it stays running and wants more input, it will put itself in
                                    # vMgrFrm.vars.currCmd[0] and return True
                                    if vMgrFrm.verb.parse(vMgrFrm):
                                        # it wants more input so put itself in vMgrFrm.vars.currCmd[0]
                                        procState = PROC_RUNNING_CMD

                                    # did not find matching command, exit loop to wait for more text in case that helps
                                    else:
                                        haveCmd = False

                                # no text to process, drop out of loop
                                else:
                                    haveCmd = False

                            # if command still running and it wants more input and we have more input
                            while procState == PROC_RUNNING_CMD and len(vMgrFrm.vars.cmdText[0]) > 0:
                                # run cmd.
                                # if returns True then it wants to keep processing input
                                # if returns false it's done.  See if there are more commands in input
                                if not vMgrFrm.vars.currCmd[0](vMgrFrm):
                                    # returned false, command is done. Check for another command in stream and clear leftover words
                                    procState = PROC_WAITING
                                    # search remaining text for a Wye command.  Clear anything not recognized
                                    # todo - collect unmatched command text strings and log them
                                    while len(vMgrFrm.vars.cmdText[0]) > 0 and procState == PROC_WAITING:
                                        # Is first remaining word start of a Wye command?
                                        if vMgrFrm.vars.cmdText[0][0] == "why":
                                            # Found Wye command, switch to building cmd
                                            procState = PROC_BUILDING_CMD
                                        # nope, delete word and loop to look at next one
                                        else:
                                            vMgrFrm.vars.cmdText[0] = vMgrFrm.vars.cmdText[0][1:]

                            haveCmd = False

                        print("Done processing text input")

                else:
                    print("Nothing parsed from input")
            else:
                print("No input")

        print("speech_recognition: messages empty, stopped recognition")


        vMgrFrm.vars.transcribe[0] = None
        print("speech_recognition thread Done")

    # parse for cmd in ouputText starting at txtIx
    def parse(frame):
        print("voiceDialog parse:", frame.vars.cmdText[0])

        # look for match in prebuilt commands
        for cmd in frame.verb.commands:
            cmdLen = len(cmd[1])
            # check text after the initial "why"
            print("  Compare input to", cmd[1])
            for wdIx in range(1,cmdLen):
                # if fail to match, kick out to try the next word
                if frame.vars.cmdText[0][wdIx] != cmd[1][wdIx]:
                    break;
            # if get here, it's a match!
            print("Found command", cmd[1])
            # call command.  Will return True if it wants to keep processing input
            cmdContinues = cmd[0](frame)
            # trim text used by command off input buffer
            frame.vars.cmdText[0] = frame.vars.cmdText[cmdLen:]
            if cmdContinues:
                frame.vars.currCmd[0] = cmd[0]
                # if cmd wants to process more text,
            return cmdContinues

        frame.vars.cmdText[0] = []
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
                vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Loading English Model")
                vMgrFrm.verb.start_recording(vMgrFrm)
                vMgrFrm.vars.shutdownCallback[0] = partial(vMgrFrm.verb.stopVoiceInput, vMgrFrm)
                WyeCore.World.shutdownCallbacks.append(vMgrFrm.vars.shutdownCallback[0])


            else:
                vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Enable Voice Input")
                vMgrFrm.verb.stop_recording(vMgrFrm)
                #print("StartStopCallback Stopped recording (maybe)")
                if vMgrFrm.vars.shutdownCallback[0] and vMgrFrm.vars.shutdownCallback[0] in WyeCore.World.shutdownCallbacks:
                    WyeCore.World.shutdownCallbacks.remove(vMgrFrm.vars.shutdownCallback[0])
                    vMgrFrm.vars.shutdownCallback[0] = None

