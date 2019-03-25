# -*- coding: utf-8 -*-
"""
parser.py - The data parser for covec

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from .models import Parser
from collections import deque
from torchplp.utils import ASTNode


class ASTParser(Parser):
    """The Abstract Syntax Tree ASTParser
    
    Args:
        root(torchplp.utils.ASTNode): The root node of AST

    """

    def __init__(self, root):
        if isinstance(root, ASTNode):
            self._root = root
        else:
            raise ValueError(f'{root} is not a ASTNode')

    def walker(self, selector=lambda x: True):
        """
        Breadth-First search every child of root and return selected node,
        if selector not given, return list of all node.

        Args:
            root (torchplp.utils.ASTNode): root node of AST
            selector (function, optional): function to select neeeded node

        Return:
            selected (list): list of selected node

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

    def walk(self):
        """
        Breadth-First search every child of root and return searched node.
        Generator style of walk
        """
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()
            for child in node.children:
                queue.appendleft(child)
            yield node
