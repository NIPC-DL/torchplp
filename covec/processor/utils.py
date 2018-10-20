# -*- coding: utf-8 -*-
"""
utils.py - Some usefully functions for processing

Author: Verf
Email: verf@protonmail.com
License: MIT
"""

import re
import clang.cindex as cc
import pprint
import hashlib


def remove_comment(text):
    """remove c/c++ style comments
    """
    return re.sub(r'//.*?\n|/\*.*?\*/', '', text, flags=re.S)


def deduplication(slice_set):
    res = []
    flag = True
    while slice_set:
        tmp = slice_set.pop(0)
        for i in slice_set:
            if tmp['slice'][1:] == i['slice'][1:]:
                flag = False
        if flag:
            res.append(tmp)
    return res


def line_split(line):
    return list(
        filter(lambda x: x not in [None, '', ' ', ';', '*'],
               re.split(r'(\(|\)|\s|\,|\;|\[|\*)', line)))


def remove_symbol(word):
    return re.sub(r'[\s!&-,;\)\*\[\]\(]', '', word)


def ppt(s):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(s)


def file_md5(file):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(2048)
            if not data:
                break
            m.update(data)
    return str(m.hexdigest())