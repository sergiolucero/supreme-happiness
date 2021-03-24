import pandas as pd
import requests
from bs4 import BeautifulSoup


















class Crawler():
    def __init__(self):
        self.url_base = 'https://elecciones2021.servel.cl/programa-candidatos-as-convencionales-constituyentes/'
        self.bs = BeautifulSoup(requests.get(self.url_base).text, 'lxml')


craw = Crawler()
