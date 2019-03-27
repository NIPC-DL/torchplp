# -*- coding: utf-8 -*-
"""
treemodel.py - transform AST into vectors

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import torchplp.processor.functional as F
from torchplp.models import jsix

class Treemodel(object):
    """transform ASTs into vectors"""
    def __init__(self, wm=None):
        self.wm = wm

    def __call__(self, nodes):
        tmps = []
        samp_lens = []
        for node in nodes:
            x = F.standardize(node)
            x = F.tree2seq(x)
            if wm is None:
                self.wm = jsix()
            x = F.vectorlize(x, self.wm)
            tmps.append(x)
        max_len = max([len(x) for x in tmps])
        samps = []
        for x in tmps:
            x, l = F.padding(x, max_len, self.wm.vector_size)
            samps.append(x)
            samp_lens.append(l)
        return samps, samp_lens

