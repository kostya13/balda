words=[]
for l in open("source"):
    w=l.split()
    words.extend([i.replace("\"","").replace(".","").replace(",","").lower() for i in w if len(i)>2])
words.sort()
wset=set(words)
for w in sorted(wset):
    print(w)

