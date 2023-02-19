import 'package:audio_waveforms/audio_waveforms.dart';
import 'package:flutter/material.dart';
import 'package:indexed/indexed.dart';
import 'package:mobis_hackathon/api/api.dart';
import 'package:mobis_hackathon/models/voice.dart';

class NoiseScreen extends StatefulWidget {
  const NoiseScreen({
    super.key,
    required this.rawPath,
  });

  final String rawPath;

  @override
  State<NoiseScreen> createState() => _NoiseScreenState();
}

class _NoiseScreenState extends State<NoiseScreen> {
  final PlayerController playerControllerRaw = PlayerController();
  final PlayerController playerControllerNoise = PlayerController();
  final PlayerController playerControllerDenoise = PlayerController();

  bool noiseWaveVisible = false;
  bool denoiseWaveVisible = false;
  bool denoiseWaveVisible1 = false;
  bool textVisible = false;
  bool textVisible1 = false;

  int zIndexOrigin = 3;
  int zIndexNoise = 2;
  int zIndexDenoise = 1;

  double yPositionOrigin = 0;
  double yPositionNoise = 150;
  double yPositionDenoise = 300;
  String text = "안녕하세요";
  String _text = "";

  String? noisePath;
  String? denoisePath = "";

  @override
  void initState() {
    super.initState();
    playerControllerRaw.preparePlayer(path: widget.rawPath);
    final voice = Voice(widget.rawPath);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).backgroundColor,
      appBar: AppBar(
        title: const Text(
          "음성 인식",
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
        backgroundColor: Theme.of(context).backgroundColor,
        elevation: 0,
      ),
      body: Indexer(
        children: [
          Indexed(
            index: zIndexOrigin,
            child: waveCard(
              context: context,
              playerController: playerControllerRaw,
              title: "원본 음성",
              request: "차량 노이즈 추가",
              btnVisible: noiseWaveVisible,
              cardVisible: true,
              yPostion: yPositionOrigin,
            ),
          ),
          Indexed(
            index: zIndexNoise,
            child: waveCard(
              context: context,
              playerController: playerControllerNoise,
              title: "노이즈 음성",
              request: "노이즈 제거",
              btnVisible: denoiseWaveVisible,
              cardVisible: noiseWaveVisible,
              yPostion: yPositionNoise,
            ),
          ),
          denoiseWaveVisible1
              ? Indexed(
                  index: zIndexDenoise,
                  child: waveCard(
                    context: context,
                    playerController: playerControllerDenoise,
                    title: "노이즈 제거 음성",
                    request: "텍스트 변환",
                    btnVisible: textVisible,
                    cardVisible: denoiseWaveVisible,
                    yPostion: yPositionDenoise,
                  ),
                )
              : Container(),
          textVisible
              ? AnimatedContainer(
                  duration: const Duration(
                    milliseconds: 1000,
                  ),
                  width: MediaQuery.of(context).size.width,
                  height: 230,
                  padding: const EdgeInsets.symmetric(
                    vertical: 15,
                    horizontal: 20,
                  ),
                  margin: const EdgeInsets.fromLTRB(20, 20, 20, 20),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.white,
                  ),
                  transform: textVisible1
                      ? (Matrix4.identity()..translate(0.0, 450.0))
                      : (Matrix4.identity()..translate(0.0, 900.0)),
                  child:
                      Text(text, style: Theme.of(context).textTheme.bodyText1),
                )
              : Container(),
        ],
      ),
    );
  }

  void _startTyping(int textLength) {
    for (int index = 0; index < textLength + 1; index++) {
      Future.delayed(Duration(milliseconds: 1500 + index * 500), () {
        setState(() {
          _text = text.substring(0, index);
        });
      });
    }
  }

  AnimatedContainer waveCard({
    required BuildContext context,
    required PlayerController playerController,
    required String title,
    required String request,
    required bool btnVisible,
    required bool cardVisible,
    required double yPostion,
  }) {
    return AnimatedContainer(
      duration: const Duration(
        milliseconds: 1000,
      ),
      width: MediaQuery.of(context).size.width,
      height: btnVisible ? 130 : 180,
      margin: const EdgeInsets.fromLTRB(20, 20, 20, 0),
      transform: !cardVisible
          ? (Matrix4.identity()
            ..translate(0.025 * 0, yPostion - yPositionNoise))
          : (Matrix4.identity()..translate(0.025 * 0, yPostion)),
      onEnd: () {
        if (request == "노이즈 제거") {
          setState(() {
            denoiseWaveVisible1 = true;
          });
        }
      },
      padding: const EdgeInsets.symmetric(
        vertical: 13,
        horizontal: 10,
      ),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: Theme.of(context).cardColor,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            width: MediaQuery.of(context).size.width * 0.8,
            margin: const EdgeInsets.symmetric(),
            padding: const EdgeInsets.symmetric(vertical: 5),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Column(
              children: [
                const SizedBox(
                  height: 7,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const SizedBox(
                      width: 20,
                    ),
                    SizedBox(
                      width: 150,
                      child: Text(
                        title,
                        style: Theme.of(context).textTheme.subtitle1,
                      ),
                    ),
                    const SizedBox(
                      width: 40,
                    ),
                    Container(
                      width: 32.0,
                      height: 32.0,
                      decoration: const BoxDecoration(
                        color: Color(0xff7E81EB),
                        shape: BoxShape.circle,
                      ),
                      alignment: Alignment.center,
                      child: InkWell(
                        onTap: () {
                          setState(() {
                            _playandPause(playerController);
                          });
                        },
                        child:
                            playerController.playerState == PlayerState.playing
                                ? const Icon(
                                    Icons.pause,
                                    color: Colors.white,
                                    size: 15,
                                  )
                                : const Icon(
                                    Icons.play_arrow,
                                    color: Colors.white,
                                    size: 15,
                                  ),
                      ),
                    ),
                    const SizedBox(
                      width: 20,
                    ),
                  ],
                ),
                const SizedBox(
                  height: 10,
                ),
                AudioFileWaveforms(
                  size: Size(MediaQuery.of(context).size.width / 2, 40),
                  playerController: playerController,
                  playerWaveStyle: PlayerWaveStyle(
                    scaleFactor: 100,
                    fixedWaveColor: const Color(0xff000000).withAlpha(30),
                    liveWaveColor: const Color(0xff7E81EB),
                    showSeekLine: false,
                    waveCap: StrokeCap.butt,
                  ),
                ),
              ],
            ),
          ),
          !btnVisible
              ? InkWell(
                  onTap: () {
                    if (request == "차량 노이즈 추가") {
                      setState(() {
                        noiseWaveVisible = true;

                        // TODO noise 백엔드에서 받기
                        getNoiseWave();
                      });
                    } else if (request == "노이즈 제거") {
                      setState(() {
                        denoiseWaveVisible = true;
                        // TODO denoise 백엔드에서 받기
                        getDenoiseWave();
                      });
                    } else if (request == "텍스트 변환") {
                      setState(() {
                        textVisible = true;
                        // TODO 텍스트 백엔드에서 받기
                        Future.delayed(const Duration(milliseconds: 200), () {
                          setState(() {
                            textVisible1 = true;
                            text = VoiceAPI.viewVoice(
                                requestType: "text", fileName: "/test.wav");
                          });
                        });
                        // _startTyping(text.length);
                      });
                    }
                  },
                  child: Container(
                    margin: const EdgeInsets.fromLTRB(0, 10, 0, 0),
                    padding: const EdgeInsets.fromLTRB(0, 10, 0, 10),
                    width: 150,
                    height: 40,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(9),
                      color: const Color(0xff7E81EB),
                    ),
                    child: Center(
                      child: Text(
                        request,
                        style: Theme.of(context).textTheme.bodyText2,
                      ),
                    ),
                  ),
                )
              : Container(),
        ],
      ),
    );
  }

  void _playandPause(PlayerController playerController) async {
    playerController.playerState == PlayerState.playing
        ? await playerController.pausePlayer()
        : await playerController.startPlayer(finishMode: FinishMode.loop);
  }

  void getNoiseWave() async {
    // 백엔드에서 노이즈 경로 가져오기
    // await Future.value('DenoisePath').then((result) {
    //   noisePath = result;
    // });
    noisePath = await VoiceAPI.viewVoice(
        requestType: "noise",
        fileName: voice.fileName,
        savePath: './noise.wav');
    playerControllerNoise.preparePlayer(path: noisePath!);
  }

  void getDenoiseWave() async {
    // 백엔드에서 디노이즈 경로 가져오기
    // await Future.value('DenoisePath').then((result) {
    //   // denoisePath = result;
    // });
    denoisePath = await VoiceAPI.viewVoice(
        requestType: "noise",
        fileName: voice.fileName,
        savePath: './noise.wav');
    playerControllerDenoise.preparePlayer(path: denoisePath!);
  }
}
