from flask import Flask,Response,request
from state import State
import time
import chess
import chess.svg
from train import Net
import torch
import json 


class Veluator():
    def __init__(self):
        self.net = Net()
        self.net.load_state_dict(torch.load('nets/values.pth',map_location = lambda x,loc:x))
        self.net.eval()
    def eval(self,board):
        outputs = {}
        for m in board.legal_moves:
            board.push(m)
            input =torch.unsqueeze( torch.from_numpy(State(board).serialize()).float(),0)
            outputs[m] =  self.net(input).data.numpy()[0][0]
            board.pop()
        return outputs 



def play_one_step(board):
    qa = v.eval(board)
    best_m = sorted(qa.items(),key = lambda x:x[1],reverse=board.turn)[0][0]
    san_m = board.san(best_m)
    board.push(best_m)
    return board,san_m

app = Flask(__name__)
v = Veluator()



@app.route("/")
def hello():
    with open('index.html','r') as f : 
        res = f.read()
        res = res.replace('vchange=','vchange=%d'% time.time())
    return res 
@app.route("/human_play",methods=['POST'])
def return_board():
    fen = request.form['fen']
    board = chess.Board(fen)
    b,m = play_one_step(board)
    return m

@app.route("/selfplay",methods=['GET'])
def self_play():
    s = State()
    res = []
    while not s.board.is_game_over():
        b,m = play_one_step(s.board) 
        res.append(m) 
    return json.dumps(res)


if __name__ == "__main__":
    app.run(debug=True)



    
