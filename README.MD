# Ultimate Tic-Tac-Toe
This program implements the game [Ultimate Tic-Tac-Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe). The idea is for you to write an agent to play the game. The game comes with an example human agent which allows human beings to play the game.

Write your agent in a python file in the agents directory. Your agent must contain a function "move(board, player)" which returns an integer indicating the move position for the player. The move will be a two digit number indicating the board and square using the following pattern:

```
 1 | 2 | 3 
---+---+---
 4 | 5 | 6 
---+---+---
 7 | 8 | 9
```

For example, the integer "15" means "Play center square of the upper left-hand board." Running the script "utt.py" will play the game. If you play a human vs human game it will help you see how the numbering works.

Your agent should implement some sort of minimax search variant.

Enjoy!