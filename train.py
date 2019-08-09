import numpy as np 
import os
import chess.pgn





file_pgns=os.listdir('data')
pgn = open(os.path.join('data',file_pgns[0]))
    
game=chess.pgn.read_game(pgn)
board = game.board()
k=0
for move in game.mainline_moves():
    board.push(move)
    if board.ep_square is not None:
       k+=1 
       print(k,board.board_fen())
       print(k,board.turn)
       print(k,board.castling_rights)
       print(k,board.ep_square)
