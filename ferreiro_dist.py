import os
import glob, pandas as pd

cdf=pd.read_csv('candidatos.csv')

for dl, dldf in cdf.groupby(['distrito','lista']):
    print(dl, len(dldf))
    lista = dl[1].replace('(','').replace(')','')
    dfol=f'FERREIRO/D{dl[0]}'
    dfol = dfol.replace('_/_','/')
    print('DIST_FOLDER:', dfol)
    if not os.path.exists(dfol):
        os.mkdir(dfol)
    dl_fol=f"FERREIRO/D{dl[0]}/{lista.replace(' ','_')}"
    dl_fol = dl_fol.replace('_/_','_')
    if not os.path.exists(dl_fol):
        os.mkdir(dl_fol)
    for _,row in dldf.iterrows():
        fn = f"TEXTOS/TODOS/D{dl[0]}_{row['candidato'].replace(' ','_')}.txt"
        try:
            txt = open(fn,'r').read()
            txt = txt.replace('medio ambiente','medioambiente').replace('Medio Ambiente','medioambiente')
            fw = open(fn,'w')
            fw.write(txt)
            fw.close()
            cmd = f'cp {fn} {dl_fol}'
        #print(cmd)
            os.system(cmd)
        except:
            print('BAD:', cmd)
