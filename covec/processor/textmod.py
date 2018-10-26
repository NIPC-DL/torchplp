# -*- coding: utf-8 -*-
"""
sysevr.py - The sysevr processing methods for datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os
import re
import numpy as np
from pprint import pprint
from .constants import KEYWORD, DEFINED
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


def vectorlize(srl, wordsmodel, vector_length):
    """
    This function converts the standarlized codes into a vector representation 
    through a words model.
    
    Args:
        srl <list>: The list of symbolic representation
        wordsmodel <covec.processor.WordsModel.model>: The words model
        vector_length <int>: All vectors will be set to a fixed length by this value

    """
    vrl = []
    for symr in srl:
        sent_set = [y for x in symr for y in wordsmodel[x]]
        if len(sent_set) < vector_length:
            padding = np.asarray(
                [[0 for x in range(100)]
                 for y in range(vector_length - len(sent_set))])
            sent_set.extend(padding)
            assert len(sent_set) == vector_length
        vrl.append(sent_set[:vector_length])
    return vrl


class Textmod(Processor):
    """The Text Mod Processor
    
    This methods is based on the paper SySeVR(arXiv:1807.06756) but have little 
    difference, so we called it Text Module. Because this method treats the 
    program code as natural language text.

    Args:
        wordsmodel <covec.processor.WordsModel>: The words model map words to 
            their vector representation
        vector_length <int>: The text module usually used on LSTM or other 
            neural networks, and they all need fixed length input, so this 
            parameter limited the length of output vector, if they are shorter
            than this number, a full-zero padding will append to the end of them,
            and if they are large than this number, we will tuncat from end
            to head to ensure they have fixed length.
        
    """

    def __init__(self, wordsmodel, vector_length=50):
        self._wm = wordsmodel
        self._vector_length = vector_length

    def process(self, data, type_, output=None, chunks=None):
        """Process input data and output or create vector data
        
        Args:
            data <iterable>: The list of other iterable object that can processed
                one by one
            type_ <str>: The type of input data
                - 'sc': Source Code
                - 'cgd': Code Gadget
            output <str, None, optional>: Default is None, this function will 
                directly return the vector data, if set as path, this function 
                will create the Cooked directory in this path and output the 
                npy format file in Cooked directory.
            chunks <int, None, optional>: Default is None. This variable only 
                used when output is a path, and this function will split the 
                output in multiple files. Only recommended when your computer's
                memory is too small to generate all the data at once.
            
        """
        if output:
            cooked_path = output + 'Cooked/'
        if not os.path.exists(cooked_path):
            os.makedirs(cooked_path)
        if type_ == 'sc':
            pass
        elif type_ == 'cgd':
            # srl - symbolic representation list
            srl = standarlize(data)
            # vrl - vector representation list
            if bool(output) and bool(chunks):
                for ind, sr in enumerate(cutlist(srl, chunks)):
                    vrl = vectorlize(sr, self._wm.model, self._vector_length)
                    x_set = np.asarray(vrl)
                    np.save(cooked_path + f'textmod_vec{ind}.npy', x_set)
                return None
            elif bool(output):
                vrl = vectorlize(srl, self._wm.model, self._vector_length)
                x_set = np.asarray(vrl)
                np.save(cooked_path, f'textmod_vec.npy', x_set)
            else:
                vrl = vectorlize(srl, self._wm.model, self._vector_length)
                return np.asarray(vrl)
        else:
            raise ValueError(f"type_ must in ['sc', 'cgd', ]")