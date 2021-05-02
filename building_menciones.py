import sqlite3, pandas as pd
import glob
import time
import re
from searcher import get_matches

men=pd.read_csv('keywords2.txt', names=['Tema'])  # redone 20/04

#men.iloc[18]['Tema']='18\tsequía'
#men['Tema']=men.Tema.apply(lambda t: t.split('\t')[1])
files = list(glob.glob('TEXTOS/TODOS/*.txt'))
nProgramas = len(files)
print('nProgramas:', nProgramas)

t0=time.time();textos=[open(fn).read() for fn in files]
print('DT:', round(time.time()-t0,2))  # 0.11 sec

matches = lambda wt: len(list(re.finditer(wt[0].lower(), wt[1])))

conn=sqlite3.connect('greenpeace.db')

nmatches=[]
amatches=[]
print('TEMAS:', men.Tema)

for word in men.Tema:
    nmatches.append(sum(matches([word,text]) for text in textos))
    amatches.append(sum([1 if word in text else 0 for text in textos])/nProgramas)    # normalized 20/04

men['nMenciones']=nmatches
men['Porc.Mencionan']=[round(100*amat,1) for amat in amatches]

BASE= 'http://greenpeace.quant.cl:8081'
men['link']=['%s/ver_menciones/%s/50' %(BASE,tema.replace(' ','_')) 
                for tema in men.Tema]
men.to_sql('menciones', conn, index=False, if_exists='replace')

