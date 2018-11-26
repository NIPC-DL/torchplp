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
import pickle
import torch
import numpy as np
from itertools import chain
from .models import Dataset
from .utils import download_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY
from .torchset import TorchSet
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

    def __init__(self,
                 root,
                 processor=None,
                 download=True,
                 proxy=None,
                 category=None):
        super(Juliet, self).__init__(root)
        self._casep = self._rawp / 'C' / 'testcases'
        # download dataset from internet
        if download:
            self.download(proxy)
        # process raw dataset by given processor
        if processor:
            self.process(processor, category)

    def __getitem__(self, index):
        return self._X[index], self._Y[index]

    def __len__(self):
        return len(self._Y)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Args:
            proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        url = DOWNLOAD_URL['juliet']
        print(f'Download from {url}')
        if not self._casep.exists():
            download_file(url, self._rawp, proxy)
            print('Download success, start extracting.')
            # Extract download zip file
            zip_file = next(self._rawp.glob('**/*.zip'))
            with zipfile.ZipFile(str(zip_file)) as z:
                z.extractall(str(self._rawp))
        else:
            print(
                f"Path {str(self._rawp) + 'testcases/'} exist, download cancel."
            )

    def process(self, processor, category):
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
            cache (bool, optional): If True, save the processed data in disk
            update (bool, optional): If true, create vector dataset whether or not file
                have already exist

        """
        Xp = self._cookp / f'{str(processor)}_X.p'
        Yp = self._cookp / f'{str(processor)}_Y.pt'
        if Xp.exists() and Yp.exists():
            print('Cache found, load from cache.')
            self._X = pickle.load(open(str(Xp)))
            self._Y = torch.load(str(Yp))
        else:
            marked, labels = self._marker(category)
            vrl = processor.process(vrl)
            print('Cooked success.')
            pickle.dump(
                marked, open(str(Xp)), protocol=pickle.HIGHEST_PROTOCOL)
            torch.save(labels, str(Yp))
            print('Cache saved success.')
            self._X = vrl
            self._Y = labels

    def _selector(self, category):
        if not category:
            category = ['AE', 'AF', 'AU', 'PU']
        category = list(chain(*[JULIET_CATEGORY[x] for x in category]))
        selected = [
            x for x in self._casep.iterdir()
            if x.name.split('_')[0] in category
        ]
        return set(selected)

    def _marker(self, category=None):
        files = self._selector(category)
        marked = []
        labels = []
        for ind, file in enumerate(files):
            for file in file.glob('**/CWE*.[c,cpp]'):
                fdecl = []
                ast = loader_cc(str(file))
                pr = Parser(ast)
                decl = pr.walker(
                    lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
                for node in decl:
                    if 'main' in str(node.data):
                        break
                    labels.append([1.0, 0.0] if 'bad' in
                                  str(node.data) else [0.0, 1.0])
                    fdecl.append(node)
                marked.extend(fdecl)
            if ind > 5:
                return marked, torch.Tensor(labels)