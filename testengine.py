"""compare model with stockfish or random choice



"""
import torch
import random
from state import State
import chess
from train import Net
import chess.engine


prams_path ='nets/value_geohot.pth'


class Old_model_Veluator():
    def __init__(self,prams_path):
        self.net = Net()
        self.net.load_state_dict(torch.load(prams_path,map_location = lambda x,loc:x))
        self.net.eval()
    def eval(self,board):
        outputs = {}
        for m in board.legal_moves:
            board.push(m)
            input =torch.unsqueeze( torch.from_numpy(State(board).serialize()).float(),0)
            outputs[m] =  self.net(input).data.numpy()[0][0]
            board.pop()
        return outputs 



    def play_one_step(self,board,verbose=False):
        qa = v.eval(board)
        # if verbose:
        #     print(qa.values())
        best_m = sorted(qa.items(),key = lambda x:x[1],reverse=board.turn)[0][0]
        san_m = board.san(best_m)
        board.push(best_m)
        if verbose:
            return board,san_m,qa.values()
        else:
            return board,san_m
            

def compare_model(time,stockfish=True):
    
    if stockfish:
        engine = chess.engine.SimpleEngine.popen_uci("/home/albb762/chessai/stockfish/Linux/stockfish_10_x64")

        engine.configure({'Skill Level':1})

    first = 0
    second = 0
    draw = 0
    for i in range(time):

        print(i)
        flag = 'stockfish'
        board = chess.Board()
        if  random.randint(0,1):
            board,_ = v.play_one_step(board)
            battle = 'model vs stockfish:'
            flag = 'model' 

        while True:
            if not board.is_game_over():
                if stockfish:
                    result = engine.play(board, chess.engine.Limit(time=0.00100,depth=1))
                    board.push(result.move)
                else:
                    board.push(random.choice(list(board.legal_moves)))
            else:
                break
            if not board.is_game_over():
                board,_ = v.play_one_step(board)
            else:
                break
        res = board.result()
        if flag == 'stockfish':
            if '1-0' ==res:
                first+=1
            if '0-1' == res:
                second+=1
            if '1/2-1/2' == res:
                draw += 1
        if flag == 'model':
            if '1-0' ==res:
                second+=1
            if '0-1' == res:
                first+=1
            if '1/2-1/2' == res:
                draw += 1
    if stockfish:
        print('stockfish vs model : ',first,second,draw)
    else:
        print('random vs model : ',first,second,draw)
        
    engine.quit()

v = Old_model_Veluator(prams_path)
# compare_model(10)

## collect the output of model for analysis
reslist =[]
for x in range(10):
    board = chess.Board()
    for i in range(444400):
        if not board.is_game_over():
            board,_,l = v.play_one_step(board,True)
            reslist.extend(l)
        else:
            # print(board.result())
            break
print(reslist)
