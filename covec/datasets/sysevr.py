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
    
    Directory Tree:
        SySeVR
            ├── Raw
            │   ├── API function call.txt
            │   ├── Arithmetic expression.txt
            │   ├── Array usage.txt
            │   ├── Pointer usage.txt
            │   └── SySeVR.git
            └── TextModel_vec.npz


    Args:
        datapath (str): Directory of dataset, will automately create SySeVR directory in it.
        processor (covec.processor.Processor): The process methods
        category (None, list): The parts of Juliet Test Suite used on dataset
            - None, default: use all categoary
            - 'AE': Arithmetic Expression
            - 'AF': API Function Call
            - 'AU': Array Usage
            - 'PU': Pointer Usage
        cache (bool, optional): Default is True to create cache file for vector data
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self,
                 datapath,
                 processor,
                 category=None,
                 cache=True,
                 download=True):
        super().__init__(datapath)
        self._datapath = self._datapath + "SySeVR/"
        self._vecpath = self._datapath + f'{processor}_vec.npz'
        if not os.path.exists(self._datapath):
            os.makedirs(self._datapath)
        if download and not os.path.exists(self._datapath + 'Raw/'):
            self.download()
        if os.path.exists(self._vecpath):
            dataset = np.load(self._vecpath)
            self.X, self.Y = dataset['arr_0'], dataset['arr_1']
        else:
            self.X, self.Y = self.process(processor, category=category)
            if cache:
                np.savez(self._vecpath, self.X, self.Y)

    def download(self):
        """Download SySeVR Datasets from their Github Repo"""
        url = DOWNLOAD_URL['sysevr']
        raw_path = self._datapath + 'Raw/'
        print(f'git clone from {url}')
        if not os.path.exists(raw_path):
            os.makedirs(raw_path)
        clone_path = raw_path + 'SySeVR.git/'
        git_clone_file(url, clone_path)
        print('clone success, Start extracting.')
        # Extract download zip file
        for file in os.listdir(clone_path):
            if file.split('.')[-1] == 'zip':
                with zipfile.ZipFile(os.path.join(clone_path, file)) as z:
                    z.extractall(path=raw_path)
        # arrange the raw directory for easy to use
        for root, _, files in os.walk(raw_path):
            for file in files:
                if file.split('.')[-1] == 'txt':
                    os.rename(
                        os.path.join(root, file), os.path.join(raw_path, file))
                    os.rmdir(root)

    def process(self, processor, category=None):
        """Process the selected data into vector by given processor and embedder
        
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
        print('cgd load finish')
        x_set = processor.process(x_set, 'cgd')
        y_set = y_set
        assert len(x_set) == len(y_set)
        return np.asarray(x_set), np.asarray(y_set)

    @property
    def torchset(self):
        """Return the Pytorch Dataset Object"""
        return TorchSet(self.X, self.Y)

    def _selected(self, category):
        """Select file from category"""
        sysevr_raw_path = self._datapath + 'Raw/'
        area = []
        if category:
            for i in category:
                area.append(SYSEVR_CATEGORY[i])
        else:
            area = SYSEVR_CATEGORY.values()
        file_list = []
        for root, _, files in os.walk(sysevr_raw_path):
            for file in files:
                if file in area:
                    file_list.append(os.path.join(root, file))
        return file_list
