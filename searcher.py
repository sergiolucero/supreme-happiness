import glob, re
import sqlite3, pandas as pd

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))

def cubicalo(tipo):     # proyecciones bidimensionales: (i) por distrito/lista/partido (ii) totales/absolutas

    tqd = {'distrito': ''}

    return matches

def querier(query):
    squery = query.lower().replace('_',' ')

    files = list(glob.glob('TEXTOS/TODOS/*.txt'))
    textos = [open(fn).read() for fn in files]
    print('QUERY:', squery)

    MARK = '<MARK>%s</MARK>'

    matches = {}
    WIDTH = 80
    for file, texto in zip(files, textos):
        tfile = file[13:-4]
        op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

        fmatches = list(re.finditer(squery, texto))
        if len(fmatches):

            matches[tfile] = [op(f).replace(squery, MARK %squery)
                                for f in fmatches]

    return matches
