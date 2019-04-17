#coding: utf-8
from torchplp.datasets import Juliet

data_path = '~/Workspace/Test/Data'

category = [
    'CWE121', 'CWE122', 'CWE123', 'CWE124','CWE126', 'CWE127', 'CWE134'
    ]

def main():
    data = Juliet(data_path)
    data._select(['CWE121'])

if __name__ == '__main__':
    main()
