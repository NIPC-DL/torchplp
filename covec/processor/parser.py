# -*- coding: utf-8 -*-
"""
parser.py - The data parser for covec

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from collections import deque
from covec.utils.astree import ASTNode


class Parser:
    """The AST Parser
    
    Args:
        root(covec.processor.ASTNode): The root node of AST
    """

    def __init__(self, root):
        if isinstance(root, ASTNode):
            self._root = root
        else:
            raise ValueError(f'{root} is not a ASTNode')

    def walker(self, selector=lambda x: True):
        """
        BFS every child of root and return selected node,
        if selector not given, return list of all node.

        Args:
            root(covec.processor.ASTNode): The root node of AST selector <function, optional>: select which node you want

        Return:
            selected(list): list of selected node
        """
        selected = []
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()
            for child in node.children:
                queue.append(child)
            if selector(node):
                selected.append(node)
        return selected