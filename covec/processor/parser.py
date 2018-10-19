# -*- coding: utf-8 -*-
"""
parser.py - The data parser for covec

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import clang.cindex as cc
from .loader import loader_cc


class Parser:
    """Upper class"""


class Parser_cc(Parser):
    """The Parser for c/c++ data
    
    Args:
        data <list, str>: list of data or data file path

    """

    def __init__(self, data):
        self._root = loader_cc(data)


def parse(data, type_):
    """Return adopt Parser by given type
    
    Args:
        data <list, str>: list of data or data file path
        type_ <str>: the program language of input data
            - 'cc': c/c++ code data
    
    Return:
        pr <covec.processor.parser.Parser>: The Parser Object

    """
    if type_ == 'cc':
        pr = Parser_cc(data)
    else:
        raise ValueError(f'Worry Parser Type: {type_}')
    return pr