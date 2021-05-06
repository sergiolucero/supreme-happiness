from searcher import *

conn=sqlite3.connect('greenpeace.db')
kw=eval(open('keywords_final.txt').read())

non = {kwk: querier(kwk)[0] 
        for kwk,kwv in kw.items()}  # querier = (matches_dict,nMenciones)
# querier = {candi_info: quotes}

from collections import defaultdict

candick = defaultdict(int)
# WATER ONLY NOW!
non = {'agua': non['agua']}

for conc, cdata in non.items():
    print(conc, len(cdata))

    for candy, quotedata in cdata.items():
        candick[candy] +=len(quotedata)

def pc():
    data = dict(candis=list(candick.items()),nMenciones=list(candick.values()))

    cdf = pd.DataFrame(data)
    cdf['lista']=cdf.candis.apply(lambda c: c[0].split('[')[1][:-1]
                                if '[' in c[0] else c[0])
    cdf['candidato']=cdf['candis'].apply(lambda c:c[0])
    cdf['candidato']=cdf.candidato.apply(lambda c:c.split('<BR>')[0])  # aqui ya es DX_AIDA_JOSE_...
    cdf['distrito'] = cdf.candidato.apply(lambda c: c.split('_')[0])
    cdf['candidato'] = cdf.candidato.apply(lambda c: '_'.join(c.split('_')[1:]))

    cdf=cdf[['candidato','distrito','lista','nMenciones']]
    #xdf = sql('SELECT candidato, lista FROM candidatos')

    #cdf['lista'] = cdf.candidato.apply(lambda x: xdf[xdf.candidato==x.split('_')[1:]])
    #wen
    #cdf = cdf.merge(xdf)
    #wot
    #cdf=cdf[['candidato','lista','nMenciones']]

    cdf = cdf.sort_values('nMenciones', ascending=False)
    return cdf.to_html(classes='mystyle')

fw = open('static/candidatos.html', 'w')
fw.write('''<link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/df_style.css') }}>''')
fw.write('<H2>Candidatos ordenados por menciones del concepto AGUA</H2>')
cdf = pc()
fw.write(cdf)
fw.close()

