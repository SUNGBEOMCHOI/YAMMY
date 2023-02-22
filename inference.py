import argparse
import yaml

from ClovaCall.las_pytorch.test import STT_Model
from WaveNet_PyTorch.wavenet_model import Denoise_Model
from preprocessing.preprocessing import Preprocessing_Model



class YAMMY:
    def __init__(self, cfg):

        denoise_cfg = cfg['denoise_model']
        sr_cfg = cfg['sr_model']

        # preprocess model 불러오기
        self.preprocess_model = Preprocessing_Model(side_remover=False, silence_remover=False, white_noise=False, BPF=False, noise_reduction=False)
        self.denoise_model = Denoise_Model()
        self.sr_model = STT_Model(sr_cfg)


    def __call__(self, file_path):
        
        self.preprocess_model.get_result(file_path)
        preprocess_file_path =file_path.replace('.wav', '_preprocess.wav')
        
        self.denoise_model.denoise_noisy_voice(preprocess_file_path)
        denoise_file_path = file_path.replace('.wav', '_denoise.wav')
        
        text = self.sr_model.speech_to_text(denoise_file_path)
        # print("Speech Recogtion Result : ", text)
        return text



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='./inference_config.yaml', help='Path to config file')
    parser.add_argument('--audio_path', type=str, default='./data/aihub_car/data/validation/test.wav', help='Path to audio file for inference')
    
    args = parser.parse_args()
    cfg_path = args.config
    file_path = args.audio_path
    
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    model = YAMMY(cfg)
    text = model(file_path)