# -*- coding: utf-8 -*-
"""
loader.py - Load data for further processing

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import fileinput
import clang.cindex as cc
from .astree import ASTNode, ASTKind
from tempfile import NamedTemporaryFile


def packer_cc(root):
    """Transform clang ast to covec ast

    Args:
        root (clang.cindex.Cursor): root of clang ast
    
    Return:
        ast (covec.utils.ast.ASTNode): covec ast
    """
    ast = ASTNode()
    ast.id = root.hash
    if root.spelling:
        ast.data = root.spelling
    else:
        ast.data = root.displayname
    ast.kind = ASTKind(root.kind, 'cc')
    ast.is_definition = root.is_definition()
    for c in root.get_children():
        child = packer_cc(c)
        child.parent = ast
        ast.children.append(child)
    return ast


def loader_cc(data):
    """Load c/c++ data (file or list of codes), return entry node

    This function load c/c++ source code file from path, the file can be
    incomplete but can't have too many errors.

    Args:
        path (str): path of the file
    
    Return:
        ast (covec.utils.ast.ASTNode): Abstract Syntax Tree
    """
    index = cc.Index.create()
    if isinstance(data, list):
        with NamedTemporaryFile('w+t', suffix='.cpp') as tf:
            tf.write('\n'.join(data))
            tf.seek(0)
            tu = index.parse(tf.name)
    else:
        tu = index.parse(data)
    return packer_cc(tu.cursor)


def loader_cgd(path):
    """Load code gadget file from path

    cgd file is a file looks like:
        ...
        title
        function name
        code block
        label
        '-'*n, n>5
        title
        ...

    Args:
        path (str): path of the file
    
    Return:
        x_set (list): code blocks
        y_set (list): labels
    """
    x_set = []
    y_set = []
    with open(path) as f:
        frag = []
        for line in f:
            if '-' * 5 not in line:
                frag.append(line[:-1])
            else:
                x_set.append(frag[2:-1])
                y_set.append(int(frag[-1]))
                frag = []
    return x_set, y_set
