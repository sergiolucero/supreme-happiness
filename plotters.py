import glob, pandas as pd, numpy as np
import re
from util import *
from searcher import *

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
plt.autoscale(enable=True, axis='x', tight=True)

files = list(glob.glob('TEXTOS/TODOS/*.txt'))
textos = [open(fn).read() for fn in files]		# ACTUALIZADO!
temas = ['agua','clima', 'medioambiente']
########################################################
df = pd.DataFrame(dict(archivo=files, texto=textos))
df['distrito'] = [fn.split('/')[2].split('_')[0] for fn in files]
df['distrito'] = ['D%02d' %(int(dist[1:])) for dist in df.distrito]
df['largo'] = df.texto.apply(len)
df['candidato'] = [' '.join(fn.split('/')[2].split('_')[1:])[:-4] for fn in files]
############ FINAL COUNTDOWN: normalized and MERGED lists ***

cdf=sql('SELECT * FROM candidatos')
xdf=df.merge(cdf, on='candidato').drop(['archivo','distrito_y','programa'],axis=1)
xdf=xdf.rename(columns={'distrito_x':'distrito'})
xdf['partido'] = xdf.partido.apply(lambda p: p.replace('PARTIDO ','P.').replace('REGIONALISTA ','REG.'))
xdf['lista'] = xdf.lista.apply(lambda lis: lis.replace('  ',' '))
xdf['lista'] = xdf.lista.apply(lambda lis: lis.rstrip())
#xdf.to_csv('candidatos_fixed.csv', index=False)
xdf = pd.read_csv('candidatos_fixed.csv')


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



#C 

#do
#print('B4:', len(xdf))
udi = xdf[xdf.partido=='UNION DEMOCRATA INDEPENDIENTE']
udi.to_html('static/udi.html', index=False)
udi2 = udi[udi.candidato=='DIEGO RIVEAUX MARCET']
udi2.iloc[0]['medioambiente']=2
print('LENU:', len(udi2))
xdf = xdf[xdf.partido!='UNION DEMOCRATA INDEPENDIENTE']
xdf = xdf.append(udi2)
#print('Afta:', len(xdf))
xdf['total_menciones'] = xdf['agua']+xdf['clima']+xdf['medioambiente']
#xdf = xdf.drop(['texto','largo'],axis=1)
ldf = xdf.groupby('lista').sum().reset_index()
print(ldf.columns)
ldf = ldf.drop(['largo'], axis=1)
ldf.to_excel('static/menciones_por_lista.xlsx',index=False)
#wow
xxdf = xdf.copy()       # collapse INDEPENDIENTES
#print(xxdf.head(10)['partido'])
xxdf['partido'] = xxdf.partido.apply(lambda p: p.replace('-IND','')) # fixer
#print(xxdf.head(10)['partido'])
#dos
ddf = xxdf.groupby('distrito').sum()
psdf = ddf.drop('largo', axis=1)

fig, ax = plt.subplots(1, figsize=(24,12))
p = sns.heatmap(psdf.replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f', cbar=False);
#print('PSDF');print(psdf)
plt.xticks(rotation=0)
plt.xticks(fontsize=18)  # agua, clima, medio
fig.subplots_adjust(left=0.3)
#plt.xticks(rotation=45)
plt.xticks(fontsize=18)  # agua, clima, medio

plt.title('Menciones ambientales por tema y distrito (excluye independientes)', size=24);
plt.savefig('static/heatmap_distritos.png')
plt.close()
#############################
PUEBLO = ['Corrientes Independientes', 'A Pulso, Por el Buen Vivir', 'Asamblea Constituyente Atacama',
          'Insulares e Independientes', 'Coordinadora Social de Magallanes']
PUEBLO = [x.lower() for x in PUEBLO]
##################
def fix_list(lis):
    slis = lis.split()

    if len(slis)>3:
        flis = (' '.join(slis[:3]))+chr(10)+(' '.join(slis[3:]))
    else:
        flis = lis
    #print(lis, flis)
    return flis

def fixer_two(flis):
    if flis.lower()[:len('Independientes')]=='independientes' or 'magallanes' in flis.lower():
        flis = 'INDEPENDIENTES NO NEUTRALES (UNIFICADA)'
    elif (flis.lower() in PUEBLO) or 'lista del pueblo' in flis.lower():
        flis = 'LISTA DEL PUEBLO (UNIFICADA)'

    return flis

xdf['lista']
#xdf['lista2'] = xdf.lista.apply(fixer_two)
#xdf['lista'] = xdf.lista.apply(lambda lis: 'if lis=='LISTA DEL PUEBLO '
#lvc = xdf.groupby(['lista','flista']).size()
#lvc = xdf.groupby(['lista']).size()
#ldp = xdf[xdf.lista2=='Lista del Pueblo (UNIFICADA)']
#lin = xdf[xdf.lista2=='Independientes No Neutrales (UNIFICADA)']
#print('PUEBLO:', len(ldp), 'INDY:', len(lin))
#wena
#print(lvc.head(20))

doPlotD = False
if doPlotD:
    for dist, dxdf in xdf.groupby('distrito'):
        dxdf['lista']= dxdf.lista.apply(fix_list)

        dldf = dxdf.groupby('lista').sum()
        psdf = dldf.drop('largo', axis=1)
        fig, ax =  plt.subplots(1, figsize=(14,8))
        fig.subplots_adjust(right=0.8)
        p=sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                annot_kws={'size':20, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f', cbar=False);
        plt.xticks(fontsize=18)  # agua, clima, medio
        plt.yticks(fontsize=14)  # agua, clima, medio
    #plt.margins(x=0.1)
        plt.title(f'Menciones ambientales por tema y lista (Distrito {dist})', size=24);
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()   # all this works!
        plt.yticks(rotation=0)
    #for tick in ax.get_yticklabels():
    #    tick(rotation=45)  # does it work?
        plt.savefig(f'static/heatmap_listas_D{dist}.png')
    #print(dist,end=':')
        plt.close()

        for tema in temas:
            #print('TEMA:', tema)
            tpidf=psdf[[tema]]
            fig, ax = plt.subplots(1, figsize=(24,12))
            p = sns.heatmap(tpidf.replace(0, np.nan),                   # PLOT1: por partido
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
                cmap='RdYlGn', fmt='.0f');
            plt.title(f'Menciones del concepto {tema} por partido (Distrito {dist}, excluye independientes)', size=24);
            plt.savefig(f'static/heatmap_D{dist}_{tema}.png')
            plt.close()


print('PLOTTED: distritos')
#############################
plotLD = False
if plotLD:
    for lista, dxdf in xdf.groupby('lista'):
        clista = lista.replace(' ','_').replace('(','').replace(')','').replace('_/_','_')
        dldf = dxdf.groupby('distrito').sum()
        psdf = dldf.drop('largo', axis=1)

        fig, ax =  plt.subplots(1, figsize=(24,12))
        p = sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                  annot_kws={'size':20, 'weight': 'bold'}, 
                  cmap='RdYlGn', fmt='.0f', cbar=False);
    #plt.xticks(rotation=45)
        plt.xticks(fontsize=18)  # agua, clima, medio
    #plt.yticks(rotation=0)
    #plt.margins(x=0.1)
        plt.title(f'Menciones ambientales por tema lista {clista})', size=24);
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        plt.yticks(rotation=0)  # does it work? 90 don't
        plt.savefig(f'static/heatmap_lista_{clista}.png')
        #print(dist,end=':')

        plt.close()

        for tema in temas:
            print('TEMA:', tema)
            tpidf=dxdf[[tema]]
            fig, ax = plt.subplots(1, figsize=(24,12))
            p = sns.heatmap(tpidf.replace(0, np.nan),                   # PLOT1: por partido
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
                cmap='RdYlGn', fmt='.0f');
            plt.title(f'Menciones del concepto {tema} por partido (excluye independientes)', size=24);
            plt.savefig(f'static/heatmap_lista_{clista}_{tema}.png')
            plt.close()

print('PLOTTED: listas')
#################################
pxdf = xdf.copy()
pxdf['partido'] = pxdf['partido'].apply(lambda p: p[:-4] if p[-4:]=='-IND' else p)   # IND RN -> RN
lisdf = pxdf.groupby('lista').agg({'total_menciones':['sum',len]}).reset_index()
jose = lisdf
jose.columns=['lista','total','nCandidatos']
jose['menciones por candidato'] = jose.total/jose.nCandidatos
lisdf = jose # albibaq
#list_size = pxdf.groupby('lista').size()
#print('CAVEAT:');print(pxdf.value_counts('lista').head(10))

fig, ax = plt.subplots(1, figsize=(24,12))
#lisdf = lisdf.drop(columns=['largo'], axis=1)
#ts = lisdf.sum(axis=1).sort_values().reset_index()
#ts.columns = ['lista','total_menciones']
#ts['total_menciones']=ts.total_menciones/2       # está duplicada
#print(ts)
#wn
ts = lisdf.sort_values('menciones por candidato').tail(20)
ax = sns.barplot(x='menciones por candidato', data=ts,
            y='lista', palette='RdYlGn')
#sns.barplot(x='total_menciones', data=ts.sort_values('total_menciones'), 
#            y='lista', palette='RdYlGn')
for xx in (20,40):    
    plt.axvline(x=xx, color='blue')
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()   # all this works!
###   plot them numbers too!
for patch in ax.patches:
    xy = patch.get_width()*0.77, patch._y0+0.33
    texto = '%.2f' %patch.get_width()
    #print(xy)
    ax.annotate(texto, xy, color='blue', fontsize=16, weight='bold')

#plt.margins(x=0.4)
#plt.xlim([0,3000])
#plt.title('Menciones ambientales TOTALES por lista (top 20)', size=24)
plt.title('Menciones ambientales POR CANDIDATO de cada lista (top 20)', size=24)
plt.subplots_adjust(left=0.1, right=0.6, top=0.9, bottom=0.1)
plt.savefig('static/barplot_listas.png')
plt.close()
##########schtoops###########
for tema in temas:
    tdf=xdf[['lista',tema]]
    tdf['lista']= tdf.lista.apply(fix_list)
    fig, ax = plt.subplots(1, figsize=(24,12))
    ts = xdf.groupby('lista').sum().reset_index()
    sns.barplot(x=tema, data=ts.sort_values(tema).tail(20), 
            y='lista', palette='RdYlGn')
    #for xx in (400,800):    
    #    plt.axvline(x=xx, color='blue')
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()   # all this works!
    plt.subplots_adjust(left=0.05, right=0.6, top=0.9, bottom=0.1)
    #plt.margins(x=0.2)
    #plt.xlim([0,1000] if tema=='agua' else [0,400] if tema=='clima' else [0,1500])
    plt.title(f'Menciones por lista del tema {tema} (top 20)', size=24)
    plt.savefig(f'static/barplot_listas_{tema}.png')
    plt.close()




##########schtoops###########

sdf = pxdf.groupby('partido').sum()
#sdf[sdf.columns[1:]].head()

temas = [k for k,v in sdf.sum().to_dict().items() if v>10 and k!='largo']

partidos=[k for k,v in sdf.sum(axis=1).to_dict().items() if v>50]
partidos = [p for p in partidos if partidos!='INDEPENDIENTES']
psdf = sdf[sdf.index.isin(partidos)]
fig, ax = plt.subplots(1, figsize=(24,12))
p=sns.heatmap(psdf[temas].replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f');
#plt.xticks(rotation=45)
plt.title('Menciones ambientales por tema y partido (incluye independientes)', size=24);
plt.savefig('static/heatmap_partidosI.png')
plt.close()
############################################### PLOT_PARTIDOS SIN_INDIES
iidf = psdf[psdf.index=='INDEPENDIENTES']
pidf = psdf[psdf.index!='INDEPENDIENTES']
pidf.to_csv('resument_partidos_sin_ind.pdf',index=False)
#print('B4:', pidf.index)
pidf.index = [p.replace('PARTIDO ','P.').replace('REGIONALISTA ','REG.') for p in pidf.index]
#print('A5:', pidf.index)
#don
#p = sns.heatmap(psdf[psdf.index!='INDEPENDIENTES'][temas].replace(0, np.nan),                   # PLOT1: por partido
fig, ax = plt.subplots(1, figsize=(24,12))
p = sns.heatmap(pidf[temas].replace(0, np.nan),                   # PLOT1: por partido
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
               cmap='RdYlGn', fmt='.0f');
#plt.xticks(rotation=45); plt.title('Menciones ambientales por tema y partido (excluye independientes)', size=24);
plt.savefig('static/heatmap_partidos.png')
plt.close()

temas = ['agua','clima','medioambiente']
for tema in temas:
    print('TEMA:', tema)
    tpidf=pidf[[tema]]
    fig, ax = plt.subplots(1, figsize=(24,12))
    p = sns.heatmap(tpidf.replace(0, np.nan),                   # PLOT1: por partido
              annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
                cmap='RdYlGn', fmt='.0f');
    plt.title(f'Menciones del concepto {tema} por partido (excluye independientes)', size=24);
    plt.savefig(f'static/heatmap_partidos_{tema}.png')
    plt.close()

tdf = psdf[psdf.index!='INDEPENDIENTES'][temas].reset_index()
tdf['partido'] = tdf['partido'].apply(lambda p: p[4:]+'-IND ' if p[:3]=='IND' else p)   # IND RN -> RN
#ts = pd.DataFrame(tdf.sum(axis=1).reset_index())
############## GRAFICO DE BARRAS POR PARTIDO: make stacks
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
#################
plt.title('Ranking partidos políticos por número total de menciones', size=20)
plt.savefig('static/ranking.png')
plt.close()
##################
ts = tdf.groupby('partido').sum().sum(axis=1).sort_values().reset_index()
sdf = ts.groupby('partido').size()
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

