import requests
import os, wget
from bs4 import BeautifulSoup
from pprint import pprint

class Crawler():
    def __init__(self):
        self.url_base = 'https://elecciones2021.servel.cl/programa-candidatos-as-convencionales-constituyentes-pueblos-indigenas/'
        self.bs = BeautifulSoup(requests.get(self.url_base).text, 'lxml')

craw = Crawler()
craw.links = [link['href'] for link in craw.bs.find_all('a') if 'repodo' in link['href']]
craw.failed = []
#!mkdir PROGRAMAS/INDIGENAS

for link in craw.links:
    slink = link.split('/')[-1]
    pueblo = slink.split('_')[0]
    pdir = os.path.join('PROGRAMAS/INDIGENAS',pueblo)
    if not os.path.exists(pdir):
        print('mkdir',pdir)
        os.mkdir(pdir)
    try:
        wget.download(link, out=pdir)
    except:
        print('FAILED:', slink)
        craw.failed.append(slink)

print('LINKS:', len(craw.links))
pprint(craw.failed)
