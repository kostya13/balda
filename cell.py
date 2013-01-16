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

