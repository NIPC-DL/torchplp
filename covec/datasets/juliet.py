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
import random
import torch
import numpy as np
from collections import deque
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

    def __init__(self, root, processor=None, download=True, proxy=None):
        super(Juliet, self).__init__(root)
        self._casep = self._rawp / 'C' / 'testcases'
        # download dataset from internet
        if download:
            self.download(proxy)
        # process raw dataset by given processor
        if processor:
            self.process(processor)

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
            print('Download success, start extracting')
            # Extract download zip file
            zip_file = next(self._rawp.glob('**/*.zip'))
            with zipfile.ZipFile(str(zip_file)) as z:
                z.extractall(str(self._rawp))
            print('Extracting success')
        else:
            print(
                f"Path {str(self._rawp / 'testcases')} exist, download cancel."
            )

    def process(self, processor):
        for case in self._casep.iterdir():
            cwep = self._cookp / f"{case.name.split('_')[0]}.p"
            if cwep.exists():
                continue
            files = case.glob('**/CWE*.[c,cpp]')
            asts, labels = self._marker(files)
            vsts = processor.process(asts)
            assert len(vsts) == len(labels)
            pickle.dump((vsts, labels),
                        open(str(cwep), 'wb'),
                        protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, category, folds):
        tx, ty = [], []
        vx, vy = [], []
        for num in category:
            cwep = self._cookp / f"{num.upper()}.p"
            if cwep.exists():
                vsts, labels = pickle.load(open(str(cwep), 'rb'))
                data = list(zip(vsts, labels))
                random.shuffle(data)
                vsts, labels = zip(*data)
                assert len(vsts) == len(labels)
                lens = len(vsts)
                if folds:
                    coe = round((folds - 1) / folds * lens)
                    tx.extend(vsts[:coe])
                    ty.extend(labels[:coe])
                    vx.extend(vsts[coe:])
                    vy.extend(labels[coe:])
                else:
                    tx.extend(vsts)
                    ty.extend(labels)
        train = TorchSet(tx, torch.Tensor(ty).long())
        valid = TorchSet(vx, torch.Tensor(vy).long())
        print(f"load {len(train)}")
        print(f"load {len(valid)}")
        return train, valid

    @staticmethod
    def _marker(files):
        asts = []
        labels = []
        for file in files:
            sel = []
            ast = loader_cc(str(file))
            pr = Parser(ast)
            decl = pr.walker(
                lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
            for node in decl:
                if 'main' in str(node.data):
                    break
                labels.append(0.0 if 'good' in str(node.data) else 1.0)
                sel.append(node)
            asts.extend(decl)
        return asts, labels
