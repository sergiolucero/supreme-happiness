from searcher import *

conn = sqlite3.connect('greenpeace.db')

kw=eval(open('keywords_final.txt').read())

non = [(kwk,querier(kwk)) for kwk,kwv in kw.items()]  # querier = matches_dict + nMenciones
ori = [(kwk,querier(kwk,tipo='ori')) for kwk,kwv in kw.items()]

df = pd.DataFrame(dict(concepto=[x[0] for x in non]))
df['nMenciones'] = [x[1][1] for x in non]
df['nProgramas'] = [len(x[1][0]) for x in non]
n1 = len(glob.glob('TEXTOS/TODOS/D*.txt'))
print('N1:',n1)
df['Porc.Programas'] = round(100*df['nProgramas']/n1,2)
print(df)
df.to_sql('menciones_todos', conn, index=False, if_exists='replace')

dfo = pd.DataFrame(dict(concepto=[x[0] for x in ori]))
dfo['nMenciones'] = [x[1][1] for x in ori]
dfo['nProgramas'] = [len(x[1][0]) for x in ori]
n2 = len(glob.glob('TEXTOS/INDIGENAS/*.txt'))
print('N2:', n2)
dfo['Porc.Programas'] = round(100*dfo['nProgramas']/n2,2)
print(dfo)
dfo.to_sql('menciones_ori', conn, index=False, if_exists='replace')
