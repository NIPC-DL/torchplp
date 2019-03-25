# -*- coding: utf-8 -*-
"""
tree2seq.py - This processor transform tree structrue to sequence structrue

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import re
from .models import Processor
from .parser import ASTParser

class Tree2Seq(Processor):
    def __init__(self, embedder):
        self._embedder = embedder

    def standarlize(self, root):
        """
        This function replace the user-defined variable and function name
        to fixed name such as var0, var1 and fun0, fun1, which we called 
        standarlize.

        Args:
            root (torchplp.utils.ASTNode): The AST of code

        Return:
            root (torchplp.utils.ASTNode): The standarlized AST of code

        """
        pr = ASTParser(root)
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
            root (torchplp.utils.ASTNode): The AST of code

        """
        vr = []
        pr = ASTParser(root)
        for node in pr.walk():
            vec = self._embedder[node.data] if node.data else self._embedder[node.kind]
            vr.append(vec.tolist())
        return vr
    
    def process(self, data, pretrain=False):
        """Process AST and output their vector representation"""
        if isinstance(data, list):
            sr = [self.standarlize(x) for x in data]
            if not pretrain:
                self._pretrain(sr)
            vr = [self.vectorlize(x) for x in sr]
        else:
            sr = self.standarlize(data)
            vr = self.vectorlize(sr)
        return vr

    def _pretrain(self, data):
        """Training the embedder by given data
        
        Args:
            data (list): The list of AST Node

        """
        sent = []
        for root in data:
            atoms = []
            pr = ASTParser(root)
            for node in pr.walk():
                if node.data:
                    atoms.append(node.data)
                if node.kind:
                    atoms.append(node.kind)
            sent.append(atoms)
        self._embedder.train(sent)
