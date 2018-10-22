#!/usr/bin/env python3
# coding: utf-8
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='covec',
    version='0.1dev',
    author="NIPC-DL",
    author_email="verf@protonmail.com",
    description="Python Code Preprocessor for Machine Learning",
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/NIPC-DL/Covec",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'clang',
        'requests',
        'tqdm',
        'gensim',
        'pyyaml',
    ],
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],
)
