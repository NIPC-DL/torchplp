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

    def addChild(self, child):
        self._children.append(child)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value