# -*- coding: utf-8 -*-
"""
sysevr.py - SySeVr Dataset defination

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
import re
import zipfile
from .utils import download_file, git_clone_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY, SYSEVR_CATEGORY
from .models import Dataset
from covec.processor import Textmod, Word2Vec
from covec.utils.loader import loader_cgd


class SySeVR(Dataset):
    """SySeVR <https://github.com/SySeVR/SySeVR> 
    
    
    SySeVR: A Framework for Using Deep Learning to Detect Software
            Vulnerabilities <https://arxiv.org/abs/1807.06756>

    Args:
        root <str>: Directory of dataset, will automately create SySeVR directory in it.
        download <bool, optional>: If true, download dataset from internet, default false.
        proxy <str>: The proxy for download.
            eg. 'http://user:pass@host:port/'
                'socks5://user:pass@host:port'

    """

    def __init__(self, datapath, download=False):
        super().__init__(datapath)
        self._datapath = self._datapath + "SySeVR/"
        if not os.path.exists(self._datapath):
            os.makedirs(self._datapath)
        if download:
            self.download()

    def download(self):
        """Download SySeVR Datasets from their Github Repo

        Directory Tree:
           <datapath>/SySeVR
                    └── Raw
                        ├── API function call.txt
                        ├── Arithmetic expression.txt
                        ├── Array usage.txt
                        ├── Pointer usage.txt
                        └── SySeVR.git
                            ├── API function call.zip
                            ├── Arithmetic expression.zip
                            ├── Array usage.zip
                            ├── library-API function calls.docx
                            ├── List of the 126 CWE IDs.docx
                            ├── Pointer usage.zip
                            └── README.md

        Args:
            None

        """
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

    def data(self, category=None):
        """Process dataset and create vector dataset

        Args:
            category <None, list>: The parts of Juliet Test Suite used on dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage

        """
        file_list = self._selected(category)
        x_set, y_set = loader_cgd(file_list)
        return x_set, y_set

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