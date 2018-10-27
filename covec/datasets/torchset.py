# -*- coding: utf-8 -*-
"""
datsets.py - Provide Pytorch Dataset Support

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import torch
from torch.utils import data


class TorchSet(data.Dataset):
    def __init__(self, X, Y):
        self.X = torch.tensor(X).float()
        self.Y = torch.tensor(Y).long()

    def __getitem__(self, index):
        return self.X[index], self.Y[index]

    def __len__(self):
        return len(self.X)
