import glob, re
import sqlite3, pandas as pd
import operator

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))
matches = lambda wt: len(list(re.finditer(wt[0].lower(), wt[1])))
cdf = pd.read_csv('candidatos.csv')

def get_party(c):
    sc = ' '.join(c.split('_')[1:])
    try:
        partido = sql(f"SELECT partido FROM candidatos WHERE candidato='{sc}'")
        return c+'<BR>'+partido
    except:  # not found
        return c+ '(N/A)'

def cubicalo(tipo):     # proyecciones bidimensionales: (i) por distrito/lista/partido (ii) totales/absolutas

    tqd = {'distrito': ''}

    return matches

def querier(query, WIDTH=80, tipo=None):
    squery = query.lower().replace('_',' ')

    FOLDER = 'TEXTOS/TODOS/*.txt' if tipo is None else 'TEXTOS/INDIGENAS/*.txt'
    files = list(glob.glob(FOLDER))
    textos = [open(fn).read().replace(chr(10),' ').replace('\\t','').replace('\\xa0',' ') for fn in files]
    print('QUERY:', squery)

    MARK = '<MARK>%s</MARK>'

    matches = {}
    for file, texto in zip(files, textos):
        tfile = file[13:-4] if tipo is None else file[17:-4]
        op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

        fmatches = list(re.finditer(squery, texto))
        if len(fmatches):
            ptfile = get_party(tfile).values[0][0]
            #ptfile = 
            print(tfile, ptfile)
            matches[ptfile] = [op(f).replace(squery, MARK %squery)
                                for f in fmatches]

    matches =  sorted(matches.items(), key=operator.itemgetter(1))
    #matches.sort('Menciones')

    return matches


def finders(textos, concepto, menciones):

    conceptos = [concepto]*len(menciones)
    smen = pd.DataFrame(dict(concepto=conceptos, mencion=menciones))
    nProgramas = len(textos)

    nmatches=[]
    amatches=[]

    for concepto, mencion in zip(conceptos, menciones):
        wnmatch = 0;         wamatch = 0.0
        print('CONCEPTO:', concepto, 'MENCION:', mencion)
        wnmatch += sum(matches([mencion,text]) for text in textos)   # missing space?
        wamatch += sum([1 if mencion in text else 0 for text in textos])/nProgramas    # normalized 20/04
        nmatches.append(wnmatch);        amatches.append(wamatch)

    smen['nMenciones']=nmatches
    smen['\% Mencionan']=[round(100*amat,2) for amat in amatches]

    return smen
