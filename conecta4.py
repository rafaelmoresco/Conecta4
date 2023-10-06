from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax, TranspositionTable, solve_with_iterative_deepening
import random
import numpy as np
from scipy.signal import convolve2d
from pprint import pprint


horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

def conecta(board):
    for kernel in detection_kernels:
        if (convolve2d(board, kernel, mode="valid") == 4).any():
            return True
    return False

class Conecta4(TwoPlayerGame):
    def __init__(self, players=None) -> None:
        super().__init__()
        self.players = players
        #self.current_player = 1
        self.current_player = random.choice([1,2])
        self.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.boardAux = [0,0,0,0,0,0,0]
        self.pBoard = [[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]]

    def possible_moves(self): 
        returnValue = []
        for i in range(7):
            if self.boardAux[i] < 6:
                returnValue.append(str(i))
        return returnValue
    def make_move(self,move): 
        self.board[int(move)][5-self.boardAux[int(move)]] = self.current_player
        if self.current_player == 1:    
            self.pBoard[0][int(move)][5-self.boardAux[int(move)]] = 1
        else:
            self.pBoard[1][int(move)][5-self.boardAux[int(move)]] = 1
        self.boardAux[int(move)] += 1
    #def win(self): 
        #for kernel in detection_kernels:
        #    if (convolve2d(self.p2Board, kernel, mode="valid") == 4).any():
        #        return True
        #return False
    def lose(self):
        #for kernel in detection_kernels:
        #    if (convolve2d(self.p1Board, kernel, mode="valid") == 4).any():
        #        return True
        #return False
        return conecta(self.pBoard[self.opponent_index-1])
    def is_over(self): 
        if self.possible_moves() == []:
            return True
        return self.lose()# Game stops when someone wins.
    def show(self): 
        print (np.transpose(np.asmatrix(self.board)))
    def scoring(self): 
        #if game.win():
        #    return 100
        if game.lose():
            return -100
        else:
            return 0
        
ai = Negamax(5) # The AI will think 13 moves in advance
ai2 = Negamax(5)
#game = Conecta4( [ Human_Player(), AI_Player(ai) ] )
game = Conecta4( [ AI_Player(ai2), AI_Player(ai) ] )
history = game.play()