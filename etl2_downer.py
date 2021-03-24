import glob, fitz
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    fo = fitz.open(fn)
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    fo = fitz.open(fn)
    fo.close()
npages={}
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    fo = fitz.open(fn)
    npages[fn] = fo.page_count()
    fo.close()
for ix, fn in enumerate(list(glob.glob('PROGRAMAS/*.pdf'))):
    fo = fitz.open(fn)
    npages[fn] = fo.page_count
    
    fo.close()
len(npages)
sum(npages.values())
len(npages)
len(npages)
sum(npages.values())
%hist -f etl2_downer.py
