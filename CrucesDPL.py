import seaborn as sns
from searcher import *
import matplotlib.pyplot as plt, numpy as np

plt.ioff()
pd.set_option('max_colwidth', None)

dxdf = sql('SELECT * FROM cruce_distrito')

def pfix(p):        # IND RN -> RN IND
    ps = p.split()
    return p if ps[0]!='IND' else ' '.join(ps[1:]+['IND'])

if True:
    fig, ax = plt.subplots(1, figsize=(20,12))
    dpdf = dxdf.pivot_table(columns='distrito', index='tema').replace(0, np.nan)
    p = sns.heatmap(dpdf['nMenciones'],annot=True, cmap='RdYlGn', annot_kws={'size':14, 'weight':'bold'})
    p.set_title('Menciones Totales por Distrito y Tema', size=18);
    plt.savefig('static/x1.png')
    plt.close()

    fig, ax = plt.subplots(1, figsize=(20,12))
    p = sns.heatmap(dpdf['nProgramas'],annot=True, cmap='RdYlGn', annot_kws={'size':14, 'weight':'bold'})
    p.set_title('Programas con Menciones por Distrito y Tema', size=18);
    plt.savefig('static/x2.png')
    plt.close()

    pdf = sql('SELECT * FROM cruce_partido')
    pdf['partido'] = pdf.partido.apply(pfix)
    fig, ax = plt.subplots(1, figsize=(24,12))
    pdf = pdf[~pdf.partido.isin(['INDEPENDIENTE','INDEPENDIENTES'])]
    dpdf = pdf.pivot_table(index='partido', columns='tema', aggfunc='sum').replace(0, np.nan)

    p = sns.heatmap(data=dpdf['nMenciones'], annot=True, cmap='RdYlGn',
                annot_kws={'size':14, 'weight':'bold'}, fmt='.0f')
    p.set_title('Menciones Totales por Partido y Tema (sin INDEPENDIENTES)', size=18);

    plt.savefig('static/x3.png')
    plt.close()
    print('DONE 3')

ldf = sql('SELECT * FROM cruce_lista')
#lista, tema, SUM(nMenciones) AS nMenciones FROM cruce_lista GROUP BY lista, tema')
fig, ax = plt.subplots(1, figsize=(24,12))
dldf = ldf.pivot_table(index='lista', columns='tema', aggfunc='sum').replace(0, np.nan)
p = sns.heatmap(dldf['nMenciones'], annot=True, cmap='RdYlGn', 
                annot_kws={'size':14, 'weight':'bold'}, fmt='.0f')
p.set_title('Menciones Totales por Lista y Tema', size=18);
plt.savefig('static/x4.png')
plt.close()



