"""This module contains simple helper functions """
from __future__ import print_function
import torch
import numpy as np
from PIL import Image
import os
import librosa
from scipy.io.wavfile import write
from pathlib import Path
import soundfile as sf


def tensor2im(input_image, imtype=np.uint8):
    """"Converts a Tensor array into a numpy image array.

    Parameters:
        input_image (tensor) --  the input image tensor array
        imtype (type)        --  the desired type of the converted numpy array
    """
    if not isinstance(input_image, np.ndarray):
        if isinstance(input_image, torch.Tensor):  # get the data from a variable
            image_tensor = input_image.data
        else:
            return input_image
        audio_numpy = image_tensor[0].cpu().float().numpy()  # convert it into a numpy array
        # if image_numpy.shape[0] == 1:  # grayscale to RGB
        #     image_numpy = np.tile(image_numpy, (3, 1, 1))

        # image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0  # post-processing: tranpose and scaling
        image_numpy = (audio_numpy + 1)/2.0 * 255.0
    else:  # if it is a numpy array, do nothing
        image_numpy = input_image
    return image_numpy.astype(imtype), audio_numpy


def diagnose_network(net, name='network'):
    """Calculate and print the mean of average absolute(gradients)

    Parameters:
        net (torch network) -- Torch network
        name (str) -- the name of the network
    """
    mean = 0.0
    count = 0
    for param in net.parameters():
        if param.grad is not None:
            mean += torch.mean(torch.abs(param.grad.data))
            count += 1
    if count > 0:
        mean = mean / count
    print(name)
    print(mean)


def save_image(image_numpy, audio_numpy, image_path, aspect_ratio=1.0, opt=None):
    """Save a numpy image to the disk

    Parameters:
        image_numpy (numpy array) -- input numpy array
        image_path (str)          -- the path of the image
    """

    image_pil = Image.fromarray(image_numpy)
    h, w= image_numpy.shape

    if aspect_ratio > 1.0:
        image_pil = image_pil.resize((h, int(w * aspect_ratio)), Image.BICUBIC)
    if aspect_ratio < 1.0:
        image_pil = image_pil.resize((int(h / aspect_ratio), w), Image.BICUBIC)
    image_pil.save(image_path)

    n_fft = int(opt.sample_rate * opt.window_size)
    window_size = n_fft
    stride_size = int(opt.sample_rate * opt.window_stride)
    y = librosa.istft(audio_numpy, hop_length=stride_size, win_length=window_size, n_fft=n_fft)

    audio_path = os.path.dirname(os.path.dirname(os.path.abspath(image_path))) + '/audio/'
    file_name = os.path.basename(image_path)[:-3] + 'wav'
    os.makedirs(audio_path, exist_ok=True)

    sf.write(audio_path + file_name, y, 16000)



    # S = librosa.feature.inverse.mel_to_stft(image_numpy, sr=16000, n_fft=n_fft)
    # y = librosa.griffinlim(S, hop_length=stride_size, win_length=window_size, n_fft=n_fft)
    # # y = librosa.griffinlim(image_numpy, hop_length=stride_size, win_length=window_size, n_fft=n_fft)
    # # y = librosa.istft(y, hop_length=stride_size, win_length=window_size, n_fft=n_fft)
    

    # rate = opt.
    # data = np.random.uniform(-1, 1, rate) # 1 second worth of random samples between -1 and 1
    # scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    # write('test.wav', rate, scaled)


def print_numpy(x, val=True, shp=False):
    """Print the mean, min, max, median, std, and size of a numpy array

    Parameters:
        val (bool) -- if print the values of the numpy array
        shp (bool) -- if print the shape of the numpy array
    """
    x = x.astype(np.float64)
    if shp:
        print('shape,', x.shape)
    if val:
        x = x.flatten()
        print('mean = %3.3f, min = %3.3f, max = %3.3f, median = %3.3f, std=%3.3f' % (
            np.mean(x), np.min(x), np.max(x), np.median(x), np.std(x)))


def mkdirs(paths):
    """create empty directories if they don't exist

    Parameters:
        paths (str list) -- a list of directory paths
    """
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir(path):
    """create a single empty directory if it didn't exist

    Parameters:
        path (str) -- a single directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)
