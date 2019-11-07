# -*- coding: utf-8 -*-
"""
loader.py - Load data for further processing

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from tempfile import NamedTemporaryFile
from concurrent import futures
from .astree import ASTNode, ASTKind
from ..core import *


def packer_cc(root: Cursor, filename: str) -> ASTNode:
    """Transform clang ast to torchplp ast

    Args:
        root (torchplp.cindex.Cursor): root of clang ast

    Return:
        ast (torchplp.utils.ASTNode): torchplp ast node

    """
    ast = ASTNode()
    ast.id = root.hash
    ast.data = root.spelling
    ast.kind = ASTKind(root.kind, 'cc')
    if ast.kind == 'BINARY_OPERATOR':
        for node in root.get_tokens():
            if node.kind == cc.TokenKind.PUNCTUATION:
                if node.spelling not in ['(', ')', '[', ']', '{', '}']:
                    ast.data = node.spelling
                    break
    ast.is_definition = root.is_definition()
    if ast.kind == 'FUNCTION_DECL':
        tokens = list()
        for tk in root.get_tokens():
            if tk.spelling == ast.data:
                tokens.append('func_root')
            elif tk.kind == cc.TokenKind.COMMENT:
                continue
            else:
                tokens.append(tk.spelling)
        ast.tokens = tokens
    for c in root.get_children():
        if str(c.location.file) != filename:
            continue
        child = packer_cc(c, filename)
        child.parent = ast
        ast.children.append(child)
    return ast


def loader_cc(data: Union[str, list], args: list=None) -> ASTNode:
    """Load c/c++ data (file or list of codes), return entry node

    This function load c/c++ source code file from path, the file can be
    incomplete but can't have too many errors.

    Args:
        path (str, list): path of the file
    
    Return:
        ast (torchplp.utils.ASTNode): Abstract Syntax Tree
    """
    index = cc.Index.create()
    if isinstance(data, list):
        with NamedTemporaryFile('w+t', suffix='.cpp') as tf:
            tf.write('\n'.join(data))
            tf.seek(0)
            tu = index.parse(tf.name, args)
    elif isinstance(data, str):
        tu = index.parse(data, args)
    else:
        raise ValueError(f'{data} must be a file path or list of code')
    return packer_cc(tu.cursor, str(tu.cursor.spelling))


def loader_cgd(path: str, spliter: str='-'*20) -> list:
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

    """
    samples = list()
    # labels = list()
    with open(path) as f:
        frag = list()
        for line in f:
            if spliter not in line:
                frag.append(line[:-1])
            else:
                if len(frag) < 3:
                   continue 
                cgd = frag[1:-1]
                if frag[-1] in ['0', '1']:
                    samples.append((cgd, int(frag[-1])))
                frag = list()
    return samples

def pool_loader(worker, callback, files, args):
    """create a multiprocessing pool to load files
    
    Args:
        worker(callable): load file from files
        callback(callable): callback function
        files(list): The file list
        args(list): Additional arguments for worker

    """
    with futures.ProcessPoolExecutor() as pool:
        for file in files:
            res = pool.submit(worker, file, args)
            res.add_done_callback(callback)
