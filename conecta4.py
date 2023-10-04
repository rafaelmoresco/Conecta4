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
"""
class GameOfBones( TwoPlayerGame ):
     In turn, the players remove one, two or three bones from a
    pile of bones. The player who removes the last bone loses. 

    def __init__(self, players=None):
        self.players = players
        self.pile = 20 # start with 20 bones in the pile
        self.current_player = 1 # player 1 starts

    def possible_moves(self): return ['1','2','3']
    def make_move(self,move): self.pile -= int(move) # remove bones.
    def win(self): return self.pile<=0 # opponent took the last bone ?
    def is_over(self): return self.win() # Game stops when someone wins.
    def show(self): print ("%d bones left in the pile" % self.pile)
    def scoring(self): return 100 if game.win() else 0 # For the AI
"""
# Start a match (and store the history of moves when it ends)


class Conecta4(TwoPlayerGame):
    def __init__(self, players=None) -> None:
        super().__init__()
        self.players = players
        self.current_player = random.choice([1,2])
        self.board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self.boardAux = [0,0,0,0,0,0]
        self.p1Board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self.p2Board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

    def possible_moves(self): 
        return['0','1','2','3','4','5']
    def make_move(self,move): 
        self.board[int(move)][self.boardAux[int(move)]] = self.current_player
        if self.current_player == 1:    
            self.p1Board[int(move)][self.boardAux[int(move)]] = 1
        else:
            self.p2Board[int(move)][self.boardAux[int(move)]] = 1
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
        if 6 in self.boardAux:
            return True
        return self.win() # Game stops when someone wins.
    def show(self): 
        pprint (self.board)
    def scoring(self): 
        return 100 if game.win() else 0 # For the AI

ai = Negamax(30) # The AI will think 13 moves in advance
game = Conecta4( [ Human_Player(), AI_Player(ai) ] )
history = game.play()