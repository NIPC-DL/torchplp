# -*- coding: utf-8 -*-
"""
embedding.py - Provide word embedding methods

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
from gensim.models import Word2Vec


class Wordsmodel:
    """Words model for word embedding by google word2vec
       <https://en.wikipedia.org/wiki/Word2vec>
    
    Args:
        
    """

    def __init__(self, sentence, parameter=None):
        pass

    def training(self, sentences):
        corpus = self._wordsplit(sentences)

    def _wordsplit(self, sentences):
        corpus = [x.split(' ') for x in sentences]
        return corpus
