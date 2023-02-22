# import librosa
# import torch
# import torchaudio
import pandas as pd
import pickle
from pydub import AudioSegment
import torchaudio
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import librosa.display
 
# shows the sound waves
def visualize(path1, path2, path3):
   
    # reading the audio file
    # raw = wave.open(path)

    voice1, srv = torchaudio.load(path1)
    voice1 = torchaudio.functional.resample(voice1, orig_freq=srv, new_freq=16000)
    voice2, srv = torchaudio.load(path2)
    voice2 = torchaudio.functional.resample(voice2, orig_freq=srv, new_freq=16000)
    voice3, srv = torchaudio.load(path3)
    voice3 = torchaudio.functional.resample(voice3, orig_freq=srv, new_freq=16000)

    if(voice1.size(0) != 1):
        voice1 = voice1.mean(dim=0).view(1, -1)
    if(voice2.size(0) != 1):
        voice2 = voice2.mean(dim=0).view(1, -1)
    if(voice3.size(0) != 1):
        voice3 = voice3.mean(dim=0).view(1, -1)
    
    voice1 = voice1.squeeze().numpy()
    voice2 = voice2.squeeze().numpy()
    voice3 = voice3.squeeze().numpy()

    for voice in [voice1, voice2, voice3]:
        mean = np.mean(voice)
        std = np.std(voice)
        voice -= mean
        voice /= std

    f_rate = 16000


    time = np.linspace(
        0, # start
        len(voice1) / f_rate,
        num = len(voice1)
    )
    plt.figure(figsize=(80,20))
    
    plt.subplot(3,1,1)
    plt.plot(time[5000:20000], voice1[5000:20000])
    plt.title('1st Graph')
    plt.ylabel('Damped oscillation')

    plt.subplot(3, 1, 2)                # nrows=2, ncols=1, index=2
    plt.plot(time[5000:20000], voice2[5000:20000])
    plt.title('2nd Graph')
    plt.xlabel('time (s)')
    plt.ylabel('Undamped')

    plt.subplot(3, 1, 3)                # nrows=2, ncols=1, index=2
    plt.plot(time[5000:20000], voice3[5000:20000])
    plt.title('3rd Graph')
    plt.xlabel('time (s)')
    plt.ylabel('Undamped')
     
        
    plt.show()
 
    plt.savefig('/root/WaveNet_PyTorch/data/NSDTSEA/samples_6/visualize.jpg')
 

def visualize2(path1, path2, path3):

    # clean data
    y, sr = librosa.load(path1)
    S = np.abs(librosa.stft(y))
    fig, ax = plt.subplots(3,1, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                            y_axis='log', x_axis='time', ax=ax[0])
    ax[0].set(title='Log-frequency power spectrogram')
    ax[0].label_outer()
    ax[0].set(ylabel='clean(Hz)')

    # noisy data
    y, sr = librosa.load(path2)
    S = np.abs(librosa.stft(y))
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                y_axis='log', x_axis='time', ax=ax[1])
    ax[1].label_outer()
    ax[1].set(ylabel='noisy')

    # denoised data
    y, sr = librosa.load(path3)
    S = np.abs(librosa.stft(y))
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                y_axis='log', x_axis='time', ax=ax[2])
    ax[2].label_outer()
    ax[2].set(ylabel='denoised')

    fig.colorbar(img, ax=ax, format="%+2.0f dB")

    plt.savefig('/root/WaveNet_PyTorch/data/NSDTSEA/samples_6/visualize2.jpg')


clean_path = '/root/WaveNet_PyTorch/data/NSDTSEA/samples/samples_2/_0180-230-04-01-LMH-M-05-A_clean.wav'
noisy_path = '/root/WaveNet_PyTorch/data/NSDTSEA/samples/samples_2/_0180-230-04-01-LMH-M-05-A_noisy_6dB.wav'
denoised_path = '/root/WaveNet_PyTorch/data/NSDTSEA/samples/samples_2/_0180-230-04-01-LMH-M-05-A_denoised_5dB.wav'


visualize2(clean_path, noisy_path, denoised_path)