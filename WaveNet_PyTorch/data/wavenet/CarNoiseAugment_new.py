import torch
import torchaudio
import numpy
import os
import json
import random
import numpy as np
import librosa
import time


class CarNoiseAugment:
    def __init__(self, data_dir_path = "/root/data/aihub_car/data/", json_file_path = "/root/data/aihub_car/scripts/noise.json") -> None:
        """
            args:
                data_dir_path : data 폴더의 경로, 아마 /root/data/aihub_car/data 가 될 것 하위 폴더에 noise 폴더가 있어야함
                json_file_path : noise.json 파일의 경로, 아마"/root/data/aihub_car/scripts/noise.json"가 될 것
        """
        print("loading noise")
        with open(json_file_path, 'r') as f:
            self.noise = json.load(f)
        self.path = data_dir_path
        self.noise_len = len(self.noise)
    
    def __call__(self, voice_path, voice_max_len, snr = 10, save_file = False):
        """
            args:
                voice_path = 목소리 파일의 경로 << 이것은 절대경로여야 함
                origin_rate = 목소리 파일의 크기를 얼마로 조절할 것인지, 1이면 원래 소리 그대로
                noise_rate = 노이즈 파일의 크기를 얼마로 조절할 것인지, 1이면 원래 소리 그대로
                save_file = True이면 파일들을 저장
        """
        voice, srv = torchaudio.load(voice_path)
        voice = torchaudio.functional.resample(voice, orig_freq=srv, new_freq=16000)
        # voice, _ = librosa.load(voice_path, sr=16000)


        # 혹시라도 노이즈보다 보이스가 길 경우 계속 찾는다.
        cnt = 0
        while(True):
            noise_idx = random.randint(0, self.noise_len)
            try:
                noise, srn = torchaudio.load(os.path.join(self.path, self.noise[noise_idx]["wav"]))
                noise = torchaudio.functional.resample(noise, orig_freq=srn, new_freq=16000)

                # noise, _ = librosa.load(os.path.join(self.path, self.noise[noise_idx]["wav"]), sr=16000)

                if(noise.size(1) > voice_max_len):
                    break
            except:
                pass
            cnt += 1
            if(cnt >= 100):
                raise NotImplementedError # 목소리가 너무 길 때 충분히 긴 노이즈를 찾을 수 없으면 오류
        
        #multi channel일 때 단일 채널로 정리
        if(voice.size(0) != 1):
            voice = voice.mean(dim=0).view(1, -1)
        if(noise.size(0) != 1):
            noise = noise.mean(dim=0).view(1, -1)
        

        voice = voice.squeeze().numpy()
        noise = noise.squeeze().numpy()

        
        # if voice.size < voice_max_len:
        #     zero_padding = np.zeros(voice_max_len-voice.size)
        #     voice = np.concatenate((voice, zero_padding))
        # else:
        #     voice = voice[:voice_max_len]
        if voice.size >= voice_max_len:
            voice = voice[:voice_max_len]
        
        clean_rate, noise_rate, noise_str_idx = self.cal_ratio(voice, noise, snr)

        # noise와 voice 더하기
        noisy = (voice*clean_rate) + (noise[noise_str_idx:noise_str_idx + voice.size] * noise_rate)
        


        # rms_noise = util.rms(noise)


        # rms_clean = util.rms(valid_clean_signal)
        # rms_noise_out = util.rms(noise_in_denoised_output)
        # rms_noise_in = util.rms(inputs['noise'])
        # print('rms_noise_out', rms_noise_out, 'rms_noise_in', rms_noise_in)

        # new_snr_db = int(np.round(util.snr_db(rms_clean, rms_noise_out)))
        # initial_snr_db = int(np.round(util.snr_db(rms_clean, rms_noise_in)))



        # 파일 저장
        if save_file:
            save_path = self.path + "/noise_added/"
            i = 0
            while(True): # 파일들이 이미 있는 경우, 하나씩 있는지 확인하며 파일이름 찾기
                filepath = save_path + "generated_" + i + ".wav"
                if not os.path.isfile(filepath):
                    torchaudio.save(filepath, voice, 16000)
                    break
                i += 1



        # voice = voice.squeeze().numpy() # numpy로 리턴
        return voice, noisy
    

    def cal_ratio(self, signal, noise, snr):
        """
        signal(numpy) : clean audio sequence
        noise(numpy) : noise audio sequence
        snr(int) : desired snr
        

        return
        clean ratio(float)
        noise ratio(float)
        """

        # if the audio is longer than the noise
        # play the noise in repeat for the duration of the audio
        while True:
            noise_str_idx = random.randint(0, noise.size-signal.size)
            noise = noise[noise_str_idx:noise_str_idx + signal.size]
            noise_energy = np.mean(noise**2)
            if noise_energy != 0:
                break

        # get the initial energy for reference
        signal_energy = np.mean(signal**2)
        noise_energy = np.mean(noise**2)
        # calculates the gain to be applied to the noise 
        # to achieve the given SNR
        g = np.sqrt(10.0 ** (-snr/10) * signal_energy / noise_energy)
        
        # Assumes signal and noise to be decorrelated
        # and calculate (a, b) such that energy of 
        # a*signal + b*noise matches the energy of the input signal
        clean_rate = np.sqrt(1 / (1 + g**2))
        noise_rate = np.sqrt(g**2 / (1 + g**2))

        # mix the signals
        return clean_rate, noise_rate, noise_str_idx