# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite (https://samate.nist.gov/SRD/testsuite.php)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
import numpy as np
import zipfile
import pickle
import random
from torchplp.utils.loader import loader_cc
from torchplp.utils.utils import download_file
from .models import Dataset, TorchPathSet

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
            self._processor = processor

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Args:
            proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        url = 'https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.3_for_C_Cpp.zip'
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

            def process(self, cwep):
                pass

    def load(self, category=None, coe=None, cache=True):
        if (self._rootp / 'train.pkl').exists():
            with open(self._rootp / 'train.pkl', 'rb') as f:
                train = pickle.load(f)
            with open(self._rootp / 'valid.pkl', 'rb') as f:
                valid = pickle.load(f)
            with open(self._rootp / 'tests.pkl', 'rb') as f:
                tests = pickle.load(f)
            train_set = TorchPathSet(train)
            valid_set = TorchPathSet(valid)
            tests_set = TorchPathSet(tests)
            return  train_set, valid_set, tests_set
        if category is None:
            category = list(self._casep.iterdir())
        else:
            category = [y for x in category for y in self._casep.iterdir() if x in y.name]
        train = {'x':[], 'y':[]}
        valid = {'x':[], 'y':[]}
        tests = {'x':[], 'y':[]}
        for ind, f in enumerate(category):
            files = list(f.glob('**/*.*'))
            samps, labels = self._marker(files)
            assert len(samps) == len(labels) != 0
            data = list(zip(samps, labels))
            random.shuffle(data)
            samps, labels = zip(*data)
            samp_lens = len(samps)
            print(f'load {category[ind]}, {samp_lens} samps')
            train_coe = round((coe[0]/sum(coe))*samp_lens)
            valid_coe = round((coe[1]/sum(coe))*samp_lens)
            tests_coe = samp_lens - train_coe - valid_coe
            train['x'].extend(samps[:train_coe])
            train['y'].extend(labels[:train_coe])
            valid['x'].extend(samps[train_coe:train_coe+valid_coe])
            valid['y'].extend(labels[train_coe:train_coe+valid_coe])
            tests['x'].extend(samps[-tests_coe:])
            tests['y'].extend(labels[-tests_coe:])
        train_cache = self._cookp / 'train'
        train_cache.mkdir(parents=True, exist_ok=True)
        train['x'], train['l'] = self._processor(train['x'], train_cache)
        train['y'] = np.array(train['y'])
        valid_cache = self._cookp / 'valid'
        valid_cache.mkdir(parents=True, exist_ok=True)
        valid['x'], valid['l'] = self._processor(valid['x'], valid_cache)
        valid['y'] = np.array(valid['y'])
        tests_cache = self._cookp / 'valid'
        tests_cache .mkdir(parents=True, exist_ok=True)
        tests['x'], tests['l'] = self._processor(tests['x'], tests_cache)
        tests['y'] = np.array(tests['y'])
        with open(self._rootp / 'train.pkl', 'wb') as f:
            pickle.dump(train, f)
        with open(self._rootp / 'valid.pkl', 'wb') as f:
            pickle.dump(valid, f)
        with open(self._rootp / 'tests.pkl', 'wb') as f:
            pickle.dump(tests, f)
        train_set = TorchPathSet(train)
        valid_set = TorchPathSet(valid)
        tests_set = TorchPathSet(tests)
        return train_set, valid_set, tests_set

    @staticmethod
    def _marker(files):
        asts = []
        labels = []
        for file in files:
            if re.match(r'^CWE.*\.(c|cpp)$', file.name) is None:
                continue
            ast = loader_cc(str(file))
            decl = [x for x in ast.walk() if x.is_definition and x.kind == 'FUNCTION_DECL']
            for node in decl:
                if 'main' in str(node.data):
                    continue
                node_list = list(node.walk())
                if len(node_list) < 5:
                    continue
                labels.append(1 if 'bad' in str(node.data) else 0)
                asts.append(node)
        assert len(asts) == len(labels)
        return asts, labels
