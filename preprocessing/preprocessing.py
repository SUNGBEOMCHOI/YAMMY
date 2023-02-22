import sys
sys.path.append('/root/preprocessing')

import pydub
from pydub import AudioSegment
from add_white_noise import WhiteNoise
import noisereduce as nr
from Silence_Remover import silence_remover
from pydub.silence import split_on_silence, detect_leading_silence
from scipy.io.wavfile import read, write
import numpy as np
import pydub.scipy_effects
import shutil

# import math
# import time


#original_path = 'C:/Users/Etoile/Desktop/EA_0180-38-04-01-LMH-M-05-A.wav'
# original_path = 'C:/Users/Etoile/Desktop/preprocessed.wav'
# path = 'C:/Users/Etoile/Desktop/preprocessing/preprocessed.wav'

#original path = 원래 파일이 있는 위치
#path = 새롭게 파일을 저장할 위치
#side remover = 음원의 처음과 끝쪽의 무음 구간을 잘라주는 함수, boolean
#silence_remover = 음원의 모든 구간의 무음 구간을 잘라주는 함수, boolean
#white_noise = 음원에 white noise를 추가해주는 함수, boolean
#BPF = Band Pass Filter를 이용해 음원을 필터링 해주는 함수, boolean
#noise_reduction = noise reduction library를 이용해 음원을 필터링하는 함수, boolean
class Preprocessing_Model():
    def __init__(self, side_remover=False, silence_remover=False, white_noise=False, BPF=False, noise_reduction=False):
        self.side_remover = side_remover
        self.silence_remover = silence_remover
        self.white_noise = white_noise
        self.BPF = BPF
        self.noise_reduction = noise_reduction

    def get_result(self, origin_path):
        # path = origin_path.replace('raw', 'preprocess')
        # self.path = origin_path.replace('noise', 'preprocess')
        self.path = origin_path.replace('.wav', '_preprocess.wav')
        shutil.copy(origin_path, self.path)
        sound = AudioSegment.from_file(self.path, format='wav')

        if self.side_remover is True:
            sound = filters(self.path).Side_Remover()
        if self.silence_remover is True:
            sound = filters(self.path).Silence_Remover()        
        if self.white_noise is True:
            sound = filters(self.path).White_Noise()
        if self.BPF is True : 
            sound = filters(self.path).Band_Pass_Filter()
        if self.noise_reduction is True:
            sound = filters(self.path).Noise_Reduce()

        return sound
        

class filters():
    def __init__(self, path):
        super().__init__()
        sound = AudioSegment.from_file(path, format='wav')
        self.sound = sound
        self.path = path
        rate, data = read(self.path)
        self.rate = rate
        self.data = data 

    def White_Noise(self):
        sound = self.sound
        noise = WhiteNoise().to_audio_segment(duration=len(sound))
        combined = sound.overlay(noise)
        combined.export(self.path, format="wav")

        return combined
    
    def Band_Pass_Filter(self, low_cutoff_freq = 250, high_cutoff_freq = 3300):
        sound = self.sound
        BPF_sound = AudioSegment.band_pass_filter(sound, low_cutoff_freq, high_cutoff_freq, order=11)
        BPF_sound.export(self.path, format="wav")
        return BPF_sound
    
    def Side_Remover(self, threshold = -30, chunk_size = 10):
        sound = self.sound
        start_trim = detect_leading_silence(sound, silence_threshold = threshold)
        end_trim = detect_leading_silence(sound.reverse(), silence_threshold = threshold)
        duration = len(sound)   

        start_trim_control = 100
        end_trim_control = 100
        
        if start_trim - start_trim_control > 0:
            start_controlled = start_trim - start_trim_control
        else: start_controlled = 0
        if end_trim - end_trim_control > 0:
            end_controlled = end_trim - end_trim_control    
        else: end_controlled = 0

        end_controlled = end_trim - end_trim_control
        trimmed_sound = sound[start_controlled:duration-end_controlled]
        trimmed_sound.export(self.path, format="wav")
        return trimmed_sound
    
    def Silence_Remover(self):
        audio_processed, rate = silence_remover(self.path).remove()
        write(self.path, rate, audio_processed)
        return audio_processed
    
    def Noise_Reduce(self):
        reduced_noise = nr.reduce_noise(y=self.data, sr=self.rate)
        write(self.path, self.rate, reduced_noise)
        return reduced_noise


side = True
silence = True
white = True
band = True
noise = True

if __name__ == "__main__":
    # start = time.time()
    a = preprocessing(original_path, path, white_noise=white, BPF=band, noise_reduction=noise, side_remover=side, silence_remover=silence).get_result()
    
    # end = time.time()
    # print(f"{end - start:.5f} sec")