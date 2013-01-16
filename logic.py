# -*- coding: cp1251 -*-
# игровая логика
from cell import *
import re

dic={}
ignore=['ь','ы','ъ']
findwords=[]
maxsize=0

def Init():
    LoadData()
    # print(dic)

def TestDic(letter,size):
    if size not in dic[letter]:
        dic[letter][size]=[]

def AppendWord(letter,size,word):
    if word not in dic[letter][size]:    
        dic[letter][size].append(word)

def LoadData():
    global words,maxsize
    dic['.']={}
    for w in open("wordlist"):
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
        if (word not in [f[0] for f in findwords]) and ('.' in word):
            findwords.append((word,letters))

def SearchInDic():
    finded=[]
    for w in findwords:
        size=len(w[0])
        pattern=re.compile(w[0])
        key=w[0][0]
        if (key in dic) and (size in dic[key]):
            for i in dic[key][size]:
                if pattern.match(i):
                    # print("=",w,i)
                    finded.append(i)
    return finded
        

def FindWords(cells):
    global findwords
    findwords=[]
    for c in cells:
        if c.letter in ignore:
            continue
        Search(c,[],[],False)
    return sorted(SearchInDic(),key=len,reverse=True)


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

