# Loading the Libraries
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt

path = '/root/preprocessing/voice_cut/EA_0180-38-04-01-LMH-M-05-A.wav'
path2 = '/root/preprocessing/voice_cut/removed_silence.wav'
# Read the Audiofile
samplerate, data = read(path)
# Frame rate for the Audio
print(samplerate)

# Duration of the audio in Seconds
duration = len(data)/samplerate
#print("Duration of Audio in Seconds", duration)
#print("Duration of Audio in Minutes", duration/60)

time = np.arange(0,duration,1/samplerate)

# Plotting the Graph using Matplotlib
plt.subplot(2,1,1)
plt.plot(time[:-1],data)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('original')

samplerate2, data2 = read(path2)
# Frame rate for the Audio
print(samplerate2)

# Duration of the audio in Seconds
duration2 = len(data2)/samplerate2
#print("Duration of Audio in Seconds", duration)
#print("Duration of Audio in Minutes", duration/60)

time2 = np.arange(0,duration2,1/samplerate2)

plt.subplot(2,1,2)
plt.plot(time2,data2)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('silence removed')

#plt.savefig(path+'.jpg')
plt.tight_layout()
plt.savefig('compared.jpg')
plt.show()