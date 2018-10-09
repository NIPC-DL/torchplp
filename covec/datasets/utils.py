# -*- coding: utf-8 -*-
import os
import requests
from tqdm import tqdm


def download_file(url, path, proxy):
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
                leave=True,):
            if chunk:
                f.write(chunk)
