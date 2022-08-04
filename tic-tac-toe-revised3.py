from abc import ABC, abstractmethod


class Token():
    """
    Needs to store
     - display values
     - unique idenfier
     - player tokens bool
    """

    #DO NOT USE. BAD PROGRAMMER, BAD!
    currentIdenifier = 0

    def __init__(self, token_str, is_player, id = -1):
        if id == -1:
            self.id = Token.currentIdenifier
            Token.currentIdenifier += 1
        else:
            self.id = id
        self.token_str = token_str
        self.is_player = is_player

    def match_token(self, token):
        """Check whether two tokens are equilivent and are not being used for whitespace"""
        return self.id == token.id and self.is_player

    def __str__(self):
        return self.token_str

    def __repr__(self):
        return str(self)


class Player():
    """
    Needs to store
        - token
        - idenfier (int)
        - name
        - next player indenfier
    Functionality
        - init with a tokens
        - past on input
        - give next players
    """

    def __init__(self, token, name, idenfier):
        self.token = token
        self.name = name
        self.idenfier = idenfier

    def update_next_player(self, next_player):
        """Creates a turn order for the players. Will be the next player in the sequence and should form a circular loop"""
        self.next_player = next_player

    def choose_move(self, board):
        """Using infomation from the board to generate a player movement. Uses algorithrim in subclasses 'decision_making' function"""
        print(board)
        coordinate = self.decision_making(board)
        return coordinate

    @abstractmethod
    def decision_making(self, board):
        pass

    @abstractmethod
    def win(self):
        pass



class HumanPlayer(Player):
    """
    TUI for player class
        -
    """
    def __init__(self, token, name, idenfier, dim):
        self.move_key = {j + dim * i : Coord(i, j) for j in range(dim) for i in range(dim)}
        super().__init__(token, name, idenfier)

    def decision_making(self, board):
        """User interface through a ASCII interuppter"""
        print()
        print(self.name + "'s turn. You are placing  '" + str(self.token) + "'")
        print("Please enter a valid move (Enter 'h' for valid moves): ")
        inp = input("")
        if inp == "h":
            print(HumanPlayer.help(board.dim))
            return self.decision_making(board)

        elif str.isdigit(inp) and (int(inp) in self.move_key.keys()):
            return self.move_key[int(inp)]

        else:
            print("Invalid response. Please try again")
            return self.decision_making(board)

    def win(self):
        """What to do when a player wins"""
        print(self.name + " wins! Everyone else sucks.")

    @staticmethod
    def help(dim):
        return Help(dim)



class Cell():
    """
    Needs to store
        - token
        - coorderinates
        - line update ids
    """

    def __init__(self, coord, token):
        self.coord = coord
        self.token = token
        self.lines = []

    def update_token(self, player):
        """Updates the token after ensuring the cell is not taken"""
        if self.token.is_player:
            return None
        self.token = player.token
        return True

    def reap_line(self, line_id):
        """Called when a line is dying. Remove line from the list"""
        tmp_lines = []
        for i in self.lines:
            if i != line_id:
                tmp_lines.append(i)
        self.lines = tmp_lines
        if len(self.lines) == 0 and not self.token.is_player:
            self.token = Token("D", False, -2)

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return str(self)



class Line():
    """
    Needs to Stores
        - cell idenfiers/coorinates
        - winning token
    """

    def __init__(self, cells, index, type):
        self.cells = cells
        self.index = index
        self.type = type
        for c in cells:
            c.lines.append(index)

    def update_cells(self, coord, player):
        """Updates the cell to the moved value then checks the status of the line"""
        for c in self.cells:
            if (c.coord.x == coord.x and c.coord.y == coord.y):
                c.update_token(player)
        self.update_line_status()

    def update_line_status(self):
        """Check for the dying, winning or continue state"""
        #TODO update based on cell not on line
        self.die = False
        self.win = False

        tmp_cell_tok_id = []
        tmp_is_all_player = True
        tm_player_tok_id = []
        for c in self.cells:
            tmp_cell_tok_id += [c.token.id]
            tmp_is_all_player &= c.token.is_player
            tm_player_tok_id = tm_player_tok_id + [c.token.id] if c.token.is_player else tm_player_tok_id
        if(len(set(tmp_cell_tok_id)) == 1 and tmp_is_all_player):
            self.win = True
            return
        elif(len(set(tm_player_tok_id)) > 1):
            self.die = True
            return

    def reap(self):
        """Terminates the line and removes references from the associated cells"""
        for c in self.cells:
            c.reap_line(self.index)

    def __str__(self):
        cells_str = []
        for c in self.cells:
            cells_str.append(str(c))
        return " " + " | ".join(cells_str) + "\n"

    def __repr__(self):
        return str(list)



class Board():
    """
    Stores the board and most major aspects of the game
    """

    def __init__(self, dim):
        self.whitespace = Token(" ", False, -1)
        self.dim = dim
        self.matrix = [[Cell(Coord(i, j), self.whitespace) for j in range(dim)] for i in range(dim)]
        self.lines = {r : self.lineify_row(r, 0) for r in range(self.dim)}
        self.lines.update({c + self.dim : self.lineify_col(c, self.dim) for c in range(self.dim)})
        self.lines.update({d + 2 * self.dim : self.lineify_dia(d, 2 * self.dim) for d in range(2)})

    def move(self, player):
        """Sets """
        coord = player.choose_move(self)
        if (coord.x >= self.dim or coord.x < 0) or (coord.y >= self.dim or coord.y < 0):
            return player.idenfier

        elif(self.matrix[coord.x][coord.y].token.is_player):
            return player.idenfier

        for i in self.matrix[coord.x][coord.y].lines:
            self.lines[i].update_cells(coord, player)
            if self.lines[i].die:
                self.lines.pop(i).reap()
            elif self.lines[i].win:
                print(self)
                player.win()
                return -1
        if len(self.lines) == 0:
            self.tie()
            print(self)
            return -2

        return player.next_player

    def lineify_row(self, row_num, offset):
        """Returns an array representing a certain 'row' in the board
            @param row, row number - Restrictions 0-'n'
        """
        return Line(self.matrix[row_num], row_num + offset, "r")

    def lineify_col(self, col_num, offset):
        """Returns an array representing a certain 'col' in the board
            @param col, column number - Restrictions 0-'n'
        """
        return Line([self.matrix[i][col_num] for i in range(self.dim)], col_num + offset, "c")

    def lineify_dia(self, dia_num, offset):
        """Returns an array representing 'dia' diagonal in the board
            @param dia, diagonal number - Restrictions 0-1

            Upper Left to Lower Right is 0
            Upper Right to Lower Left is 1
            Example
             0      1
                01
             1      0
        """
        if(dia_num not in [0, 1]):
            return
        return Line([self.matrix[dia_num*(self.dim - 2*i - 1) + i][i] for i in range(self.dim)], dia_num + offset, "d")

    def tie(self):
        """What to do if there is a tie"""
        print("There was a tie")

    def stringify_row(self, row):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        strRows = " "
        for c in self.matrix[row]:
            strRows += str(c.token)
            strRows += " | "
        return strRows[0: len(strRows)-2] + "\n"

    def __str__(self):
        strRows = [self.stringify_row(r) for r in range(self.dim)]
        horizBar = "---" * self.dim + "-" * (self.dim - 1) + "\n"
        return horizBar.join(strRows)

    def __repr__(self):
        return str(self)



class Help():
    def __init__(self, dim):
        self.dim = dim

    def __str__(self):
        s = ""
        for i in range(self.dim):
            s += " "
            for j in range(self.dim):
                s += str(j + self.dim * i)
                s += " | "
            s = s[0 : len(s)-2]
            s += "\n"
            s += "---" * self.dim + "-" * (self.dim - 1) + "\n"
        s = s[0 : len(s) - self.dim*4 - 2]
        return s

    def __repr__(self):
        return str(self)



class Game():
    """Main loop of to run the game """
    def __init__(self):
        self.get_game_info()
        self.run()

    def run(self):
        """"Main loop to run the game"""
        self.board = Board(self.dim)
        self.current_turn = 0
        while(True):
            next_player = self.board.move(self.players[self.current_turn])
            if(next_player < 0):
                break
            if(next_player == self.current_turn):
                print("Try Again")
                continue
            else:
                self.current_turn = next_player

    def get_game_info(self):
        while(True):
            print("Size of Board?")
            self.dim = input("")
            if str.isdigit(self.dim):
                self.dim = int(self.dim)
                break
            else:
                print("Put a number dumbass")

        while(True):
            print("Number of Player?")
            self.num_of_players = input("")
            if str.isdigit(self.num_of_players) and int(self.num_of_players) > 1:
                self.num_of_players = int(self.num_of_players)
                break
            else:
                print("Put a number dumbass. Or be a competitive person")
        self.players = []
        for i in range(self.num_of_players):

            print("Name of Player " + str(i+1) + ":")
            tmp_name = input("")
            while(True):
                print("Token Symbol:")
                tmp_token_str = input("")
                if len(tmp_token_str) == 1 and (tmp_token_str != " " or tmp_token_str != "D"):
                    break
                else:
                    print("Put a single character dumbass")
            tmp_token = Token(tmp_token_str, True, -1)
            tmp_player = HumanPlayer(tmp_token, tmp_name, i, self.dim)
            tmp_player.next_player = i + 1 if i < self.num_of_players - 1 else 0
            self.players.append(tmp_player)



class Coord():
    """ x and y coorderinates storing"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.x) + ", " + str(self.y)



while(True):
    g = Game()
    x = input("Play again? (y/n) ")
    if x == "n":
        break
