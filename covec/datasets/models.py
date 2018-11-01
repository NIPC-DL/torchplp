# -*- coding: utf-8 -*-
"""
models.py - The covec dataset model defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import pathlib


class Dataset:
    """Upper dataset class"""

    def __init__(self, datapath):
        # expand given path
        self._datapath = pathlib.Path(datapath).expanduser()
        # create unique directory in datapath to save datasets
        self._datapath = self._datapath / str(self)
        self._datapath.mkdir(parents=True, exist_ok=True)
        # create raw path to save raw datasets
        self._rawpath = self._datapath / 'raw'
        self._rawpath.mkdir(parents=True, exist_ok=True)
        # create cooked path to save processed datasets (vector data)
        self._cookedpath = self._datapath / 'cooked'
        self._cookedpath.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return self.__class__.__name__