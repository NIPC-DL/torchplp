# -*- coding: utf-8 -*-
"""
textmodel.py - transform AST into text data

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
    tokens = []
    if not root.tokens:
        print(root.tokens)
    tokens[:] = root.tokens
    for ind, token in enumerate(tokens):
        if token in var_names:
            tokens[ind] = f'var{var_names.index(token)}'
        if token in fun_names:
            tokens[ind] = f'fun{fun_names.index(token)}'
        if 'good' in token.lower() or 'bad' in token.lower():
            tokens[ind] = 'varx'
    return tokens

def vectorlize(data, embedder):
    vr = []
    for token in data:
        try:
            vec = embedder[token]
        except Exception:
            vec = np.zeros(embedder.vector_size)
        vr.append(vec.tolist())
    vr = np.asarray(vr)
    return vr
