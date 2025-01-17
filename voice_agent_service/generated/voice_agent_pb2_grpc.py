# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import voice_agent_pb2 as voice__agent__pb2


class VoiceAgentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DetectWakeWord = channel.unary_stream(
                '/VoiceAgentService/DetectWakeWord',
                request_serializer=voice__agent__pb2.Empty.SerializeToString,
                response_deserializer=voice__agent__pb2.WakeWordStatus.FromString,
                )
        self.RecognizeVoiceCommand = channel.unary_unary(
                '/VoiceAgentService/RecognizeVoiceCommand',
                request_serializer=voice__agent__pb2.RecognizeControl.SerializeToString,
                response_deserializer=voice__agent__pb2.RecognizeResult.FromString,
                )


class VoiceAgentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DetectWakeWord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RecognizeVoiceCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VoiceAgentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DetectWakeWord': grpc.unary_stream_rpc_method_handler(
                    servicer.DetectWakeWord,
                    request_deserializer=voice__agent__pb2.Empty.FromString,
                    response_serializer=voice__agent__pb2.WakeWordStatus.SerializeToString,
            ),
            'RecognizeVoiceCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RecognizeVoiceCommand,
                    request_deserializer=voice__agent__pb2.RecognizeControl.FromString,
                    response_serializer=voice__agent__pb2.RecognizeResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'VoiceAgentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VoiceAgentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DetectWakeWord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/VoiceAgentService/DetectWakeWord',
            voice__agent__pb2.Empty.SerializeToString,
            voice__agent__pb2.WakeWordStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RecognizeVoiceCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VoiceAgentService/RecognizeVoiceCommand',
            voice__agent__pb2.RecognizeControl.SerializeToString,
            voice__agent__pb2.RecognizeResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
