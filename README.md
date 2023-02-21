<div align="center">
 
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2&height=200&section=header&text=Y%20A%20M%20M%20Y&fontSize=90)
</div>

# Yonsei Ai with hyundai Mobis MobilitY
 
## 모빌리티 최적화 Speech Recognition

### 우리 팀만의 핵심 포인트

1. 다른 차량용 음성인식 솔루션보다 더 뛰어난 인식률을 보여준다
2. 차량마다 노이즈(차종, 속도, 주차상황)와 남녀노소의 데이터를 모두 학습한 모델
3. 실제 자동차에서 사용되는 어휘들에 대해서 집중적으로 학습하였다.

### 프로젝트 개요

- 프로젝트 기획 배경 및 목적
    - 차량내에서 발생하는 다양한 잡음에 대해서 뛰어난 안정성을 보이는 음성인식 모델
- 개발 환경 및 언어
    - Pipeline : <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white" />
    - [Front-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/frontend/mobis_hackathon) : <img src="https://img.shields.io/badge/Flutter-02569B?style=flat&logo=Flutter&logoColor=white" />
    - [Back-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/backend) : <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white" />

### 프로젝트 프로세스
<div align="center">
 
![Untitled](https://user-images.githubusercontent.com/68505714/220406531-77d82218-7641-4100-a3d8-e79443b87de8.png)
</div>

- Pre Processing
- [Wavenet](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/WaveNet_PyTorch) &emsp; [\<paper\>](https://github.com/drethage/speech-denoising-wavenet)
- [ClovaCall](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/ClovaCall) &emsp; [\<paper\>](https://arxiv.org/pdf/2004.09367.pdf)

### 학습 데이터
[AIHub 차량 내 대화 및 명령어 AI 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=112)


### 결과(시연) 화면
<div align="center">
 
<img src="https://user-images.githubusercontent.com/68505714/220413066-cb517248-b008-4ab5-92c8-c9e2a8561681.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413072-69444049-7d64-463a-8b07-284c8125f03a.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413075-4b5b556e-a368-49ad-808b-3f94992c8325.png" width="30%" height="30%"/>
</div>


### 성능

- 노이즈에 따른 CER

||Clova Call(pre trained)|YAMMY|
|:---|:---:|:---:|
|---|---|---|
|Noisy Data|||
|Clean Data|||

- 화자에 따른 CER

||Clova Call(pre trained)|YAMMY|
|:---|:---:|:---:|
|여자|||
|남자|||
|20 ~ 29세|||
|30 ~ 39세|||
|40 ~ 49세|||
|50 ~ 59세|||

- 노이즈 종류에 따른 CER

||Clova Call(pre trained)|YAMMY|
|:---|:---:|:---:|
|저속|||
|중속|||
|고속|||
|정차|||
|후진|||
|공조 X|||
|공조 O|||
|후진경고음|||
|고속도로|||
|일반도로|||
