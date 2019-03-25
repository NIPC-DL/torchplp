# -*- coding: utf-8 -*-
"""
sysevr.py - The Text Model Processor

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
from .models import Processor
from .parser import ASTParser


def code_split(line):
    """split code line into atom
    
    Args:
        line (str): The code line
    
    Return:
        tokens (list): The list of atom token for code line

    """
    return list(
        filter(lambda x: x and x not in [' ', ''], re.split(r'(\W|\s)', line)))


class TextModel(Processor):
    """
    This methods is based on the paper VulDeePecker...(arXiv:1801.01681) but have little 
    difference, so we called it Text Model. Because this method treats the 
    program code as natural language text.

    Args:
        embedder (covec.processor.WordsModel): The words model map words to 
            their vector representation

    """

    def __init__(self, embedder):
        self._embedder = embedder

    def standarlize(self, code):
        """
        This function replace the user-defined variable and function name
        to fixed name such as var0, var1 and fun0, fun1, which we called it
        standarlize.

        Args:
            x (list): The fragment of source code.

        Return:
            sr (list): The standarlize representation of source code

        """
        assert len(code) != 0
        sr = []
        pr = ASTParser(code)
        var_decl = pr.walker(lambda x: x.kind == 'VAR_DECL')
        var_names = [x.data for x in var_decl]
        fun_decl = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
        fun_names = [x.data for x in fun_decl]
        for line in code:
            tokens = code_split(line)
            for ind, val in enumerate(tokens):
                if val in var_names:
                    tokens[ind] = 'var' + str(var_names.index(val))
                if val in fun_names:
                    tokens[ind] = 'fun' + str(fun_names.index(val))
                # some long data that can not parsed by libclang
                if re.match(r'^CWE\d{2,3}_.*Data$', val):
                    tokens[ind] = f'var{str(len(var_names))}'
            sr.append(tokens)
        return sr

    def vectorlize(self, sr):
        """
        This function converts the standarlized codes into a vector representation 
        through a words model.

        Args:
            sr (list): symbolic representation of code fragment

        Returns:
            vr (list): list of vector representation

        """
        vr = [self._embedder[word].tolist() for line in sr for word in line]
        return vr

    def process(self, data, pretrain=False):
        """Process source code and output their vector representation"""
        if isinstance(data[0], str):
            sr = self.standarlize(data)
            vr = self.vectorlize(sr)
        else:
            sr = [self.standarlize(x) for x in data]
            if not pretrain:
                self._pretrain(sr)
            vr = [self.vectorlize(x) for x in sr]
        return vr

    def _pretrain(self, data):
        sent = sum(data, [])
        self._embedder.train(sent)
