from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import random
import numpy as np
from scipy.signal import convolve2d
from pprint import pprint


horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

class Conecta4(TwoPlayerGame):
    def __init__(self, players=None) -> None:
        super().__init__()
        self.players = players
        self.current_player = 1
        #self.current_player = random.choice([1,2])
        self.board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self.boardAux = [0,0,0,0,0,0]
        self.p1Board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self.p2Board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

    def possible_moves(self): 
        returnValue = []
        for i in range:
            if self.boardAux[i] < 7:
                returnValue.append(str(self.boardAux[i]))
        return returnValue
    def make_move(self,move): 
        self.board[int(move)][6-self.boardAux[int(move)]] = self.current_player
        if self.current_player == 1:    
            self.p1Board[int(move)][6-self.boardAux[int(move)]] = 1
        else:
            self.p2Board[int(move)][6-self.boardAux[int(move)]] = 1
        self.boardAux[int(move)] += 1
    def win(self): 
        for kernel in detection_kernels:
            if self.current_player == 1 :
                if (convolve2d(self.p1Board, kernel, mode="valid") == 4).any():
                    return True
            else:
                if (convolve2d(self.p2Board, kernel, mode="valid") == 4).any():
                    return True
        return False

    def is_over(self): 
        if 7 in self.boardAux:
            return True
        return self.win() # Game stops when someone wins.
    def show(self): 
        pprint (self.board)
    def scoring(self): 
        if game.win():
            return 100
        elif game.is_over():
            return 50
        else:
            return 0
        

ai = Negamax(100) # The AI will think 13 moves in advance
game = Conecta4( [ Human_Player(), AI_Player(ai) ] )
history = game.play()