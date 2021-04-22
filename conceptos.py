import sqlite3, pandas as pd
import glob
import time
import re

matches = lambda wt: len(list(re.finditer(wt[0].lower(), wt[1])))
conn=sqlite3.connect('greenpeace.db')

pfiles = {'todos': list(glob.glob('TEXTOS/TODOS/*.txt')),
          'originarios': list(glob.glob('TEXTOS/INDIGENAS/*.txt')),
}

for tabla, files in pfiles.items():
    men = pd.read_csv('keywords2.txt', header=0)  # redone 21/04 concepto, tema
    nProgramas = len(files)
    print('nProgramas:', nProgramas)

    t0 = time.time()
    textos=[open(fn).read() for fn in files]
    print('DT:', round(time.time()-t0,2))  # 0.11 sec

    nmatches=[]
    amatches=[]
    print('TEMAS:', men['tema'])
    smen = pd.DataFrame(men['concepto'].unique(), columns=['concepto'])

    for word, cdf in men.groupby('concepto'):
        wnmatch = 0;         wamatch = 0.0
        for _, row in cdf.iterrows():
            print('CONCEPTO:', word, 'TEMA:', row['tema'])
            wnmatch += sum(matches([row['tema'],text]) for text in textos)   # missing space?
            wamatch += sum([1 if row['tema'] in text else 0 for text in textos])/nProgramas    # normalized 20/04
        nmatches.append(wnmatch);        amatches.append(wamatch)
    print('NA', nmatches, amatches)
    smen['nMenciones']=nmatches
    smen['\% Mencionan']=[round(100*amat,2) for amat in amatches]

    BASE= 'http://greenpeace.quant.cl:8081'
    smen['link']=men.concepto.apply(lambda concepto: '%s/ver_menciones/%s/50' %(BASE,concepto))
    smen.to_sql(f'menciones_{tabla}', conn, index=False, if_exists='replace')

    print(tabla); print(men)
