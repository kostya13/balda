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

def CleanBackground():
    for i in range(5):
        for j in range(5):
            rows[i][j].config(bg='white')     

def NewGame():
    firstword="�����" #askstring("������ ����","������� �����")
    usedwords.append(firstword)
    if len(firstword)!=5:
        showerror("������!","����� ����� ������ ���� 5 ��������")
        return
    CleanBoard()
    for i in range(5):
       rows[2][i].insert(END,firstword[i])
    findwords.config(state=NORMAL)

def FindWords():
    global listcell
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
    listcell=[]
    for w in logic.FindWords(cells):
        if w[0] not in usedwords:
            words.insert('end',w[0])
            newwords.append(w[0])
            listcell.append((w[1],w[2],w[3]))
    usedwords.extend(newwords)
    

def ListClicked(event):
    index = words.curselection() 
    if index:
        CleanBackground()
        label = words.get(index)  
        item=listcell[int(index[0])]
        for i in item[0]:
            rows[i.row][i.column].config(bg='yellow')
        newletterpos=rows[item[0][item[2]].row][item[0][item[2]].column]
        newletterpos.delete(0,END)
        newletterpos.insert(END,item[1])
        newletterpos.config(bg='cyan')


board = Frame(root, bd=5, relief=RAISED)
rows = []
usedwords=[]
listcell=[]

for i in range(5):
    cols = []
    for j in range(5):
        ent = Entry(board,width=2)
        ent.grid(row=i, column=j, sticky=NSEW)
        cols.append(ent)
    rows.append(cols)

newgame = Button(root, text='����� ����',command=NewGame)
findwords = Button(root, text='����� �����',command=FindWords,state=DISABLED)
words =  Listbox(root, height=20,selectmode=SINGLE)
words.bind('<Double-1>', ListClicked) 
newgame.pack(pady=10)
board.pack()
findwords.pack(pady=3)
words.pack()
logic.Init()
mainloop()