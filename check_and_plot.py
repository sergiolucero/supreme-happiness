from plotters import *
########################
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
#print('ooYYYYurop')
cdf=sql('SELECT * FROM candidatos')
xdf=df.merge(cdf, on='candidato').drop(['archivo','distrito_y','programa'],axis=1)
xdf=xdf.rename(columns={'distrito_x':'distrito'})
xdf['partido'] = xdf.partido.apply(lambda p: p.replace('PARTIDO ','P.').replace('REGIONALISTA ','REG.'))
xdf['lista'] = xdf.lista.apply(lambda lis: lis.replace('  ',' '))
xdf['lista'] = xdf.lista.apply(lambda lis: lis.rstrip())
#xdf.to_csv('candidatos_fixed.csv', index=False)
xdf = pd.read_csv('candidatos_fixed.csv')
edf = pd.read_csv('electos.csv')   # filtro 19 mayo

bads = []
oxdf = pd.DataFrame()

for candi in edf.NOMBRE:
    cs = candi.split()
    cs = [c for c in cs if '.' not in c]
    cq = ' AND '.join([f" candidato LIKE '%{c.upper()}%'" for c in cs])
    q = f'SELECT * FROM candidatos WHERE {cq}'
    
    #if 'TOLOZA' in q:
    #    print('TOLOZA')
    #    q = "SELECT * FROM candidatos WHERE candidato LIKE '%TOLOZA%'"
    #q = f"SELECT * FROM candidatos WHERE candidato LIKE '%{cs[0].upper()}%'"
    #sq = sql(q)
    sq = cdf.copy();lens=[]
    for c in cs:
        sq = sq[sq.candidato.str.contains(c.upper())]
        lens.append(len(sq))
    #for ccs in cs[1:]:
    #    sq = sq[sq.candidato.str.contains(ccs)]

    if len(sq)==1:
        ucand = sq.iloc[0]['candidato'].upper()
        scdf = cdf[cdf.candidato.str.contains(ucand)]
        if len(scdf)==0:
            #print(candi, len(scdf))
            #print(ucand)
            #print(q)
            #wet
        oxdf = oxdf.append(scdf)
        #print(oxdf)
        print(len(oxdf),end=':')
    else:  # try originarios
        print('oricheck', lens)
        q = f'SELECT * FROM candidatos_originarios WHERE {cq.upper()}'
        sq = sql(q)
        if len(sq)==1:
            oxdf=oxdf.append(sq)
        else:        #jose
            #print('BAD:', candi, len(sq))
            #print(q)
            bads.append(candi)
xdf = oxdf
xdf['partido'] = xdf.partido.apply(lambda p: 'ORIGINARIOS' if isinstance(p,float) else p)
xdf['lista'] = xdf.lista.apply(lambda p: 'ORIGINARIOS' if isinstance(p,float) else p)
print('BADS:', bads)

N = len(xdf)
print('N=',N)
#wtf
#print(len(xdf), len(edf))
#wey
#####################
kw = eval(open('keywords_final.txt').read())
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
#udi = xdf[xdf.partido=='UNION DEMOCRATA INDEPENDIENTE']
#udi.to_html('static/udi.html', index=False)
#udi2 = udi[udi.candidato=='DIEGO RIVEAUX MARCET']
#udi2.iloc[0]['medioambiente']=2
#print('LENU:', len(udi2))
#xdf = xdf[xdf.partido!='UNION DEMOCRATA INDEPENDIENTE']
#xdf = xdf.append(udi2)
#print('Afta:', len(xdf))
xdf['total_menciones'] = xdf['agua']+xdf['clima']+xdf['medioambiente']

xdf.to_excel('static/menciones_por_candidato.xlsx', index=False)

print('DONE CLEANING')
plotme(xdf)
