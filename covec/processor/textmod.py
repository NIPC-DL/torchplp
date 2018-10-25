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

def standardize(codes):
    star = []
    ast = loader_cc(codes)
    parser = Parser(ast)
    var_decl = parser.walker(lambda x: x.kind == 'VAR_DECL')
    var_names = [x.data for x in var_decl]
    fun_decl = parser.walker(lambda x: x.kind == 'FUNCTION_DECL')
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
                tokens[ind] = 'varx'
        star.append(tokens)
    # filter the None data in star
    star = [x for x in star if x]
    return star

def symbolize(cgd_list):
    """transform code gadget to symbolic representation
    
    Args:
        cgd_list <list>: The list of code gadget

    Return:
        srl <list>: The symbolic representation list of code gadget
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


def vectorlize(srl, wordsmodel, length):
    """Create vector representation file from given symbolic representation
    
    Args:
        srl <list>: The list of symbolic representation
        wordsmodel <covec.processor.WordsModel.model>: The words model
        length <int>: All vectors will be set to a fixed length by this value

    """
    vrl = []
    for symr in srl:
        sent_set = [y for x in symr for y in wordsmodel[x]]
        if len(sent_set) < length:
            padding = np.asarray([[0 for x in range(100)]
                                  for y in range(length - len(sent_set))])
            sent_set.extend(padding)
            assert len(sent_set) == length
        vrl.append(sent_set[:length])
    return vrl


class Textmod(Processor):
    """The Text Mod Processor
    
    This methods is based on the paper SySeVR(arXiv:1807.06756) but have little difference,
        
    """

    def __init__(self, wordsmodel, length=50):
        self._wm = wordsmodel
        self._length = length

    def process(self, root, data, type_, output=True, chunks=10000):
        cooked_path = root + 'Cooked/'
        if not os.path.exists(cooked_path):
            os.makedirs(cooked_path)
        if type_ == 'sc':
            pass
        elif type_ == 'cgd':
            # srl - symbolic representation list
            srl = symbolize(data
def main():
    pass

if __name__ == '__main__':
    main())
            sents = [y for x in 
def main():
    pass

if __name__ == '__main__':
    main()srl for y in x]
            self._wm.train(sents
def main():
    pass

if __name__ == '__main__':
    main())
            # vrl - vector representation list
            if output:
                for ind, sr in enumerate(cutlist(srl, chunks)):
                    vrl = vectorlize(sr, self._wm.model, self._length)
                    x_set = np.asarray(vrl)
                    np.save(cooked_path + f'textmod_vec{ind}.npy', x_set)
                return None
            else:

                vrl = vectorlize(srl, self._wm.model, self._length)
                return np.asarray(vrl)
        else:
            raise ValueError(f"type_ must in ['sc', 'cgd', ]")
        return vrl