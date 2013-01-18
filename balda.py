# -*- coding: cp1251 -*-
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox   import askquestion, showerror,showinfo,showwarning
import logic
from cell import *


def CleanBoard():
    for i in range(5):
        for j in range(5):
            rows[i][j].delete(0,END)        

def CleanBackground():
    for i in range(5):
        for j in range(5):
            rows[i][j].config(bg='white')     

def CleanList(l):
    if l.size():
        l.delete(0,l.size())

def AddToUsedList(word):
    usedwords.append(word)
    usedlist.insert('end',word)

def AddToUsed():
    used=askstring("Использованное слово","Введите слово")
    AddToUsedList(used)

def CheckWord():
    title="Результат проверки"
    checkword=askstring("Проверить слово","Введите слово")
    if logic.CheckWord(checkword):
        showinfo(title,"слово найдено")
    else:
        showwarning(title,"слово не найдено")
    


def NewWord():
    newword=askstring("Новое слово","Введите слово")
    if len(newword)<3:
        showerror("ошибка!","длина слова должна быть меньше 3 символов")
        return
    if logic.CheckWord(newword):
        return
    dictfile=open("userdict","a")
    dictfile.write(newword+"\n")
    dictfile.close()
    logic.ReloadUserDict()

def NewGame():
    global usedwords,listcell
    usedwords=[]
    listcell=[]
    firstword=askstring("Начало игры","Введите слово") #"слово" #
    if len(firstword)!=5:
        showerror("ошибка!","длина слова должна быть 5 символов")
        return
    CleanBoard()
    CleanBackground()
    CleanList(usedlist)
    CleanList(words)
    for i in range(5):
       rows[2][i].insert(END,firstword[i])
    findwords.config(state=NORMAL)
    AddToUsedList(firstword)

def FindWords():
    global listcell,newletterpos
    newletterpos=None
    index = words.curselection() 
    if index:
        label = words.get(index)  
        AddToUsedList(label)
    CleanList(words)
    cellrow=[]
    cells=[]
    for i in range(5):
        cellcols = []
        for j in range(5):
            c=Cell(i,j,rows[i][j].get())
            cellcols.append(c)
            cells.append(c)
        cellrow.append(cellcols)
    for c in cells:
        c.MakeNodes(cellrow)
    listcell=[]
    findedwords=sorted(logic.FindWords(cells),key=lambda item: len(item[0]),reverse=True)
    for w in findedwords:     
        if w[0] not in usedwords:
            words.insert('end',w[0])
            listcell.append((w[1],w[2],w[3]))
    
    
def ListClicked(event):
    global newletterpos
    if newletterpos:
        newletterpos.delete(0,END)
    index = words.curselection() 
    if index:
        CleanBackground()
        item=listcell[int(index[0])]
        for i in item[0]:
            rows[i.row][i.column].config(bg='yellow')
        newletterpos=rows[item[0][item[2]].row][item[0][item[2]].column]
        newletterpos.delete(0,END)
        newletterpos.insert(END,item[1])
        newletterpos.config(bg='cyan')


rows = []
usedwords=[]
listcell=[]
newletterpos=None

root = Tk()
board = Frame(root)
for i in range(5):
    cols = []
    for j in range(5):
        ent = Entry(board,width=2,justify=CENTER)
        ent.grid(row=i, column=j, sticky=NSEW)
        cols.append(ent)
    rows.append(cols)

newword = Button(root, text='Добавить в словарь',command=NewWord)
checkword = Button(root, text='Проверить в словаре',command=CheckWord)
newgame = Button(root, text='Новая игра',command=NewGame)
findwords = Button(root, text='Найти слова',command=FindWords,state=DISABLED)
words =  Listbox(root, height=10,selectmode=SINGLE)
usedlist =  Listbox(root, height=20,selectmode=SINGLE)
addtoused = Button(root, text='Добавить в использованные',command=AddToUsed)
words.bind('<Double-1>', ListClicked) 
newword.pack(pady=5)
checkword.pack(pady=5)
newgame.pack(pady=10)
board.pack()
findwords.pack(pady=3)
words.pack()
usedlist.pack(pady=3)
addtoused.pack()

logic.Init()
mainloop()
