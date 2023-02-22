import sys
sys.path.append('/root/WaveNet_PyTorch')

import torch
import torchaudio
import data.wavenet.denoise as denoise
import data.wavenet.models as models
import data.wavenet.util as util
import json
import os

class Denoise_Model:
    def __init__(self):

        self.config_path = '/root/WaveNet_PyTorch/data/wavenet/config.json'
        self.load_checkpoint='/root/WaveNet_PyTorch/data/NSDTSEA/checkpoints1/config1_epoch0317.pth'
        self.condition_value=0
        self.batch_size=1
        self.target_field_length=None

    def get_config(self, config_filepath):
        try:
            config_file = open(config_filepath, 'r')
        except IOError:
            print('No readable config file at path: ' + config_filepath)
            exit()
        else:
            with config_file:
                return json.load(config_file)

    def get_model(self, config):
        model = models.DenoisingWavenet(config, target_field_length=self.target_field_length)
        predict_config = models.PredictConfig(model, self.load_checkpoint)
        return predict_config

    def open_audio(self, audio_path):
        noisy, srn = torchaudio.load(audio_path)
        noisy = torchaudio.functional.resample(noisy, orig_freq=srn, new_freq=16000)

        if(noisy.size(0) != 1):
            noisy = noisy.mean(dim=0).view(1, -1)
        
        noisy = noisy.squeeze().numpy()
		
        return noisy

    def denoise_noisy_voice(self, audio_path):
        config = self.get_config(self.config_path)
        noisy = self.open_audio(audio_path)
        predict_config = self.get_model(config)
        inputs = {'noisy': noisy, 'clean': None}
        condition_input = util.binary_encode(int(self.condition_value), 29)[0]
        
        
        # new_path = audio_path.replace("noise", "denoise")
        new_path = audio_path.replace("preprocess", "denoise")
        paths = new_path.split('/')
        
        output_filename_prefix = paths[-1][:-4]

        output_folder_path = ''
        
        for p in paths[:-1]:
            output_folder_path = os.path.join(output_folder_path, p)
        output_folder_path = '/' + output_folder_path

        denoise.denoise_sample(predict_config, inputs, condition_input, self.batch_size, 
            output_filename_prefix, config['dataset']['sample_rate'], output_folder_path)



if __name__ == "__main__":
    a = Denoise_Model()
    a.denoise('/root/WaveNet_PyTorch/_0180-149-04-01-LMH-M-05-A_noisy_6dB.wav')


