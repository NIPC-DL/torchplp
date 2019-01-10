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

    def __init__(self, X, Y):
        self._X = X
        self._Y = Y

    def __getitem__(self, index):
        return self._X[index], self._Y[index]

    def __len__(self):
        return len(self._Y)
