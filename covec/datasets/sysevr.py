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
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, datapath, download=True):
        super().__init__(datapath)
        if download:
            self.download()

    def download(self):
        """Download SySeVR Datasets from their Github Repo"""
        url = DOWNLOAD_URL['sysevr']
        print(f'git clone from {url}')
        clone_path = self._rawp / 'SySeVR.git'
        if not clone_path.exists():
            git_clone_file(str(url), str(clone_path))
            # Extract download zip file
            zip_files = list(self._rawp.glob('**/*.zip'))
            for file in zip_files:
                with zipfile.ZipFile(str(file)) as z:
                    z.extractall(path=str(self._rawp))
            # arrange the raw directory for easy to use
            data_text_file = list(self._rawp.glob('**/**/*.txt'))
            for text in data_text_file:
                shutil.move(str(text), str(self._rawp))
                shutil.rmtree(text.parent, ignore_errors=True)
        else:
            print('warn: directoy exist, download cancel')

    def process(self, processor):
        """Process the selected data into vector by given processor and embedder

        This method will update the self._X and self._Y variable point to processed
        data, and if cache is True, it will save processed data in cooked directory.
        
        Args:
            processor (covec.processor.Processor): The process methods
           
        """
        pass

    def load(self, category, folds):
        """Return the Pytorch Dataset Object

        Args:
            name (str, None): The name of process methods, if not set,
                will return the lastest processed data

        """
        pass
