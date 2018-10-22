# -*- coding: utf-8 -*-
"""
sysevr.py - The sysevr processing methods for datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import re
from pprint import pprint
from .constants import KEYWORD, DEFINED
from .parser import Parser
from .embedding import Wordsmodel
from covec.utils.loader import loader_cgd, loader_cc


def code_split(line):
    """split code line into atom
    
    Args:
        line: The code line
    
    Return:
        tokens <list>: The list of atom token for code line
    """
    return list(
        filter(lambda x: x not in [None, ' ', ''], re.split(r'(\W|\s)', line)))


def symbolize(cgd_list):
    """transform code gadget to symbolic representation
    
    Args:
        cgd_list <list>: The list of code gadget, each code gadget is a list 
                         like [<codes>, <label>]
    
    Return:
        symr_list <list>: The symbolic representation list of code gadget, each
                          of it looks like [<codes in split>, <label>]
    """

    symr_list = []
    for code, label in cgd_list:
        symr = []
        ast = loader_cc(code)
        pr = Parser(ast)
        # get variable and function declaration
        var_decl = pr.walker(lambda x: x.kind == 'VAR_DECL')
        var_names = [x.data for x in var_decl]
        fun_decl = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
        fun_names = [x.data for x in fun_decl]
        for line in code:
            tokens = code_split(line)
            for ind, val in enumerate(tokens):
                if val in var_names:
                    tokens[ind] = 'var' + str(var_names.index(val))
                if val in fun_names:
                    tokens[ind] = 'fun' + str(fun_names.index(val))
                # some long data that can't found by libclang
                if re.match(r'^CWE\d{2,3}_.*Data$', val):
                    tokens[ind] = 'varx'
            symr.append(tokens)
        symr_list.append([symr, label])
    return symr_list


def sysevr(root, file_list, type_, sample_size, tuncat=50):
    if type_ == 'sc':
        pass
    elif type_ == 'cgd':
        # load the sample_size number of code gadget
        cgd_list = []
        for file in file_list:
            cgd_list.extend(loader_cgd(file))
            if sample_size and len(cgd_list) > sample_size:
                cgd_list = cgd_list[:sample_size]
                break
        # get the symbolic representation
        symr_list = symbolize(cgd_list)
        # train word model

    else:
        raise ValueError(f"type_ must in ['sc', 'cgd', ]")
