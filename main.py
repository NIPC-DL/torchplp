#coding: utf-8
import maya
from torchplp.datasets import Juliet, SySeVR
from torchplp.processor.treemodel import TreeModel
from torchplp.processor.textmodel import TextModel

data_path = '~/Workspace/Test/Data'

def test_juliet():
    juliet = Juliet(data_path)
    juliet_samples = juliet.load(category=['CWE121'])
    pr = TreeModel()
    print(juliet_samples)
    for key, data in juliet_samples.items():
        print(f'process {key}')
        samples, labels = zip(*data)
        samples = pr(samples)
        print(len(samples), len(labels))
    now = maya.now()
    print(f'start max {now}')
    print(max([len(x) for x in samples]))
    now = maya.now()
    print(f'finish max {now}')

def test_sysevr():
    sysevr = SySeVR(data_path)
    sysevr_samples = sysevr.load(category=['FC']) # 'AE', 'AU', 'PU', 'FC'
    pr = TextModel()
    # for key, data in sysevr_samples.items():
    #     print(f'process {key}')
    #     samples, labels = zip(*data)
    #     samples = pr(samples)
    #     print(len(samples), len(labels))
    # now = maya.now()
    # print(f'start max {now}')
    # print(max([len(x) for x in samples]))
    # now = maya.now()
    # print(f'finish max {now}')


def main():
    test_juliet()
    # test_sysevr()
    
if __name__ == '__main__':
    main()
