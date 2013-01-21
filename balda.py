# -*- coding: cp1251 -*-
# графический интерфейс для решателя "Балды"
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox   import askquestion, showerror,showinfo,showwarning
import logic
from time import clock

class Cell:
    def __init__(self,row,column,letter):
        self.row=row
        self.column=column
        if len(letter)<1:
            letter='.'
        self.letter=letter
        self.nodes=[]

    def MakeNodes(self,cells):
        if self.row>0:
            self.nodes.append(cells[self.row-1][self.column])
        if self.row<4:
            self.nodes.append(cells[self.row+1][self.column])
        if self.column>0:
            self.nodes.append(cells[self.row][self.column-1])            
        if self.column<4:
            self.nodes.append(cells[self.row][self.column+1])            

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

def AddToUsedList():
    index = words.curselection() 
    if index:
        label = words.get(index)  
        usedwords.append(label)
        usedlist.insert('end',label)

def AddToUsed():
    FindWords(True)

def NewWord():
    newword=askstring("Новое слово","Введите слово").strip()
    if len(newword)<3:
        showerror("ошибка!","длина слова должна быть не меньше 3 символов")
        return
    if logic.CheckWord(newword):
        return
    dictfile=open("userdict","a")
    dictfile.write(newword+"\n")
    dictfile.close()
    logic.ReloadUserDict()
    wordcount.config(text="слов: "+str(logic.GetWordCount()))

def DeleteWord():
    pass

def NewGame():
    global usedwords,listcell
    firstword=askstring("Начало игры","Введите слово") #"слово" #
    if len(firstword)!=5:
        showerror("ошибка!","длина слова должна быть 5 символов")
        return
    usedwords=[]
    listcell=[]
    CleanBoard()
    CleanBackground()
    CleanList(usedlist)
    CleanList(words)
    for i in range(5):
       rows[2][i].insert(END,firstword[i])
    findwords.config(state=NORMAL)
    # AddToUsedList(firstword)
    usedwords.append(firstword)
    

def FindWords(toignore=False):
    global listcell,newletterpos
    # start=clock()
    if toignore and newletterpos:
        newletterpos.delete(0,END)
        CleanBackground()
    newletterpos=None
    AddToUsedList()
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
    # print(clock()-start)
    
    
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
root.title("Балда игратор")
board = Frame(root)
for i in range(5):
    cols = []
    for j in range(5):
        ent = Entry(board,width=2,justify=CENTER)
        ent.grid(row=i, column=j, sticky=NSEW)
        cols.append(ent)
    rows.append(cols)

newword = Button(root, text='Добавить в словарь',command=NewWord)
newgame = Button(root, text='Новая игра',command=NewGame)
findwords = Button(root, text='Найти слова',command=FindWords,state=DISABLED)
words =  Listbox(root, height=7,selectmode=EXTENDED)
usedlist =  Listbox(root, height=21,selectmode=SINGLE)
wordcount = Label(text='0')
addtoused = Button(root, text='Игнорировать слово',command=AddToUsed)
delword = Button(root, text='Удалить из словаря',command=DeleteWord)
words.bind('<Button-1>', ListClicked) 
newword.pack()
wordcount.pack()
newgame.pack(pady=10)
board.pack()
findwords.pack(pady=3)
words.pack()
addtoused.pack()
usedlist.pack(pady=3)
delword.pack()

logic.Init()
wordcount.config(text="слов: "+str(logic.GetWordCount()))
mainloop()
