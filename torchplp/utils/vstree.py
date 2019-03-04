# -*- coding: utf-8 -*-
"""
vstree.py - The Vector Syntax Tree

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""


class VSTNode:
    def __init__(self):
        self._parent = None
        self._children = []
        self._vector = None

    def to(self, dev):
        self._vector = self._vector.to(dev)
        for child in self._children:
            child.to(dev)
        return self

    def _to(self, dev):
        self._vector = self._vector.to(dev)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value