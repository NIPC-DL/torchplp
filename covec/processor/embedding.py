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
        sentences <list>: The list of sentence
        parameter <dict>: The gensim.models.Word2Vec parameter
        
    """

    def __init__(self, corpus, parameter=dict()):
        self._model = Word2Vec(sentences=corpus, **parameter)

    def training(self, corpus):
        self._model.build_vocab(corpus, update=True)
        self._model.train(corpus)

    def save(self, name):
        self._model.save(name)