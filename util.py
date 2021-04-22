import sqlite3, pandas as pd

sql = lambda q: pd.read_sql(q, sqlite3.connect('greenpeace.db'))