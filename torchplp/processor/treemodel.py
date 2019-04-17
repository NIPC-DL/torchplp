# -*- coding: utf-8 -*-
"""
treemodel.py - transform AST into vectors

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import numpy as np
import torchplp.processor.functional as F
from torchplp.models import jsix

class Treemodel(object):
    """transform ASTs into vectors"""
    def __init__(self, wm=None, length=None):
        self._wm = wm
        self._length = length

    def __call__(self, nodes, cache=None):
        samps = []
        assert len(nodes) != 0
        for node in nodes:
            x = F.standardize(node)
            x = F.tree2seq(x)
            if self._wm is None:
                self._wm = jsix()
            x = F.vectorlize(x, self._wm)
            samps.append(x)
        if self._length is None:
            max_len = max([len(x) for x in samps])
        else:
            max_len = self._length
        vectors = []
        lengths = []
        for ind, samp in enumerate(samps):
            x, l = F.padding(samp, max_len, self._wm.vector_size)
            assert x.shape[0] == max_len
            if cache is not None:
                np.save(str(cache/f'{ind}.npy'), x)
                vectors.append(cache/f'{ind}.npy')
            else:
                vectors.append(x)
            lengths.append(l)
        assert len(vectors) == len(lengths)
        return vectors, np.array(lengths)

