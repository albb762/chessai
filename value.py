import time
from state import State
from train import Net
import torch
import chess
from flask import Flask,escape,request,Response,render_template
import chess.svg
import chess
import base64



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
    board.push(best_m)


def to_svgdata(s):
    return base64.b64encode(chess.svg.board(s.board).encode('utf-8')).decode('utf-8')

app = Flask(__name__)  
@app.route("/")
def hello():
    
    res = '<html><head>'
    res += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>'
    res +='<style>button {font-size : 20px;}</style>'
    res +='</head>'
    res +='<h1>chessai</h1>'
    res +='<img heigh=500px width = 500px src="data:image/svg+xml;base64,%s"></img></br>' % to_svgdata(s)
    res +='<button onclick=\'$.post("/move");\'>Make a computer Move</button>'
    # res +='<form method="POST" action="/human_move"><input name="human_move" type="text"></input><input type="submit" value="Move"></form><br/>'
    # res +='<form action="/human"; onsubmit="myButton.disabled = true; return true;"><input name="move" type="text"></input><input type="submit" name="myButton" value="Move"></form><br/>'
    res +='<form action="/human";><input name="move" type="text"></input></form><br/>'
    # res +='<form><input name="human_move" type="text"></input><input onclick=\'$.post("/human_move",function(data){location.reload();});\' type="submit" value="Move"></form><br/>'
    return res
# <input type="submit" value="Send Request">


@app.route("/selfplay")
def self_play():
    s = State()
    res = '<html><head>'
    while not s.board.is_game_over():
        play_one_step(s.board) 
        res +='<img heigh=500px width = 500px src="data:image/svg+xml;base64,%s"></img></br>' % to_svgdata(s)
    return res

@app.route("/human")
def move2():
    move = request.args.get('move',default='')
    print('human_action') 
    if not s.board.is_game_over(): 
        try:
            s.board.push_san(move)
            play_one_step(s.board)
        except ValueError:
            print(ValueError,s.board.legal_moves)
        return hello() 
    else:
        return "GAME OVER"
@app.route("/board.svg")
def return_board():
    return  Response(chess.svg.board(s.board),mimetype='image/svg+xml')
@app.route("/move", methods=["POST"])
def move():
    print(request)
    if not s.board.is_game_over(): 
        play_one_step(s.board)
    else:
        Print('game over')
    return hello() 
@app.route("/human_move",methods=["GET","POST"])
def human_move():
    move = request.form["human_move"]
    # print(list(s.board.legal_moves))
    # if move in s.board.legal_moves:
    #     print(move)
    try:
        s.board.push_san(move)
    except ValueError:
        print("illegal")
    return ""
if __name__ == '__main__':

    v = Veluator()
    s = State()
    # print(play_one_step(board))
    # results = self_play(board)    
    app.run(debug=True) 

