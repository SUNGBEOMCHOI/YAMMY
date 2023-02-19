import os
import math
import torch
import librosa
import numpy as np
import scipy.signal
import random

from data.base_dataset import BaseDataset
from data.audio_folder import make_dataset
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.sampler import Sampler
from data.CarNoiseAugment import CarNoiseAugment


class SpectogramDataset(BaseDataset):

    def __init__(self, opt, normalize=False):
        BaseDataset.__init__(self, opt)
        self.dir_A = os.path.join(opt.dataroot, 'aihub_car/scripts/new_all_train.json')  # create a path '/path/to/data/trainA'  
        self.dir_B = os.path.join(opt.dataroot, 'aihub_car/scripts/new_all_train.json')  # create a path '/path/to/data/trainB'

        self.A_paths = sorted(make_dataset(self.dir_A, opt.max_dataset_size))   # load images from '/path/to/data/trainA audio파일 path가 담긴 list'
        self.B_paths = sorted(make_dataset(self.dir_B, opt.max_dataset_size))    # load images from '/path/to/data/trainB'
        self.A_size = len(self.A_paths)  # get the size of dataset A
        self.B_size = len(self.B_paths)  # get the size of dataset B
        self.aug = CarNoiseAugment()

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index (int)      -- a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor)       -- an image in the input domain
            B (tensor)       -- its corresponding image in the target domain
            A_paths (str)    -- image paths
            B_paths (str)    -- image paths
        """
        A_path = self.A_paths[index % self.A_size]  # make sure index is within then range
        if self.opt.serial_batches:   # make sure index is within then range
            index_B = index % self.B_size
        else:   # randomize the index for domain B to avoid fixed pairs.
            index_B = random.randint(0, self.B_size - 1)
        B_path = self.B_paths[index_B]


        # dataloader에 넣기 위한 A_path와 B_path 파일의 전처리 실행
        # A와 B가 transform을 거친 최종 결과
        A = self.parse_audio(A_path, aug=True)
        B = self.parse_audio(B_path, aug=False)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path}

    def parse_audio(self, audio_path, aug=False):
        y = self.load_audio(audio_path, aug)


        n_fft = int(self.opt.sample_rate * self.opt.window_size)
        window_size = n_fft
        stride_size = int(self.opt.sample_rate * self.opt.window_stride)


        # STFT
        spect = librosa.stft(y, n_fft=n_fft, hop_length=stride_size, win_length=window_size, window=scipy.signal.hamming)
        # spect, phase = librosa.magphase(D)
        # S = log(S+1)
        # spect = np.log1p(spect)
        if self.opt.audio_normalize:
            mean = np.mean(spect)
            std = np.std(spect)
            spect -= mean
            if std == 0:
                spect /= 1e-6
            else:
                spect /= std

        spect = torch.FloatTensor(spect)
        # print('final spect shape:', spect.shape)
        return spect
    
    def load_audio(self, path, aug):
        sound = self.aug(path, self.opt.audio_max_length, noise_rate = 1 if aug else 0)
        # else:
        #     sound = np.memmap(path, dtype='h', mode='r')  #len가 60,000에 1초정도라고 생각하면 된다 정확한 값은 아님
        #     sound = sound.astype('float32') / 32767
        #     assert len(sound)
            

        #     sound = torch.from_numpy(sound).view(-1, 1).type(torch.FloatTensor)
        #     sound = sound.numpy()

        #     if len(sound.shape) > 1:
        #         if sound.shape[1] == 1:
        #             sound = sound.squeeze()
        #         else:
        #             sound = sound.mean(axis=1)  # multiple channels, average


        #make sound length constantly

        # max_sound_len = self.opt.audio_max_length
        # if len(sound) < max_sound_len:
        #     zero_padding = np.zeros(shape = (max_sound_len-len(sound),))
        #     sound = np.concatenate((sound, zero_padding))
        # else:
        #     sound = sound[:max_sound_len]

        return sound


    def __len__(self):
        """Return the total number of images in the dataset.

        As we have two datasets with potentially different number of images,
        we take a maximum of
        """
        return max(self.A_size, self.B_size)



# class SpectrogramDataset(Dataset):
#     def __init__(self, audio_conf, dataset_path, data_list, char2index, sos_id, eos_id, normalize=False):
#         super(SpectrogramDataset, self).__init__()
#         """
#         Dataset loads data from a list contatining wav_name, transcripts, speaker_id by dictionary.
#         :param audio_conf: Dictionary containing the sample rate, window and the window length/stride in seconds.
#         :param data_list: List of dictionary. key : "wav", "text", "speaker_id"
#         :param char2index: Dictionary mapping character to index value.
#         :param sos_id: Start token index.
#         :param eos_id: End token index.
#         :param normalize: Normalized by instance-wise standardazation.
#         """
#         self.audio_conf = audio_conf
#         self.data_list = data_list
#         self.size = len(self.data_list)
#         self.char2index = char2index
#         self.sos_id = sos_id
#         self.eos_id = eos_id
#         self.PAD = 0
#         self.normalize = normalize
#         self.dataset_path = dataset_path

#     def __getitem__(self, index):
#         wav_name = self.data_list[index]['wav']
#         audio_path = os.path.join(self.dataset_path, wav_name)
        
#         transcript = self.data_list[index]['text']
#         spect = self.parse_audio(audio_path)
#         transcript = self.parse_transcript(transcript)
#         return spect, transcript

#     def parse_audio(self, audio_path):
#         y = load_audio(audio_path)

#         n_fft = int(self.audio_conf['sample_rate'] * self.audio_conf['window_size'])
#         window_size = n_fft
#         stride_size = int(self.audio_conf['sample_rate'] * self.audio_conf['window_stride'])

#         # STFT
#         D = librosa.stft(y, n_fft=n_fft, hop_length=stride_size, win_length=window_size, window=scipy.signal.hamming)
#         spect, phase = librosa.magphase(D)

#         # S = log(S+1)
#         spect = np.log1p(spect)
#         if self.normalize:
#             mean = np.mean(spect)
#             std = np.std(spect)
#             spect -= mean
#             spect /= std

#         spect = torch.FloatTensor(spect)

#         return spect

#     def parse_transcript(self, transcript):
#         transcript = list(filter(None, [self.char2index.get(x) for x in list(transcript)]))
#         transcript = [self.sos_id] + transcript + [self.eos_id]
#         return transcript

#     def __len__(self):
#         return self.size


# def _collate_fn(batch):
#     def seq_length_(p):
#         return p[0].size(1)
#     def target_length_(p):
#         return len(p[1])

#     batch = sorted(batch, key=lambda sample: sample[0].size(1), reverse=True)
#     seq_lengths    = [s[0].size(1) for s in batch]
#     target_lengths = [len(s[1]) for s in batch]

#     max_seq_size = max(seq_lengths)
#     max_target_size = max(target_lengths)

#     feat_size = batch[0][0].size(0)
#     batch_size = len(batch)

#     seqs = torch.zeros(batch_size, 1, feat_size, max_seq_size)
#     targets = torch.zeros(batch_size, max_target_size).to(torch.long)

#     for x in range(batch_size):
#         sample = batch[x]
#         tensor = sample[0]
#         target = sample[1]
#         seq_length = tensor.size(1)
#         seqs[x][0].narrow(1, 0, seq_length).copy_(tensor)
#         targets[x].narrow(0, 0, len(target)).copy_(torch.LongTensor(target))

#     seq_lengths = torch.IntTensor(seq_lengths)
#     return seqs, targets, seq_lengths, target_lengths


# class AudioDataLoader(DataLoader):
#     def __init__(self, *args, **kwargs):
#         super(AudioDataLoader, self).__init__(*args, **kwargs)
#         self.collate_fn = _collate_fn


# class BucketingSampler(Sampler):
#     def __init__(self, data_source, batch_size=1):
#         """
#         Samples batches assuming they are in order of size to batch similarly sized samples together.
#         """
#         super(BucketingSampler, self).__init__(data_source)
#         self.data_source = data_source
#         ids = list(range(0, len(data_source)))
#         self.bins = [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

#     def __iter__(self):
#         for ids in self.bins:
#             np.random.shuffle(ids)
#             yield ids

#     def __len__(self):
#         return len(self.bins)

#     def shuffle(self, epoch):
#         np.random.shuffle(self.bins)