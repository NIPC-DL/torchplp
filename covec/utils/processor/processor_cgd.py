# -*- coding: utf-8 -*-
"""
processor_cgd.py - The processor method for code gadget datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import re
from . import utils
from .constants import KEYWORD, DEFINED
from covec.utils.loader import loader_cgd
from .model import Processor


def _get_var_from_defined(tokens):
    defin = list(set([x for x in tokens if x in DEFINED]))
    var_list = []
    if defin:
        index = tokens.index(defin[0])
        try:
            var_list.append(utils.remove_symbol(tokens[index + 1]))
        except IndexError:
            pass
    return [x for x in var_list if x not in KEYWORD + [None, '', ' ']]


def _get_var_from_regexp(tokens):
    var_list = []
    for tok in tokens:
        rep = re.search(r'^\w{1,10}_\w{1,10}[^(]$', tok)
        if rep:
            var_list.append(utils.remove_symbol(rep.group(0)))
    return list(
        filter(
            lambda x: x not in KEYWORD + DEFINED + [None, '', ' '] and x.find('(') == -1,
            var_list))


def _get_func_from_regxp(tokens):
    func_list = []
    for tok in tokens:
        rep = re.search(r"^CWE[\w:~]*\(?\)?$", tok)
        if rep:
            func_list.append(utils.remove_symbol(rep.group(0)))
    return func_list


def _get_var_func(codes):
    var_list = []
    func_list = []
    for line in codes:
        tokens = utils.line_split(line)
        var_list += _get_var_from_defined(tokens) + _get_var_from_regexp(
            tokens)
        func_list += _get_func_from_regxp(tokens)
    return var_list, func_list


def _var_replace(codes, var_list, func_list):
    syms = []
    var_list.sort()
    for line in codes:
        tokens = utils.line_split_plus(line)
        for k, v in enumerate(tokens):
            if v in var_list:
                tokens[k] = "VAR" + str(var_list.index(v))
            if v in func_list:
                tokens[k] = "FUNC" + str(func_list.index(v))
        syms.append(' '.join(tokens))
    assert len(syms) > 0
    return syms


class Processor_cgd(Processor):
    """The processor for code gadget file
    
    Args:
        None
    """

    def __init__(self):
        pass

    def process(self, path):
        cgd_list = loader_cgd(path)
        symr_list = self.symbolize_r(cgd_list)

    def symbolize_r(self, cgd_list):
        sym_set = []
        for codes, label in cgd_list:
            var_list, func_list = _get_var_func(codes)
            syms = _var_replace(codes, var_list, func_list)
            sym_set.append([syms, label])
        return sym_set

    def symbolize_l(self, cgd_list):
        pass
