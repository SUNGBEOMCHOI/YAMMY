"""
@author : Hyunwoong
@when : 2019-10-29
@homepage : https://github.com/gusdnd852
"""
from conf import *
import json
import torch
from torch.nn.utils.rnn import pad_sequence
import random

class Tokenizer:
    # token means letters ex) 가, 나, 다, 라
    # idx means index ex) 1, 2, 3, 4
    def __init__(self, token_path = "/root/data/post_processing/kor_syllable.json"):
        with open(token_path, "r") as file:
            self.idx2token = json.load(file)
        self.token_UNK = "!"
        self.token_SOS = "@"
        self.token_EOS = "#"
        self.token_PAD = "^"
        self.idx2token.append(self.token_UNK) # unknown token
        self.idx2token.append(self.token_SOS) # start of sequence token
        self.idx2token.append(self.token_EOS) # end of sequence token
        self.idx2token.append(self.token_PAD) # padding token
        self.token2idx = {}
        for i in range(len(self.idx2token)):
            self.token2idx[self.idx2token[i]] = i
        self.token_UNK_idx = self.token2idx["!"]
        self.token_SOS_idx = self.token2idx["@"]
        self.token_EOS_idx = self.token2idx["#"]
        self.token_PAD_idx = self.token2idx["^"]
        
    # token_list : str
    # output : longtensor
    def tokens_2_idxs(self, token_list):
        idxs = []
        assert len(token_list) != 0
        for token in token_list: 
            try:
                idxs.append(self.token2idx[token])
            except:
                idxs.append(self.token2idx["!"])
        return torch.LongTensor(idxs)
    
    # idx_list : longtensor
    # output : str
    def idxs_2_tokens(self, idx_list):
        tokens = ""
        for idx in idx_list:
            try:
                tokens += self.idx2token[idx]
            except:
                tokens += self.token_UNK
        return tokens

class Dataset_Postprocessing(torch.utils.data.Dataset):
    # validation data_path "/root/data/post_processing/validation.txt"
    def __init__(self, tokenizer, data_path = "/root/data/post_processing/train.txt"):
        with open(data_path, "r", encoding='utf-8-sig') as file:
            self.data = file.readlines()
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        cur_data = self.data[idx].split('\t')
        src = self.tokenizer.tokens_2_idxs(cur_data[0] + self.tokenizer.token_EOS)
        tgt = self.tokenizer.tokens_2_idxs(self.tokenizer.token_SOS + cur_data[1][:-1] + self.tokenizer.token_EOS) # except new line character
        return (src, tgt)

def batch_sampling(sequence_lengths, batch_size):
    seq_lens = [(i, seq_len, tgt_len) for i, (seq_len, tgt_len) in enumerate(sequence_lengths)]
    seq_lens = sorted(seq_lens, key = lambda x:x[1])
    seq_lens = [sample[0] for sample in seq_lens]
    sample_indices = [seq_lens[i:i+batch_size] for i in range(0, len(seq_lens), batch_size)]
    random.shuffle(sample_indices)
    return sample_indices

def collate_fn(batch_samples, pad_idx, device):
    src_sentences = pad_sequence([src for src, _ in batch_samples], batch_first=True, padding_value=pad_idx).to(device)
    tgt_sentences = pad_sequence([tgt for _, tgt in batch_samples], batch_first=True, padding_value=pad_idx).to(device)
    return src_sentences, tgt_sentences

def batch_sampling(sequence_lengths, batch_size):
    seq_lens = [(i, seq_len, tgt_len) for i, (seq_len, tgt_len) in enumerate(sequence_lengths)]
    seq_lens = sorted(seq_lens, key = lambda x:x[1])
    seq_lens = [sample[0] for sample in seq_lens]
    sample_indices = [seq_lens[i:i+batch_size] for i in range(0, len(seq_lens), batch_size)]
    random.shuffle(sample_indices)
    return sample_indices

def build_dataloader(token_path, data_path, batch_size, device):
    tokenizer = Tokenizer(token_path)
    dataset = Dataset_Postprocessing(tokenizer = tokenizer, data_path=data_path)
    seq_lengths = list(map(lambda x: (len(x[0]), len(x[1])), dataset))
    batch_sampler = batch_sampling(seq_lengths, batch_size)
    train_loader = torch.utils.data.DataLoader(dataset, collate_fn=lambda x: collate_fn(x, tokenizer.token_PAD_idx, device), batch_sampler=batch_sampler)
    return train_loader, tokenizer
