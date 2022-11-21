///
//  Generated code. Do not modify.
//  source: recognize.proto
//
// @dart = 2.12
// ignore_for_file: annotate_overrides,camel_case_types,constant_identifier_names,directives_ordering,library_prefixes,non_constant_identifier_names,prefer_final_fields,return_of_invalid_type,unnecessary_const,unnecessary_import,unnecessary_this,unused_import,unused_shown_name

import 'dart:async' as $async;

import 'dart:core' as $core;

import 'package:grpc/service_api.dart' as $grpc;
import 'recognize.pb.dart' as $0;
export 'recognize.pb.dart';

class RecognizerServiceClient extends $grpc.Client {
  static final _$recognize = $grpc.ClientMethod<$0.Control, $0.Result>(
      '/RecognizerService/Recognize',
      ($0.Control value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.Result.fromBuffer(value));

  RecognizerServiceClient($grpc.ClientChannel channel,
      {$grpc.CallOptions? options,
      $core.Iterable<$grpc.ClientInterceptor>? interceptors})
      : super(channel, options: options, interceptors: interceptors);

  $grpc.ResponseFuture<$0.Result> recognize($0.Control request,
      {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$recognize, request, options: options);
  }
}

abstract class RecognizerServiceBase extends $grpc.Service {
  $core.String get $name => 'RecognizerService';

  RecognizerServiceBase() {
    $addMethod($grpc.ServiceMethod<$0.Control, $0.Result>(
        'Recognize',
        recognize_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.Control.fromBuffer(value),
        ($0.Result value) => value.writeToBuffer()));
  }

  $async.Future<$0.Result> recognize_Pre(
      $grpc.ServiceCall call, $async.Future<$0.Control> request) async {
    return recognize(call, await request);
  }

  $async.Future<$0.Result> recognize(
      $grpc.ServiceCall call, $0.Control request);
}
