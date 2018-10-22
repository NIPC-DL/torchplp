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
from covec.processor import sysevr


class Sysevr(Dataset):
    """Sysevr <https://github.com/SySeVR/SySeVR> 
    
    
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
        datapath = os.path.expanduser(datapath)
        # Make sure directory path end with '/'
        if datapath[-1] != '/':
            datapath += '/'
        self._datapath = datapath + "SySeVR/"
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

    def process(self, methods=None, category=None, sample_size=None,
                **setting):
        """Process dataset and create dataset

        Directory Tree:
            <datapath>/SySeVR
            TODO: w

        Args:
            method <None, list>: The process methods used on dataset
                - None, default: use all methods
                - 'sysevr': source from arXiv:1807.06756
            category <None, list>: The parts of Juliet Test Suite used on 
                                   dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage
            sample_size <int, None, optional>: How many samples are used for 
                                               processing.
            **config <dict, optional>: The optional setting for selected methods

        """
        cooked_path = self._datapath + 'Cooked/'
        if not os.path.exists(cooked_path):
            os.makedirs(cooked_path)
        file_list = self._selected(category)
        if not methods:
            methods = [
                'sysevr',
            ]
        if 'sysevr' in methods:
            sysevr(cooked_path, file_list, 'cgd', sample_size, **setting)

    def _selected(self, category):
        """Selected file by category
        
        Args:
            category <None, list>: The parts of Juliet Test Suite used on dataset
            - None, default: use all categoary
            - 'AE': Arithmetic Expression
            - 'AF': API Function Call
            - 'AU': Array Usage
            - 'PU': Pointer Usage
        
        Return:
            sel_files <list>: file path list selected by category
            
        """
        sysevr_raw_path = self._datapath + 'Raw/'
        area = []
        if category:
            for i in category:
                area.append(SYSEVR_CATEGORY[i])
        else:
            area = SYSEVR_CATEGORY.values()
        print(area)
        file_list = []
        for root, _, files in os.walk(sysevr_raw_path):
            for file in files:
                if file in area:
                    file_list.append(os.path.join(root, file))
        return file_list