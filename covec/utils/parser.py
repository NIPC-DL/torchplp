# -*- coding: utf-8 -*-
"""
parser.py - The data parser for covec

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import clang.cindex as cc
from covec.utils.loader import loader_cc


class Parser:
    """covec.utils.Parser class"""

class Parser_cc(Parser):
    def __init__(self, data):
        self._root = loader_cc(data)

    def parse(self):
        pass

def parser(type_):
    """Return adopt Parser by given type
    
    Args:
    TODO: w
    
    Return:

    """
    pass