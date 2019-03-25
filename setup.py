#!/usr/bin/env python3
# coding: utf-8
from setuptools import setup, find_packages

VERSION = '0.1'
REQUIREMENTS = [
        'numpy',
        'torch',
        'gensim',
        ]

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='torchplp',
    version=VERSION,
    author='NIPC-DL',
    author_email='verf@protonmail.com',
    url="https://github.com/NIPC-DL/torchplp",
    description='datasets and process methods for program source code analysis',
    long_description=readme(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=('test',)),
    install_requires=REQUIREMENTS
)
