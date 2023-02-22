from pydub import AudioSegment
import pydub.scipy_effects


low_cutoff_freq = 300
high_cutoff_freq = 3000

#path = '/root/preprocessing/voice_cut/EA_0180-38-04-01-LMH-M-05-A.wav'
path = 'C:/Users/Etoile/Desktop/preprocessing/preprocessed.wav'

sound = AudioSegment.from_file(path, format='wav')

BPF_sound = AudioSegment.band_pass_filter(sound, low_cutoff_freq, high_cutoff_freq, order=5)

BPF_sound.export(path, format="wav")