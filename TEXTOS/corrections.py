import glob

for fn in glob.glob('TODOS/*.txt'):
    text=open(fn).read().replace('\\n','').replace('\n','').replace('\t','')
    fw = open(fn,'w')
    fw.write(text)
    fw.close()
