class Line():
    """
    - type ("c", "r", "d")
    - alive flag
    - win flag
    - token
    - index (0, 1, 2, 3, ...) Note the major diagonal is expected to be 0 and the minor 1
    """

    def __init__(self, type, index, tokens):
        self.type = type
        self.index = index
        self.tokens = tokens

    def update_status(self):
        if(len(set(self.values)) == 1 and self.values[0] != " "):
            self.win = True
            return

        elif (len(set(self.values)) == 1 and " " not in self.values):
            self.alive = False
            return

        self.win = False
        self.alive = True

    def update_tokens(self, tokens):
        self.tokens = tokens
        self.update_status()
        return self.win

    def __str__(self):
        return self.type + " " + str(self.index) + " { " + " , ".join(self.tokens) + " }"





class Board():
    """Represents an n by n tic-tac-toe board"""

    def __init__(self, n):
        self.n = n
        self.board = [ [" "] * n for i in range(n)]
        self.val = " "
        self.lines = []
        self.linify_board()

    def set_element(self, coord, val):
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

    def linify_board(self):
        for i in range(self.n):
            self.lines.append(Line("r", i, self.rectify_row(i)))
            self.lines.append(Line("c", i, self.rectify_col(i)))
            print("c" + self.rectify_col(i)[0])
        for d in range(2):
            self.lines.append(Line("d", i, self.rectify_dia(d)))

    def update_lines(self, type, index, line):
        for l in self.lines:
            if l.type == type and l.index == l.index:
                l.tokens = line
                return

    def dead_board(self):
        toRemove = []
        for l in self.lines:
            if l.alive:
                return False
            else:
                toRemove.append(l)

        for l in toRemove:
            self.lines.remove(l)
        return True

    def win_board(self):
        for l in self.lines:
            if l.win:
                return l.tokens[0]
        return " "

    def rectify_row(self, row):
        """
            Returns an array representing a certain 'row' in the board
            @param row, row number - Restrictions 0-'n'
        """
        return self.board[row]

    def rectify_col(self, col):
        """
            Returns an array representing a certain 'col' in the board
            @param col, column number - Restrictions 0-'n'
        """
        return [self.board[i][col] for i in range(self.n)]

    def rectify_dia(self, dia):
        """
            Returns an array representing 'dia' diagonal in the board
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


    @staticmethod
    def stringify_row(row):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        return " " + " | ".join(row) + "\n"

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
