import glob, operator
import pandas as pd
from pprint import pprint
from collections import OrderedDict
##############################################
files=glob.glob('TEXTOS/TODOS/*.txt')
textos=[open(fn).read() for fn in files]
stext=set(textos)
clus={text: [ix for ix,txt in enumerate(textos) if txt==text] for text in stext}
lendick={len(k):len(v) for k,v in clus.items()}
longdicks={len(k): v for k,v in clus.items() if len(v)>1}

df=pd.read_csv('candidatos.csv')

ix=0;lens = {}; nCopias=0
for k,v in longdicks.items():
    ix+=1; n=len(v); # nOffenders
    vfiles=[files[ix] for ix in v]
    #vdf=??
    vx = [f.split('/')[-1].replace('_',' ') for f in vfiles]
    clist = [(' '.join(c.split()[1:]))[:-4] for c in vx]  # DX JUAN VERA CARRASCO.txt
    vdf = df[df.candidato.isin(clist)]
    vdf = vdf[['candidato','distrito','partido','lista']]
    partidos = vdf.partido.value_counts()
    listas = vdf.lista.value_counts()
    lens[ix] = (n, partidos.to_dict(), listas, vdf)
    print(k,len(clist))
    nCopias += n

print('RESUMEN:', nCopias, 'out of', len(textos), 'Porc:', 100*nCopias/len(textos))

lens =  sorted(lens.items(), key=lambda x: x[1][0], reverse=True)
lens = OrderedDict(lens)

fw=open('static/copiones.html','w')
for cidx, clus in lens.items():
    n, pdict, listas, vdf = clus
    pprint(f'<H3>Cluster {cidx} ({n} programas idénticos)</H3>', fw)
    pprint('<HR>',fw)
    vdf.to_html(fw, index=False,escape=True)
fw.close()

lv=list(lens.values())

lengths=[llv[0] for llv in lv]
parts=[llv[1] for llv in lv]
listas=[pd.DataFrame(llv[2]).to_html(escape=True, index=False) for llv in lv]

cdf=pd.DataFrame(dict(dimension=lengths,partidos=parts,listas=listas))
cdf.sort_values('dimension',ascending=False).to_html('Copiones.html', escape=True,index=False)

