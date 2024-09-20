"""
Module to manage and print ultimate tic-tac-toe boards.
"""

bigX = [ "   X    X  ",
         "    X  X   ",
         "     XX    ",
         "    X  X   ", 
         "   X    X  " ] 

bigO = [ "  OOOOOO   ",
         " O      O  ",
         " O      O  ",
         " O      O  ",
         "  OOOOOO   " ]

def gridxy(num):
    """
    Convert a grid number into an x y coordinate
     1 | 2 | 3
    ---+---+---
     4 | 5 | 6
    ---+---+---
     7 | 8 | 9
    Returns x,y
    """
    x=(num-1)%3
    y=(num-1)//3
    return x,y

def mnum(x,y):
    """
    Convert x y into a move number. Returns the move number
    """
    return y*3+1+x

class XOGrid:
    """
    A standard tic-tac-toe grid
    """

    def __init__(self):
        self.grid = [[' ' for j in range(3)] for i in range(3)]


    def winner(self):
        """
        Returns the winner of a grid. This is one of:
        X
        O
        S - Scratch / Tie
        N - None
        """

        def has_win(l):
            """
            Check to see if the specified list l is a winner
            (filled with the same non-space)
            """
            return l[0] != ' ' and len(set(l)) == 1 
            #check each row

        for row in self.grid:
            if has_win(row):
                return row[0]
        
        #check each column
        for x in range(len(self.grid[0])):
            col = [self.grid[i][x] for i in range(len(self.grid))]
            if has_win(col):
                return col[0]
        
        #check the diagonals
        diag = [[self.grid[i][i] for i in range(len(self.grid))], 
                [self.grid[i][len(self.grid)-i-1] for i in range(len(self.grid))]]
        for d in diag:
            if has_win(d):
                return d[0]
        
        #check for open game
        for row in self.grid:
            for c in row:
                if c == ' ':
                    return 'N'
        
        # must be a scratch
        return 'S'
    
    def moves(self):
        """
        Return a list of legal moves.
        """
        result = []

        # try out each quadrant
        for i in range(1,10):
            x,y = gridxy(i)
            if self.grid[y][x] == ' ':
                result.append(i)
        
        return result
    
    def move(self, m, player):
        """
        Attempt to take move m for player.
        Return true on success, false on failure.
        """
        if player not in ['X', 'O'] or m not in self.moves():
            return False
        
        # Make the move
        x,y=gridxy(m)
        self.grid[y][x] = player
        return True


class UTTBoard:
    def __init__(self):
        """
        Initialize an empty board.
        """
        self.board = [[XOGrid() for j in range(3)] for i in range(3)]
        self.outer = XOGrid()
        self.last_move = None
    
    def __str__(self):
        out = []

        for by in range(len(self.outer.grid)):
            for srow in range(5):
                rstr = ""
                for bx in range(len(self.outer.grid[0])):
                    if self.outer.grid[by][bx] == 'X':
                        rstr += bigX[srow]
                    elif self.outer.grid[by][bx] == 'O':
                        rstr += bigO[srow]
                    else:
                        if srow % 2 == 0:
                            gy = srow // 2
                            for gx in range(len(self.board[by][bx].grid[gy])):
                                c = self.board[by][bx].grid[gy][gx]
                                if c == ' ':
                                    m = mnum(bx,by)*10 + mnum(gx,gy)
                                    if m in self.moves():
                                        c = m
                                else:
                                    c += ' '
                                rstr += "{:>3}".format(c)
                                if gx != len(self.board[by][bx].grid[gy])-1:
                                    rstr += "|"
                        else:
                            rstr += "---+---+---"
                    if bx != len(self.outer.grid[0])-1:
                        rstr += " # "
                out.append(rstr)
            if by != len(self.outer.grid) - 1:
                out.append("#"*39)
        return "\n".join(out)

    def moves(self):
        # Which boards can I move on?
        if self.last_move is None:
            boards = list(range(1,10))
        else:
            boards = [self.last_move%10]
            x,y=gridxy(boards[0])
            if self.outer.grid[y][x] != ' ':
                boards = list(range(1,10))
        
        # build the results
        result = []
        for board in boards:
            x,y = gridxy(board)
            for m in self.board[y][x].moves():
                result.append(board*10 + m)
        
        return result
    
    def move(self, m, player):
        """
        Attempt to make the move. Returns true on success, false on failure.
        """
        # validate the move
        if m not in self.moves():
            return False

        # get coordinates for the board and square
        board = m//10
        square = m%10
        bx,by = gridxy(board)

        # make the move
        result = self.board[by][bx].move(square, player)
        if result:
            self.last_move = m

        # update the outer move
        w = self.board[by][bx].winner()
        if w in ['X', 'O'] :
            self.outer.move(board, w)
        
        return result
    
    def winner(self):
        """
        Return the winner of the over all game.
        X, O, S, N
        """
        return self.outer.winner()

def get_agent(agents, player):
    done = False
    while not done:
        print("Who will play {}?".format(player))
        for i in range(len(agents)):
            aname = agents[i]
            print("{}.) {}".format(i+1, aname))
        i = int(input("Choice: ")) - 1
        if i < 0 or i >= len(agents):
            print("Invaid choice. Please try again.")
        else:
            return __import__("agents."+agents[i], None, None, ['move']).move


def main(argv):
    """
    Let's play some ultimate Tic-Tac-Toe!
    """
    from glob import glob

    # get the agent list
    agents = []
    for agent in glob("agents/*.py"):
        aname = agent.split("/")[-1].split(".")[0]
        agents.append(aname)
    
    # load the players
    xplayer = get_agent(agents, 'X')
    oplayer = get_agent(agents, 'O')

    # play the game
    board = UTTBoard()
    to_play = 'X'
    while board.winner() not in ('X', 'O', 'S'):
        print(board)
        if to_play == 'X':
            if board.move(xplayer(board, to_play), to_play):
                to_play = 'O'
        else:
            if board.move(oplayer(board, to_play), to_play):
                to_play = 'X'
    print(board)
    w = board.winner()
    if w == 'S':
        print('Scratch Game')
    else:
        print('{} wins!'.format(w))
    

if __name__ == "__main__":
    import sys
    main(sys.argv)