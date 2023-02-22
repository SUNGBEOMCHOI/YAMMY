from pydub import AudioSegment
#from pydub.generators import WhiteNoise
#import utils
import random
import itertools
import array
FRAME_WIDTHS = {
    8: 1,
    16: 2,
    32: 4,
}
ARRAY_TYPES = {
    8: "b",
    16: "h",
    32: "i",
}
ARRAY_RANGES = {
    8: (-0x80, 0x7f),
    16: (-0x8000, 0x7fff),
    32: (-0x80000000, 0x7fffffff),
}
def db_to_float(db, using_amplitude=True):
    """
    Converts the input db to a float, which represents the equivalent
    ratio in power.
    """
    db = float(db)
    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)

def get_frame_width(bit_depth):
    return FRAME_WIDTHS[bit_depth]

def get_array_type(bit_depth, signed=True):
    t = ARRAY_TYPES[bit_depth]
    if not signed:
        t = t.upper()
    return t

def get_min_max_value(bit_depth):
    return ARRAY_RANGES[bit_depth]    

class SignalGenerator(object):
    def __init__(self, sample_rate=44100, bit_depth=16):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth

    def to_audio_segment(self, duration=1000.0, volume=0.0):
        """
        Duration in milliseconds
            (default: 1 second)
        Volume in DB relative to maximum amplitude
            (default 0.0 dBFS, which is the maximum value)
        """
        minval, maxval = get_min_max_value(self.bit_depth)
        sample_width = get_frame_width(self.bit_depth)
        array_type = get_array_type(self.bit_depth)

        gain = db_to_float(volume)
        sample_count = int(self.sample_rate * (duration / 1000.0))

        sample_data = (int(val * maxval * gain) for val in self.generate())
        sample_data = itertools.islice(sample_data, 0, sample_count)

        data = array.array(array_type, sample_data)
        
        try:
            data = data.tobytes()
        except:
            data = data.tostring()

        return AudioSegment(data=data, metadata={
            "channels": 1,
            "sample_width": sample_width,
            "frame_rate": self.sample_rate,
            "frame_width": sample_width,
        })

    def generate(self):
        raise NotImplementedError("SignalGenerator subclasses must implement the generate() method, and *should not* call the superclass implementation.")

class WhiteNoise(SignalGenerator):
    def generate(self):
        while True:
            yield ((random.random() * 2) - 1.0)*0.1

path = '/root/preprocessing/voice_cut/EA_0180-38-04-01-LMH-M-05-A.wav'

sound = AudioSegment.from_file(path, format='wav')
noise = WhiteNoise().to_audio_segment(duration=len(sound))

combined = sound.overlay(noise)

combined.export("/root/preprocessing/add_noise/white_noise_added.wav", format="wav")
