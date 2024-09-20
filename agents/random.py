from random import choice

def move(board, player):
    return choice(board.moves())