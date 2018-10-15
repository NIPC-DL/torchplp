# -*- coding: utf-8 -*-
"""
ast - defination of ast
"""
from collections import Iterable


class NodeType:
    def __init__(self):
        pass


class ASTNode:
    def __init__(self):
        self._parent = None
        self._children = list()
        self._id = None
        self._data = None
        self._type = None
        self._raw = None

    @property
    def parent(self):
        """Return Node parent"""
        return self._parent

    @property.setter
    def parent(self, node):
        """Set parent of Node"""
        if isinstance(node, ASTNode):
            self._parent = node
        else:
            raise ValueError(f'{node} is not a ASTNode')

    @property
    def children(self):
        """Return children of Node"""
        return self._children

    @property.setter
    def children(self, nodes):
        """Set children of Node"""
        if isinstance(nodes, Iterable):
            for n in nodes:
                if isinstance(n, ASTNode):
                    self._children.append(n)
                else:
                    raise ValueError(f'{n} is not a ASTNode')
        else:
            raise ValueError(f'{nodes} is not Iterable')

    @property
    def id(self):
        """Return Node id"""
        return self._id

    @property.setter
    def id(self, value):
        """Set id of Node"""
        self._id = str(value)

    @property
    def data(self):
        """Return Node data"""
        return self._data

    @property.setter
    def data(self, value):
        """Set data of Node"""
        self._data = str(value)

    @property
    def type(self):
        """Return type of Node"""
        return self._type

    @property.setter
    def type(self, value):
        pass

    @property
    def raw(self):
        """
        Return raw class of Node,
        raw class is a raw data created by each language parser,
        for c/cpp, raw means clang.cindex.Cursor.
        """
        return self._raw

    @property.setter
    def raw(self, value):
        """set raw data of node"""
        self._raw = value
