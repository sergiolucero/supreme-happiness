import glob, os
import fitz
from pprint import pprint

for fn in glob.glob('*/*.pdf'):
    if '(1)' not in fn: # skip doubles
        text = [page.getText() for page in fitz.open(fn)]
        print(fn, len(text))
        sfn = '_'.join(fn.split('_')[1:])
        fw = open(f"../../TEXTOS/INDIGENAS/{sfn.replace('pdf','txt')}", 'w')
        for t in text:
            pprint(t, fw)
        fw.close()
