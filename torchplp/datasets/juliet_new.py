# -*- coding: utf-8 -*-
"""
juliet.py - Juliet Test Suite (https://samate.nist.gov/SRD/testsuite.php)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import pathlib
import zipfile
import torch
import torch.utils.data as data
from torchplp.utils.utils import download_file, i2h
from torchplp.utils.loader import loader_cc

url = 'https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.3_for_C_Cpp.zip'

class JulietN(data.Dataset):
    def __init__(self,
                 root,
                 category=None,
                 processor=default_processor,
                 label_type='onehot',
                 download=True,
                 proxy=None):
        self._root = pathlib.Path(root).expanduser()
        self._root = self._root / 'Juliet'
        self._root.mkdir(parents=True, exist_ok=True)
        self._case = self._root / 'C' / 'testcases'
        self._processor = processor
        if download:
            self.download(proxy)
        assert label_type in ['int', 'float', 'onehot']
        self._label_type = label_type
        self.process()
        x, self._y, self._dist = self.load(category)
        self._x, self._len = self.process(x)

    def __getitem__(self, index):
        x = self._x[index]
        l = self._len[index]
        y = self._y[index]
        x = torch.from_numpy(x)
        y = self._label_transform(y)
        return x, l, y

    def __len__(self):
        return len(self._y)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Args:
            proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

        """
        print(f'Download from {url}')
        if not self._case.exists():
            download_file(url, self._root, proxy)
            print('Download success, start extracting')
            # Extract download zip file
            zip_file = next(self._root.glob('**/*.zip'))
            with zipfile.ZipFile(str(zip_file)) as z:
                z.extractall(str(self._root))
            print('Extracting success')
        else:
            print(f"Path {str(self._case)} exist, download cancel.")

    def process(x):
        x, lens = self._processor(x)
        return x, lens

    def load(self, category):
        dist = [0]
        functs = []
        labels = []
        if not category:
            category = [
                i.name.split('_')[0] for i in self._case.iterdir()
                if 'CWE' in i.name
            ]
        for cwe in self._case.iterdir():
            if cwe.name.split('_')[0] in category:
                for file in cwe.glob('**/CWE*.[c,cpp]'):
                    ast = loader_cc(str(file))
                    tmp = 0
                    for node in ast.walk():
                        if node.kind == 'FUNCTION_DECL':
                            node_list = list(node.walk())
                            if len(node_list) < 5:
                                continue
                            functs.append(node)
                            labels.append(0 if 'good' in node.data else 1)
                            tmp += 1
                    dist.append(tmp)
        assert len(functs) == len(labels)
        assert len(category) == len(dist)-1
        return functs, labels, dist

    def _label_transform(self, y):
        if self._label_type == 'int':
            y = torch.IntTensor(y)
        elif self._label_type == 'float':
            y = torch.FloatTensor(y)
        else:
            y = i2h(y, 2)
        return y

    @property
    def dist(self):
        return self._dist

