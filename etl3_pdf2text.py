import glob, fitz, os
from pprint import pprint

#!mkdir TEXTOS
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    if ix%50==25:
        print(ix,fn)
    tfn = fn.replace('PROGRAMAS','TEXTOS/TODOS').replace('.pdf','.txt')
    if os.path.exists(tfn):
        pass
    else:
        fo = fitz.open(fn)
        text = [page.getText() for page in fo]
        fo.close()
        fw = open(tfn, 'w')
        for page in text:
            pprint(page, fw)
        fw.close()
