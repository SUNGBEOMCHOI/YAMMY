import os
import sys
sys.path.append('/root')

import yaml
from django.apps import AppConfig
from ClovaCall.las_pytorch.test import STT_Model
# from unsup_speech_enh_adaptation.inference import Denoise_Model
from WaveNet_PyTorch.wavenet_model import Denoise_Model
from preprocessing.preprocessing import Preprocessing_Model


class HackathonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hackathon'

    sr_cfg_path = "/root/ClovaCall/config.yaml"
    with open(sr_cfg_path) as f:
        sr_cfg = yaml.safe_load(f)
    preprocess_model = Preprocessing_Model(side_remover=True, silence_remover=True, white_noise=True, BPF=False, noise_reduction=False)
    denoise_model = Denoise_Model()
    sr_model = STT_Model(sr_cfg)


    