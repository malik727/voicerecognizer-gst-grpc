#!/usr/bin/env python

# grpc imports
import grpc
from generated import voice_agent_pb2
from generated import voice_agent_pb2_grpc
from concurrent import futures

# wav and vosk recognizer imports
import os
import sys
import wave
import json
from vosk import Model, KaldiRecognizer

# gst imports
import gi
from time import sleep
import asyncio
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()

autoaudiosrc = Gst.ElementFactory.make("autoaudiosrc", "autoaudiosrc")
queue = Gst.ElementFactory.make("queue", "queue")
audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
wavenc = Gst.ElementFactory.make("wavenc", "wavenc")
filesink = Gst.ElementFactory.make("filesink", "filesink")
# with tempfile.TemporaryDirectory() as tmpdirname:
#     print('created temporary directory', tmpdirname)
#     url = tmpdirname + "/recorded_audio.wav"

url = "recorded_audio.wav"
filesink.set_property("location",url)
pipeline.add( autoaudiosrc)
pipeline.add( queue)
pipeline.add( audioconvert)
pipeline.add( capsfilter)
pipeline.add( wavenc)
pipeline.add( filesink)

autoaudiosrc.link( queue)
queue.link( audioconvert)
audioconvert.link( capsfilter)
capsfilter.link( wavenc)
wavenc.link( filesink)
bus = pipeline.get_bus()

def record_from_microphone():
    capsfilter.set_property("caps", Gst.Caps.from_string("audio/x-raw,channels=1"))
    pipeline.set_state(Gst.State.PLAYING)
    print('Recording Voice Input')

def stop_recording():
    print("Sending EOS")
    pipeline.send_event(Gst.Event.new_eos())
    print('Ending Pipeline')
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)


# Vosk voice recognition

if len(sys.argv) > 1:
   vosk_model_path = sys.argv[1]

def voice_recognizer(filename):

    if len(sys.argv) > 1:
        vosk_model_path = sys.argv[1]
    # if not os.path.exists("model"):
    #     print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    #     exit (1)
    else:
        print("Model path must be given as arg")
        exit(1)

    wf = wave.open(filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    buffer_size = int(wf.getframerate() * 2.5) # 2.5 seconds of audio

    model = Model(vosk_model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    text_lst = []
    p_text_lst = []
    p_str = []
    len_p_str = []
    
    while True:
        data = wf.readframes(buffer_size)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text_lst.append(rec.Result())
            print(rec.Result())
        else:
            p_text_lst.append(rec.PartialResult())
            print(rec.PartialResult())

    if len(p_text_lst) != 0:
        combined_out = ""
        print(p_text_lst)
        for partial_dict in p_text_lst:
            jd = json.loads(partial_dict)
            combined_out = combined_out + jd["partial"] + "\n"
        return combined_out

    # if len(text_lst) !=0:
    #     jd = json.loads(text_lst[-1]) # get the final output from vosk
    #     # get the partial output from vosk

    #     txt_str = jd["text"]
    #     print(text_str)
    #     return text_str
    else:
        return "Voice not recognized. Please speak again..."


class VoiceAgentServicer(voice_agent_pb2_grpc.VoiceAgentServiceServicer):
    def Recognize(self, request, context):
        if request.action == voice_agent_pb2.AgentAction.START:
            record_from_microphone()
            result = "Recording..."
        elif request.action == voice_agent_pb2.AgentAction.STOP:
            stop_recording()
            result = voice_recognizer(url)
        else:
            result = "Some exception occured"
        return voice_agent_pb2.AgentResult(user_command = result)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    voice_agent_pb2_grpc.add_VoiceAgentServiceServicer_to_server(VoiceAgentServicer(), server)
    print("Server running now.")
    server.add_insecure_port('[::]:51053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
