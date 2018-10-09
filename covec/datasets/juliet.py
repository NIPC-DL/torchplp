# -*- coding: utf-8 -*-
import os
import zipfile
from .utils import download_file
from .constants import DOWNLOAD_URL
from .models import Dataset


class Juliet(Dataset):
    """`Juliet Test Suite <https://samate.nist.gov/SRD/testsuite.php>`

    Args:
        root: str
            Directory of dataset, will automately create Juliet_Test_Suite
            directory in it.
        method: str in ['sysevr', ]
            The process methods used on dataset.
        download: bool, optional
            If true, download dataset from internet, default false.
        proxy: str
            The proxy for download.
            eg. 'http://user:pass@host:port/'
                'socks5://user:pass@host:port'
    """

    def __init__(self, datapath, method=None, download=False, proxy=None):
        datapath = os.path.expanduser(datapath)
        if datapath[-1] != '/':
            datapath = datapath + '/'
        self.datapath = datapath + "Juliet_Test_Suite/"
        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)
        if download:
            self.download(proxy)

    def download(self, proxy):
        """Download Juliet Test Suiet from NIST website

        Dir:
           datapath/Juliet_Test_Suite
                └── Raw
                    ├── C
                    └── Juliet_Test_Suite_v1.3_for_C_Cpp.zip

        Para:
            proxy: str
                The proxy used for download.
                eg. 'http://user:pass@host:port/'
                    'socks5://user:pass@host:port'
        """
        URL = DOWNLOAD_URL['juliet']
        PATH = self.datapath + 'Raw/'
        print(f'Download from {URL}')
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        download_file(URL, PATH, proxy)
        print('Download success, Start extracting.')
        with zipfile.ZipFile(PATH + URL.split('/')[-1]) as z:
            z.extractall(PATH)

    def parse(self):
        """Parse something
        """
        pass

    def process(self, method):
        """Process dataset by selected method

        Para:
            method: str in ['sysevr',]
                The process methods used on dataset.
        """
        if method == 'sysevr':
            pass

    def get_dataloader(self):
        pass
