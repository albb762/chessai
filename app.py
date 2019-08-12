from flask import Flask,Response
import chess
import chess.svg



app = Flask(__name__)
svg = chess.svg.board(chess.Board(),size=500) 



@app.route("/")
def hello():
    res = "<h1>hello<h1><img src='/board.svg'/>"
    return res
@app.route("/board.svg")
def return_board():
    return  Response(svg,mimetype='image/svg+xml')
if __name__ == "__main__":
    app.run(debug=True)



    
