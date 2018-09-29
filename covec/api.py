# -*- coding: utf-8 -*-
from .parser import Parser_cc
from .loader import loader_cc


def parse(path, type_=None):
    """return appropriate Parser class

    :param path: the path of input file : string
    :param type_:optinal, the program of input file : string
    :return pr: Parser class : Parser
    """
    if not type_:
        type_ = path.split('.')[-1]
    if type_ in ['c', 'cpp']:
        pr = Parser_cc(path)
    else:
        raise ValueError(f'{type_} is not a correct file type')
    return pr
