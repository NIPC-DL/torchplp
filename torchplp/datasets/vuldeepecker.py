# -*- coding: utf-8 -*-
"""
vuldeepecker.py - VulDeePecker Dataset defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import re
import zipfile
import random
import shutil
import pickle
import torch
import numpy as np
from torch.utils.data import DataLoader
from torchplp.utils.loader import loader_cgd
from torchplp.utils.utils import git_clone_file
from .models import Dataset


class VulDeePecker(Dataset):
    """VulDeePecker Dataset <https://github.com/CGCL-codes/VulDeePecker> 
    
    From Paper:
        VulDeePecker: A Deep Learning-Based System for Vulnerability Detection

    Args:
        datapath (str): Directory of dataset, will automately create
        VulDeePecker directory in it.
        download (bool, optional): If true, download dataset from internet, default false.

    """

    def __init__(self, datapath, processor=None, download=True):
        super().__init__(datapath)
        if download:
            self.download()

    def download(self):
        """Download VulDeePecker Datasets from their Github Repo"""
        url = 'https://github.com/CGCL-codes/VulDeePecker.git'
        git_clone_file(url, self._root)