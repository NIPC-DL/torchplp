# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite (https://samate.nist.gov/SRD/testsuite.php)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
import random
import pathlib
import zipfile
from .models import TorchSet2
from torchplp.utils.loader import loader_cc
from torchplp.utils.utils import download_file

class JulietN(object):
    """Juliet Test Suite <https://samate.nist.gov/SRD/testsuite.php>

    Args:
        root (str): Directory of dataset, will automately create Juliet directory in it.
        download (bool, optional): If true, download dataset from internet, default false.
        proxy (str): The proxy for download.
            eg. 'http://user:pass@host:port/'
                'socks5://user:pass@host:port'

    """

    def __init__(self, root, download=True, proxy=None):
        root = pathlib.Path(root).expanduser()
        self._root = root / 'Juliet_Test_Suite'
        self._root.mkdir(parents=True, exist_ok=True)
        self._raw = self._root / 'raw'
        self._raw.mkdir(parents=True, exist_ok=True)
        self._case = self._raw / 'C' / 'testcases'
        self._split = self._root / 'split'
        self._split.mkdir(parents=True, exist_ok=True)
        if download:
            self.download(proxy)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Args:
            proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        url = 'https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.3_for_C_Cpp.zip'
        if not (self._raw / url.split('/')[-1]).exists():
            download_file(url, self._raw, proxy)
            # Extract download zip file
            zip_file = next(self._raw.glob('**/*.zip'))
            with zipfile.ZipFile(str(zip_file), 'r') as z:
                z.extractall(str(self._raw))

    def load(self, processor, category=None, ratio=[6,1,1]):
        train_files, valid_files, tests_files = self.data_split(category, ratio)
        train_samps, train_labels = self._marker(train_files)
        train_set = TorchSet2(train_samps, train_labels, processor)
        valid_samps, valid_labels = self._marker(valid_files)
        valid_set = TorchSet2(valid_samps, valid_labels, processor)
        tests_samps, tests_labels = self._marker(tests_files)
        tests_set = TorchSet2(tests_samps, tests_labels, processor)
        return train_set, valid_set, tests_set

    def data_split(self, category=None, ratio=[6,1,1]):
        """Split dataset into train, valid and tests set"""
        if category is None:
            dirs = list(self._case.iterdir())
        else:
            dirs = [d for d in self._case.iterdir() if d.stem.split('_')[0] in category]
        ratio = [x/sum(ratio) for x in ratio]
        train, valid, tests = [], [], []
        for d in dirs:
            filt = lambda x:'CWE' in x.stem and x.suffix in ['.c', '.cpp']
            files = [f for f in d.glob('**/*.*') if filt(f)]
            random.shuffle(files)
            file_len = len(files)
            train_ratio = round(file_len*ratio[0])
            valid_ratio = round(file_len*ratio[1])
            tests_ratio = file_len - train_ratio - valid_ratio
            train.extend(files[:train_ratio])
            valid.extend(files[train_ratio:train_ratio+valid_ratio])
            tests.extend(files[-tests_ratio:])
        return train, valid, tests

    @staticmethod
    def _marker(files):
        asts = []
        labels = []
        for file in files:
            ast = loader_cc(str(file))
            filt = lambda x: x.is_definition and x.kind == 'FUNCTION_DECL'
            decl = [x for x in ast.walk() if filt(x)]
            for node in decl:
                if 'main' in str(node.data):
                    continue
                node_list = list(node.walk())
                if len(node_list) < 5:
                    continue
                labels.append(0 if 'good' in str(node.data) else 1)
                asts.append(node)
        assert len(asts) == len(labels)
        return asts, labels
