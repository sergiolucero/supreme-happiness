import glob, re
import sqlite3, pandas as pd
import operator
import collections

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))
keywords = eval(open('keywords_final.txt').read())
#####################################
def read_text(fn):
    rfn = open(fn).read()
    for rep in [(chr(10),' '),('\\t',''),('\\xa0',' ')]:
        rfn = rfn.replace(rep[0],rep[1])
    return rfn

def clean_read(fn):
    return read_text(fn)


def get_party(c):
    sc = ' '.join(c.split('_')[1:])
    try:
        partido = sql(f"SELECT partido FROM candidatos WHERE candidato='{sc}'").values[0][0]
        return c+'<BR>'+f'[{partido}]'
    except:  # not found
        return c+ '(N/A)'

def get_lista(c):
    sc = ' '.join(c.split('_')[1:])
    try:
        lista = sql(f"SELECT lista FROM candidatos WHERE candidato='{sc}'").values[0][0]
        return c+'<BR>'+f'[{lista}]'
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

fixers = {'medioambiente': ['naturaleza humana', 'propia naturaleza', 'naturaleza positiva',
					'naturaleza del derecho', 'naturaleza social',
					'naturaleza colectiva', 'naturaleza política',],
          'clima': ['clima político','clima más', 'clima actual', 'clima del país',
				'clima social', 'clima beligerante', 'clima ambiente', 'clima de temor']}

def get_matches(squery, texto, WIDTH):      # CONTAINS EXCLUSIONS

    op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

    if isinstance(squery, list):
            fmatches = []
            for sq in squery:
                fmatches+=list(re.finditer(sq+' ', texto))
    else:
            fmatches = list(re.finditer(squery, texto))

    if len(fmatches):
            ftextos = [op(f) for f in fmatches]
            #print('FT:', ftextos)
            qfix = fixers.get(squery,[])
            bad_mat = []
            for qf in qfix:
                bad_mat += [x for x in ftextos if qf in x]
            if len(bad_mat): # must remove, use zip
                #print(squery, bad_mat)
                fmatches = [f for f in fmatches if op(f) not in bad_mat]
                #print('FMAT2:', fmatches)
                #somebad

    return fmatches

def querier(query, WIDTH=80, tipo=None):

    kw = eval(open('keywords_final.txt').read())

    squery = query.lower().replace('_',' ')

    if squery in kw:  # agua, clima, medioambiente
        squery = [squery] + kw[squery]  # becomes a list

    FOLDER = 'TEXTOS/TODOS/*.txt' if tipo is None \
        else 'TEXTOS/INDIGENAS/*.txt'
    files = list(glob.glob(FOLDER))
    textos = [read_text(fn) for fn in files]

    MARK = '<MARK>%s</MARK>'

    matches = {}
    nMenciones = 0
   
    for file, texto in zip(files, textos):
        tfile = file[13:-4] if tipo is None else file[17:-4]
        op = lambda f: (texto[(f.start()-WIDTH):(f.end()+WIDTH)]).replace('\n','')

        #if isinstance(squery, list):
        #    fmatches = []
        #    for sq in squery:
        #        fmatches+=list(re.finditer(sq+' ', texto))
        #else:
        #    fmatches = list(re.finditer(squery, texto))

        #if len(fmatches):
        #    ftextos = [op(f) for f in fmatches]
        #    qfix = fixers.get(query,[])
        #    bad_mat = []
        #    for qf in qfix:
        #        bad_mat += [x for x in ftextos if qf in x]
        #    if len(bad_mat): # must remove, use zip
        #        fmatches = [f for f in fmatches if op(f) not in bad_mat]
        fmatches = get_matches(query, texto, WIDTH)

        if len(fmatches):
            nMenciones += len(fmatches)
            #ptfile = get_party(tfile)
            ptfile = get_lista(tfile)
            #ptfile = 
            #print(tfile, ptfile)
            if isinstance(squery, list):
                mptf = [op(f).replace(squery[0], MARK %squery[0])
                                for f in fmatches]
                for sq in squery[1:]:
                    mptf = [m.replace(sq, MARK %sq) for m in mptf]
                matches[ptfile] = mptf
            else:
                matches[ptfile] = [op(f).replace(squery, MARK %squery)
                                for f in fmatches] 
    #print('B4:', len(matches))
    matches = {k:v for k,v in matches.items() if len(v)>0}
    #print('AFTA:', len(matches))
    matches =  sorted(matches.items(), key=operator.itemgetter(1))
    #matches.sort('Menciones')
    matches = collections.OrderedDict(matches)

    return matches, nMenciones

matches = lambda wt: len(list(re.finditer(wt[0].lower(), wt[1])))
fmatches = lambda wt: list(re.finditer(wt[0].lower(), wt[1]))

# PROBLEMA: 

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

def get_candy():

    cdf = sql('SELECT * FROM candidatos')

    return cdata
