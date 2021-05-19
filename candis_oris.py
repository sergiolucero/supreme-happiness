from util import *
files=glob.glob('TEXTOS/INDIGENAS/*.txt')
import glob
files=glob.glob('TEXTOS/INDIGENAS/*.txt')
textos=[open(fn).read().replace(chr(10), ' ') for fn in files]
df=pd.DataFrame(dict(archivo=files, texto=textos))
df.iloc[0]
df['candidato']=df.archivo.apply(lambda a: a.split('/')[-1].split('.')[0])
df.head()
df.to_sql('candidatos_originarios', sqlite3.connect('greenpeace.db'), index=False)
%hist -f candis_oris.py
