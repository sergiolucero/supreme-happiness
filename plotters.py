import glob, pandas as pd, numpy as np
import re
from util import *
from searcher import *

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

files = list(glob.glob('TEXTOS/TODOS/*.txt'))
textos = [open(fn).read() for fn in files]		# ACTUALIZADO!

df = pd.DataFrame(dict(archivo=files, texto=textos))
df['distrito'] = [fn.split('/')[2].split('_')[0] for fn in files]
df['largo'] = df.texto.apply(len)
df['candidato'] = [' '.join(fn.split('/')[2].split('_')[1:])[:-4] for fn in files]

cdf=sql('SELECT * FROM candidatos')
xdf=df.merge(cdf, on='candidato').drop(['archivo','distrito_y','programa'],axis=1)
xdf=xdf.rename(columns={'distrito_x':'distrito'})
xdf['partido'] = xdf.partido.apply(lambda p: p.replace('PARTIDO ','P.').replace('REGIONALISTA ','REG.'))
#kw = pd.read_csv('keywords.txt', names=['palabra'])
kw = eval(open('keywords_final.txt').read())
#kw['palabra'] = kw.palabra.apply(lambda p: p.split('\t')[1])
#WORDS = list(kw.keys())
#for v in kw.values():
#    WORDS += v
#print('WORDS:', WORDS)
#kw = {'concepto': [menciones]}

#for word in WORDS:
#    xdf[word] = xdf.texto.apply(lambda t: len(list(re.finditer(word.lower(), t))))

kw = {k: [k]+v for k,v in kw.items()}
for conc, mens in kw.items():
    xconc = [0]*len(xdf)
    for word in mens:
        #xdf_word = xdf.texto.apply(lambda t: len(list(re.finditer(word.lower(), t))))
        xdf_word = xdf.texto.apply(lambda t: len(get_matches(word, t, 50)))  # no EXCEPTIONS!!
        xconc = [x+y for x,y in zip(xconc, xdf_word.values)]
    xdf[conc] = xconc
#print(xdf[xdf.partido=='UNION DEMOCRATICA INDEPENDIENTE'])

xdf['partido'] = xdf.partido.apply(lambda p: p.split('IND ')[1]+'-IND' if 'IND ' in p else p) # fixer
xdf['lista'] = xdf.lista.apply(lambda x: x.split('(')[0] if '(' in x else x)
#do
print('B4:', len(xdf))
udi = xdf[xdf.partido=='UNION DEMOCRATA INDEPENDIENTE']
udi.to_html('static/udi.html', index=False)
xdf = xdf[xdf.partido!='UNION DEMOCRATA INDEPENDIENTE']
print('Afta:', len(xdf))
#sexi    

ddf = xdf.groupby('distrito').sum()
psdf = ddf.drop('largo', axis=1)

fig, ax = plt.subplots(1, figsize=(24,12))
p=sns.heatmap(psdf.replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y distrito (excluye independientes)', size=24);
plt.savefig('static/heatmap_distritos.png')
plt.close()
#############################
for dist, dxdf in xdf.groupby('distrito'):
    dldf = dxdf.groupby('lista').sum()
    psdf = dldf.drop('largo', axis=1)
    fig, ax =  plt.subplots(1, figsize=(24,12))
    p=sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                annot_kws={'size':20, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
    plt.xticks(rotation=45)
    plt.margins(x=0.1)
    plt.title(f'Menciones ambientales por tema y lista (Distrito {dist})', size=24);
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    plt.savefig(f'static/heatmap_listas_D{dist}.png')
    print(dist,end=':')
    plt.close()
#############################
for lista, dxdf in xdf.groupby('lista'):
    dldf = dxdf.groupby('distrito').sum()
    psdf = dldf.drop('largo', axis=1)
    fig, ax =  plt.subplots(1, figsize=(24,12))
    p=sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                  annot_kws={'size':20, 'weight': 'bold'}, 
                  cmap='RdYlGn', fmt='.0f');
    plt.xticks(rotation=45)
    plt.margins(x=0.1)
    plt.title(f'Menciones ambientales por tema lista {lista})', size=24);
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    clista = lista.replace(' ','_').replace('(','').replace(')','').replace('_/_','_')
    plt.savefig(f'static/heatmap_lista_{clista}.png')
    print(dist,end=':')
    plt.close()


sdf=xdf.groupby('partido').sum()
sdf[sdf.columns[1:]].head()

temas = [k for k,v in sdf.sum().to_dict().items() if v>10 and k!='largo']

partidos=[k for k,v in sdf.sum(axis=1).to_dict().items() if v>50]
partidos = [p for p in partidos if partidos!='INDEPENDIENTES']
psdf = sdf[sdf.index.isin(partidos)]
fig, ax = plt.subplots(1, figsize=(24,12))
p=sns.heatmap(psdf[temas].replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y partido (incluye independientes)', size=24);
plt.savefig('static/heatmap_partidosI.png')
plt.close()

fig, ax = plt.subplots(1, figsize=(24,12))
pidf = psdf[psdf.index!='INDEPENDIENTES']
pidf.to_csv('resument_partidos_sin_ind.pdf',index=False)
#print('B4:', pidf.index)
pidf.index = [p.replace('PARTIDO ','P.').replace('REGIONALISTA ','REG.') for p in pidf.index]
#print('A5:', pidf.index)
#don
p = sns.heatmap(psdf[psdf.index!='INDEPENDIENTES'][temas].replace(0, np.nan),                   # PLOT1: por partido
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y partido (excluye independientes)', size=24);
plt.savefig('static/heatmap_partidos.png')
plt.close()

tdf = psdf[psdf.index!='INDEPENDIENTES'][temas].reset_index()
tdf['partido'] = tdf['partido'].apply(lambda p: p[4:]+'-IND ' if p[:3]=='IND' else p)   # IND RN -> RN
#ts = pd.DataFrame(tdf.sum(axis=1).reset_index())
ts = tdf.groupby('partido').sum().sum(axis=1).sort_values().reset_index()
ts.columns = ['partido','total_menciones']
ts = ts[ts.total_menciones>0]
fig,ax = plt.subplots(1, figsize=(24,12))
sns.barplot(x='total_menciones', data=ts.sort_values('total_menciones'), y='partido', palette='RdYlGn');
for xx in range(200,1000,200):
    plt.axvline(x=xx, color='blue')
plt.margins(x=0.1)

arr_lena = mpimg.imread('greenpeace.png')
imagebox = OffsetImage(arr_lena, zoom=1.0)
ab = AnnotationBbox(imagebox, (825, 1.0))
ax.add_artist(ab)

plt.title('Ranking partidos políticos por número total de menciones', size=20)
plt.savefig('static/ranking.png')
plt.close()
