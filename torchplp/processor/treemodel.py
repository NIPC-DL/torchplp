# -*- coding: utf-8 -*-
"""
treemodel.py - transform AST into vectors

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""

def standardize(root):
    var_names = []
    fun_names = []
    root.data = 'func_name'
    for node in root.walk():
        if node.kind == 'VAR_DECL':
            var_names.append(node.data)
        if 'CWE' in node.data or 'good' in node.data and node.data not in fun_names:
            fun_names.append(node.data)
    for node in root.walk():
        if node.data in var_names:
            node.data = f'var{var_names.index(node.data)}'
        if node.data in fun_names:
            node.data = f'fun{fun_names.index(node.data)}'
    return root

def tree2seq(data, path='DFS'):
    """transform tree structrue to sequence"""
    assert isinstance(data, ASTNode)
    return list(data.walk(path))

def vectorlize(data, embedder):
    """transform sequence data to its vector representation"""
    vr = []
    for node in data:
        try:
            vec = embedder[node.data] if node.data else embedder[node.kind]
        except Exception:
            vec = np.zeros(embedder.vector_size)
        vr.append(vec.tolist())
    vr = np.array(vr)
    return vr

class TreeModel(object):
    """transform ASTs into vectors"""
    def __init__(self, embedder=None, pretrain=False):
        self._embedder = embedder
        self._pretrain = pretrain

    def __call__(self, nodes):
        samples = list()
        for node in nodes:
            x = standardize(node)
            x = tree2seq(x)
            if not self._pretrain:
                self._embedder.train(x)
            x = vectorlize(x, self._embedder)
            samples.append(x)
        return samples

