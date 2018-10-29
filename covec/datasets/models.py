# -*- coding: utf-8 -*-
"""
models.py - The covec dataset model defination

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import os


class Dataset:
    """Upper dataset class"""

    def __init__(self, datapath):
        datapath = os.path.expanduser(datapath)
        # Make sure directory path end with '/'
        if datapath[-1] != '/':
            datapath += '/'
        self._datapath = datapath