import sqlite3, pandas as pd
import glob
from searcher import finders

conn=sqlite3.connect('greenpeace.db')

pfiles = {'todos': list(glob.glob('TEXTOS/TODOS/*.txt')),
          'originarios': list(glob.glob('TEXTOS/INDIGENAS/*.txt')),
}

for tabla, files in pfiles.items():
    kw = eval(open('keywords_final.txt').read())  # last train
    textos=[open(fn).read() for fn in files]

    smen = pd.DataFrame()
    for concepto, menciones in kw.items():
        # buscamos el concepto, tomando en cuenta si está en menciones
        smen = smen.append(finders(textos, concepto, menciones))

    #BASE= 'http://greenpeace.quant.cl:8081'
    BASE= 'http://greenpeace-monitor.herokuapp.com'
    smen['link'] = smen.concepto.apply(lambda concepto: '%s/ver_menciones/%s/50' %(BASE,concepto))
    smen.to_sql(f'menciones_{tabla}', conn, index=False, if_exists='replace')

    print(tabla); print(smen)
