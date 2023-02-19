import os
import sys
sys.path.append('/root')

import yaml
from django.apps import AppConfig
from ClovaCall.las_pytorch.test import STT_Model


class HackathonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hackathon'

    sr_cfg_path = "/root/ClovaCall/config.yaml"
    with open(sr_cfg_path) as f:
        sr_cfg = yaml.safe_load(f)
    sr_model = STT_Model(sr_cfg)

    