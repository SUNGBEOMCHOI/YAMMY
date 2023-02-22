<div align="center">
 
<img width="100%" height="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2&height=200&section=header&animation=fadeIn&fontAlignY=40&text=Y%20A%20M%20M%20Y&fontSize=75" alt="header" />
</div>

<h3 align="center">🚗 Yonsei Ai with hyundai Mobis MobilitY 🚗</h3>

<h4 align="center">✨ Contributors ✨</h4>
<p align="center">
<a href="https://github.com/ori-orori"><b>🚆 KIM GUNHA</b></a><br>
<a href="https://github.com/etoilekim"><b>✈️ KIM NAMHOON</b></a><br>
<a href="https://github.com/0601p"><b>🚑 PARK MINSU</b></a><br>
<a href="https://github.com/SUNGBEOMCHOI"><b>🚒 CHOI SUNGBEOM</b></a>
</p>

<br>

<hr>

### 모빌리티 최적화 Speech Recognition

#### 우리 팀만의 핵심 포인트

1. 다른 차량용 음성인식 솔루션보다 더 뛰어난 인식률을 보여준다
2. 차량마다 노이즈(차종, 속도, 주차상황)와 남녀노소의 데이터를 모두 학습한 모델
3. 실제 자동차에서 사용되는 어휘들에 대해서 집중적으로 학습하였다.

#### 프로젝트 개요

- 프로젝트 기획 배경 및 목적
    - 차량내에서 발생하는 다양한 소음에 대해서 안정성을 보이는 음성인식 모델 개발
- 개발 환경 및 언어
    - Pipeline : <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white" />
    - [Front-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/frontend/mobis_hackathon) : <img src="https://img.shields.io/badge/Flutter-02569B?style=flat&logo=Flutter&logoColor=white" />
    - [Back-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/backend) : <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white" />

#### 프로젝트 프로세스
<div align="center">

![pipeline](https://user-images.githubusercontent.com/63270534/220610742-bf791ac6-1f79-41f6-9aa8-b60c1f605745.png)
</div>

- Pre Processing
- [Wavenet](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/WaveNet_PyTorch) &emsp; [\<paper\>](https://github.com/drethage/speech-denoising-wavenet)
- [LAS](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/ClovaCall) &emsp; [\<paper\>](https://arxiv.org/abs/1508.01211)

#### 학습 데이터
- [AIHub 한국어 음성 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)
- [AIHub 차량 내 대화 및 명령어 AI 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=112)


#### 결과(시연) 화면
<div align="center">
 
<img src="https://user-images.githubusercontent.com/68505714/220413066-cb517248-b008-4ab5-92c8-c9e2a8561681.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413072-69444049-7d64-463a-8b07-284c8125f03a.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413075-4b5b556e-a368-49ad-808b-3f94992c8325.png" width="30%" height="30%"/>
</div>

<p align="center">
https://user-images.githubusercontent.com/63270534/220625030-be277b9d-d4be-4c10-bc38-85ed1a8b5c49.mp4
</p>

#### 성능

- 노이즈에 따른 CER(%)

||Clova API|YAMMY|
|:---|:---:|:---:|
|Noisy Data|29.20|17.8|

- 화자에 따른 CER(%)

||LAS(pre trained)|       YAMMY       |
|:---|:---:|:---:|
|여자|128.86|16.01|
|남자|114.18|23.88|
|20 ~ 29세|124.79|21.04|
|30 ~ 39세|126.69|23.12|
|40 ~ 49세|93.65|12.95|
|50 ~ 59세|98.89|19.13|
|60 ~ 69세|181.72|16.38|

- 노이즈 종류에 따른 CER(%)

||LAS(pre trained)|YAMMY|
|:---|:---:|:---:|
|고속|92.40|21.02|
|중속|90.02|15.96|
|저속|94.20|21.45|
|정차|87.07|16.61|
|후진|102.68|23.37|
|공조장치 MAX|96.23|21.02|
|공조장치 MID|90.15|15.96|
|공조장치 MIN|90.07|20.93|
|후진경고음|110.49|24.83|


<br>

<hr>

<img width="100%" height="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2&height=200&section=footer&animation=fadeIn" alt="header" />
</div>
