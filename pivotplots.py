import seaborn as sns
from searcher import *
import matplotlib.pyplot as plt, numpy as np

dxdf = sql('SELECT * FROM cruce_distrito')
fig, ax = plt.subplots(1, figsize=(20,12))
dpdf = dxdf.pivot_table(columns='distrito', index='tema').replace(0, np.nan)

print('what?')
p = sns.heatmap(dpdf['nMenciones'],annot=True, cmap='RdYlGn', annot_kws={'size':14, 'weight':'bold'})
p.set_title('Menciones Totales por Distrito y Tema', size=18);
p.savefig('plot1_DT_MTot.png')
