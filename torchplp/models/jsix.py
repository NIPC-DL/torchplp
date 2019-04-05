# -*- coding: utf-8 -*-
"""
jsix.py - Wor2Vec model trained from Juliet and Six other open source project


:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import pathlib
from torchplp.processor.embedder import Word2Vec
from torchplp.utils.utils import download_file


url = 'https://nas.dothings.top:5002/NIPCDL/Jsix/jsix_{}.w2v'

def jsix(root='/tmp', length=100, delete=True, proxy=None):
    """word2vec model trained by juliet and other six open source project"""
    root = pathlib.Path(root).expanduser()
    file = root / f'jsix_{length}.w2v'
    download_file(url.format(length), root, proxy)
    wm = Word2Vec()
    wm.load(str(file))
    if delete:
        file.unlink()
    return wm
