import pandas as pd
import requests
from bs4 import BeautifulSoup
import wget

class Crawler():
    def __init__(self):
        self.url_base = 'https://elecciones2021.servel.cl/programa-candidatos-as-convencionales-constituyentes/'
        self.bs = BeautifulSoup(requests.get(self.url_base).text, 'lxml')
        self.links = [link['href'] for link in self.bs.find_all('a') if 'repodo' in link['href']]

    def down(self, folder):
        self.failed = []
        print('DOWNLOADING %d PROGRAMS' %len(self.links))
        for link in self.links:
            try:
                wget.download(link, out=folder)
            except:
                print('FAILED:', link)
                self.failed.append(link)

craw = Crawler()
craw.down('PROGRAMAS/TODOS2')
print(craw.failed)
