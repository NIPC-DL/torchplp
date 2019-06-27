# -*- coding: utf-8 -*-
"""
sysevr.py - SySeVr Dataset defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import shutil
import zipfile
from torchplp.utils.loader import loader_cgd
from torchplp.utils.utils import git_clone_file
from .models import Dataset
from .constants import SYSEVR_URL


class SySeVR(Dataset):
    """SySeVR Dataset <https://github.com/SySeVR/SySeVR> 
    
    From Paper:
        SySeVR: A Framework for Using Deep Learning to Detect Software
            Vulnerabilities <https://arxiv.org/abs/1807.06756>

    Args:
        datapath (str): Directory of dataset, will automately create SySeVR directory in it.
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, root, download=True):
        super().__init__(root)
        if download:
            self.download()

        self._category = dict()
        for file in self._root.glob('**/*.txt'):
            name = ''.join([x[0] for x in file.stem.split(' ')[-2:]]).upper()
            self._category[name] = file

    def download(self):
        """Download SySeVR Datasets from their Github Repo"""
        print(f'git clone from {SYSEVR_URL}')
        clone_path = self._root / 'SySeVR.git'
        if not clone_path.exists():
            git_clone_file(SYSEVR_URL, str(clone_path))
            for file in clone_path.glob('**/*.zip'):
                with zipfile.ZipFile(str(file)) as z:
                    z.extractall(str(self._root))
        else:
            print(f'{str(clone_path)} exist, download cancel')

    def load(self, category=None):
        for cate in category:
            samples = loader_cgd(str(self._category[cate]))
            assert len(samples) != 0
            yield cate, samples
