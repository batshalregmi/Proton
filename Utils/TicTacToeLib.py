class Board:

    def __init__(self):
        self.board = [[":one:", ":two:", ":three:"], [":four:", ":five:", ":six:"], [":seven:", ":eight:", ":nine:"]]

    
    def printStr(self):
        basestr = "**The Board:**\n\n"
        for i in self.board:
            for j in i:
                basestr += j
            basestr += "\n"
        return basestr
    
    def checkWin(self, player):
        #Right Diagonal Check
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True
        #Left Diagonal Check
        elif self.board[0][0] ==  player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        #Vertical Check
        for i in range(3):
            if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                return True
        #Horizontal Check
        for i in range(3):
            if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                return True
        #Executed if no check passes
        return False
    def checkMove(self, cell):
        row, index = self.cellConvert(cell)
        value = self.board[row][index]
        if value == ":o:":
            return False
        elif value == ":x:":
            return False
        else:
            return True

    def cellConvert(self, cell):
        if cell <= 3:
            con = (0, cell-1)
            return con
        elif cell > 3 and cell <=6:
            con = (1, cell-4)
            return con
        elif cell > 6 and cell <=9:
            con = (2, cell-7)
            return con
        return

    def playMove(self, cell, player):
        row, index = self.cellConvert(cell)
        self.board[row][index] = player

    def isFull(self):    
        count = 0
        for i in self.board:
            for j in i:
                if j == ":o:" or j == ":x:":
                    count += 1
                else:
                    pass
        if count < 9:
            return False
        return True