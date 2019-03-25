# -*- coding: utf-8 -*-
"""
functional.py - The collection of process function

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import numpy as np
from torchplp.utils import ASTNode

def standardize(root):
    var_names = []
    fun_names = []
    for node in root.walk():
        if node.kind == 'VAR_DECL':
            var_names.append(node.data)
        if node.kind == 'FUNCTION_DECL':
            fun_names.append(node.data)
    for node in root.walk():
        if node.data in var_names:
            node.data = f'var{var_names.index(node.data)}'
        if node.data in fun_names:
            node.data = f'fun{fun_names.index(node.data)}'
    return root

def tree2seq(data, path):
    assert isinstance(data, ASTNode)
    return list(data.walk(path))

def vectorlize(data, embedder):
    vr = []
    for node in data:
        vec = embedder[node.data] if node.data else embedder[node.kind]
        vr.append(vec.tolist())
    return np.asarray(vr)

def padding(data, max_length, word_size):
    real_length = data.shape(0)
    if data.shape(0) < max_length:
        pad = np.zeros((length-data.shape(0), word_size))
        data = np.concatenate((data, pad), axis=0)
    return data, real_length
