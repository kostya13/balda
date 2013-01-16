# -*- coding: cp1251 -*-
# игровая логика
from cell import *
import re

dic={}
ignore=['ь','ы','ъ']
findwords=[]
findcheck={}
rawwords={}
maxsize=0


def Init():
    dic['.']={}
    LoadData("wordlist")
    LoadData("userdict")

def TestDic(letter,size):
    if size not in dic[letter]:
        dic[letter][size]=[]

def AppendWord(letter,size,word):
    if word not in dic[letter][size]:    
        dic[letter][size].append(word)

def ReloadUserDict():
    global rawwords
    LoadData("userdict")
    rawwords={}

def LoadData(filename):
    global words,maxsize
    for w in open(filename):
        word=w.strip()
        size=len(word)
        maxsize=max(maxsize,size)
        if size<2:
            continue
        first=word[0]
        if  first not in dic:
            dic[first]={}
        TestDic(first,size)
        AppendWord(first,size,word)
        #все слова для поиска слов начинающихся с пустой клетки
        TestDic('.',size)
        AppendWord('.',size,word)

def AddWord(letters):
    if len(letters)>2:
        word=''.join([c.letter for c in letters])
        if ('.' in word) and (word not in findcheck): #(word not in [f[0] for f in findwords]) and 
            findwords.append((word,letters))
            findcheck[word]=True

def SearchInDic():
    finded=[]
    # print("searched: ",len(findwords))
    for w in findwords:
        if w[0] not in rawwords:
            rawwords[w[0]]=True
            # print(w[0])
        if rawwords[w[0]]:
            size=len(w[0])
            pattern=re.compile(w[0])
            key=w[0][0]
            if (key in dic) and (size in dic[key]):
                for i in dic[key][size]:
                    if pattern.match(i):
                        # print("=",w[0],i)
                        index=w[0].index('.')
                        newletter=i[index]
                        finded.append((i,w[1],newletter,index))
            if not finded:
                rawwords[w[0]]=False

        # print(w[0],rawwords[w[0]])  
    # print(finded)
    return finded
        

def FindWords(cells):
    global findwords,findcheck
    findwords=[]
    findcheck={}
    for c in cells:
        # print( c.row,c.column)
        if c.letter in ignore:
            continue
        Search(c,[],[],False)
    return SearchInDic()


def Search(cell,letters,visited,hasempty):
    # print("->",letters,cell.letter,cell.row,cell.column)
    #если ячейка была посещена или
    #пустая, а пустая ячейка в слове уже была или
    #найдено слово длинее, чем самое длинное слово в словаре
    if cell in visited or (cell.letter=='.' and hasempty) or len(letters)>maxsize:
        return None
    letters.append(cell)
    visited.append(cell)
    if cell.letter=='.':
        hasempty=True
    for n in cell.nodes:
        # print("cell",cell.row,cell.column,"-> ",n.row,n.column)
        res=Search(n,list(letters),list(visited),hasempty)
        if not res:
            AddWord(letters)
    return True

