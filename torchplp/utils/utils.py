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
        call(['git', 'clone', url, path])
    else:
        raise SystemError("git not found, please install git first.")

def i2h(labels, classes):
    """convert int to one-hot"""
    y = torch.LongTensor(labels)
    y_onehot = torch.FloatTensor(len(labels), classes)
    y_onehot.zero_()
    y_onehot.scatter_(1, y, 1)
    return y_onehot

def split_by_category(category, ratio, shuffle=True):
    if len(ratio) != 3:
        raise ValueError(f'ratio must include three int numbers')
    train, valid, tests = list(), list(), list()
    for samples in category:
        sample_lens = len(samples)
        train_ratio = round(sample_lens * (ratio[0]/sum(ratio)))
        tests_ratio = round(sample_lens * (ratio[2]/sum(ratio)))
        valid_ratio = sample_lens - train_ratio - tests_ratio
        if shuffle:
            random.shuffle(samples)
        train.extend(samples[:train_ratio])
        valid.extend(samples[train_ratio:train_ratio+valid_ratio])
        tests.extend(samples[-tests_ratio:])
    return train, valid, tests

