# -*- coding: utf-8 -*-
"""
parser.py - The data parser for covec

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from graphviz import Digraph
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

    def walk(self):
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()
            for child in node.children:
                queue.append(child)
            yield node

    def graph(self, path):
        dot = Digraph(comment='Abstract Syntax Tree')
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()
            dot.node(str(node.id), f'{node.data}\n{node.kind}')
            for child in node.children:
                queue.append(child)
                dot.node(str(child.id), f'{child.data}\n{child.kind}')
                dot.edge(str(node.id), str(child.id))
        dot.render(path + f'{self._root.data}_ast.gv', view=True)