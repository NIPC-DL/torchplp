# -*- coding: utf-8 -*-
"""
utils.py - The utils function for datasets

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import requests
from tqdm import tqdm
from subprocess import call


def download_file(url, path, proxy):
    """Donwloade file from url

    Args:
        url (str): download url
        path (str): saved path
        proxy (str): proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'

    """
    path = os.path.expanduser(path)
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        r = requests.get(url, stream=True, proxies=proxies)
    else:
        r = requests.get(url, stream=True)
    total_size = int(r.headers["Content-Length"])
    chunk_size = 1024
    bar_num = int(total_size / chunk_size)
    with open(path + url.split('/')[-1], 'wb') as f:
        for chunk in tqdm(
                iterable=r.iter_content(chunk_size=chunk_size),
                total=bar_num,
                unit='KB',
                leave=True,
        ):
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
