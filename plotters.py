import glob, pandas as pd, numpy as np
import re
from util import *
import seaborn as sns
import matplotlib.pyplot as plt

files = list(glob.glob('TEXTOS/TODOS/*.txt'))
textos = [open(fn).read() for fn in files]

df = pd.DataFrame(dict(archivo=files, texto=textos))
df['distrito'] = [fn.split('/')[2].split('_')[0] for fn in files]
df['largo'] = df.texto.apply(len)
df['candidato'] = [' '.join(fn.split('/')[2].split('_')[1:])[:-4] for fn in files]

cdf=sql('SELECT * FROM candidatos')
xdf=df.merge(cdf, on='candidato').drop(['archivo','distrito_y','programa'],axis=1)

kw = pd.read_csv('keywords.txt', names=['palabra'])
kw['palabra'] = kw.palabra.apply(lambda p: p.split('\t')[1])

for word in kw.palabra:
    xdf[word] = xdf.texto.apply(lambda t: len(list(re.finditer(word.lower(), t))))

sdf=xdf.groupby('partido').sum()
sdf[sdf.columns[1:]].head()

temas = [k for k,v in sdf.sum().to_dict().items() if v>10 and k!='largo']

partidos=[k for k,v in sdf.sum(axis=1).to_dict().items() if v>50]
psdf = sdf[sdf.index.isin(partidos)]
fig, ax = plt.subplots(1, figsize=(20,12))
p=sns.heatmap(psdf[temas].replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y partido (incluye independientes)', size=24);
plt.savefig('heatmap1.png')

fig, ax = plt.subplots(1, figsize=(20,12))
p=sns.heatmap(psdf[psdf.index!='INDEPENDIENTES'][temas].replace(0, np.nan), 
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, cmap='RdYlGn', fmt='.0f');
plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y partido (excluye independientes)', size=24);
plt.savefig('heatmap2.png')

tdf = psdf[psdf.index!='INDEPENDIENTES'][temas]
tdf['partido'] = tdf['partido'].apply(lambda p: p.replace('IND ',''))   # IND RN -> RN
ts = pd.DataFrame(tdf.sum(axis=1).reset_index())
ts.columns = ['partido','total_menciones']
ts = ts[ts.total_menciones>0]
fig,ax = plt.subplots(1, figsize=(20,12))
sns.barplot(x='total_menciones', data=ts.sort_values('total_menciones'), y='partido', palette='RdYlGn');
plt.title('Ranking partidos políticos por número total de menciones', size=20)
plt.savefig('ranking.png')
