# -*- coding: utf-8 -*-
"""
models.py - The covec dataset model defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import pathlib
from torch.utils import data


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
