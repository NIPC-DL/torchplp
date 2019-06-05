# -*- coding: utf-8 -*-
"""
utils.py - The collection of utils

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import random
import torch
import requests
import numpy as np
from subprocess import call


def download_file(url, path, proxy=None):
    """Donwloade file from url

    Args:
        url (str): download url
        path (pathlib.Path): saved path
        proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

    """
    # set proxy if exist
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        r = requests.get(url, stream=True, proxies=proxies)
    else:
        r = requests.get(url, stream=True)
    chunk_size = 1024
    with open(str(path / url.split('/')[-1]), 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)

def git_clone_file(url, path):
    """git clone repo from url

    Args:
        url (str): git repo url
        path (str): saved path

    """
    if os.path.exists('/usr/bin/git') or os.path.exists('/bin/git'):
        call(['git', 'clone', url, str(path)])
    else:
        raise SystemError("git not found, please install git first.")

def spliter(data_dict, ratio=[6,1,1], shuffle=True):
    """split dict dataset into train, valid and tests set

    Args:
        data_dict (dict): dataset in dict
        ratio (list): list of ratio for train, valid and tests split
        shuffle (bool): shuffle or not
    
    """
    if len(ratio) != 3:
        raise ValueError(f'ratio must include three int numbers')
    train = {'x':list(), 'y':list()}
    valid = {'x':list(), 'y':list()}
    tests = {'x':list(), 'y':list()}
    for _, [samples, labels] in data_dict.items():
        samples_lens = len(samples)
        train_ratio = round(samples_lens * (ratio[0]/sum(ratio)))
        tests_ratio = round(samples_lens * (ratio[2]/sum(ratio)))
        valid_ratio = samples_lens - train_ratio - tests_ratio
        data = list(zip(samples, labels))
        if shuffle:
            random.shuffle(data)
        x, y = zip(*data)
        train['x'].extend(x[:train_ratio])
        train['y'].extend(y[:train_ratio])
        valid['x'].extend(x[train_ratio:train_ratio+valid_ratio])
        valid['y'].extend(y[train_ratio:train_ratio+valid_ratio])
        tests['x'].extend(x[-tests_ratio:])
        tests['y'].extend(y[-tests_ratio:])
    return train, valid, tests

def truncate_and_padding(data, word_size, length):
    """truncate and padding data"""
    if not isinstance(data, np.ndarray):
        data = np.asarray(data)
    real_length = len(data)
    if real_length < length:
        try:
            pad = np.zeros((length-real_length, word_size))
            data = np.concatenate((data, pad), axis=0)
        except Exception:
            print(data.shape)
            print(pad.shape)
            return
    else:
        data = data[:length]
    return data

