# -*- coding: utf-8 -*-
"""
datsets.py - Provide Pytorch Dataset Support

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import torch
from torch.utils import data


class TorchSet(data.Dataset):
    """The Pytorch Dataset"""

    def __init__(self, X, Y, type_):
        if type_ == 'array':
            self.X = torch.tensor(X).float()
        elif type_ == 'tree':
            self.X = X
        self.Y = torch.tensor(Y)

    def __getitem__(self, index):
        return self.X[index], self.Y[index]

    def __len__(self):
        return len(self.X)
