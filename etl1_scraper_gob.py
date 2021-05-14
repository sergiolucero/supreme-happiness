from crawler import Crawler

craw = Crawler('https://elecciones2021.servel.cl/programas-candidatos-as-a-gobernador-a-regional/')
craw.down('GOBERNADORES')
print(craw.failed)

