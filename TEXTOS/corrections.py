import glob, time

t0=time.time()
for fn in glob.glob('TODOS/*.txt'):
    text=open(fn).read().replace('\\n','').replace('\n','').replace('\t','').replace("' '",'')
    fw = open(fn,'w')
    fw.write(text)
    fw.close()

print('DT:', round(time.time()-t0,2))
