<div align="center">
 
<img width="100%" height="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2&height=200&section=header&animation=fadeIn&fontAlignY=40&text=Y%20A%20M%20M%20Y&fontSize=75" alt="header" />
</div>

<h3 align="center">π₯ Yonsei Ai with hyundai Mobis MobilitY π₯</h3>

<h4 align="center">β¨ Contributors β¨</h4>
<p align="center">
<a href="https://github.com/ori-orori"><b>π KIM GUNHA</b></a><br>
<a href="https://github.com/etoilekim"><b>βοΈ KIM NAMHOON</b></a><br>
<a href="https://github.com/0601p"><b>π PARK MINSU</b></a><br>
<a href="https://github.com/SUNGBEOMCHOI"><b>π CHOI SUNGBEOM</b></a>
</p>

<br>

<hr>

### λͺ¨λΉλ¦¬ν° μ΅μ ν Speech Recognition

#### μ°λ¦¬ νλ§μ ν΅μ¬ ν¬μΈνΈ

1. λ€λ₯Έ μ°¨λμ© μμ±μΈμ μλ£¨μλ³΄λ€ λ λ°μ΄λ μΈμλ₯ μ λ³΄μ¬μ€λ€
2. μ°¨λλ§λ€ λΈμ΄μ¦(μ°¨μ’, μλ, μ£Όμ°¨μν©)μ λ¨λλΈμμ λ°μ΄ν°λ₯Ό λͺ¨λ νμ΅ν λͺ¨λΈ
3. μ€μ  μλμ°¨μμ μ¬μ©λλ μ΄νλ€μ λν΄μ μ§μ€μ μΌλ‘ νμ΅νμλ€.

#### νλ‘μ νΈ κ°μ

- νλ‘μ νΈ κΈ°ν λ°°κ²½ λ° λͺ©μ 
    - μ°¨λλ΄μμ λ°μνλ λ€μν μμμ λν΄μ μμ μ±μ λ³΄μ΄λ μμ±μΈμ λͺ¨λΈ κ°λ°
- κ°λ° νκ²½ λ° μΈμ΄
    - Pipeline : <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white" />
    - [Front-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/frontend/mobis_hackathon) : <img src="https://img.shields.io/badge/Flutter-02569B?style=flat&logo=Flutter&logoColor=white" />
    - [Back-end](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/backend) : <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white" />

#### νλ‘μ νΈ νλ‘μΈμ€
<div align="center">

![pipeline](https://user-images.githubusercontent.com/63270534/220610742-bf791ac6-1f79-41f6-9aa8-b60c1f605745.png)
</div>

- Pre Processing
- [Wavenet](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/WaveNet_PyTorch) &emsp; [\<paper\>](https://github.com/drethage/speech-denoising-wavenet)
- [LAS](https://github.com/SUNGBEOMCHOI/YAMMY/tree/main/ClovaCall) &emsp; [\<paper\>](https://arxiv.org/abs/1508.01211)

#### νμ΅ λ°μ΄ν°
- [AIHub νκ΅­μ΄ μμ± λ°μ΄ν°](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)
- [AIHub μ°¨λ λ΄ λν λ° λͺλ Ήμ΄ AI λ°μ΄ν°](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=112)


#### κ²°κ³Ό(μμ°) νλ©΄
<div align="center">
 
<img src="https://user-images.githubusercontent.com/68505714/220413066-cb517248-b008-4ab5-92c8-c9e2a8561681.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413072-69444049-7d64-463a-8b07-284c8125f03a.png" width="30%" height="30%"/>&emsp;&emsp;<img src="https://user-images.githubusercontent.com/68505714/220413075-4b5b556e-a368-49ad-808b-3f94992c8325.png" width="30%" height="30%"/>
</div>


https://user-images.githubusercontent.com/63270534/220625030-be277b9d-d4be-4c10-bc38-85ed1a8b5c49.mp4


#### μ±λ₯

- λΈμ΄μ¦μ λ°λ₯Έ CER(%)

||Clova API|YAMMY|
|:---|:---:|:---:|
|Noisy Data|29.20|17.8|

- νμμ λ°λ₯Έ CER(%)

||LAS(pre trained)|       YAMMY       |
|:---|:---:|:---:|
|μ¬μ|128.86|16.01|
|λ¨μ|114.18|23.88|
|20 ~ 29μΈ|124.79|21.04|
|30 ~ 39μΈ|126.69|23.12|
|40 ~ 49μΈ|93.65|12.95|
|50 ~ 59μΈ|98.89|19.13|
|60 ~ 69μΈ|181.72|16.38|

- λΈμ΄μ¦ μ’λ₯μ λ°λ₯Έ CER(%)

||LAS(pre trained)|YAMMY|
|:---|:---:|:---:|
|κ³ μ|92.40|21.02|
|μ€μ|90.02|15.96|
|μ μ|94.20|21.45|
|μ μ°¨|87.07|16.61|
|νμ§|102.68|23.37|
|κ³΅μ‘°μ₯μΉ MAX|96.23|21.02|
|κ³΅μ‘°μ₯μΉ MID|90.15|15.96|
|κ³΅μ‘°μ₯μΉ MIN|90.07|20.93|
|νμ§κ²½κ³ μ|110.49|24.83|


<br>

<hr>

<img width="100%" height="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2&height=200&section=footer&animation=fadeIn" alt="header" />
</div>
