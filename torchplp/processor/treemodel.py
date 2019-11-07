# -*- coding: utf-8 -*-
"""
treemodel.py - transform AST into vectors

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import numpy as np
from torchplp.utils.astree import ASTNode

def standardize(root):
    var_names = []
    fun_names = []
    root.data = 'func_root'
    for node in root.walk():
        if node.kind == 'VAR_DECL':
            var_names.append(node.data)
        if 'CWE' in node.data and node.data not in fun_names:
            fun_names.append(node.data)
    for node in root.walk():
        if node.data in var_names:
            node.data = f'var{var_names.index(node.data)}'
        if node.data in fun_names:
            node.data = f'fun{fun_names.index(node.data)}'
    return root

def tree2seq(data, path='DFS'):
    """transform tree structrue to sequence"""
    sample = list()
    for node in data.walk(path):
        if node.spelling:
            sample.append(node.spelling)
        else:
            sample.append(node.kind)
    return sample

def vectorlize(data, embedder):
    """transform sequence data to its vector representation"""
    vr = []
    for node in data:
        try:
            vec = embedder[node[0]] if bool(node[0]) else embedder[node[1]]
        except Exception:
            vec = np.zeros(embedder.vector_size)
        vr.append(vec.tolist())
    vr = np.asarray(vr)
    return vr
