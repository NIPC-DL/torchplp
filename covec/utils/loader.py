# -*- coding: utf-8 -*-
"""
loader.py - Load data for further processing

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import clang.cindex as cc
from .astree import ASTNode, ASTKind
from tempfile import NamedTemporaryFile


def packer_cc(root):
    """Transform clang ast to covec ast

    Args:
        root <clang.cindex.Cursor>: root of clang ast
    
    Return:
        ast <covec.utils.ast.ASTNode>: covec ast
    """
    ast = ASTNode()
    ast.id = root.hash
    if root.spelling:
        ast.data = root.spelling
    else:
        ast.data = root.displayname
    ast.kind = ASTKind(root.kind, 'cc')
    ast.raw = root
    for c in root.get_children():
        child = packer_cc(c)
        child.parent = ast
        ast.children.append(child)
    return ast


def loader_cc(data):
    """Load c/c++ file from path, return entry node

    This function load c/c++ source code file from path, the file can be
    incomplete but can't have too many errors.

    Args:
        path <str>: path of the file
    
    Return:
        ast <covec.utils.ast.ASTNode>: Abstract Syntax Tree
    """
    if isinstance(data, list):
        with NamedTemporaryFile('w+t', suffix='.cpp') as f:
            f.write('\n'.join(data))
            f.seek(0)
            index = cc.Index.create()
            tu = index.parse(f.name)
    else:
        index = cc.Index.create()
        tu = index.parse(data)
    return packer_cc(tu.cursor)


def loader_cgd(path):
    """Load code gadget file from path

    cgd file is a file looks like:
        < title >
        < function name >
        < code block >
        < label >
        < '-'*n, n>5 >
        < title >
        ...

    Args:
        path <str>: path of the file
    
    Return:
        set of cgd_list:
        (
            (cgd, label),
            ...
        )
    """
    cgd_list = []
    with open(path, 'r', encoding='utf-8') as f:
        frag = []
        for line in f:
            if '-' * 5 not in line:
                frag.append(line[:-1])
            else:
                cgd_list.append(frag)
                frag = []
    return ((x[2:-1], x[-1]) for x in cgd_list)