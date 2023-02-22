#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import sys
sys.path.append('/root/WaveNet_PyTorch')

import data.wavenet.util as util
import torch.utils.data as data
import os
import numpy as np
import torch
from data.wavenet.CarNoiseAugment_new import CarNoiseAugment
import json
from data.wavenet.audio_folder import make_dataset
import time
import random


# In[ ]:


class NSDTSEADataset(data.Dataset):

    def __init__(self, config, model):

        self.model = model
        self.path = config['dataset']['path']
        self.json_path = config['dataset']['json_path']
        self.sample_rate = config['dataset']['sample_rate']
        self.file_paths = {'train': {'clean': [], 'noisy': []}, 'test': {'clean': [], 'noisy': []}}
        self.sequences = {'train': {'clean': [], 'noisy': []}, 'test': {'clean': [], 'noisy': []}}
        self.voice_indices = {'train': [], 'test': []}
        self.regain_factors = {'train': [], 'test': []}
        self.speakers = {'train': [], 'test': []}
        self.speaker_mapping = {}
        self.batch_size = config['training']['batch_size']
        self.noise_only_percent = config['dataset']['noise_only_percent']
        self.regain = config['dataset']['regain']
        self.extract_voice = config['dataset']['extract_voice']
        self.in_memory_percentage = config['dataset']['in_memory_percentage']
        self.num_sequences_in_memory = 0
        self.condition_encode_function = util.get_condition_input_encode_func(config['model']['condition_encoding'])
        self.load_audio = CarNoiseAugment()
        self.sequence_max_len = config['dataset']['sequence_max_len']    
        self.sequence_min_len = config['dataset']['sequence_min_len']
        self.audio_paths = sorted(make_dataset(self.json_path, float("inf")))  

    def __getitem__(self, index):

        sample_snr = [0,5,10,15]
        snr = random.choice(sample_snr)

        while True:
            file_path = self.audio_paths[index]
            # clean data

            speech, noisy = self.load_audio(file_path, self.sequence_max_len, snr)
            if util.rms(speech) == 0:
                index = np.random.randint(0, len(self))
            else:
                regain_factors = self.regain / util.rms(speech)
                if self.extract_voice:
                    speech_onset_offset_indice = util.get_subsequence_with_speech_indices(speech)
                # noisy data
                noise = noisy - speech
                if self.extract_voice:
                    speech = speech[speech_onset_offset_indice[0]:speech_onset_offset_indice[1]]
                speech_regained = speech * regain_factors
                noise_regained = noise * regain_factors
                
                if len(speech_regained) < self.model.input_length:
                    index = np.random.randint(0, len(self))
                else:
                    break

        
        offset = np.squeeze(np.random.randint(0, len(speech_regained) - self.model.input_length, 1))
        speech_fragment = speech_regained[offset:offset + self.model.input_length]
        noise_fragment = noise_regained[offset:offset + self.model.input_length]
        Input = noise_fragment + speech_fragment
        output_speech = speech_fragment
        output_noise = noise_fragment
        if self.noise_only_percent > 0:
            if np.random.uniform(0, 1) <= self.noise_only_percent:
                Input = output_noise #Noise only
                output_speech = np.array([0] * self.model.input_length) #Silence
        # speaker에 따라 구분해주기
        condition_input = 0

        output_speech = output_speech[self.model.get_padded_target_field_indices()]
        output_noise = output_noise[self.model.get_padded_target_field_indices()]
        return {'data_input': Input.astype('float32'), 'condition_input': self.condition_encode_function(np.array(condition_input, dtype='uint8'), self.model.num_condition_classes)}, {
            'data_output_1': output_speech.astype('float32'), 'data_output_2': output_noise.astype('float32')}

    def __len__(self):
        return len(self.audio_paths)



    # def load_dataset(self):

    #     print('Loading NSDTSEA dataset...')

    #     for condition in ['clean', 'noisy']:
    #         # current_directory = os.path.join(self.path, condition + '_' + Set + 'set_wav')
            

    #         sequences, file_paths, speakers, speech_onset_offset_indices, regain_factors = self.load_directory(self.json_path, condition)

    #         self.file_paths[Set][condition] = file_paths
    #         self.speakers[Set] = speakers
    #         self.sequences[Set][condition] = sequences

    #         if condition == 'clean':
    #             self.voice_indices[Set] = speech_onset_offset_indices
    #             self.regain_factors[Set] = regain_factors
    #     return self

    # def load_directory(self, directory_path, condition):
    #     """
    #     directory path : clean data의 path
    #     """
    #     assert os.path.isfile(directory_path), '%s is not a valid directory' % directory_path

    #     with open(directory_path, 'r', encoding='utf-8-sig') as f:
    #         json_file = json.load(f)

    #     filenames=[]
    #     for fname in json_file:
    #         filenames.append(fname["wav"])

    #     speakers = []
    #     file_paths = []
    #     speech_onset_offset_indices = []
    #     regain_factors = []
    #     sequences = []
    #     for filepath in filenames:

    #         speaker_name = 'nan'
    #         speakers.append(speaker_name)


    #         if condition == 'clean':

    #             # sequence = util.load_wav(filepath, self.sample_rate)
    #             sequence = self.aug(filepath, self.sequence_max_len, noise_rate = 0)
    #             sequences.append(sequence)
    #             self.num_sequences_in_memory += 1
    #             regain_factors.append(self.regain / util.rms(sequence))

    #             if self.extract_voice:
    #                 speech_onset_offset_indices.append(util.get_subsequence_with_speech_indices(sequence))
    #         else:
    #             if self.in_memory_percentage == 1 or np.random.uniform(0, 1) <= (self.in_memory_percentage-0.5)*2:
    #                 # sequence = util.load_wav(filepath, self.sample_rate)
    #                 sequence = self.aug(filepath, self.sequence_max_len, noise_rate = 1)
    #                 sequences.append(sequence)
    #                 self.num_sequences_in_memory += 1
    #             else:
    #                 sequences.append([-1])

        
    #         # if speaker_name not in self.speaker_mapping:
    #         #     self.speaker_mapping[speaker_name] = len(self.speaker_mapping) + 1

    #         file_paths.append(filepath)
    #     self.speaker_mapping['nan'] = 29

    #     return sequences, file_paths, speakers, speech_onset_offset_indices, regain_factors

    def get_num_sequences_in_dataset(self):
        return len(self.sequences['train']['clean']) + len(self.sequences['train']['noisy']) + len(self.sequences['test']['clean']) + len(self.sequences['test']['noisy'])

    def retrieve_sequence(self, Set, condition, sequence_num):

        if len(self.sequences[Set][condition][sequence_num]) == 1:
            sequence = util.load_wav(self.file_paths[Set][condition][sequence_num], self.sample_rate)

            if (float(self.num_sequences_in_memory) / self.get_num_sequences_in_dataset()) < self.in_memory_percentage:
                self.sequences[Set][condition][sequence_num] = sequence
                self.num_sequences_in_memory += 1
        else:
            sequence = self.sequences[Set][condition][sequence_num]

        return np.array(sequence)

    # def get_random_batch_generator(self, Set):

    #     if Set not in ['train', 'test']:
    #         raise ValueError("Argument SET must be either 'train' or 'test'")

    #     while True:
    #         sample_indices = np.random.randint(0, len(self.sequences[Set]['clean']), self.batch_size)
    #         condition_inputs = []
    #         batch_inputs = []
    #         batch_outputs_1 = []
    #         batch_outputs_2 = []

    #         for i, sample_i in enumerate(sample_indices):

    #             while True:

    #                 speech = self.retrieve_sequence(Set, 'clean', sample_i)
    #                 noisy = self.retrieve_sequence(Set, 'noisy', sample_i)
    #                 noise = noisy - speech

    #                 if self.extract_voice:
    #                     speech = speech[self.voice_indices[Set][sample_i][0]:self.voice_indices[Set][sample_i][1]]

    #                 speech_regained = speech * self.regain_factors[Set][sample_i]
    #                 noise_regained = noise * self.regain_factors[Set][sample_i]

    #                 if len(speech_regained) < self.model.input_length:
    #                     sample_i = np.random.randint(0, len(self.sequences[Set]['clean']))
    #                 else:
    #                     break

    #             offset = np.squeeze(np.random.randint(0, len(speech_regained) - self.model.input_length, 1))

    #             speech_fragment = speech_regained[offset:offset + self.model.input_length]
    #             noise_fragment = noise_regained[offset:offset + self.model.input_length]

    #             Input = noise_fragment + speech_fragment
    #             output_speech = speech_fragment
    #             output_noise = noise_fragment

    #             if self.noise_only_percent > 0:
    #                 if np.random.uniform(0, 1) <= self.noise_only_percent:
    #                     Input = output_noise #Noise only
    #                     output_speech = np.array([0] * self.model.input_length) #Silence

    #             batch_inputs.append(Input)
    #             batch_outputs_1.append(output_speech)
    #             batch_outputs_2.append(output_noise)

    #             if np.random.uniform(0, 1) <= 1.0 / self.get_num_condition_classes():
    #                 condition_input = 0
    #             else:
    #                 condition_input = self.speaker_mapping[self.speakers[Set][sample_i]]
    #                 if condition_input > 28: #If speaker is in test set, use wildcard condition class 0
    #                     condition_input = 0

    #             condition_inputs.append(condition_input)

    #         batch_inputs = np.array(batch_inputs, dtype='float32')
    #         batch_outputs_1 = np.array(batch_outputs_1, dtype='float32')
    #         batch_outputs_2 = np.array(batch_outputs_2, dtype='float32')
    #         batch_outputs_1 = batch_outputs_1[:, self.model.get_padded_target_field_indices()]
    #         batch_outputs_2 = batch_outputs_2[:, self.model.get_padded_target_field_indices()]
    #         condition_inputs = self.condition_encode_function(np.array(condition_inputs, dtype='uint8'), self.model.num_condition_classes)

    #         batch = {'data_input': batch_inputs, 'condition_input': condition_inputs}, {
    #             'data_output_1': batch_outputs_1, 'data_output_2': batch_outputs_2}

    #         yield batch

    def get_condition_input_encode_func(self, representation):

        if representation == 'binary':
            return util.binary_encode
        else:
            return util.one_hot_encode

    def get_num_condition_classes(self):
        return 29

    def get_target_sample_index(self):
        return int(np.floor(self.fragment_length / 2.0))

    def get_samples_of_interest_indices(self, causal=False):

        if causal:
            return -1
        else:
            target_sample_index = self.get_target_sample_index()
            return range(target_sample_index - self.half_target_field_length - self.target_padding,
                         target_sample_index + self.half_target_field_length + self.target_padding + 1)

    def get_sample_weight_vector_length(self):
        if self.samples_of_interest_only:
            return len(self.get_samples_of_interest_indices())
        else:
            return self.fragment_length


# In[ ]:


class denoising_dataset(torch.utils.data.IterableDataset):
    def __init__(self, generator):
        self.generator = generator
    def __iter__(self):
        return self.generator

