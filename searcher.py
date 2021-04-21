import glob, re
import sqlite3, pandas as pd

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))

def cubicalo(tipo):     # proyecciones bidimensionales: (i) por distrito/lista/partido (ii) totales/absolutas

    tqd = {'distrito': ''}

    return matches

def querier(query, WIDTH=80, tipo=None):
    squery = query.lower().replace('_',' ')

    FOLDER = 'TEXTOS/TODOS/*.txt' if tipo is None else 'TEXTOS/INDIGENAS/*.txt'
    files = list(glob.glob(FOLDER))
    textos = [open(fn).read().replace(chr(10),' ') for fn in files]
    print('QUERY:', squery)

    MARK = '<MARK>%s</MARK>'

    matches = {}
    for file, texto in zip(files, textos):
        tfile = file[13:-4] if tipo is None else file[17:-4]
        op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

        fmatches = list(re.finditer(squery, texto))
        if len(fmatches):

            matches[tfile] = [op(f).replace(squery, MARK %squery)
                                for f in fmatches]

    return matches
