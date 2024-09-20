from utt import UTTBoard

b = UTTBoard()
print(b)
b.outer.grid[0] = list("X X")
b.outer.grid[1] = list("OX ")
b.outer.grid[2] = list(" OX")
b.board[0][1].grid = [list("XXX"), list(" O "), list("XOX")]
b.last_move=16
print(b)