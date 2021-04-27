import glob, re
import sqlite3, pandas as pd
import operator
import collections

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))
#####################################
def get_party(c):
    sc = ' '.join(c.split('_')[1:])
    try:
        partido = sql(f"SELECT partido FROM candidatos WHERE candidato='{sc}'").values[0][0]
        return c+'<BR>'+f'[{partido}]'
    except:  # not found
        return c+ '(N/A)'

def party(c):
    sc = ' '.join(c.split('_')[1:])
    try:
        partido = sql(f"SELECT partido FROM candidatos WHERE candidato='{sc}'").values[0][0]
        return partido
    except:  # not found
        return '(N/A)'

def cubicalo(tipo):     # proyecciones bidimensionales: (i) por distrito/lista/partido (ii) totales/absolutas

    tqd = {'distrito': ''}

    return matches


def querier(query, WIDTH=80, tipo=None):

    kw = eval(open('keywords_final.txt').read())

    squery = query.lower().replace('_',' ')

    if squery in kw:  # agua, clima, medioambiente
        squery = [squery] + kw[squery]  # becomes a list

    FOLDER = 'TEXTOS/TODOS/*.txt' if tipo is None \
        else 'TEXTOS/INDIGENAS/*.txt'
    files = list(glob.glob(FOLDER))
    textos = [open(fn).read().replace(chr(10),' ').replace('\\t','').replace('\\xa0',' ') for fn in files]
    print('QUERY:', squery)

    MARK = '<MARK>%s</MARK>'

    matches = {}
    for file, texto in zip(files, textos):
        tfile = file[13:-4] if tipo is None else file[17:-4]
        op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

        if isinstance(squery, list):
            fmatches = []
            for sq in squery:
                fmatches.append(list(re.finditer(sq, texto)))
        else:
            fmatches = list(re.finditer(squery, texto))

        if len(fmatches):
            ptfile = get_party(tfile)
            #ptfile = 
            print(tfile, ptfile)
            matches[ptfile] = [op(f).replace(squery, MARK %squery)
                                for f in fmatches]

    matches =  sorted(matches.items(), key=operator.itemgetter(1))
    #matches.sort('Menciones')
    matches = collections.OrderedDict(matches)

    return matches

matches = lambda wt: len(list(re.finditer(wt[0].lower(), wt[1])))
fmatches = lambda wt: list(re.finditer(wt[0].lower(), wt[1]))

def finders(textos, concepto, menciones):

    # agua: [derecho al agua, etcagua, 3crisis hídrica...]
    # clima: [emergencia...], medio: [medio(SP),...]

    if concepto=='agua':  # it's complicated
        wnmatch = sum(matches(['agua ',text]) for text in textos)   # missing space?
        wamatch = sum([1 if 'agua ' in text else 0 for text in textos])    # unnormalized 23/04
        print('agua',wamatch)
        for mencion in menciones[3:]:
            wnmatch += sum(matches([mencion,text]) for text in textos)   # missing space?
            wamatch += sum([1 if mencion in text else 0 for text in textos])    # unnormalized 23/04
            print(mencion, wamatch)
            #wamatch += sum([1 if mencion in text else 0 for text in textos])/nProgramas    # normalized 20/04
    else:
        #shoot
        wnmatch = sum(matches([concepto,text]) for text in textos)   # missing space?
        wamatch = sum([1 if concepto in text else 0 for text in textos])    # unnormalized 23/04
        for mencion in menciones:
            wnmatch += sum(matches([mencion,text]) for text in textos)   # missing space?
            wamatch += sum([1 if mencion in text else 0 for text in textos])    # unnormalized 23/04

    smen = pd.DataFrame(dict(concepto=concepto, nMenciones=wnmatch, PorcMencionan=wamatch),index=[0])

    return smen
