import grpc
from generated import voice_agent_pb2
from generated import voice_agent_pb2_grpc
from time import sleep

def run():
    with grpc.insecure_channel('0.0.0.0:51053') as channel:
        stub = voice_agent_pb2_grpc.VoiceAgentServiceStub(channel)
        print("Recording started...")
        result = stub.VoiceAgent(voice_agent_pb2.AgentControl(action=voice_agent_pb2.START, nlu_model=voice_agent_pb2.SNIPS))
        sleep(10)
        result = stub.VoiceAgent(voice_agent_pb2.AgentControl(action=voice_agent_pb2.STOP, nlu_model=voice_agent_pb2.SNIPS))
        print("Recording stopped...")
        print(result)

if __name__ == '__main__':
    run()
