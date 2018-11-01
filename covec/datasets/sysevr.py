# -*- coding: utf-8 -*-
"""
sysevr.py - SySeVr Dataset defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import re
import zipfile
import random
import shutil
import numpy as np
from torch.utils.data import DataLoader
from .utils import download_file, git_clone_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY, SYSEVR_CATEGORY
from .models import Dataset
from .torchset import TorchSet
from covec.processor import TextModel, Word2Vec
from covec.utils.loader import loader_cgd


class SySeVR(Dataset):
    """SySeVR Dataset <https://github.com/SySeVR/SySeVR> 
    
    From Paper:
        SySeVR: A Framework for Using Deep Learning to Detect Software
            Vulnerabilities <https://arxiv.org/abs/1807.06756>

    Args:
        datapath (str): Directory of dataset, will automately create SySeVR directory in it.
        category (None, list): The parts of Juliet Test Suite used on dataset
            - None, default: use all categoary
            - 'AE': Arithmetic Expression
            - 'AF': API Function Call
            - 'AU': Array Usage
            - 'PU': Pointer Usage
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, datapath, category=None, download=True):
        super().__init__(datapath)
        if download:
            self.download()

    def download(self):
        """Download SySeVR Datasets from their Github Repo"""
        url = DOWNLOAD_URL['sysevr']
        print(f'git clone from {url}')
        clone_path = self._rawpath / 'SySeVR.git'
        if not clone_path.exists():
            git_clone_file(str(url), str(clone_path))
            print('clone success, Start extracting.')
            # Extract download zip file
            zip_files = list(self._rawpath.glob('**/*.zip'))
            for file in zip_files:
                with zipfile.ZipFile(str(file)) as z:
                    z.extractall(path=str(self._rawpath))
            # arrange the raw directory for easy to use
            data_text_file = list(self._rawpath.glob('**/**/*.txt'))
            for text in data_text_file:
                shutil.move(str(text), str(self._rawpath))
                shutil.rmtree(text.parent, ignore_errors=True)
        else:
            print('warn: directoy exist, download cancel')

    def process(self, processor, category=None, cache=True):
        """Process the selected data into vector by given processor and embedder

        This method will update the self._X and self._Y variable point to processed
        data, and if cache is True, it will save processed data in cooked directory.
        
        Args:
            processor (covec.processor.Processor): The process methods
            category (None, list): The parts of Juliet Test Suite used on dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage
            
        """
        file_list = self._selected(category)
        x_set, y_set = loader_cgd(file_list)
        x_set = processor.process(x_set, 'cgd')
        assert len(x_set) == len(y_set)
        self._X, self._Y = np.asarray(x_set), np.asarray(y_set)
        if cache:
            np.savez(
                str(self._cookedpath / f'{str(processor).lower()}_vec.npz'),
                self._X, self._Y)

    def torchset(self, name=None):
        """Return the Pytorch Dataset Object

        Args:
            name (str, None): The name of process methods, if not set,
                will return the lastest processed data

        """
        if name:
            dataset = np.load(
                str(self._cookedpath / f'{name.lower()}_vec.npz'))
            X, Y = dataset['arr_0'], dataset['arr_1']
            tset = TorchSet(X, Y)
        else:
            tset = TorchSet(self._X, self._Y)
        return tset

    def _selected(self, category):
        """Select file from category"""
        area = []
        if category:
            for i in category:
                area.append(SYSEVR_CATEGORY[i])
        else:
            area = SYSEVR_CATEGORY.values()
        file_list = []
        for file in self._rawpath.glob('**/*.txt'):
            if file.name in area:
                file_list.append(str(file))
        return file_list
