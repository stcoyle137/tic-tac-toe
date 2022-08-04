## TODO add oop with players and game states


class Board():
    """Represents an n by n tic-tac-toe board"""

    def __init__(self, n):
        self.n = n
        self.board = [ [" "] * n for i in range(n)]
        self.val = " "
        self.createWinningSpace()

    def setElement(self, coord, val):
        """Sets element in the board at a coorderinate 'coord' with a value of 'val'"""
        if(val not in ["x", "o"]):
            return 0
        if((coord.x >= self.n) or (coord.y >= self.n)):
            return 0
        if(self.board[coord.x][coord.y] != " "):
            return 0
        if(self.val == val):
            return 0
        self.val = val
        self.board[coord.x][coord.y] = val
        return b

    #Create list of possible winning spaces
    def createWinningSpace(self):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        self.winningSpace = {}
        for i in range(self.n):
            self.winningSpace["r" + str(i)] = self.rectifyRow(i)
            self.winningSpace["c" + str(i)] = self.rectifyCol(i)
        for d in range(2):
            self.winningSpace["d" + str(d)] = self.rectifyDia(d)
        self.processWinningSpace()


    def processWinningSpace(self):
        """Updates the winning space list and deletes winning space groups that no long can win. Return the winning group"""
        toDelete = []
        for key in self.winningSpace.keys():
            if Board.deadList(self.winningSpace[key]):
                toDelete = key
            if Board.winList(self.winningSpace[key]):
                return self.winningSpace[key]
        for key in toDelete:
            self.winningSpace.pop(key)

    def updateWinningSpace(self):
        for key in self.winningSpace.keys():
            if key


    def win(self):
        """Returns 2 if a player has won, 1 if there is a tie, 0 if the game can continue"""
        winKey = self.updateWinningSpace()
        if winKey is not None:
            return 2, winKey
        if not self.winningSpace:
            return 1
        return 0

    @staticmethod
    def deadList(list):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        s = ""
        for i in range(len(list)):
            s += list[i]
        return s.count("x") != 0 and s.count("o") != 0


    @staticmethod
    def winList(list):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        #Checks a list of strings to see
        s = ""
        for i in range(len(list)):
            s += list[i]
        return s.count("x") == len(list) or s.count("o") == len(list)

    @staticmethod
    def stringify_row(row):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        return " " + " | ".join(row) + "\n"


    def rectifyRow(self, row):
        """Returns an array representing a certain 'row' in the board
            @param row, row number - Restrictions 0-'n'
        """
        return self.board[row]

    def rectifyCol(self, col):
        """Returns an array representing a certain 'col' in the board
            @param col, column number - Restrictions 0-'n'
        """
        return [self.board[i][col] for i in range(self.n)]

    def rectifyDia(self, dia):
        """Returns an array representing 'dia' diagonal in the board
            @param dia, diagonal number - Restrictions 0-1

            Upper Left to Lower Right is 0
            Upper Right to Lower Left is 1
            Example
             0      1
                01
             1      0
        """
        if(dia not in [0, 1]):
            return
        return [self.board[dia*(self.n - 2*i - 1) + i][i] for i in range(self.n)]

    def __str__(self):
        strRows = [Board.stringify_row(row) for row in self.board]
        horizBar = "---" * self.n + "-" * (self.n - 1) + "\n"
        return horizBar.join(strRows)

    def __repr__(self):
        return str(self)

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
