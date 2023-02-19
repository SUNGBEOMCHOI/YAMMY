import 'package:dio/dio.dart';
import 'dart:io';
import 'package:http_parser/http_parser.dart';
import 'package:path_provider/path_provider.dart';
import 'package:mobis_hackathon/models/voice.dart';

final dio = Dio();

const String ip = "95.217.244.39";
// const String ip = "ssh4.vast.ai";
const String port = "22";

class VoiceAPI {
  static uploadVoice(voice) async {
    Response response;
    final formData = FormData.fromMap({
      "voice_file": await MultipartFile.fromFile(
        voice.fullPath,
        contentType: MediaType('audio', 'wav'),
      ),
      "file_name": voice.fileName,
    });
    response = await dio.post(
      'http://$ip:$port/api/voice_list',
      data: formData,
    );
  }

  static viewVoice(
      {String? requestType, String? fileName, String? savePath}) async {
    Response response;
    final appDirectory = await getApplicationDocumentsDirectory();

    if (requestType == 'list') {
      response = await dio.get(
        'http://$ip:$port/api/voice_list',
        queryParameters: {'request_type': "list"},
      );
    } else if (requestType == 'text') {
      response = await dio.get(
        'http://$ip:$port/api/voice_list',
        queryParameters: {'request_type': "text", "file_name": fileName},
      );
    } else {
      response = await dio.get('http://$ip:$port/api/voice_list',
          queryParameters: {'request_type': requestType, "file_name": fileName},
          options: Options(responseType: ResponseType.bytes));
    }

    if (response.statusCode == 200) {
      if (requestType == 'list') {
        print(response.data);
      } else if (requestType == 'text') {
        return response.data['sr_result'];
      } else {
        if (savePath != null) {
          savePath = "${appDirectory.path}$savePath";
          File(savePath).writeAsBytes(response.data);
          return savePath;
        } else {
          File('/data/user/0/com.example.mobis_hackathon/app_flutter/unknown.wav')
              .writeAsBytes(response.data);
          return savePath;
        }
      }
    } else {
      print('Error while connecting to server.');
    }
  }
}

final voice = Voice('C:/Users/chois/Desktop/mobis_hackathon/lib/api/test.wav');

void main() {
  VoiceAPI.uploadVoice(voice);
  VoiceAPI.viewVoice(
      requestType: "noise", fileName: "/test.wav", savePath: "/test_noise.wav");
  VoiceAPI.viewVoice(
      requestType: "dnoise",
      fileName: "/test.wav",
      savePath: "/test_denoise.wav");
  // VoiceAPI.viewVoice(requestType: "text", fileName: "/test.wav",);
}
