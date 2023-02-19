"""A modified image folder class

We modify the official PyTorch image folder (https://github.com/pytorch/vision/blob/master/torchvision/datasets/folder.py)
so that this class can load audios from both current directory and its subdirectories.
"""

import torch.utils.data as data

from PIL import Image
import os
import json

AUDIO_EXTENSIONS = [
    '.pcm', '.wav'
]


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in AUDIO_EXTENSIONS)


def make_dataset(json_dir, max_dataset_size=float("inf")):
    '''
    Parameters:
        dir : directory of jsonfile
    '''
    audios = []
    assert os.path.isfile(json_dir), '%s is not a valid directory' % json_dir

    with open(json_dir, "r", encoding='utf-8-sig') as file:
        json_data = json.load(file)
    
    for fname in json_data:
        path = fname["wav"]
        audios.append(path)

    # for root, _, fnames in sorted(os.walk(json_dir)):
    #     for fname in fnames:
    #         if is_image_file(fname):
    #             path = os.path.join(root, fname)
    #             audios.append(path)
    return audios[:min(max_dataset_size, len(audios))]


# def default_loader(path):
#     return Image.open(path).convert('RGB')


# class ImageFolder(data.Dataset):

#     def __init__(self, root, transform=None, return_paths=False,
#                  loader=default_loader):
#         imgs = make_dataset(root)
#         if len(imgs) == 0:
#             raise(RuntimeError("Found 0 audios in: " + root + "\n"
#                                "Supported image extensions are: " + ",".join(IMG_EXTENSIONS)))

#         self.root = root
#         self.imgs = imgs
#         self.transform = transform
#         self.return_paths = return_paths
#         self.loader = loader

#     def __getitem__(self, index):
#         path = self.imgs[index]
#         img = self.loader(path)
#         if self.transform is not None:
#             img = self.transform(img)
#         if self.return_paths:
#             return img, path
#         else:
#             return img

#     def __len__(self):
#         return len(self.imgs)
