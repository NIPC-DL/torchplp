# -*- coding: utf-8 -*-
"""
sysevr.py - SySeVr Dataset defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import zipfile
import random
import shutil
import pickle
import torch
from .models import Dataset, TorchSet
from torchplp.utils.loader import loader_cgd
from torchplp.utils.utils import git_clone_file


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
        url = ''
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
            print(f'{str(clone_path)} exist, download cancel')

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
                continue
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
            category = ['AF', 'AE', 'AU']
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
                    tx.extend(x)
                    ty.extend(y)
        train = TorchSet(torch.Tensor(tx).float(), torch.Tensor(ty).long())
        valid = TorchSet(torch.Tensor(vx).float(), torch.Tensor(vy).long())
        print(f"Load train {len(train)}")
        print(f"Load valid {len(valid)}")
        return train, valid
