# -*- coding: cp1251 -*-
tree={}

def MakeTree(w,t):
    if not w:
        return
    # print(w)
    if w[0] not in t:
        t[w[0]]={}
    MakeTree(w[1:],t[w[0]])

def PrintTree(t):
    if not t:
        return
    for k in t:
        print(k)
        PrintTree(t[k])

def Find(w,t):
    # print(w,t)
    if w[0]=='.':
        res=False
        for v in t:
            res=res or Find(v+w[1:],t)
            if res:
                break
        return res
    if w[0] not  in t:
        return False
    if len(w)==1:
          return True
    return Find(w[1:],t[w[0]])

for w in open("userdict"):
    word=w.strip()
    if word:
        MakeTree(word,tree)
# print(tree)
print(Find("абсолютн.",tree))
