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
import numpy as np
from itertools import chain
from .utils import download_file
from .constants import DOWNLOAD_URL, JULIET_CATEGORY
from .models import Dataset
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

    def process(self, processor, category=None, cache=True, update=False):
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
        saved_path = self._cookedpath / f'{str(processor).lower()}_vec.p'
        if update or not saved_path.exists():
            marked, labels = self.marker(category)
            vrl = processor.process(marked)
            print(f'found {saved_path.name}, load cache.')
        else:
            vrl, labels = pickle.load(open(str(saved_path), 'rb'))
        self._X = vrl
        self._Y = labels
        if cache:
            pickle.dump((vrl, labels),
                        open(str(saved_path), 'wb'),
                        protocol=pickle.HIGHEST_PROTOCOL)

    def torchset(self, name=None):
        """Return the Pytorch Dataset Object

        Args:
            name (str, None): The name of process methods, if not set,
                will return the lastest processed data

        """
        if name:
            vrl, labels = pickle.load(
                str(self._cookedpath / f'{name.lower()}_vec.p'))
            X = vrl
            Y = labels
            tset = TorchSet(X, Y, 'tree')
        else:
            tset = TorchSet(self._X, self._Y, 'tree')
        return tset

    def _selector(self, category):
        if not category:
            category = ['AE', 'AF', 'AU', 'PU']
        category = list(chain(*[JULIET_CATEGORY[x] for x in category]))
        selected = [
            x for x in self._casepath.iterdir()
            if x.name.split('_')[0] in category
        ]
        return set(selected)

    def marker(self, category=None):
        files = self._selector(category)
        marked = []
        labels = []
        for ind, file in enumerate(files):
            for file in file.glob('**/CWE*.[c,cpp]'):
                marked_decl = []
                ast = loader_cc(str(file))
                pr = Parser(ast)
                decl = pr.walker(
                    lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
                for node in decl:
                    if 'main' in str(node.data):
                        break
                    node.source = file.name
                    if 'bad' in str(node.data):
                        labels.append(np.array([1.0, 0.0]))
                    else:
                        labels.append(np.array([0.0, 1.0]))
                    marked_decl.append(node)
                marked.extend(marked_decl)
            if ind > 5:
                return marked, labels
