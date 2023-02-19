"""
@author : Hyunwoong
@when : 2019-10-22
@homepage : https://github.com/gusdnd852
"""
import math
from time import time
import os
import random
import argparse

import numpy as np

import torch
from torch import nn, optim
from torch.optim import Adam

from data import build_dataloader
from conf import *
from models.model.transformer import Transformer
from util.bleu import idx_to_word, get_bleu
from util.epoch_timer import epoch_time


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def initialize_weights(m):
    if hasattr(m, 'weight') and m.weight.dim() > 1:
        nn.init.kaiming_uniform(m.weight.data)

def train(model, iterator, optimizer, criterion, clip):
    model.train()
    epoch_loss = 0
    for i, (src, trg) in enumerate(iterator):
        optimizer.zero_grad()
        output = model(src, trg[:, :-1])
        output_reshape = output.contiguous().view(-1, output.shape[-1])
        trg = trg[:, 1:].contiguous().view(-1)

        loss = criterion(output_reshape, trg)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()

        epoch_loss += loss.item()
        print('step :', round((i / len(iterator)) * 100, 2), '% , loss :', loss.item())

    return epoch_loss / len(iterator)


def evaluate(model, iterator, criterion, tokenizer, batch_size):
    model.eval()
    epoch_loss = 0
    batch_cer = []
    first = True
    with torch.no_grad():
        for i, (src, trg) in enumerate(iterator):
            output = model(src, trg[:, :-1])
            output_reshape = output.contiguous().view(-1, output.shape[-1])
            trg_reshape = trg[:, 1:].contiguous().view(-1)

            loss = criterion(output_reshape, trg_reshape)
            epoch_loss += loss.item()

            total_cer = []
            for j in range(batch_size):
                
                trg_words = tokenizer.idxs_2_tokens(trg[j])
                output_words = output[j, :, :].max(dim=1)[1]
                output_words = tokenizer.idxs_2_tokens(output_words)
                cer = get_bleu(hypotheses=output_words.split(), reference=trg_words.split())
                print(tokenizer.idxs_2_tokens(src[j]))
                if first:
                    print(trg_words)
                    print(output_words)
                total_cer.append(cer)
            first = False

            total_cer = sum(total_cer) / len(total_cer)
            batch_cer.append(total_cer)

    batch_cer = sum(batch_cer) / len(batch_cer)
    return epoch_loss / len(iterator), batch_cer


def run(total_epoch, best_loss):
    parser = argparse.ArgumentParser(description='TEC')
    parser.add_argument('--model-name', type=str, default='TEC')
    # Dataset
    parser.add_argument('--train-file', type=str,
                        help='data list about train dataset', default='/root/data/post_processing/train.txt')
    parser.add_argument('--test-file', type=str,
                        help='data list about test dataset', default='/root/data/post_processing/validation.txt')
    parser.add_argument('--labels-path', default='/root/data/post_processing/kor_syllable.json', help='Contains large characters over korean')
    # Hyperparameters
    parser.add_argument('--batch_size', type=int, default=256, help='Batch size in training (default: 256)')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers in dataset loader (default: 4)')
    parser.add_argument('--epochs', type=int, default=100, help='Number of max epochs in training (default: 100)')
    parser.add_argument('--lr', type=float, default=3e-5, help='Learning rate (default: 3e-4)')
    parser.add_argument('--learning-anneal', default=1.1, type=float, help='Annealing learning rate every epoch')
    parser.add_argument('--max_len', type=int, default=80, help='Maximum characters of sentence (default: 80)')
    parser.add_argument('--max-norm', default=400, type=int, help='Norm cutoff to prevent explosion of gradients')
    # System
    parser.add_argument('--save-folder', default='models', help='Location to save epoch models')
    parser.add_argument('--model-path', default='/root/post_processing/transformer/saved/model-2.40297115856493.pt', help='Location to save best validation model')
    parser.add_argument('--log-path', default='log/', help='path to predict log about valid and test dataset')
    parser.add_argument('--cuda', action='store_true', default=False, help='using CUDA')
    parser.add_argument('--seed', type=int, default=123456, help='random seed (default: 123456)')
    parser.add_argument('--mode', type=str, default='train', help='Train or Test')
    parser.add_argument('--load-model', action='store_true', default=False, help='Load model')
    parser.add_argument('--finetune', dest='finetune', action='store_true', default=False,
                        help='Finetune the model after load model')
    args = parser.parse_args()
    
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    device = torch.device('cuda:0' if args.cuda else 'cpu')

    # Batch Size
    batch_size = args.batch_size

    print(">> Loading Train dataset : ", args.train_file)
    train_loader, tokenizer = build_dataloader(args.labels_path, args.train_file, batch_size, device)

    print(">> Loading Test dataset : ", args.test_file)
    test_loader, _ = build_dataloader(args.labels_path, args.test_file, batch_size, device)

    pad_idx = tokenizer.token_PAD_idx
    voc_size = len(tokenizer.idx2token)

    # TODO 트랜스 포머 이해 필요, 들어가는 hyperparameter
    model = Transformer(src_pad_idx=pad_idx,
                        trg_pad_idx=pad_idx,
                        d_model=d_model,
                        enc_voc_size=voc_size,
                        dec_voc_size=voc_size,
                        max_len=max_len,
                        ffn_hidden=ffn_hidden,
                        n_head=n_heads,
                        n_layers=n_layers,
                        drop_prob=drop_prob,
                        device=device).to(device)

    print(f'The model has {count_parameters(model):,} trainable parameters')
    model.apply(initialize_weights)
    optimizer = Adam(params=model.parameters(),
                    lr=init_lr,
                    weight_decay=weight_decay,
                    eps=adam_eps)

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer=optimizer,
                                                    verbose=True,
                                                    factor=factor,
                                                    patience=patience)

    criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

    save_folder = args.save_folder
    os.makedirs(save_folder, exist_ok=True)

    optim_state = None
    if args.load_model:  # Starting from previous model
        print("Loading checkpoint model %s" % args.model_path)
        state = torch.load(args.model_path)
        model.load_state_dict(state)
        print('Model loaded')

    #     if not args.finetune:  # Just load model
    #         optim_state = state['optimizer']

    # if optim_state is not None:
    #     optimizer.load_state_dict(optim_state)

    if args.mode != "train":
        valid_loss, cer = evaluate(model, test_loader, criterion, tokenizer, batch_size)
        print(f'\tVal Loss: {valid_loss:.3f} |  Val PPL: {math.exp(valid_loss):7.3f}')
        print(f'\tcer Score: {cer:.3f}')
    else:
        train_losses, test_losses, cers = [], [], []

        for step in range(total_epoch):
            start_time = time()
            train_loss = train(model, train_loader, optimizer, criterion, clip)
            valid_loss, cer = evaluate(model, test_loader, criterion, tokenizer, batch_size)

            if step > warmup:
                scheduler.step(valid_loss)

            train_losses.append(train_loss)
            test_losses.append(valid_loss)
            cers.append(cer)

            if valid_loss < best_loss:
                best_loss = valid_loss
                torch.save(model.state_dict(), 'saved/model-{0}.pt'.format(valid_loss))

            end_time = time()

            print(f'Epoch: {step + 1} | Time: {end_time - start_time}s')
            print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
            print(f'\tVal Loss: {valid_loss:.3f} |  Val PPL: {math.exp(valid_loss):7.3f}')
            print(f'\tcer Score: {cer:.3f}')


if __name__ == '__main__':
    run(total_epoch=epoch, best_loss=inf)
