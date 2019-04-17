# -*- coding: utf-8 -*-
"""
models.py - The covec dataset model defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import pathlib
import pickle
import numpy as np
import torch
from torch.utils import data

def l2o(y):
    y_onehot = torch.FloatTensor(1, 2)
    y_onehot.zero_()
    y_onehot.scatter_(1, y, 1)
    return y_onehot


class Dataset(object):
    """Upper dataset class"""

    def __init__(self, root):
        # expand given path
        self._rootp = pathlib.Path(root).expanduser()
        # create unique directory in datapath to save datasets
        self._rootp = self._rootp / str(self)
        self._rootp.mkdir(parents=True, exist_ok=True)
        # create raw path to save raw datasets
        self._rawp = self._rootp / 'raw'
        self._rawp.mkdir(parents=True, exist_ok=True)
        # create cooked path to save processed datasets (vector data)
        self._cookp = self._rootp / 'cook'
        self._cookp.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return self.__class__.__name__

class TorchSet(data.Dataset):
    """The Pytorch Dataset"""

    def __init__(self, X, L, Y):
        self._X = torch.from_numpy(X).float()
        self._L = torch.LongTensor(L)
        self._Y = torch.from_numpy(Y).long()

    def __getitem__(self, index):
        return self._X[index], self._L[index], self._Y[index]

    def __len__(self):
        return len(self._X)

class TorchPathSet(data.Dataset):
    def __init__(self, x, l, y):
        self._x = x
        self._l = torch.from_numpy(l).long()
        self._y = torch.from_numpy(y).long()
        assert len(self._x) == len(self._l) == len(self._y) != 0

    def __getitem__(self, index):
        x = self._x[index]
        x = np.load(x)
        x = torch.from_numpy(x).float()
        l = self._l[index]
        y = self._y[index]
        return x, l ,y

    def __len__(self):
        return len(self._x)

class TorchSet2(data.Dataset):
    def __init__(self, samps, labels, processor=None):
        if processor is not None:
            paths, lens = processor(samps)
            self._x = paths
            self._l = torch.LongTensor(lens)
        else:
            self._x = samps
        self._y = torch.LongTensor(labels)

    def __getitem__(self, index):
        x = self._x[index]
        x = np.load(x)
        x = torch.from_numpy(x).float()
        l = self._l[index]
        y = self._y[index]
        return x, l ,y

    def __len__(self):
        return len(self._y)

