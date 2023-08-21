import gi
import vosk
import time
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)
GObject.threads_init()

class AudioRecorder:
    def __init__(self, audio_files_basedir, vosk_model_path):
        self.pipeline = None
        self.bus = None
        self.audio_files_basedir = audio_files_basedir
        self.wake_word_detected = False
        self.sample_rate = 16000  # Adjust this based on your needs
        self.channels = 1
        self.bits_per_sample = 16
        self.frame_size = int(self.sample_rate * 0.02)  # 20 ms frame size
        self.model = vosk.Model(vosk_model_path)
        self.rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
        self.buffer_duration = 1  # Buffer audio for atleast 1 second
        self.audio_buffer = bytearray()
    
    def get_wake_word_detected(self):
        return self.wake_word_detected

    def create_pipeline(self, mode="auto"):
        print("Creating pipeline in {} mode...".format(mode))
        self.pipeline = Gst.Pipeline()
        autoaudiosrc = Gst.ElementFactory.make("autoaudiosrc", "autoaudiosrc")
        queue = Gst.ElementFactory.make("queue", "queue")
        audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        wavenc = Gst.ElementFactory.make("wavenc", "wavenc")

        capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        caps = Gst.Caps.new_empty_simple("audio/x-raw")
        caps.set_value("format", "S16LE")
        caps.set_value("rate", self.sample_rate)
        caps.set_value("channels", self.channels)
        capsfilter.set_property("caps", caps)

        self.pipeline.add(autoaudiosrc)
        self.pipeline.add(queue)
        self.pipeline.add(audioconvert)
        self.pipeline.add(wavenc)
        self.pipeline.add(capsfilter)

        if mode == "auto":
            appsink = Gst.ElementFactory.make("appsink", "appsink")
            appsink.set_property("emit-signals", True)
            appsink.set_property("sync", False)  # Set sync property to False for async processing
            appsink.connect("new-sample", self.on_new_buffer, None)
            self.pipeline.add(appsink)
            wavenc.link(appsink)
        elif mode == "manual":
            filesink = Gst.ElementFactory.make("filesink", "filesink")
            filesink.set_property("location", f"{self.audio_files_basedir}{int(time.time())}.wav")
            self.pipeline.add(filesink)
            wavenc.link(filesink)
        
        autoaudiosrc.link(queue)
        queue.link(audioconvert)
        audioconvert.link(capsfilter)
        capsfilter.link(wavenc)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_bus_message)

    def on_new_buffer(self, appsink, data) -> Gst.FlowReturn:
        sample = appsink.emit("pull-sample")
        buffer = sample.get_buffer()
        data = buffer.extract_dup(0, buffer.get_size())
        self.audio_buffer.extend(data)

        if len(self.audio_buffer) >= self.sample_rate * self.buffer_duration * self.channels * self.bits_per_sample // 8:
            self.process_audio_buffer()

        return Gst.FlowReturn.OK
    
    def process_audio_buffer(self):
        # Process the accumulated audio data using the recognizer
        audio_data = bytes(self.audio_buffer)
        if self.rec.AcceptWaveform(audio_data):
            self.rec.SetWords(True)
            text = self.rec.Result()
            print("Text: ", text)
            if "hey auto" in text:
                self.wake_word_detected = True
                print("Wake word detected!")
                self.stop_recording()  # Stop recording when wake word is detected

        self.audio_buffer.clear()  # Clear the buffer


    def record(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        print("Recording Voice Input...")

    def stop_recording(self):
        print("Stopping recording...")
        self.cleanup_pipeline()
        print("Recording finished...")

    def wait_for_wake_word(self):
        print("Listening for wake word...")
        self.record()
    
    def record_command(self):
        print("Recording command...")
        self.record()
    
    # this method helps with error handling
    def on_bus_message(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            print("End-of-stream message received")
            self.stop_recording()
        elif message.type == Gst.MessageType.ERROR:
            err, debug_info = message.parse_error()
            print(f"Error received from element {message.src.get_name()}: {err.message}")
            print(f"Debugging information: {debug_info}")
            self.stop_recording()
        elif message.type == Gst.MessageType.WARNING:
            err, debug_info = message.parse_warning()
            print(f"Warning received from element {message.src.get_name()}: {err.message}")
            print(f"Debugging information: {debug_info}")
    
    def cleanup_pipeline(self):
        if self.pipeline is not None:
            print("Cleaning up pipeline...")
            self.pipeline.set_state(Gst.State.NULL)
            self.bus.remove_signal_watch()
            print("Pipeline cleanup complete!")
            self.bus = None
            self.pipeline = None
