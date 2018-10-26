# -*- coding: utf-8 -*-
"""
models.py - The processor model defination

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import abc


class Processor(metaclass=abc.ABCMeta):
    """The upper class of processor"""

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError


class WordsModel(metaclass=abc.ABCMeta):
    """The upper class of words model"""

    @abc.abstractmethod
    def train(self, sents):
        """Training words model"""
        raise NotImplementedError

    @abc.abstractmethod
    def model(self):
        """Return trained dict"""
        raise NotImplementedError