# -*- coding: cp1251 -*-
# ������� ������
# from cell import *
import re

dic={}
findwords=set()
tree={}
wordcount=0

def Init():
    LoadData("wordlist")
    LoadData("userdict")

def ReloadUserDict():
    LoadData("userdict")

def TestDic(letter,size):
    if  letter not in dic:
       dic[letter]={}
    if size not in dic[letter]:
        dic[letter][size]=[]

def AppendWord(letter,size,word):
    global wordcount
    if word not in dic[letter][size]:    
        dic[letter][size].append(word)
        if letter != '.':
            wordcount+=1

def GetWordCount():
    return wordcount

def MakeTree(w,t):
    if not w:
        return
    # print(w)
    if w[0] not in t:
        t[w[0]]={}
    MakeTree(w[1:],t[w[0]])

def LoadData(filename):
    global words
    for w in open(filename,"r",1,'utf8'):
        word=w.strip()
        size=len(word)
        if size<2:
            continue
        first=word[0]
        TestDic(first,size)
        AppendWord(first,size,word)

        #��� ����� ��� ������ ���� ������������ � ������ ������
        TestDic('.',size)
        AppendWord('.',size,word)
        MakeTree(word,tree)

def CheckWord(word):
    if word[0] in dic:
        return word in dic[word[0]][len(word)]
    else:
        return False

def SearchInDic():
    finded=[]
    # c=0
    # print("searched: ",len(findwords))
    for w in findwords:
        # c+=1
        size=len(w[0])
        pattern=re.compile(w[0])
        key=w[0][0]
        wordfound=False
        if (key in dic) and (size in dic[key]):
            for i in dic[key][size]:
                # print("=",w[0],i)
                if pattern.match(i):
                    index=w[0].index('.')
                    newletter=i[index]
                    finded.append((i,w[1],newletter,index))
                    wordfound=True
    # print(finded)
    # print("c=",c)
    return finded
        
def FindWords(cells):
    global findwords
    findwords=set()
    for c in cells:
        # print( c.row,c.column)
        Search(c,[],False,'')
    return SearchInDic()

def FindTree(w,t):
    if not w:
        return True
    # print(w,t)
    if w[0]=='.':
        for v in t:
            if FindTree(v+w[1:],t):
                return True
        return False
    if w[0] not  in t:
        return False
    if len(w)==1:
          return True
    return FindTree(w[1:],t[w[0]])

def Search(cell,letters,hasempty,word):
    # print("->",letters,cell.letter,cell.row,cell.column)
    emptycell = cell.letter=='.'
    if  not FindTree(word,tree) or cell in letters or (emptycell and hasempty)  :
        return None
    letters.append(cell)
    if emptycell:
        hasempty=True
    for n in cell.nodes:
        word=''.join([c.letter for c in letters])
        # print("cell",cell.row,cell.column,"-> ",n.row,n.column)
        res=Search(n,list(letters),hasempty,word)
        if not res and hasempty:
            if len(letters)>2:
                findwords.add((word,tuple(letters)))
    return True

