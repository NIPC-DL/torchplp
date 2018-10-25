# -*- coding: utf-8 -*-
"""
configer.py - Ths file provide the global configuration for covec

Author: Verf
Email: verf@protonmail.com
License: MIT
"""
import yaml


class Configer:
    def __init__(self):
        pass

    @staticmethod
    def load(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.load(f)
        except FileNotFoundError:
            print(f'{path} not found')
        return config