import chess

class State(object):
    def __init__(self):
        self.board = chess.Board()

    def edge(self):
        return self.board.legal_moves
def main():
    s = State()
    print(s.edge())
main()

