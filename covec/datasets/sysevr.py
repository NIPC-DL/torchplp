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
from covec.utils.processor import sysevr


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
            self.download(proxy)

    def download(self):
        """Download SySeVR Datasets from their Github Repo

        Directory Tree:
           <datapath>/SySeVR
                └── Raw
                    └── SySeVR

        Args:
            proxy <str>: The proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

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
    
    def process(self, methods=None, category=None):
        """Process dataset and create dataset

        Directory Tree:
            <datapath>/SySeVR
            TODO: w

        Args:
            method <None, list>: The process methods used on dataset
                - None, default: use all methods
                - 'sysevr': source from arXiv:1807.06756
            category <None, list>: The parts of Juliet Test Suite used on dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage

        """
        file_list = self._selected(category)
        print(file_list)
        if not methods:
            methods = ['sysevr', ]
        if 'sysevr' in methods:
            sysevr(file_list, 'cgd')
    
    def _selected(self, category):
        """Selected file by categoryVulDeePecker and 
        VulDeePecker and 
        Args:VulDeePecker and 
            category <None, list>: TheVulDeePecker and  parts of Juliet Test Suite used on dataset
            - None, default: use all cVulDeePecker and ategoary
            - 'AE': Arithmetic ExpressVulDeePecker and ion
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