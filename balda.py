# -*- coding: cp1251 -*-
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox   import askquestion, showerror
import logic
from cell import *
root = Tk()


def CleanBoard():
    for i in range(5):
        for j in range(5):
            rows[i][j].delete(0,END)        

def NewGame():
    firstword="слово" #askstring("Начало игры","Введите слово")
    usedwords.append(firstword)
    if len(firstword)!=5:
        showerror("ошибка!","длина слова должна быть 5 символов")
        return
    CleanBoard()
    for i in range(5):
       rows[2][i].insert(END,firstword[i])
       rows[2][i].config(bg='yellow')
    findwords.config(state=NORMAL)

def FindWords():
    if words.size():
        words.delete(0,words.size())
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
        # print(c.letter)
    newwords=[]
    for w in logic.FindWords(cells):
        if w not in usedwords:
            words.insert('end',w)
            newwords.append(w)
    usedwords.extend(newwords)
    


board = Frame(root, bd=5, relief=RAISED)
rows = []
usedwords=[]

for i in range(5):
    cols = []
    for j in range(5):
        ent = Entry(board,width=2)
        ent.grid(row=i, column=j, sticky=NSEW)
        cols.append(ent)
    rows.append(cols)

newgame = Button(root, text='Новая игра',command=NewGame)
findwords = Button(root, text='Найти слова',command=FindWords,state=DISABLED)
words =  Listbox(root, height=30)
newgame.pack()
board.pack()
findwords.pack()
words.pack()
logic.Init()
mainloop()
