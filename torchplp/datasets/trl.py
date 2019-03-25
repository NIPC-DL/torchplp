# -*- coding: utf-8 -*-
"""
trl.py - Transferable Representation Learning Dataset
(https://github.com/DanielLin1986/TransferRepresentationLearning)

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import pickle
import zipfile
import shutil
import random
import numpy as np
from .models import Dataset, TorchPathSet
from torchplp.utils.utils import git_clone_file
from torchplp.utils.loader import loader_cc
from torchplp.processor import ASTParser


class TRL(Dataset):
    def __init__(self, root, processor, download=True):
        super().__init__(root)
        self._processor = processor
        self._casep = self._rawp / 'Project_Six'
        if download:
            self.download()
        self.process()

    def download(self):
        URL = 'https://github.com/DanielLin1986/TransferRepresentationLearning'
        print(f'git clone from {URL}')
        clone_path = self._rawp / 'trl'
        if not clone_path.exists():
            git_clone_file(URL, str(clone_path))
            zip_path = clone_path / 'Data' / 'VulnerabilityData' / '6_projects_functions.zip'
            with zipfile.ZipFile(str(zip_path)) as z:
                z.extractall(str(self._casep))
        else:
            print(f'{str(clone_path)} exists, download cancel')

    def process(self):
        print('start processing')
        tx, ty, vx, vy = self._marker()
        tx = self._processor.process(tx)
        vx = self._processor.process(vx)
        assert len(tx) == len(ty)
        assert len(vx) == len(vy)
        pickle.dump((tx, ty),
                    open(str(self._cookp / 'train.p'), 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump((vx, vy),
                    open(str(self._cookp / 'valid.p'), 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, category=None, folds=None):
        print('start loading')
        tx, ty = pickle.load(open(str(self._cookp / 'train.p'), 'rb'))
        vx, vy = pickle.load(open(str(self._cookp / 'valid.p'), 'rb'))
        train_path = self._cache(tx, ty)
        valid_path = self._cache(vx, vy, train=False)
        train = TorchPathSet(train_path)
        valid = TorchPathSet(valid_path)
        return train, valid

    def _marker(self):
        tx = []
        ty = []
        vx = []
        vy = []
        for d in self._casep.iterdir():
            for file in d.glob('**/*.*'):
                ast = loader_cc(str(file))
                pr = ASTParser(ast)
                decl = pr.walker(
                    lambda x: x.is_definition and x.kind == 'FUNCTION_DECL')
                if len(decl) == 1:
                    x = decl[0]
                    y = 1.0 if 'cve' in file.name.lower() else 0.0
                else:
                    continue
                if random.random() > 0.3:
                    tx.append(x)
                    ty.append(y)
                else:
                    vx.append(x)
                    vy.append(y)
        print(len(tx), sum(ty))
        print(len(vx), sum(vy))
        return tx, ty, vx, vy

    def _cache(self, X, Y, train=True):
        T = 1000
        cachep = self._rootp / 'cache'
        cachep.mkdir(parents=True, exist_ok=True)
        datap = cachep / 'train' if train else cachep / 'valid'
        if datap.exists():
            # return datap
            shutil.rmtree(str(datap))
        datap.mkdir(parents=True, exist_ok=True)
        for i, x in enumerate(X):
            tmp = x[:]
            if len(tmp) < T:
                pad = np.zeros(((T - len(tmp)), len(tmp[0]))).tolist()
                tmp.extend(pad)
            else:
                tmp = x[:T]
            with open(str(datap / f'{i}.p'), 'wb') as f:
                pickle.dump(tmp, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(str(datap / 'Y.p'), 'wb') as f:
            pickle.dump(Y[:], f, protocol=pickle.HIGHEST_PROTOCOL)
        return datap
