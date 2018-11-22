# -*- coding: utf-8 -*-
"""
test_juliet.py - test juliet class


:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import sys
from covec.datasets import Juliet, SySeVR
from covec.processor import TextModel, TreeModel, Word2Vec, Parser
from multiprocessing import cpu_count
from torch.utils.data import DataLoader

test_path = os.path.expanduser('~/WorkSpace/Data')


def test_sysevr():
    wm = Word2Vec(size=50, min_count=1, workers=12)
    pr = TextModel(wm)
    dataset = SySeVR(test_path)
    dataset.process(pr, category=['AF'])
    trochset = dataset.torchset()
    print(type(trochset))


def test_juliet():
    wm = Word2Vec(size=50, min_count=1, workers=12)
    pr = TreeModel(wm, 100)
    dataset = Juliet(
        test_path,
        processor=pr,
        download=False,
        proxy='socks5://127.0.0.1:1080',
        category=[
            'AF',
        ])


if __name__ == '__main__':
    # test_juliet()
    # test_sysevr()
    from covec.utils.loader import loader_cc
    root = loader_cc(sys.argv[1])
    pr = Parser(root)
    func = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
    for i in func:
        pr = Parser(i)
        pr.graph('/home/verf/WorkSpace/Test/graph/')