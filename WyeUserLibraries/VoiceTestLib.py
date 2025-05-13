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

from queue import Queue

# global comm queues
messages = Queue()
recordings = Queue()

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
                ("cmdLst", Wye.dType.STRING_LIST, []),
                ("outputText", Wye.dType.STRING_LIST, []),
                )

    # global list of libs being edited
    activeFrames = {}

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

                frame.vars.loadLbl[0] = WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "Loading language model")

                #WyeCore.libs.WyeUIUtilsLib.doInputLabel(dlgFrm, "  Set Window Size (F11)", color=Wye.color.NORMAL_COLOR)
                frame.vars.startStopFrm[0] = WyeCore.libs.WyeUIUtilsLib.doInputCheckbox(dlgFrm, "Start",
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
                print("VoiceDialog close any open threads")
                if frame.vars.load[0]:
                    print("Wait for dictionary load thread to finish", flush=True)
                    frame.vars.load[0].join()
                    frame.vars.load[0] = None
                if frame.vars.record[0]:
                    print("Wait for transcribe thread to finish", flush=True)
                    frame.vars.record[0].join()
                    frame.vars.record[0] = None
                if frame.vars.transcribe[0]:
                    print("Wait for mic input thread to finish", flush=True)
                    frame.vars.transcribe[0].join()
                    frame.vars.transcribe[0] = None

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

    def record_microphone(vMgrFrm, chunk=1024):
        global CHANNELS
        global FRAME_RATE
        global INPUT_DEV

        print("record_microphone: thread started, chan", CHANNELS, " rate", FRAME_RATE, " input", INPUT_DEV)
        vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Stop")

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


        while not messages.empty():
            data = stream.read(chunk)
            #print("rec: data len", len(data), " data", *data[0:20])
            frames.append(data)

            if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
                #print("rec: write", len(frames))
                recordings.put(frames.copy())
                frames = []

        print("record_microphone: Done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        vMgrFrm.vars.record[0] = None

    def speech_recognition_load(vMgrFrm):
        print("speech_recognition_load thread started")
        if not vMgrFrm.vars.model[0]:
            vMgrFrm.vars.model[0] = Model(model_path=WyeCore.Utils.userLibPath() + "vosk-model-en-us-0.22")
            vMgrFrm.vars.rec[0] = KaldiRecognizer(vMgrFrm.vars.model[0], FRAME_RATE)
            vMgrFrm.vars.rec[0].SetWords(True)

        print("speech_recognition model loaded, show start/stop")
        vMgrFrm.vars.loadLbl[0].verb.setLabel(vMgrFrm.vars.loadLbl[0], "VOSK US English Loaded")
        vMgrFrm.vars.startStopFrm[0].verb.show(vMgrFrm.vars.startStopFrm[0])
        vMgrFrm.vars.textFrm[0].verb.show(vMgrFrm.vars.textFrm[0])
        vMgrFrm.vars.load[0] = None

    def speech_recognition(vMgrFrm):
        print("speech_recognition thread started")

        while not messages.empty():
            frames = recordings.get()
            if len(frames):
                vMgrFrm.vars.rec[0].AcceptWaveform(b''.join(frames))
                result = vMgrFrm.vars.rec[0].Result()
                #print("speech_recognition result", result)
                text = json.loads(result)["text"]
                print("speech", text)

                textLst = text.split(" ")
                vMgrFrm.vars.outputText[0].extend(textLst)
                vMgrFrm.vars.outputText[0] = vMgrFrm.vars.outputText[0][-10:]
                print(" agg", vMgrFrm.vars.outputText[0])
                txt = ""
                for s in vMgrFrm.vars.outputText[0]:
                    txt += s + " "
                vMgrFrm.vars.textFrm[0].verb.setLabel(vMgrFrm.vars.textFrm[0], txt)
                txtLen = len(vMgrFrm.vars.outputText[0])
                if txtLen:
                    usedThru = 0
                    for ii in range(txtLen-1):
                        cmd = vMgrFrm.vars.outputText[0][ii]
                        if cmd.lower() == "why":
                            usedThru = ii + vMgrFrm.verb.parse(vMgrFrm, ii)

                    vMgrFrm.vars.outputText[0] = vMgrFrm.vars.outputText[0][usedThru:]
                    print("remaining text", vMgrFrm.vars.outputText[0])
            else:
                print("No input")

        print("speech_recognition Done")
        vMgrFrm.vars.transcribe[0] = None

    # parse for cmd in ouputText starting at txtIx
    def parse(frame, txtIx):
        print("voiceDialog parse:", frame.vars.outputText[0][txtIx:])
        return 1

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

            else:
                vMgrFrm.vars.startStopFrm[0].verb.setLabel(vMgrFrm.vars.startStopFrm[0], "Start")
                vMgrFrm.verb.stop_recording(vMgrFrm)
                #print("StartStopCallback Stopped recording (maybe)")

