# -*- coding: utf-8 -*-
"""
sysevr.py - The sysevr processing methods for datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import re
from . import utils
from .constants import KEYWORD, DEFINED
from .loader import loader_cgd, loader_cc
from .parser import Parser


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


def symbolize_r(cgd_list):
    sym_set = []
    for codes, label in cgd_list:
        var_list, func_list = _get_var_func(codes)
        syms = _var_replace(codes, var_list, func_list)
        sym_set.append([syms, label])
    return sym_set


def symbolize_l(cgd_list):
    symr_list = []
    for code, label in cgd_list:
        ast = loader_cc(code)
        pr = Parser(ast)
        var_decl = pr.walker(lambda x: x.kind == 'VAR_DECL')
        var_names = [x.data for x in var_decl]
        fun_decl = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
        fun_names = [x.data for x in fun_decl]


def sysevr(file_list, type_, sample_size, tuncat=50):
    if type_ == 'sc':
        pass
    elif type_ == 'cgd':
        cgd_list = []
        for file in file_list:
            cgd_list.extend(loader_cgd(file))
            if sample_size and len(cgd_list) > sample_size:
                cgd_list = cgd_list[:sample_size]
                break
        symr_list = symbolize_l(cgd_list)
    else:
        raise ValueError(f"type_ must in ['sc', 'cgd', ]")
