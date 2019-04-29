# -*- coding: utf-8 -*-
"""
treemodel.py - transform AST into vectors

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import torchplp.processor.functional as F
from torchplp.models import jsix

class TreeModel(object):
    """transform ASTs into vectors"""
    def __init__(self, embedder=None):
        self._embedder = embedder

    def __call__(self, nodes):
        samples = list()
        for node in nodes:
            x = F.standardize(node)
            x = F.tree2seq(x)
            if self._embedder is None:
                self._embedder = jsix()
            x = F.vectorlize(x, self._embedder)
            samples.append(x)
        return samples

