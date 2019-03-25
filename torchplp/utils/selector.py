# -*- coding: utf-8 -*-
"""
selector.py - Usefully function to split data

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import random

def list_split(data, coe, shuffle, seed):
    if shuffle:
        random.seed(seed)
        random.shuffle(data)
    l = len(data)
    coe = [i*l/sum(coe) for i in coe]
    coe.insert(0, 0)
    sel = [data[coe[i]:coe[i+1]] for i in range(len(coe)-1)]
    return sel

def data_split(data, coe=[4,1,0], shuffle=True, seed=None):
    assert sum(coe) > 1
    train = []
    valid = []
    tests = []
    if isinstance(data, dict):
        for k, v in data.items():
            t,v,tt = list_split(v, coe, shuffle, seed)
            train.extend(t)
            valid.extend(v)
            tests.extend(tt)
    elif isinstance(data, list):
        train, valid, tests = list_split(data, coe, shuffle, seed)
    else:
        raise TypeError(f'{data} is not a list or dict')
    assert len(train) != 0
    return train, valid, tests

def indices_by_dist(indes, dist, coe=[4,1,0], shuffle=True, seed=None):
    assert sum(coe) > 1
    train = []
    valid = []
    tests = []
    for i in range(len(dist)-1):
        chunk = indes[dist[i]:dist[i+1]]
        t, v, tt = list_split(chunk, coe, shuffle, seed)
        train.extend(t)
        valid.extend(v)
        tests.extend(tt)
    return train, valid, tests

