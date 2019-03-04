# -*- coding: utf-8 -*-
"""
vuldeepecker.py - VulDeePecker Dataset defination

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
import torch
import numpy as np
from torch.utils.data import DataLoader
from .utils import download_file, git_clone_file
from .constants import DOWNLOAD_URL
from .models import Dataset, TorchSet
from covec.processor import TextModel, Word2Vec
from covec.utils.loader import loader_cgd


class VulDeePecker(Dataset):
    """VulDeePecker Dataset <https://github.com/CGCL-codes/VulDeePecker> 
    
    From Paper:
        VulDeePecker: A Deep Learning-Based System for Vulnerability Detection

    Args:
        datapath (str): Directory of dataset, will automately create
        VulDeePecker directory in it.
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, datapath, processor=None, download=True):
        super().__init__(datapath)
        if download:
            self.download()
        if processor:
            self.process(processor)

    def download(self):
        """Download VulDeePecker Datasets from their Github Repo"""
        url = DOWNLOAD_URL['vuldeepecker']
        print(f'git clone from {url}')
        clone_path = self._rawp / 'VulDeePecker.git'
        if not clone_path.exists():
            git_clone_file(str(url), str(clone_path))


    def process(self, processor):
        """Process the selected data into vector by given processor and embedder

        This method will update the self._X and self._Y variable point to processed
        data, and if cache is True, it will save processed data in cooked directory.
        
        Args:
            processor (covec.processor.Processor): The process methods
           """
        for file in self._rawp.glob('**/*_cgd.txt'):
            print(str(file))
            filep = self._cookp / f'{file.stem}.p'
            if filep.exists():
                continue
            x, y = loader_cgd(str(file))
            assert len(x) == len(y)
            x = processor.process(x, 'cgd')
            assert len(x) == len(y)
            pickle.dump((x,y), open(str(filep), 'wb'),
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
            filep = self._cookp / f"{file}_cgd.p"
            if filep.exists():
                x, y= pickle.load(open(str(filep), 'rb'))
                assert len(x) == len(y)
                data = list(zip(x, y))
                random.shuffle(data)
                x, y = zip(*data)
                assert len(x) == len(y)
                lens = len(x)
                if folds:
                    coe = round((folds - 1) / folds * lens)
                    print(coe)
                    tx.extend(x[:coe])
                    ty.extend(y[:coe])
                    vx.extend(x[coe:])
                    vy.extend(y[coe:])
                else:
                    tx.extend(vsts)
                    ty.extend(labels)
        train = TorchSet(torch.Tensor(tx).float(), torch.Tensor(ty).long())
        valid = TorchSet(torch.Tensor(vx).float(), torch.Tensor(vy).long())
        print(f"Load train {len(train)}")
        print(f"Load valid {len(valid)}")
        return train, valid
