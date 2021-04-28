from searcher import *

conn = sqlite3.connect('greenpeace.db')

kw=eval(open('keywords_final.txt').read())

non = [(kwk,querier(kwk)) for kwk,kwv in kw.items()]  # querier = matches_dict + nMenciones
ori = [(kwk,querier(kwk,tipo='ori')) for kwk,kwv in kw.items()]

df = pd.DataFrame(dict(concepto=[x[0] for x in non]))
df['nMenciones'] = [x[1][1] for x in non]
df['nProgramas'] = [len(x[1][0]) for x in non]
df.to_sql('menciones_todos', conn, index=False, if_exists='replace')

dfo = pd.DataFrame(dict(concepto=[x[0] for x in ori]))
dfo['nMenciones'] = [x[1][1] for x in ori]
dfo['nProgramas'] = [len(x[1][0]) for x in ori]
dfo.to_sql('menciones_ori', conn, index=False, if_exists='replace')
