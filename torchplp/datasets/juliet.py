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

    def load(self, category=None, coe=None, cache=True):
        if (self._rootp / 'train.pkl').exists():
            with open(self._rootp / 'train.pkl', 'rb') as f:
                train_x, train_l, train_y = pickle.load(f)
                print(sum(train_y))
            train_set = TorchPathSet(train_x, train_l, train_y)
        if (self._rootp / 'valid.pkl').exists():
            with open(self._rootp / 'valid.pkl', 'rb') as f:
                valid_x, valid_l, valid_y = pickle.load(f)
                print(sum(valid_y))
            valid_set = TorchPathSet(valid_x, valid_l, valid_y)
        if (self._rootp / 'tests.pkl').exists():
            with open(self._rootp / 'tests.pkl', 'rb') as f:
                tests_x, tests_l, tests_y = pickle.load(f)
                print(sum(tests_y))
            tests_set = TorchPathSet(tests_x, tests_l, tests_y)
        if (self._rootp / 'train.pkl').exists():
            return train_set, valid_set, tests_set
        if category is None:
            category = list(self._casep.iterdir())
        else:
            category = [y for x in category for y in self._casep.iterdir() if x in y.name]
        train = []
        valid = []
        tests = []
        for ind, f in enumerate(category):
            files = list(f.glob('**/*.*'))
            random.shuffle(files)
            file_num = len(files)
            print(f'load {category[ind]}, {file_num} samps')
            train_coe = round((coe[0]/sum(coe))*file_num)
            valid_coe = round((coe[1]/sum(coe))*file_num)
            tests_coe = file_num - train_coe - valid_coe
            train.extend(files[:train_coe])
            valid.extend(files[train_coe:train_coe+valid_coe])
            tests.extend(files[-tests_coe:])
        train_cache = self._cookp / 'train'
        train_cache.mkdir(parents=True, exist_ok=True)
        train_samps, train_labels = self._marker(train)
        train_x, train_l = self._processor(train_samps, train_cache)
        train_y = np.array(train_labels)
        valid_cache = self._cookp / 'valid'
        valid_cache.mkdir(parents=True, exist_ok=True)
        valid_samps, valid_labels = self._marker(valid)
        valid_x, valid_l = self._processor(valid_samps, valid_cache)
        valid_y = np.array(valid_labels)
        tests_cache = self._cookp / 'tests'
        tests_cache .mkdir(parents=True, exist_ok=True)
        tests_samps, tests_labels = self._marker(tests)
        tests_x, tests_l = self._processor(tests_samps, tests_cache)
        tests_y = np.array(tests_labels)
        with open(self._rootp / 'train.pkl', 'wb') as f:
            pickle.dump((train_x, train_l, train_y), f)
        with open(self._rootp / 'valid.pkl', 'wb') as f:
            pickle.dump((valid_x, valid_l, valid_y), f)
        with open(self._rootp / 'tests.pkl', 'wb') as f:
            pickle.dump((tests_x, tests_l, tests_y), f)
        train_set = TorchPathSet(train_x, train_l, train_y)
        valid_set = TorchPathSet(valid_x, valid_l, valid_y)
        tests_set = TorchPathSet(tests_x, tests_l, tests_y)
        return train_set, valid_set, tests_set

    def _select(self, category):
        category = [y for x in category for y in self._casep.iterdir() if x in y.stem][0]
        filt = lambda x: 'CWE' in x.stem and x.suffix in ['.c', '.cpp']
        files = [f for f in category.glob('**/*.*') if filt(f)]
        random.shuffle(files)
        f = files[0]
        print(f)
        asts, _ = self._marker([f])
        print(len(asts))
        for decl in asts:
            dot = decl.graph()
            dot.render('tmp.gv', view=True)
            for n in decl.walk():
                print(f'{n.data}-{n.kind}')
            break

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
                if str(node.data) == 'good':
                    continue
                labels.append(1.0 if 'bad' in str(node.data) else 0.0)
                asts.append(node)
        assert len(asts) == len(labels)
        return asts, labels
