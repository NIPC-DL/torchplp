# -*- coding: utf-8 -*-
"""
vdp.py - VulDeePecker Dataset defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import re
import zipfile
import random
import shutil
import pickle
import numpy as np
from torch.utils.data import DataLoader
from .utils import download_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY, SYSEVR_CATEGORY
from .models import Dataset, TorchSet
from covec.processor import TextModel, Word2Vec
from covec.utils.loader import loader_cgd


class VDP(Dataset):
    """VulDeePecker Dataset <https://github.com/CGCL-codes/VulDeePecker> 
    
    From Paper:
        VulDeePecker: A Deep Learning-Based System for Vulnerability Detection
        <https://arxiv.org/abs/1801.01681>

    Args:
        datapath (str): Directory of dataset, will automately create SySeVR directory in it.
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, datapath, download=True, proxy=None):
        super().__init__(datapath)
        if download:
            self.download(proxy)

    def download(self, proxy):
        """Download SySeVR Datasets from their Github Repo"""
        cwe119 = self._rawp / 'cwe119_cgd.txt'
        cwe399 = self._rawp / 'cwe399_cgd.txt'
        if not cwe119.exists():
            download_file('https://raw.githubusercontent.com/CGCL-codes/VulDeePecker/master/CWE-119/CGD/cwe119_cgd.txt',
                    str(cwe119), proxy)
        if not cwe399.exists():
            download_file('https://raw.githubusercontent.com/CGCL-codes/VulDeePecker/master/CWE-399/CGD/cwe399_cgd.txt',
                    str(cwe399), proxy)

    def process(self, processor):
        """Process the selected data into vector by given processor and embedder

        This method will update the self._X and self._Y variable point to processed
        data, and if cache is True, it will save processed data in cooked directory.
        
        Args:
            processor (covec.processor.Processor): The process methods
           """
        for file in self._rawp.glob('**/*.txt'):
            if '119' in file.name:
                file_name = 'cwe119'
            else:
                file_name = 'cwe399'
            filep = self._cookp / f'{file_name}.p'
            if filep.exists():
                continue
            x, y = loader_cgd(str(file))
            x = processor.process(x)
            pickle.dump((x,y), open(str(filep), 'rb'),
                        protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, category=None, folds=None):
        """Return the Pytorch Dataset Object

        Args:
            category (list, None): The class of load datasets, 
                if None, load all datasets
            folds (int): The folds of validation

        """
        tx, ty = [], []
        vx, vy = [], []
        if not category:
            category = ['cwe119', 'cwe399']
        for file in category:
            filep = self._cookp / f"{file.upper()}.p"
            if filep.exists():
                x, y= pickle.load(open(str(filep), 'rb'))
                data = list(zip(x, y))
                random.shuffle(data)
                x, y = zip(*data)
                assert len(x) == len(y)
                lens = len(x)
                if folds:
                    coe = round((folds - 1) / folds * lens)
                    tx.extend(x[:coe])
                    ty.extend(y[:coe])
                    vx.extend(x[-coe:])
                    vy.extend(y[-coe:])
                else:
                    tx.extend(vsts)
                    ty.extend(labels)
        train = TorchSet(torch.Tensor(tx).float(), torch.Tensor(ty).long())
        valid = TorchSet(torch.Tensor(vy).float(), torch.Tensor(vy).long())
        print(f"Load train {len(train)}")
        print(f"Load valid {len(valid)}")
        return train, valid

