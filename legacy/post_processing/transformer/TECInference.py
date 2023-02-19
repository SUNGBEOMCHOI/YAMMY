import math
from time import time
import os
import random
import argparse

import numpy as np

import torch
from torch import nn, optim
from torch.optim import Adam

from data import Tokenizer
from conf import *
from models.model.transformer import Transformer
from util.bleu import idx_to_word, get_bleu
from util.epoch_timer import epoch_time

class TEC:
    def __init__(self, model_path = "/root/post_processing/transformer/saved/model-2.40297115856493.pt"):
        self.device = torch.device('cpu')
        self.tokenizer = Tokenizer()

        self.sos_idx = self.tokenizer.token_SOS_idx
        self.eos_idx = self.tokenizer.token_EOS_idx
        self.pad_idx = self.tokenizer.token_PAD_idx
        self.voc_size = len(self.tokenizer.idx2token)

        self.model = Transformer(src_pad_idx=self.pad_idx,
                            trg_pad_idx=self.pad_idx,
                            d_model=d_model,
                            enc_voc_size=self.voc_size,
                            dec_voc_size=self.voc_size,
                            max_len=max_len,
                            ffn_hidden=ffn_hidden,
                            n_head=n_heads,
                            n_layers=n_layers,
                            drop_prob=drop_prob,
                            device=self.device).to(self.device)
        
        state = torch.load(model_path)
        self.model.load_state_dict(state)
        self.max_len = 80
    
    def __call__(self, text):
        inp_seq = self.tokenizer.tokens_2_idxs(text).to(self.device).view(1, -1)
        tmp = torch.full((1, self.max_len), self.pad_idx).long().to(self.device)
        tmp[0, :inp_seq.size(1)] = inp_seq
        with torch.no_grad():
            out, eos_pos = self.model.forward_generate(inp_seq, self.max_len, self.pad_idx, self.sos_idx, self.eos_idx)
        out_str = self.tokenizer.idxs_2_tokens(out.squeeze()[:eos_pos])
        return out_str
        

t = TEC()
print(t("신발장에 에어컨이 있는지 알아 와.#"))
src = t.tokenizer.tokens_2_idxs("신발장에 에어컨이 있는지 알아 와.#").to(t.device).view(1, -1)
tgt = t.tokenizer.tokens_2_idxs("@신발장에 에어컨이 있는지 알아 와.#").to(t.device).view(1, -1)
print(t.model(src, tgt))