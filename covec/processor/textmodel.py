# -*- coding: utf-8 -*-
"""
sysevr.py - The Text Model Processor

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
import re
import numpy as np
from .models import Processor
from .parser import Parser
from .embedding import Word2Vec
from covec.utils.loader import loader_cgd, loader_cc


def code_split(line):
    """split code line into atom
    
    Args:
        line: The code line
    
    Return:
        tokens <list>: The list of atom token for code line
    """
    return list(
        filter(lambda x: x and x not in [' ', ''], re.split(r'(\W|\s)', line)))


def cutlist(l, size):
    """The geneator function cut list into sevevl blocks,
    if the list can not divide equally, this function will 
    keep the other blocks except the last one equal
    
    Args:
        l <list>: The iterable object
        size <int>: The number of block size you want to divide
    
    Return:
        yield every blocks
    """

    for i in range(0, len(l), size):
        yield l[i:i + size]


def standarlize(cgd_list):
    """
    This function replace the user-defined variable and function name
    to fixed name such as var0, var1 and fun0, fun1, which we called 
    standarlize. In SySeVR, they called this procedure symbolize.
    
    Args:
        cgd_list <list>: The list of code gadget

    Return:
        srl <list>: The standarlize representation list of code gadget
    """

    srl = []
    for code in cgd_list:
        symr = []
        ast = loader_cc(code)
        pr = Parser(ast)
        # get variable and function declaration
        var_decl = pr.walker(lambda x: x.kind == 'VAR_DECL')
        var_names = [x.data for x in var_decl]
        fun_decl = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
        fun_names = [x.data for x in fun_decl]
        # replace names
        for line in code:
            tokens = code_split(line)
            for ind, val in enumerate(tokens):
                if val in var_names:
                    tokens[ind] = 'var' + str(var_names.index(val))
                if val in fun_names:
                    tokens[ind] = 'fun' + str(fun_names.index(val))
                # some long data that can not parsed by libclang
                if re.match(r'^CWE\d{2,3}_.*Data$', val):
                    tokens[ind] = 'varx'
            symr.append(tokens)
        # filter the None data in symr
        symr = [x for x in symr if x]
        srl.append(symr)
    return srl


def vectorlize(srl, embedder, vector_length):
    """
    This function converts the standarlized codes into a vector representation 
    through a words model.
    
    Args:
        srl <list>: The list of symbolic representation
        embedder <covec.processor.WordsModel.model>: The words model that map words to vector
        vector_length <int>: All vectors will be set to a fixed length by this value

    """
    vrl = []
    for symr in srl:
        sent_set = [y for x in symr for y in embedder[x]]
        if len(sent_set) < vector_length:
            padding = np.asarray(
                [[0 for x in range(100)]
                 for y in range(vector_length - len(sent_set))])
            sent_set.extend(padding)
            assert len(sent_set) == vector_length
        vrl.append(sent_set[:vector_length])
    return vrl


class TextModel(Processor):
    """The Text Mod Processor
    
    This methods is based on the paper SySeVR(arXiv:1807.06756) but have little 
    difference, so we called it Text Model. Because this method treats the 
    program code as natural language text.

    Args:
        wordsmodel <covec.processor.WordsModel>: The words model map words to 
            their vector representation
        vector_length <int>: The text model usually used on LSTM or other 
            neural networks, and they all need fixed length input, so this 
            parameter limited the length of output vector, if they are shorter
            than this number, a full-zero padding will append to the end of them,
            and if they are large than this number, we will tuncat from end
            to head to ensure they have fixed length.
        
    """

    def __init__(self, embedder, vector_length=50):
        self._embedder = embedder
        self._vector_length = vector_length

    def process(self, data, type_):
        """Process input data and output or create vector data
        
        Args:
            data <iterable>: The list of iterable object that can processed
                one by one
            type_ <str>: The type of input data
                - 'sc': Source Code
                - 'cgd': Code Gadget
            embedder <covec.processor.WordsModel>: The words embedding module
            output <str>: The path where to output vector data
            
        """
        if type_ == 'sc':
            pass
        elif type_ == 'cgd':
            # srl - standarlize representation list
            srl = standarlize(data)
            print('standarlize finish')
            # vrl - vector representation list
            sents = [y for x in srl for y in x]
            # train words model
            self._embedder.train(sents)
            print('embedding train finish')
            # words embedding
            vrl = vectorlize(srl, self._embedder, self._vector_length)
            print('vectorlize finish')
            return vrl
        else:
            raise ValueError(f"type_ must in ['sc', 'cgd', ]")