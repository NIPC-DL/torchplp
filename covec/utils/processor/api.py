# -*- coding: utf-8 -*-
"""
api.py - processor api interface

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
from .processor_cgd import Processor_cgd


def sysevr(files, type_):
    """Process given file and create their vector representation

    This method used in SySeVR <https://arxiv.org/abs/1807.06756>

    Directory Tree:
        TODO: w

    Args:
        files <list>: file list to process
        type_ <str>: type of input files
            - 'sc': source code
            - 'cgd': code gadget used in SySeVR (and VulDeePecker)

    Create:
        TODO: w

    """
    if type_ == 'sc':
        pass
    elif type_ == 'cgd':
        for file in files:
            processor = Processor_cgd(file)
            