# -*- coding: utf-8 -*-
"""
tree2seq.py - This processor transform tree structrue to sequence structrue

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
import numpy as np
from .models import Processor
from .parser import Parser

class Tree2Seq(Processor):
    def __init__(self, embedder, length):
        self._embedder = embedder
        self._length = length

    def process(self, data, pretrain=False):
        srl = [self.standarlize(x) for x in data]
        if not pretrain:
            self._pretrain(srl)
        vrl = [self.vectorlize(x) for x in srl]
        return vrl

    @staticmethod
    def standarlize(root):
        """
        This function replace the user-defined variable and function name
        to fixed name such as var0, var1 and fun0, fun1, which we called 
        standarlize. In SySeVR, they called this procedure symbolize.

        Args:
            data (list): The list of AST

        Return:
            data (list): The standarlize data list

        """
        pr = Parser(root)
        var_decl = pr.walker(lambda x: x.kind == 'VAR_DECL')
        var_names = [x.data for x in var_decl]
        fun_decl = pr.walker(lambda x: x.kind == 'FUNCTION_DECL')
        fun_names = [x.data for x in fun_decl]
        for node in pr.walk():
            if node.data in var_names:
                node.data = f'var{var_names.index(node.data)}'
            if node.data in fun_names:
                node.data = f'fun{fun_names.index(node.data)}'
            if re.match(r'^CWE\d{2,3}_.*Data$', node.data):
                node.data = f'var{str(len(var_names))}'
        return root

    def vectorlize(self, root):
        """
        This function converts the standarlized codes into a vector representation 
        through a words model.

        Args:
            root (ASTNode): The Abstract Syntax Tree Node

        """
        vrl = []
        pr = Parser(root)
        for node in pr.walk():
            data_vec = self._embedder[node.data] if node.data else np.zeros(
                int(self._length / 2))
            kind_vec = self._embedder[node.kind] if node.kind else np.zeros(
                int(self._length / 2))
            vec = np.append(data_vec, kind_vec)
            vrl.append(vec.tolist())
        return vrl
    
    def _pretrain(self, data):
        """Training the embedder by given data
        
        Args:
            data (list): The list of AST Node

        """
        sent = []
        for root in data:
            atoms = []
            pr = Parser(root)
            for node in pr.walk():
                if node.data:
                    atoms.append(node.data)
                if node.kind:
                    atoms.append(node.kind)
            sent.append(atoms)
        self._embedder.train(sent)
