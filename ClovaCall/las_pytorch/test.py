import sys
sys.path.append('/root/ClovaCall/las_pytorch')

import math

import yaml
import numpy as np
import scipy
import librosa
import torch
import torch.nn as nn
import torchaudio

import label_loader
from ClovaCall.las_pytorch.CarNoiseAugment import CarNoiseAugment
from models import EncoderRNN, DecoderRNN, Seq2Seq

class STT_Model:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cuda = cfg['cuda']
        self.model_path = self.cfg['model_path']
        self.labels_path = self.cfg['labels_path']

        self.sample_rate = self.cfg['sample_rate']
        self.window_size = self.cfg['window_size']
        self.window_stride = self.cfg['window_stride']
        
        self.max_len = self.cfg['max_len']
        self.dropout = self.cfg['dropout']
        self.rnn_type = self.cfg['rnn_type']
        self.bidirectional = self.cfg['bidirectional']
        self.encoder_size = self.cfg['encoder_size']
        self.decoder_size = self.cfg['decoder_size']
        self.encoder_layers = self.cfg['encoder_layers']
        self.decoder_layers = self.cfg['decoder_layers']

        self.load_audio = CarNoiseAugment()

        self.device = torch.device('cuda:0' if self.cuda else 'cpu')

        char2index, self.index2char = label_loader.load_label_json(self.labels_path)
        self.SOS_token = char2index['<s>']
        self.EOS_token = char2index['</s>']

        self.audio_conf = dict(sample_rate=self.sample_rate,
                        window_size=self.window_size,
                        window_stride=self.window_stride)

        input_size = int(math.floor((self.sample_rate * self.window_size) / 2) + 1)
        self.enc = EncoderRNN(input_size, self.encoder_size, n_layers=self.encoder_layers,
                            dropout_p=self.dropout, bidirectional=self.bidirectional, 
                            rnn_cell=self.rnn_type, variable_lengths=False)

        self.dec = DecoderRNN(len(char2index), self.max_len, self.decoder_size, self.encoder_size,
                            self.SOS_token, self.EOS_token,
                            n_layers=self.decoder_layers, rnn_cell=self.rnn_type, 
                            dropout_p=self.dropout, bidirectional_encoder=self.bidirectional)


        self.model = Seq2Seq(self.enc, self.dec)

        # print("Loading checkpoint model %s" % self.model_path)
        state = torch.load(self.model_path)
        self.model.load_state_dict(state['model'])
        # print('Model loaded')

        self.model = self.model.to(self.device)
        self.model.eval()

        # print(self.model)
        # print("Number of parameters: %d" % Seq2Seq.get_param_size(self.model))
        print('Speech Recognition Model loaded')

    def generate_noisy_voice(self, audio_path):
        file_path = audio_path.replace("raw", "noise")
        audio = self.load_audio(audio_path)
        torchaudio.save(file_path, torch.Tensor(audio).view(1, -1), 16000)

    def parse_audio(self, audio_path):
        y = self.load_audio(audio_path, noise_rate = 0.0)
        n_fft = int(self.audio_conf['sample_rate'] * self.audio_conf['window_size'])
        window_size = n_fft
        stride_size = int(self.audio_conf['sample_rate'] * self.audio_conf['window_stride'])

        # STFT
        D = librosa.stft(y, n_fft=n_fft, hop_length=stride_size, win_length=window_size, window=scipy.signal.hamming)
        spect, phase = librosa.magphase(D)

        # S = log(S+1)
        spect = np.log1p(spect)
        mean = np.mean(spect)
        std = np.std(spect)
        spect -= mean
        spect /= std

        spect = torch.FloatTensor(spect)

        return spect

    def speech_to_text(self, audio_path):
        with torch.no_grad():
            feats = self.parse_audio(audio_path)
            feats = feats.unsqueeze(0).unsqueeze(0)
            feats = feats.to(self.device)

            feat_lengths = [feats[0].size(2)]
            feat_lengths = torch.IntTensor(feat_lengths)
            feat_lengths = feat_lengths.to(self.device)

            logit = self.model(feats, feat_lengths, None, teacher_forcing_ratio=0.0)
            logit = torch.stack(logit, dim=1).to(self.device)
            y_hat = logit.max(-1)[1]
            hyp = self.label_to_string(y_hat[0])
            return hyp


    def label_to_string(self, labels):
        if len(labels.shape) == 1:
            sent = str()
            for i in labels:
                if i.item() == self.EOS_token:
                    break
                sent += self.index2char[i.item()]
            return sent

        elif len(labels.shape) == 2:
            sents = list()
            for i in labels:
                sent = str()
                for j in i:
                    if j.item() == self.EOS_token:
                        break
                    sent += self.index2char[j.item()]
                sents.append(sent)

            return sents

if __name__ == "__main__":
    sr_cfg_path = "/root/ClovaCall/config.yaml"
    with open(sr_cfg_path) as f:
        sr_cfg = yaml.safe_load(f)
    sr_model = STT_Model(sr_cfg)
    audio_path = "/root/data/aihub_car/data/train/AI비서/EB_0166/EB_0166-2501-04-01-KSH-F-07-A.wav"
    sr_model.speech_to_text(audio_path)