# -*- coding: utf-8 -*-
"""
sysevr.py - The Text Model Processor

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
import numpy as np
from multiprocessing import cpu_count
from torchplp.processor.embedder import Word2Vec
from torchplp.utils.loader import loader_cc


def code_split(line):
    """split code line into atom
    
    Args:
        line (str): The code line
    
    Return:
        tokens (list): The list of atom token for code line

    """
    return list(
        filter(lambda x: x and x not in [' ', ''], re.split(r'(\W|\s)', line)))

def standardize(code):
    """
    This function replace the user-defined variable and function name
    to fixed name such as var0, var1 and fun0, fun1, which we called it
    standarlize.

    Args:
        code (list): The fragment of source code.

    Return:
        sr (list): The standarlize representation of source code

    """
    sr = []
    ast = loader_cc(code)
    var_names = list()
    fun_names = list()
    for node in ast.walk():
        if node.kind == 'VAR_DECL':
            var_names.append(node.data)
        if node.kind == 'FUNCTION_DECL':
            fun_names.append(node.data)
    for line in code:
        tokens = code_split(line)
        for ind, val in enumerate(tokens):
            if val in var_names:
                tokens[ind] = 'var' + str(var_names.index(val))
            if val in fun_names:
                tokens[ind] = 'fun' + str(fun_names.index(val))
            # some long data that can not parsed by libclang
            if re.match(r'^CWE\d{2,3}_.*Data$', val):
                tokens[ind] = f'var{str(len(var_names))}'
        sr.append(tokens)
    return sr

def vectorlize(sr, embedder):
    """
    This function converts the standarlized codes into a vector representation 
    through a words model.

    Args:
        sr (list): symbolic representation of code fragment

    Returns:
        vr (list): list of vector representation

    """
    vr = [embedder[word].tolist() for line in sr for word in line]
    return np.asarray(vr)

class CGDModel(object):
    """
    This methods is based on the paper VulDeePecker...(arXiv:1801.01681) but have little 
    difference, so we called it Text Model. Because this method treats the 
    program code as natural language text.

    """

    def __init__(self, embedder=None, pretrain=False):
        self._embedder = embedder
        self._pretrain = pretrain

    def __call__(self, data):
        sr = [standardize(x) for x in data]
        if not self._pretrain:
            sent = [sum(x, []) for x in sr]
            self._embedder.train(sent)
        vr = [vectorlize(x, self._embedder) for x in sr]
        return vr
