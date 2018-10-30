# -*- coding: utf-8 -*-
"""
This subpackage is the collection of all process for datasets

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
from .textmodel import TextModel
from .embedding import Word2Vec
from .models import Processor, WordsModel

__all__ = [
    'TextModel',
    'Word2Vec',
    'Processor',
    'WordsModel',
]
