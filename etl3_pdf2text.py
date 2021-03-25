import glob, fitz
from pprint import pprint

#!mkdir TEXTOS
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    if ix%50==25:
        print(ix,fn)
    fo = fitz.open(fn)
    text = [page.getText() for page in fo]
    fo.close()
    tfn = fn.replace('PROGRAMAS','TEXTOS').replace('.pdf','.txt')
    fw = open(tfn, 'w')
    for page in text:
        pprint(page, fw)
    fw.close()
