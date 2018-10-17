# -*- coding: utf-8 -*-
"""
processor_cgd.py - The processor method for code gadget datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
from covec.utils.loader import loader_cgd
from .models import Processor

class Processor_cgd(Processor):
    def __init__(self, path):
        self._raw_path = path
        self._cgd_list = loader_cgd(path)
        