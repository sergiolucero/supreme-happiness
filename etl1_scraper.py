from crawler import Crawler

craw = Crawler('https://elecciones2021.servel.cl/programa-candidatos-as-convencionales-constituyentes')
craw.down('PROGRAMAS/TODOS')
print(craw.failed)
