# Import required libraries
from pydub.silence import split_on_silence
from pydub import AudioSegment, effects 
from scipy.io.wavfile import read, write
import numpy as np
# Pass audio path
# path ='/root/preprocessing/voice_cut/EA_0180-38-04-01-LMH-M-05-A.wav'

class silence_remover:
    def __init__(self, path):
        self.path = path
        

    def remove(self, min_silence_len = 20, silence_thresh = -30, keep_silence = 100, ):
        rate, audio = read(self.path)        
        aud = AudioSegment(audio.tobytes(),frame_rate = rate, sample_width = audio.dtype.itemsize,channels = 1)
        audio_chunks = split_on_silence(aud, min_silence_len = min_silence_len, silence_thresh = silence_thresh, keep_silence = keep_silence)

        #audio chunks are combined here
        audio_processed = sum(audio_chunks)
        audio_processed = np.array(audio_processed.get_array_of_samples())
        
        return audio_processed, rate

# audio_processed, rate = silence_remover(path).remove()
# write("/root/preprocessing/voice_cut/removed_silence.wav", rate, audio_processed)

