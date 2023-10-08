try:
    import numpy as np
except ImportError:
    print("Numpy não econtrado !")
    raise

from easyAI import TwoPlayerGame, AI_Player, Negamax, SSS, Human_Player


class ConnectFour(TwoPlayerGame):
    """
    O jogo Connect 4 (Lig 4), descrito em:
    http://en.wikipedia.org/wiki/Connect_Four
    """

    def __init__(self, players, board=None):
        self.players = players
        self.board = (
            board
            if (board is not None)
            else (np.array([[0 for i in range(7)] for j in range(6)]))
        )
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player

    def show(self):
        print(
            "\n"
            + "\n".join(
                ["0 1 2 3 4 5 6", 13 * "-"]
                + [
                    " ".join([[".", "O", "X"][self.board[5 - j][i]] for i in range(7)])
                    for j in range(6)
                ]
            )
        )

    def lose(self):
        return find_four(self.board, self.opponent_index)
    
    def win(self):
        return find_four(self.board, self.current_player)

    def score_two(self):
        return find_two(self.board, self.current_player)

    def is_over(self):
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        if self.lose():
            return -100
        if find_three(self.board, self.opponent_index):
            return -50
        if find_two(self.board, self.current_player):
            return 25
        if find_three(self.board, self.current_player):
            return 50
        if self.win():
            return 100
        return 0


def find_four(board, current_player):
    """
    Verifica se o jogador tem 4 peças conectadas
    """
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False

def find_two(board, current_player):
    """
    Verifica se o jogador tem 2 peças conectadas
    """
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 2:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False

def find_three(board, current_player):
    """
    Verifica se o jogador tem 3 peças conectadas
    """
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 3:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False

POS_DIR = np.array(
    [[[i, 0], [0, 1]] for i in range(6)]
    + [[[0, i], [1, 0]] for i in range(7)]
    + [[[i, 0], [1, 1]] for i in range(1, 3)]
    + [[[0, i], [1, 1]] for i in range(4)]
    + [[[i, 6], [1, -1]] for i in range(1, 3)]
    + [[[0, i], [1, -1]] for i in range(3, 7)]
)

print("Escolha o modo de jogo: Jogador vs IA (1) ou IA vs IA (2): ",end='')
x = int(input())
print("Escolha quantos passos a IA vai analisar (5 é o recomandado): ",end='')
y = int(input())

ai = Negamax(y)

if x == 1:
    game = ConnectFour([Human_Player(), AI_Player(ai)])
else:
    game = ConnectFour([AI_Player(ai), AI_Player(ai)])

game.play()

if game.lose():
    print("Jogador %d ganhou!" % (game.opponent_index))
else:
    print("Jogo empatado!")