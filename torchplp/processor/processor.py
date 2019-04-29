# -*- coding: utf-8 -*-
"""
processor.py - Processor Class

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from . import functional as F
from .models import Processor

__all__ = ['Compose', 'Standardize', 'Tree2Seq', 'Vectorlize']


class Compose(object):
    """Composes several transforms together.
    Args:
        processors (list of ``Processor`` objects): list of processors to compose.

    """

    def __init__(self, processors):
        assert isinstance(processors, list)
        self._processors = processors

    def __call__(self, data):
        for p in self._processors:
            assert isinstance(p, Processor)
            data = p(data)
        return data

    def __repr__(self):
        comp_str = '\n'.join(['  '+str(x) for x in self._processors])
        return f'Compose ({comp_str})'

class Standardize(Processor):
    """Replace the user-defined variable names and function names to fixed
    names. eg.var0, var1, var2, fun0, fun1, fun2
    """
    def __init__(self):
        pass

    def __call__(self, data):
        return F.standardize(data)

class Tree2Seq(Processor):
    """Transform tree structrue data into sequence data

    Args:
        path (str): The tree search algorithm
            - DFS: Deep-First Search
            - BFS: Breadth-First Search

    """
    def __init__(self, path='DFS'):
        self._path = path

    def __call__(self, data):
        return F.tree2seq(data, self._path)

class Vectorlize(Processor):
    """Transform sequence data into vector sequence data

    Args:
        embedder (torchplp.Processor.WordsModel)
    """
    def __init__(self, embedder):
        self._embedder = embedder

    def __call__(self, data):
        return F.vectorlize(data, self._embedder)
