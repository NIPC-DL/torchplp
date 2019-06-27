# -*- coding: utf-8 -*-
"""
embedding.py - Provide word embedding methods

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import gensim
from .models import Embedder


class Word2Vec(Embedder):
    """Words model for word embedding by google word2vec
       <https://en.wikipedia.org/wiki/Word2vec>
    
    Args:
        parameter (dict): The gensim.models.Word2Vec parameter
        
    """

    def __init__(self, **kwargs):
        self._model = gensim.models.Word2Vec(**kwargs)

    def __getitem__(self, key):
        return self._model[key]

    def train(self, sents):
        """Train words model by given sentences
        
        Args:
            sents (list): The list of sentences

        """
        if self.isempty():
            self._model.build_vocab(sents)
        else:
            self._model.build_vocab(sents, update=True)
        self._model.train(
            sents,
            total_examples=self._model.corpus_count,
            epochs=self._model.epochs)

    def isempty(self):
        """Determine if the model is empty"""
        return not bool(self._model.wv.vocab)

    def load(self, path):
        """load words model from pretrain"""
        self._model = gensim.models.Word2Vec.load(path)

    def save(self, path):
        """Save words module

        Args:
            path (str): The save path

        """
        self._model.save(path)

    @property
    def model(self):
        return self._model

    @property
    def length(self):
        return len(self._model.wv.vocab)

    @property
    def vector_size(self):
        return self._model.vector_size
