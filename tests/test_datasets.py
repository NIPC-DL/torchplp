# -*- coding: utf-8 -*-
"""
test_juliet.py - test juliet class


Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
from covec.datasets import Juliet, SySeVR
from covec.processor import TextModel, Word2Vec
from multiprocessing import cpu_count

test_path = os.path.expanduser('~/WorkSpace/Test/covec_test/')


def test_sysevr():
    wm = Word2Vec(size=20, min_count=1, workers=12)
    pr = TextModel(wm)
    dataset = SySeVR(test_path, pr, category=['AF'])
    train, valid = dataset.get_dataset(5)


if __name__ == '__main__':
    test_sysevr()