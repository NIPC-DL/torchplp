# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite (https://samate.nist.gov/SRD/testsuite.php)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import zipfile
import pickle
import random
import shutil
import numpy as np
from .models import Dataset, TorchPathSet
from .utils import download_file
from .constants import DOWNLOAD_URL
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
            x, y = self._marker(files)
            x = processor.process(x)
            assert len(x) == len(y)
            pickle.dump((x, y),
                        open(str(cwep), 'wb'),
                        protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, category=None, folds=None):
        tx, ty = [], []
        vx, vy = [], []
        if not category:
            category = [i.name for i in self._cookp.glob('**/*p')]
        for num in category:
            cwep = self._cookp / f"{num.upper()}.p"
            if cwep.exists():
                x, y = pickle.load(open(str(cwep), 'rb'))
                print(f'Load {str(cwep)}')
                data = list(zip(x, y))
                random.shuffle(data)
                x, y = zip(*data)
                assert len(x) == len(y)
                lens = len(x)
                if folds:
                    coe = round((folds - 1) / folds * lens)
                    tx.extend(x[:coe])
                    ty.extend(y[:coe])
                    vx.extend(x[coe:])
                    vy.extend(y[coe:])
                else:
                    tx.extend(x)
                    ty.extend(y)
        assert len(tx) == len(ty)
        print('Start train cache')
        train_path = self._cache2(tx, ty)
        train = TorchPathSet(train_path)
        print(f'Load train {len(train)}')
        valid = None
        if bool(vx):
            assert len(vx) == len(vy)
            print('Start valid cache')
            valid_path = self._cache2(vx, vy, train=False)
            valid = TorchPathSet(valid_path)
            print(f'Load valid {len(valid)}')
        return train, valid

    @staticmethod
    def _marker(files):
        asts = []
        labels = []
        for file in files:
            ast = loader_cc(str(file))
            pr = Parser(ast)
            decl = pr.walker(
                lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
            for node in decl:
                if 'main' in str(node.data):
                    continue
                pr = Parser(node)
                node_list = pr.walker()
                if len(node_list) < 5:
                    continue
                labels.append(0 if 'good' in str(node.data) else 1)
                asts.append(node)
        assert len(asts) == len(labels)
        return asts, labels

    def _cache(self, X, Y, train=True):
        cachep = self._rootp / 'cache'
        cachep.mkdir(parents=True, exist_ok=True)
        datap = cachep / 'train' if train else cachep / 'valid'
        if datap.exists():
            # return datap
            shutil.rmtree(str(datap))
        datap.mkdir(parents=True, exist_ok=True)
        max_len = max([len(x) for x in X])
        print(f'max length: {max_len}')
        for i, x in enumerate(X):
            tmp = x[:]
            pad = np.zeros(((max_len-len(x)), len(x[0]))).tolist()
            tmp.extend(pad)
            with open(str(datap / f'{i}.p'), 'wb') as f:
                pickle.dump(tmp, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(str(datap / 'Y.p'), 'wb') as f:
            pickle.dump(Y[:], f, protocol=pickle.HIGHEST_PROTOCOL)
        return datap

    def _cache2(self, X, Y, train=True):
        cachep = self._rootp / 'cache'
        cachep.mkdir(parents=True, exist_ok=True)
        datap = cachep / 'train' if train else cachep / 'valid'
        if datap.exists():
            # return datap
            shutil.rmtree(str(datap))
        datap.mkdir(parents=True, exist_ok=True)
        for i, x in enumerate(X):
            tmp = x[:]
            if len(tmp) < 433:
                pad = np.zeros(((433-len(tmp)), len(tmp[0]))).tolist()
                tmp.extend(pad)
            else:
                tmp = x[:433]
            with open(str(datap / f'{i}.p'), 'wb') as f:
                pickle.dump(tmp, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(str(datap / 'Y.p'), 'wb') as f:
            pickle.dump(Y[:], f, protocol=pickle.HIGHEST_PROTOCOL)
        return datap
