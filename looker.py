from searcher import *
import time

WIDTH = 50

class Looker:

    def __init__(self, txt_token):

        self.folder = txt_token
        self.files = glob.glob(self.folder)
        self.textos = [read_text(fn) for fn in self.files]
        self.nFiles = len(self.textos)
        self.keywords = keywords # {'agua': [], 'clima':[], 'MA':[]}
        print('LOOKER[%s]: %d files' %(self.folder, self.nFiles))

    def save(self):     # store in sql/HTML
        conceptos = list(self.keywords.keys())
        nMenciones = list(self.nMatches.values())
        nProgramas = list(self.nPrograms.values())
        PorcMencion = [100*x/self.nFiles for x in nProgramas]
        self.df = pd.DataFrame(dict(concepto=conceptos,
                                    nMenciones=nMenciones,
                                    PorcMencionan=PorcMencion))
        BASE= 'http://greenpeace-monitor.herokuapp.com'
        url = 'ver_menciones_ori' if 'INDIGENAS' in self.folder else 'ver_menciones'
        
        self.df['link'] = self.df.concepto.apply(lambda concepto: '%s/%s/%s/50' %(BASE,url,concepto))
        tabla = 'originarios' if 'INDIGENAS' in self.folder else 'todos'
        self.df.to_sql(f'menciones_{tabla}', sqlite3.connect('greenpeace.db'), 
                        index=False, if_exists='replace')
        print(f'SAVED to {tabla}')

    def process(self):      # using fixers, get_matches
        # will obtain nMatches and nPrograms
        # total number of Matches
        self.matches = {concepto: {} for concepto in self.keywords.keys()}
        self.nMatches = {concepto: 0 for concepto in self.keywords.keys()}
        t0 = time.time()
        for concepto, menciones in self.keywords.items(): 
            cmenciones = [concepto] + menciones
            print(concepto, len(menciones))
            for mencion in cmenciones:
                self.matches[concepto][mencion] = [get_matches(mencion, texto, WIDTH) 
                                                    for texto in self.textos]
                # this already contains exclusion
            for word, matches in self.matches[concepto].items():
                self.nMatches[concepto] += len([maa for maa in matches if len(maa)])

        print('PROCESSED:', round(time.time()-t0,2))
        print(self.nMatches)

        # now number of PROGRAMS
        self.nPrograms = {concepto: 0 for concepto in self.keywords.keys()}
        for concepto, menciones in self.keywords.items(): 
            cmenciones = [concepto] + menciones
            # revisemos todos los programas, uno por uno
            progs = 0
            for texto in self.textos:
                matches = [len(get_matches(mencion, texto, 50))
                           for mencion in cmenciones]
                total = sum(matches)
                if total>0:
                    progs+=1
            #print(concepto, progs, self.nFiles)
            self.nPrograms[concepto] = progs
        self.save()
