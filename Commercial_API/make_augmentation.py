import os
import sys
sys.path.append('/root')

import torchaudio
import json
import requests
import Levenshtein as Lev 

from CarNoiseAugment import CarNoiseAugment
from ClovaCall.las_pytorch import label_loader

data_path = "/root/data/aihub_car/data/"
#directory_path_list = ['./validation/자율주행/EB_0850', './validation/AI비서/EA_0180', './validation/카투홈/EA_2070', './validation/홈투카/EB_2116']

directory_path_list = []
patha = os.listdir("/root/data/aihub_car/data/validation")
for a in patha:
    curpath = os.path.join("/root/data/aihub_car/data/validation", a)
    pathb = os.listdir(curpath)
    for b in pathb:
        path = os.path.join(curpath, b)
        directory_path_list.append(os.path.join("validation/",a, b))

directory_path_list.remove("validation/자율주행/noise.json")

# directory_path_list = ['./validation/AI비서/EA_0179']
target_json_path = "/root/data/aihub_car/scripts/clova_validation.json"
labels_path = "/root/ClovaCall/data/kor_syllable.json"

Lang = "Kor" # Kor / Jpn / Chn / Eng
URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang
    
ID = "sqpn9chmw2" # 인증 정보의 Client ID
Secret = "Y4KuJCpBbnq7DZk2fIunfpgxetvEalucmLH4TzIM" # 인증 정보의 Client Secret
    
headers = {
    "Content-Type": "application/octet-stream", # Fix   
    "X-NCP-APIGW-API-KEY-ID": ID,
    "X-NCP-APIGW-API-KEY": Secret,
}


char2index, index2char = label_loader.load_label_json(labels_path)
SOS_token = char2index['<s>']
EOS_token = char2index['</s>']
PAD_token = char2index['_']


def recognition_clova(path):
    data = open(path, "rb") # STT를 진행하고자 하는 음성 파일

    response = requests.post(URL,  data=data, headers=headers)
    rescode = response.status_code
    if(rescode == 200):
        return response.json()['text']
    else:
        print("Error : " + response.text)

def char_distance(ref, hyp):
    ref = ref.replace(' ', '') 
    hyp = hyp.replace(' ', '') 

    dist = Lev.distance(hyp, ref)
    length = len(ref.replace(' ', ''))

    return dist, length 

with open(target_json_path, "r", encoding='utf-8-sig') as f:
    target_json = json.load(f)

audio_load = CarNoiseAugment()
total_dist = 0
total_length = 0
for directory_path in directory_path_list:
    file_path_list = os.listdir(os.path.join(data_path, directory_path))
    for file_path in file_path_list[:10]:
        full_file_path = os.path.join(data_path, directory_path, file_path)
        audio = audio_load(full_file_path, origin_rate = 1, noise_rate = 1)
        os.makedirs(os.path.join("/root/data/aihub_car/data/validation_noisy", directory_path), exist_ok = True)
        torchaudio.save(os.path.join("/root/data/aihub_car/data/validation_noisy", directory_path, file_path), audio, 16000)

