# -*- coding: utf-8 -*-
"""
sysevr.py - The sysevr processing methods for datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
import re
import h5py
import numpy as np
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
        filter(lambda x: x and x not in [' ', ''], re.split(r'(\W|\s)', line)))


def cutlist(l, size):
    for i in range(0, len(l), size):
        yield l[i:i + size]


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
        # replace names
        for line in code:
            tokens = code_split(line)
            for ind, val in enumerate(tokens):
                if val in var_names:
                    tokens[ind] = 'var' + str(var_names.index(val))
                if val in fun_names:
                    tokens[ind] = 'fun' + str(fun_names.index(val))
                # some long data that can not parsed by libclang
                if re.match(r'^CWE\d{2,3}_.*Data$', val):
                    tokens[ind] = 'varx'
            symr.append(tokens)
        symr = [x for x in symr if x]
        symr_list.append([symr, label])
    return symr_list


def vectorlize(chunk, wm, tuncat):
    x_set = []
    y_set = []
    for symr, label in chunk:
        sent_set = [y for x in symr for y in wm.model[x]]
        if len(sent_set) < tuncat:
            padding = np.asarray([[0 for x in range(100)]
                                  for y in range(tuncat - len(sent_set))])
            sent_set.extend(padding)
            assert len(sent_set) == tuncat
        x_set.append(sent_set[:tuncat])
        y_set.append(int(label))
    return np.asarray(x_set), np.asarray(y_set)


def sysevr(root,
           file_list,
           type_,
           range_,
           wm_setting=dict(),
           chunks=None,
           tuncat=50):
    root = root + 'sysevr/'
    if not os.path.exists(root):
        os.makedirs(root)
    if type_ == 'sc':
        pass
    elif type_ == 'cgd':
        # load the range_ number of code gadget
        cgd_list = []
        for file in file_list:
            cgd_list.extend(loader_cgd(file))
            if range_ and len(cgd_list) > range_:
                cgd_list = cgd_list[:range_]
                break
        # get the symbolic representation splited in atom
        symr_list = symbolize(cgd_list)
        # train word model
        sent = [y for x in symr_list for y in x[0]]
        wm = Wordsmodel(sent, wm_setting)
        wm.save(root + 'sysevr.wm')
        # create vector representation
        if chunks:
            num = 0
            for chunk in cutlist(symr_list, chunks):
                X, Y = vectorlize(chunk, wm, tuncat)
                np.savez(root + f'sy_vec{num}.npz', X, Y)
                num += 1
        else:
            X, Y = vectorlize(symr_list, wm, tuncat)
            np.savez(root + 'sy_vec.npz', X, Y)

    else:
        raise ValueError(f"type_ must in ['sc', 'cgd', ]")
