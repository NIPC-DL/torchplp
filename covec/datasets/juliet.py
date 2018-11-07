# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite (https://samate.nist.gov/SRD/testsuite.php)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import re
import zipfile
import pathlib
import shutil
from .utils import download_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY
from .models import Dataset
from covec.utils.loader import loader_cc
from covec.processor import Parser


class Juliet(Dataset):
    """Juliet Test Suite <https://samate.nist.gov/SRD/testsuite.php>

    Args:
        root (str): Directory of dataset, will automately create Juliet directory in it.
        download (bool, optional): If true, download dataset from internet, default false.
        proxy (str): The proxy for download.
            eg. 'http://user:pass@host:port/'
                'socks5://user:pass@host:port'

    """

    def __init__(self, datapath, download=True, proxy=None):
        super().__init__(datapath)
        self._casepath = self._rawpath / 'C' / 'testcases'
        if download:
            self.download(proxy)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Args:
            proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        url = DOWNLOAD_URL['juliet']
        print(f'Download from {url}')
        if not self._casepath.exists():
            download_file(url, self._rawpath, proxy)
            print('Download success, Start extracting.')
            # Extract download zip file
            zip_file = next(self._rawpath.glob('**/*.zip'))
            with zipfile.ZipFile(str(zip_file)) as z:
                z.extractall(str(self._rawpath))
        else:
            print(
                f"warn: {str(self._rawpath) + 'testcases/'}directory exist, download cancel"
            )

    def process(self, processor, category=None):
        """Process the selected data into vector by given processor and embedder
        
        Args:
            processor (covec.processor.Processor): The process methods
            embedder (covec.processor.WordsModel): The words embedding methods
            category (None, list): The parts of Juliet Test Suite used on dataset
                - None, default: use all categoary
                - 'AE': Arithmetic Expression
                - 'AF': API Function Call
                - 'AU': Array Usage
                - 'PU': Pointer Usage
        TODO:
        """
        pass

    def mark(self):
        selected = []
        fdecl = []
        num = 0
        for i in self._casepath.iterdir():
            if i.name.split('_')[0] in JULIET_CATEGORY['AF']:
                selected.append(i)
        for i in selected:
            flag = 0
            for file in i.glob('**/CWE*.[c,cpp]'):
                ast = loader_cc(str(file))
                pr = Parser(ast)
                decl = pr.walker(
                    lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
                flag += len(decl)
                fdecl.extend(decl)
                if flag >= 100:
                    break
            break
        for i in fdecl[:5]:
            pr = Parser(i)
            pr.graph('/home/verf/WorkSpace/Test/')
