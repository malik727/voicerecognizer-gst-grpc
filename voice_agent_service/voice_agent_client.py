import grpc
import voice_agent_pb2
import voice_agent_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:51053') as channel:
        stub = voice_agent_pb2_grpc.VoiceAgentServiceStub(channel)
        print("Listening for wake word...")
        wake_request = voice_agent_pb2.Empty()
        wake_results = stub.WaitForWakeWord(wake_request)
        wake_word_detected = False
        for wake_result in wake_results:
            if wake_result.wake_word:
                print("Wake word detected!")
                wake_word_detected = True
                break

        if wake_word_detected:
            print("Command Recording started...")
            recording_request = voice_agent_pb2.AgentControl(action=voice_agent_pb2.START, nlu_model=voice_agent_pb2.SNIPS)
            recording_result = stub.VoiceAgent(recording_request)
            print("Command Recording stopped...")
            print(recording_result)

if __name__ == '__main__':
    run()
