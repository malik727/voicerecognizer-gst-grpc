# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import recognize_pb2 as recognize__pb2


class RecognizerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Recognize = channel.unary_unary(
                '/vosk.stt.v1.RecognizerService/Recognize',
                request_serializer=recognize__pb2.Control.SerializeToString,
                response_deserializer=recognize__pb2.Result.FromString,
                )


class RecognizerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Recognize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecognizerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Recognize': grpc.unary_unary_rpc_method_handler(
                    servicer.Recognize,
                    request_deserializer=recognize__pb2.Control.FromString,
                    response_serializer=recognize__pb2.Result.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'vosk.stt.v1.RecognizerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RecognizerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Recognize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vosk.stt.v1.RecognizerService/Recognize',
            recognize__pb2.Control.SerializeToString,
            recognize__pb2.Result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
