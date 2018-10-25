# -*- coding: utf-8 -*-
"""
test_juliet.py - test juliet class


Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
from covec.datasets import Juliet, SySeVR
from covec.processor import Textmod, Word2Vec
from multiprocessing import cpu_count

test_path = os.path.expanduser('~/WorkSpace/Test/covec_test/')


def test_juliet():
    if not os.path.exists(test_path + 'Juliet_Test_Suite/Raw/'):
        data = Juliet(
            test_path, download=True, proxy='socks5://127.0.0.1:1080')
    else:
        data = Juliet(test_path, download=False)
    data.process(category=[
        'AF',
    ])


def test_sysevr():
    if not os.path.exists(test_path + 'SySeVR/Raw/'):
        dataset = SySeVR(test_path, download=True)
    else:
        dataset = SySeVR(test_path, download=False)
    x_set, y_set = dataset.data([
        'AF',
    ])
    wm = Word2Vec(size=20, min_count=1, workers=12)
    pr = Textmod(wm)
    pr.process(test_path + 'SySeVR/', x_set, 'cgd')
    wm.save(test_path + 'SySeVR/Cooked/wm.model')


if __name__ == '__main__':
    test_sysevr()