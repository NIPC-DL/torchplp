# -*- coding: utf-8 -*-
"""
test_juliet.py - test juliet class


Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
from covec.datasets import Juliet, Sysevr

test_path = os.path.expanduser('~/WorkSpace/Test/covec_test/')


def test_juliet():
    if not os.path.exists(test_path + 'Juliet_Test_Suite/Raw/'):
        data = Juliet(test_path, download=True, proxy='socks5://127.0.0.1:1080')
    else:
        data = Juliet(test_path, download=False)
    data.process(category=['AF', ])

def test_sysevr():
    if not os.path.exists(test_path + 'SySeVR/Raw/'):
        data = Sysevr(test_path, download=True)
    else:
        data = Sysevr(test_path, download=False)
    data.process(category=['AF', ])

if __name__ == '__main__':
    test_sysevr()