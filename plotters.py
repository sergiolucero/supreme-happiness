import glob, pandas as pd, numpy as np
import re
from util import *
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
        xdf_word = xdf.texto.apply(lambda t: len(list(re.finditer(word.lower(), t))))
        xconc = [x+y for x,y in zip(xconc, xdf_word.values)]
    xdf[conc] = xconc

xdf['partido'] = xdf.partido.apply(lambda p: p.split('IND ')[1]+'-IND' if 'IND ' in p else p) # fixer

ddf = xdf.groupby('distrito').sum()
psdf = ddf.drop('largo', axis=1)
fig, ax = plt.subplots(1, figsize=(24,12))
p=sns.heatmap(psdf.replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y distrito (excluye independientes)', size=24);
plt.savefig('static/heatmap_distritos.png')
plt.close()
#############################
ldf = xdf.groupby('lista').sum()
psdf = ldf.drop('largo', axis=1)
fig, ax = plt.subplots(1, figsize=(24,12))
p=sns.heatmap(psdf.replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y lista', size=24);
plt.savefig('static/heatmap_listas.png')
plt.close()
#############################



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
p=sns.heatmap(psdf[psdf.index!='INDEPENDIENTES'][temas].replace(0, np.nan), 
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

arr_lena = mpimg.imread('greenpeace.png')
imagebox = OffsetImage(arr_lena, zoom=1.0)
ab = AnnotationBbox(imagebox, (825, 0.3))
ax.add_artist(ab)

plt.title('Ranking partidos políticos por número total de menciones', size=20)
plt.savefig('static/ranking.png')
plt.close()
