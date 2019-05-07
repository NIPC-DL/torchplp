# -*- coding: utf-8 -*-
import pathlib
import maya
from torchplp.datasets import Juliet

data_path = '~/Workspace/Test/Data'

def main():
    dataset = Juliet(data_path)
    print(f'load start {maya.now()}')
    for c, samples in dataset.load(category=['CWE121']):
        print(c, len(samples))
    print(f'load finish {maya.now()}')

if __name__ == '__main__':
    main()
