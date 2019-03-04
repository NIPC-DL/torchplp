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
import pickle
import torch
import numpy as np
from torch.utils.data import DataLoader
from .utils import download_file, git_clone_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY, SYSEVR_CATEGORY
from .models import Dataset, TorchSet
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

    def __init__(self, datapath, processor=None, download=True):
        super().__init__(datapath)
        if download:
            self.download()
        if processor:
            self.process(processor)

    def download(self):
        """Download SySeVR Datasets from their Github Repo"""
        url = DOWNLOAD_URL['sysevr']
        print(f'git clone from {url}')
        # download sysevr dataset
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
        print(f'Start Processing: {str(processor)}')
        for file in self._rawp.glob('**/*.txt'):
            if 'API' in file.name:
                file_name = 'AF'
            elif 'Array' in file.name:
                file_name = 'AU'
            elif 'Pointer' in file.name:
                file_name = 'PU'
            else:
                file_name = 'AE'
            filep = self._cookp / f'{file_name.lower()}.p'
            if filep.exists():
                continue
            print(f'Create {filep.name} from {file.name}')
            x, y = loader_cgd(str(file))
            assert len(x) == len(y) > 0
            print(f'Processing')
            if file_name == 'PU':
                # coe = round(len(x)/3)
                # x1 = processor.process(x[:coe], 'cgd')
                # pickle.dump((x1,y[:coe]), open(str(self._cookp / 'pu1.p'), 'wb'),
                #             protocol=pickle.HIGHEST_PROTOCOL)
                # x2 = processor.process(x[coe:coe*2], 'cgd')
                # pickle.dump((x2,y[coe:coe*2]), open(str(self._cookp / 'pu2.p'), 'wb'),
                #             protocol=pickle.HIGHEST_PROTOCOL)
                # x3 = processor.process(x[coe*2:], 'cgd')
                # pickle.dump((x2,y[coe*2:]), open(str(self._cookp / 'pu3.p'), 'wb'),
                #             protocol=pickle.HIGHEST_PROTOCOL)
                pass
            else:
                x = processor.process(x, 'cgd')
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
            category = ['AF', 'AE', 'PU1', 'PU2', 'PU3', 'AU']
        for file in category:
            filep = self._cookp / f"{file.lower()}.p"
            if filep.exists():
                print(f'Load {str(filep)}')
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

