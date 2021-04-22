from searcher import *
from itertools import product

conn = sqlite3.connect('greenpeace.db')

temas=sql('SELECT LOWER(Tema) FROM menciones').values
print('TEMAS:', temas)
temas = [t[0] for t in temas]

cdf = pd.read_csv('candidatos.csv')
cdf['partido'] = cdf.partido.apply(lambda p: p[4:]+'-IND' if p[:3]=='IND' else p)
distritos = cdf.distrito.unique()
files = list(glob.glob('TEXTOS/TODOS/*.txt'))
textos = [open(fn).read() for fn in files]

#proyeccion por distrito, lista, partido...
# 1. por distrito

nMen=[];nProg=[];Temas=[];Dists=[]

for tema, dist in product(temas, distritos):
    #print(tema,dist)
    Dist = 'D%d_' %dist
    dist_idx = [ix for ix,fn in enumerate(files) if Dist in fn]
    dtextos = [textos[idx] for idx in dist_idx]
    #print(tema,dist, len(dtextos))
    nprogs = len([ix for ix,txt in enumerate(dtextos) if tema in txt])
    nmencs = sum([len(list(re.finditer(tema,txt))) for txt in dtextos])
    Temas.append(tema);Dists.append(dist)
    nMen.append(nmencs); nProg.append(nprogs)

dxdf = pd.DataFrame(dict(tema=Temas,distrito=Dists,
                         nProgramas=nProg,nMenciones=nMen))
dxdf.to_html('static/cruce_tema_distrito.html', index=False)
dxdf.to_sql('cruce_distrito', conn, index=False, if_exists='replace')

# 2. por lista/partido
for token in ['lista','partido']:
    nMen=[];nProg=[];Temas=[];Tokes=[];nBads=0;Dists=[]
    for toke, tdf in cdf.groupby(token):
        tcands = tdf.candidato
        tdists = tdf.distrito
        for dist, cand in zip(tdists, tcands):
            mask = 'D%d_%s' %(dist,cand.replace(' ','_'))
            tdc_idx = [ix for ix,fn in enumerate(files) if mask in fn]
            tdc_txt = [textos[idx] for idx in tdc_idx]

            if len(tdc_txt)==0:
                tdc_idx = [ix for ix,fn in enumerate(files) if mask[:20] in fn]
                tdc_txt = [textos[idx] for idx in tdc_idx]

            if len(tdc_txt)==0:
                print(mask[:20])
                #print('BAD:', token, mask, len(tdc_txt))
                nBads+=1

            if len(tdc_txt)>0:
                texto = tdc_txt[0]
                for tema in temas:
                    nprogs = 1 if tema in texto else 0
                    nmencs = len(list(re.finditer(tema,texto)))
                    Temas.append(tema);Tokes.append(token);Dists.append(toke)
                    nMen.append(nmencs); nProg.append(nprogs)

    tdf = pd.DataFrame(dict(tipo=Tokes, tema=Temas, nMenciones=nMen, nProgramas=nProg))
    tdf[token] = Dists
    tdf.to_sql('cruce_'+token, conn, index=False, if_exists='replace')
    
    print(token, nBads, '-'*80)
    print(tdf.head())
