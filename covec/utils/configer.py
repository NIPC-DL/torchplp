# -*- coding: utf-8 -*-
"""
configer.py - Ths file provide the global configuration for covec

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import yaml


class Config:
    def __init__(self):
        self._data = None

    def load(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self._data = yaml.load(f)
        except FileNotFoundError:
            print(f'{path} not found')


config = Config()