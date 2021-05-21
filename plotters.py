import glob, pandas as pd, numpy as np
import re
from util import *
from searcher import *
from graphics import *
########################
files = list(glob.glob('TEXTOS/TODOS/*.txt'))
textos = [open(fn).read() for fn in files]		# ACTUALIZADO!
temas = ['agua','clima', 'medioambiente']
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
########################################################
def plotme(xdf):
    ldf = xdf.groupby('lista').sum().reset_index()
    print(ldf.columns)
    ldf = ldf.drop(['largo'], axis=1)
    ldf.to_excel('static/menciones_por_lista.xlsx',index=False)
    xxdf = xdf.copy()       # collapse INDEPENDIENTES
    xxdf['partido'] = xxdf.partido.apply(lambda p: p.replace('-IND','')) # fixer
    ddf = xxdf.groupby('distrito').sum()
    psdf = ddf.drop('largo', axis=1)

    fig, ax = plt.subplots(1, figsize=(24,12))
    p = sns.heatmap(psdf.replace(0,np.nan), annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
              cmap='RdYlGn', fmt='.0f', cbar=False);
    plt.xticks(rotation=0)
    plt.xticks(fontsize=18)  # agua, clima, medio
    fig.subplots_adjust(left=0.3)
    plt.xticks(fontsize=18)  # agua, clima, medio

    plt.title('Menciones ambientales por tema y distrito (excluye independientes)', size=24);
    plt.savefig('static/heatmap_distritos.png')
    plt.close()

    xdf['lista'] = xdf.lista.apply(fixer_two)

    ldp = xdf[xdf.lista=='LISTA DEL PUEBLO (UNIFICADA)']
    lin = xdf[xdf.lista=='INDEPENDIENTES NO NEUTRALES (UNIFICADA)']
    print('PUEBLO:', len(ldp), 'INDY:', len(lin))
    #wena
    #print(lvc.head(20))

    doPlotD = True
    if doPlotD:
        for dist, dxdf in xdf.groupby('distrito'):
            dxdf['lista']= dxdf.lista.apply(fix_list)

            dldf = dxdf.groupby('lista').sum()
            dldfs = dxdf.groupby('lista').size()

            psdf = dldf.drop('largo', axis=1)

            for col in psdf.columns:
                psdf[col]/=dldfs.values

            fig, ax =  plt.subplots(1, figsize=(14,8))
            fig.subplots_adjust(right=0.8)
            p=sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                    annot_kws={'size':20, 'weight': 'bold'}, 
                  cmap='RdYlGn', fmt='.1f', cbar=False);
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
            if len(psdf):
                fig, ax =  plt.subplots(1, figsize=(24,12))
                p = sns.heatmap(psdf.replace(0,np.nan), annot=True, 
                      annot_kws={'size':20, 'weight': 'bold'}, 
                      cmap='RdYlGn', fmt='.0f', cbar=False);
                plt.xticks(fontsize=18)  # agua, clima, medio
                plt.title(f'Menciones ambientales por tema lista {clista})', size=24);
                ax.yaxis.set_label_position("right")
                ax.yaxis.tick_right()
                plt.yticks(rotation=0)  # does it work? 90 don't
                plt.savefig(f'static/heatmap_lista_{clista}.png')
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

    parsize = pxdf.groupby('partido').size().reset_index()
    parsize.columns = ['partido','nCandidatos']
    pardict = {parsize.partido.values[ix]: parsize.nCandidatos.values[ix]
               for ix in range(len(parsize))}

    #were

    lisdf = pxdf.groupby('lista').agg({'total_menciones':['sum',len]}).reset_index()
    jose = lisdf
    jose.columns=['lista','total','nCandidatos']
    jose['menciones por candidato'] = jose.total/jose.nCandidatos
    claves = jose.lista.values
    candis = jose.nCandidatos.values
    candick = {claves[ix]: candis[ix] for ix in range(len(jose))}
    #jose.nCandidatos.to_dict()
    #valle
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

    #plt.margins(x=0.4)
    #plt.xlim([0,3000])
    #plt.title('Menciones ambientales TOTALES por lista (top 20)', size=24)
    label_barplot(ax)
    plt.title('Menciones ambientales POR CANDIDATO de cada lista (top 20)', size=24)
    plt.subplots_adjust(left=0.1, right=0.6, top=0.9, bottom=0.1)
    plt.savefig('static/barplot_listas.png')
    plt.close()
    ##########schtoops###########
    for tema in temas:
        tdf=xdf[['lista',tema]]
        tdf['lista'] = tdf['lista'].apply(fix_list) #, in_place=True)
        fig, ax = plt.subplots(1, figsize=(24,12))
        ts = xdf.groupby('lista').sum().reset_index()
        # ahora los promedios
        ts[tema]=[row[tema]/candick[row['lista']] for _,row in ts.iterrows()]
        ax = sns.barplot(x=tema, data=ts.sort_values(tema).tail(20), 
                y='lista', palette='RdYlGn')
        #if tema=='agua':        wendy
        #print('-'*32, tema, '-*32')
        #print(ts.sort_values(tema))
        #for xx in (400,800):    
        #    plt.axvline(x=xx, color='blue')
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()   # all this works!
        plt.subplots_adjust(left=0.05, right=0.6, top=0.9, bottom=0.1)
        #plt.margins(x=0.2)
        #plt.xlim([0,1000] if tema=='agua' else [0,400] if tema=='clima' else [0,1500])
        label_barplot(ax)
        plt.title(f'Menciones por candidato del tema {tema} (top 20)', size=24)
        plt.savefig(f'static/barplot_listas_{tema}.png')
        plt.close()




    ##########schtoops###########

    sdf = pxdf.groupby('partido').sum()
    #sdf[sdf.columns[1:]].head()
    for col in sdf.columns[1:]:
        sdf[col] = sdf[col]/[pardict[p] for p in sdf.index]

    temas = [k for k,v in sdf.sum().to_dict().items() if v>0 and k!='largo']

    partidos=[k for k,v in sdf.sum(axis=1).to_dict().items() if v>0]
    partidos = [p for p in partidos if partidos!='INDEPENDIENTES']
    psdf = sdf[sdf.index.isin(partidos)]
    fig, ax = plt.subplots(1, figsize=(24,12))
    p=sns.heatmap(psdf[temas].replace(0,np.nan), annot=True, 
                    annot_kws={'size':16, 'weight': 'bold'}, 
                  cmap='RdYlGn', fmt='.1f');
    #plt.xticks(rotation=45)
    plt.title('Menciones ambientales PROMEDIO por tema y partido (incluye independientes)', size=24);
    ax.xaxis.label.set_size(18)
    label_barplot(p)
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
                   cmap='RdYlGn', fmt='.1f');
    #plt.xticks(rotation=45); 
    plt.title('Menciones ambientales PROMEDIO por tema y partido (excluye independientes)', size=24);
    ax.xaxis.label.set_size(18)
    #plt.xlabel('menciones', fontsize=18)
    plt.savefig('static/heatmap_partidos.png')
    plt.close()

    temas = ['agua','clima','medioambiente']
    for tema in temas:
        print('TEMA:', tema)
        tpidf=pidf[[tema]]
        fig, ax = plt.subplots(1, figsize=(24,12))
        p = sns.heatmap(tpidf.replace(0, np.nan),                   # PLOT1: por partido
                  annot=True, annot_kws={'size':16, 'weight': 'bold'}, 
                    cmap='RdYlGn', fmt='.1f');
        plt.title(f'Menciones PROMEDIO del concepto {tema} por partido (excluye independientes)', size=24);
        ax.xaxis.label.set_size(18)
        #plt.xlabel(tema, fontsize=18)
        plt.savefig(f'static/heatmap_partidos_{tema}.png')
        plt.close()

    tdf = psdf[psdf.index!='INDEPENDIENTES'][temas].reset_index()
    #tdf['partido'] = tdf['partido'].apply(lambda p: p[4:]+'-IND ' if p[:3]=='IND' else p)   # IND RN -> RN
    #tptp

    #ts = pd.DataFrame(tdf.sum(axis=1).reset_index())
    ############## GRAFICO DE BARRAS POR PARTIDO: make stacks
    ts = tdf.groupby('partido').sum().sum(axis=1).sort_values().reset_index()
    ts.columns = ['partido','promedio_menciones']
    ts = ts[ts.promedio_menciones>0]
    fig,ax = plt.subplots(1, figsize=(24,12))
    N=len(xdf)
    #print('DAAAARK')
    ax = sns.barplot(x='promedio_menciones', 
                data=ts.sort_values('promedio_menciones'), 
                y='partido', palette='RdYlGn');
    for xx in (10,20,30):
        plt.axvline(x=xx, color='blue')
    plt.margins(x=0.1)
    label_barplot(ax)
    #############################################   LOGOS
    arr_lena = mpimg.imread('static/greenpeace.png')
    imagebox = OffsetImage(arr_lena, zoom=1.0)
    ab = AnnotationBbox(imagebox, (30.5, 1.0))
    ax.add_artist(ab)

    arr_lena = mpimg.imread('static/QuantLogo2.png')
    imagebox = OffsetImage(arr_lena, zoom=0.2)
    ab = AnnotationBbox(imagebox, (32, 3.0))
    ax.add_artist(ab)
    #################
    plt.title(f'Ranking partidos políticos por número de menciones medioambientales por candidato (N={N})', 
                size=20)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.savefig('static/ranking.png')
    plt.close()
    ##################
    #ts = tdf.groupby('partido').sum().sum(axis=1).sort_values().reset_index()
    #sdf = ts.groupby('partido').size()
    #ts.columns = ['partido','promedio_menciones']
    #ts = ts[ts.promedio_menciones>0]
    #fig,ax = plt.subplots(1, figsize=(24,12))
    #sns.barplot(x='promedio_menciones', data=ts.sort_values('promedio_menciones'), y='partido', palette='RdYlGn');
    #for xx in range(200,1000,200):
    #    plt.axvline(x=xx, color='blue')
    #plt.margins(x=0.1)

    #arr_lena = mpimg.imread('static/greenpeace.png')
    #imagebox = OffsetImage(arr_lena, zoom=1.0)
    #ab = AnnotationBbox(imagebox, (825, 1.0))
    #ax.add_artist(ab)

