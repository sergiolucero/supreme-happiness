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

data = dict(candis=list(candick.items()),nMenciones=list(candick.values()))

cdf = pd.DataFrame(data)
cdf['partido']=cdf.candis.apply(lambda c: c[0].split('[')[1][:-1]
                                if '[' in c[0] else c[0])
cdf['candidato']=cdf['candis'].apply(lambda c:c[0])
cdf['candidato']=cdf.candidato.apply(lambda c:c.split('<BR>')[0])
cdf=cdf[['candidato','partido','nMenciones']]
cdf = cdf.sort_values('nMenciones', ascending=False)

fw = open('static/candidatos.html', 'w')
fw.write('''<link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/df_style.css') }}>''')
fw.write('<H2>Candidatos ordenados por menciones del concepto AGUA</H2>')
cdf.to_html(fw, index=False, classes='mystyle')
fw.close()
