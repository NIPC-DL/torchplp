# -*- coding: utf-8 -*-
"""
utils.py - The utils function for processor

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import re
import pprint
import hashlib


def line_split(line):
    return list(filter(lambda x: x not in [None, '', ' ', ';', '*'], re.split(r'(\(|\)|\s|\,|\;|\[|\*)', line)))

def line_split_plus(line):
    return list(filter(lambda x: x not in [None, '', ' '], re.split(r'(\*|\;|\!|\&|\,|\s|\(|\]|\[|\)|\-\>)', line)))

def remove_symbol(word):
    return re.sub(r'[\s!&-,;\)\*\[\]\(]', '', word)

def ppt(s):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(s)

def file_md5(file):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data =f.read(2048)
            if not data:
                break
            m.update(data)
    return str(m.hexdigest())
