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
        pass

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
                self.matches[concepto][mencion] = [get_matches(mencion, texto, WIDTH) for texto in self.textos]
                # this already contains exclusion
            for word, matches in self.matches[concepto].items():
                self.nMatches[concepto] += len([maa for maa in matches if len(maa)])

        print('PROCESSED:', round(time.time()-t0,2))
        print(self.nMatches)

        # now number of PROGRAMS


        self.save()
