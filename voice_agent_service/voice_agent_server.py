import grpc
import time
from concurrent import futures
import voice_agent_pb2
import voice_agent_pb2_grpc
from utils.AudioRecorder import AudioRecorder

BASE_AUDIO_DIR = "commands/"
VOSK_MODEL_PATH = "/home/malik/Desktop/AGL Local/voicerecognizer-gst-grpc/voice_agent_service/voice-model/vosk-model-small-en-us-0.15"


class VoiceAgentServicer(voice_agent_pb2_grpc.VoiceAgentServiceServicer):
    def __init__(self):
        self.recorder = AudioRecorder(BASE_AUDIO_DIR, VOSK_MODEL_PATH)

    def WaitForWakeWord(self, request, context):
        self.recorder.cleanup_pipeline()
        self.recorder.create_pipeline("auto")
        self.recorder.wait_for_wake_word()
        while True:
            word = self.recorder.get_wake_word_detected()
            time.sleep(1)
            yield voice_agent_pb2.WakeWordDetected(wake_word=word)
            if word:
                break
    
    def VoiceAgent(self, request, context):
        result = {
            "user_command": "Command not recognized. Please speak again...",
            "user_intent": "",
            "intent_slots": []
            
        }
        if request.action == voice_agent_pb2.START:
            self.recorder.cleanup_pipeline()
            self.recorder.create_pipeline("manual")
            self.recorder.record_command()
            time.sleep(5)
            self.recorder.stop_recording()
        
        return result
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voice_agent_pb2_grpc.add_VoiceAgentServiceServicer_to_server(VoiceAgentServicer(), server)
    server.add_insecure_port('[::]:51053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()