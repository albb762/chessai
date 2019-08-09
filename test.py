import chess.pgn
from state import State
import os
import numpy as np
def get_date(files_list,sample_size=None):
    fn =0
    X,Y = [],[]
    for f in files_list:
            
        pgn = open(os.path.join('data',f))
        
        while 1 : 
            fn +=1
            try:
                game=chess.pgn.read_game(pgn)
            except Exception:
                break
            print('parsing game %d,got example %d'%(fn,len(X)))
            board = game.board()
            value = {'1/2-1/2':0,'1-0':1,'0-1':-1}[game.headers['Result']]
            for move in game.mainline_moves():
                board.push(move)
                Y.append(value)
                X.append(State(board).serialize()) 
            if sample_size is not None and len(X)>sample_size:
                return np.array(X),np.array(Y) 
    return np.array(X),np.array(Y) 

def main():
    file_pgns=os.listdir('data')
    train_x,train_y = get_date(file_pgns,1e5)
    np.savez('train_data_10k.npy',train_x,train_y)
    print('saved')


main()
