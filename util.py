import sqlite3, pandas as pd
import pickle

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))
pload = lambda fn: pickle.load(open(fn,'rb'))

def psave(x, fn):
    pickle.dumps(x, open(fn, 'wb'))
