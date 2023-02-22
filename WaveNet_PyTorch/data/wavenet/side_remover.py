from pydub import AudioSegment

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

path = '/root/preprocessing/voice_cut/EA_0180-38-04-01-LMH-M-05-A.wav'
sound = AudioSegment.from_file(path, format="wav")

start_trim = detect_leading_silence(sound)
end_trim = detect_leading_silence(sound.reverse())

duration = len(sound)   

start_trim_control = 100
end_trim_control = 100
start_controlled = start_trim - start_trim_control
end_controlled = end_trim - end_trim_control
trimmed_sound = sound[start_controlled:duration-end_controlled]
new_duration=duration-end_controlled-start_controlled
trimmed_sound.export("/root/preprocessing/voice_cut/sidecut.wav", format="wav")