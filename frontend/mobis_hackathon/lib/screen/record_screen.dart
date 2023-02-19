import 'dart:io';

import 'package:flutter/material.dart';
import 'package:audio_waveforms/audio_waveforms.dart';
import 'package:mobis_hackathon/api/api.dart';
import 'package:mobis_hackathon/models/voice.dart';
import 'package:mobis_hackathon/screen/noise_screen.dart';
import 'package:path_provider/path_provider.dart';

class RecordScreen extends StatefulWidget {
  const RecordScreen({super.key});

  @override
  State<RecordScreen> createState() => _RecordScreenState();
}

class _RecordScreenState extends State<RecordScreen> {
  late final RecorderController recorderController;
  bool ispause = true;
  String rawPath = "";
  late Directory appDirectory;

  @override
  void initState() {
    super.initState();
    _getDir();
    _initialiseController();
  }

  @override
  Widget build(BuildContext context) {
    Voice voice;
    return WillPopScope(
      onWillPop: () async => false,
      child: Scaffold(
        backgroundColor: Theme.of(context).backgroundColor,
        appBar: AppBar(
          title: Text(
            "음성 녹음",
            style: Theme.of(context).textTheme.headline2,
          ),
          automaticallyImplyLeading: false,
          actions: [
            IconButton(
                onPressed: () {
                  Navigator.push(
                      context,
                      SlideRightRoute(
                        page: NoiseScreen(
                          rawPath: rawPath,
                        ),
                      ));
                  voice = Voice(rawPath);
                  VoiceAPI.uploadVoice(voice);
                },
                icon: const Icon(
                  Icons.chevron_right_rounded,
                ))
          ],
          centerTitle: true,
          backgroundColor: Theme.of(context).backgroundColor,
          elevation: 0,
        ),
        body: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(
              height: 100,
            ),
            SizedBox(
              height: 300,
              child: Column(
                children: [
                  AudioWaveforms(
                    size: Size(MediaQuery.of(context).size.width, 300.0),
                    recorderController: recorderController,
                    enableGesture: true,
                    decoration: BoxDecoration(
                      color: Theme.of(context).canvasColor,
                    ),
                    waveStyle: const WaveStyle(
                      waveColor: Colors.white,
                      showDurationLabel: true,
                      showHourInDuration: true,
                      durationLinesColor: Colors.white,
                      durationStyle: TextStyle(
                          color: Colors.white, fontSize: 12.0, height: -4),
                      durationLinesHeight: -10,
                      durationTextPadding: 22.0,
                      spacing: 8.0,
                      scaleFactor: 50.0,
                      showBottom: true,
                      extendWaveform: true,
                      showMiddleLine: false,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(
              height: 150,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 60.0,
                  height: 60.0,
                  decoration: const BoxDecoration(
                    color: Color(0xff747474),
                    shape: BoxShape.circle,
                  ),
                  child: InkWell(
                    onTap: () {
                      setState(() {
                        _stopRecording();
                        ispause = true;
                      });
                    },
                    child: const Icon(
                      Icons.stop,
                      color: Colors.white,
                      size: 40,
                    ),
                  ),
                ),
                const SizedBox(
                  width: 40,
                ),
                Container(
                  width: 80.0,
                  height: 80.0,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                  ),
                  child: InkWell(
                    onTap: () {
                      ispause
                          ? setState(() {
                              _startRecording();
                              ispause = false;
                            })
                          : setState(() {
                              _pauseRecording();
                              ispause = true;
                            });
                    },
                    child: ispause
                        ? const Icon(
                            Icons.fiber_manual_record,
                            color: Colors.red,
                            size: 40,
                          )
                        : const Icon(
                            Icons.pause,
                            color: Colors.black45,
                            size: 40,
                          ),
                  ),
                ),
                const SizedBox(
                  width: 40,
                ),
                Container(
                  width: 60.0,
                  height: 60.0,
                  decoration: const BoxDecoration(
                    color: Color(0xff747474),
                    shape: BoxShape.circle,
                  ),
                  child: InkWell(
                    onTap: () {
                      setState(() {
                        _resetRecording();
                        ispause = true;
                      });
                    },
                    child: const Icon(
                      Icons.refresh_outlined,
                      color: Colors.white,
                      size: 40,
                    ),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }

  void _initialiseController() {
    recorderController = RecorderController()
      ..androidEncoder = AndroidEncoder.aac
      ..androidOutputFormat = AndroidOutputFormat.mpeg4
      ..iosEncoder = IosEncoder.kAudioFormatMPEG4AAC
      ..sampleRate = 16000;
  }

  void _startRecording() async {
    await recorderController.record(path: rawPath);
  }

  void _stopRecording() async {
    await recorderController.pause();
    await recorderController.stop();
  }

  void _pauseRecording() async {
    await recorderController.pause();
  }

  void _resetRecording() async {
    await recorderController.pause();
    recorderController.reset();
  }

  void _getDir() async {
    appDirectory = await getApplicationDocumentsDirectory();
    rawPath = "${appDirectory.path}/raw.m4a";
    setState(() {});
  }
}

class SlideRightRoute extends PageRouteBuilder {
  final Widget page;
  SlideRightRoute({required this.page})
      : super(
          pageBuilder: (
            BuildContext context,
            Animation<double> animation,
            Animation<double> secondaryAnimation,
          ) =>
              page,
          transitionsBuilder: (
            BuildContext context,
            Animation<double> animation,
            Animation<double> secondaryAnimation,
            Widget child,
          ) =>
              SlideTransition(
            position: Tween<Offset>(
              begin: const Offset(1, 0),
              end: Offset.zero,
            ).animate(animation),
            child: child,
          ),
        );
}
