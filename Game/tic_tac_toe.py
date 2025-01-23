import numpy as np

class TicTacToe:

    def __init__(self):
        # 0: empty, 1: player, -1: AI
        self.board = np.zeros((3, 3), dtype = int)
        self.currentWinner = None
    
    def available_moves(self):
        # Returns a list of rows and cols that have empty spots
        return [(i, j)for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def make_move(self, row, col, player):
        #place the players piece on the board
        if self.board[row, col] == 0:
            self.board[row, col] = player
            if self.check_winner(player):
                self.currentWinner = player
            return True
        return False
    def check_winner(self, player):
        #check rows, cols, and diags for a winner
        for i in range(3):
            if all ([self.board[i, j] == player for j in range(3)]) \
                or all ([self.board[j, i] == player for j in range(3)]):
                    return True
        if all([self.board[i, i] == player for i in range(3)]) \
                or all([self.board[i, 2 - i] == player for i in range(3)]):
                    return True
        return False

    def is_full(self):
        return not any(self.board[i, j] == 0 for i in range(3) for j in range(3))

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.currentWinner = None

    def print_board(self):
        # Print the board to the console with row and column labels
        symbol_map = {1: 'X', -1: 'O', 0: ' '}
        print("\nBoard:")
        # Print column labels
        print('   ' + '   '.join(str(j) for j in range(3)))
        print('  ' + '----' * 3)
        for i, row in enumerate(self.board):
            # Print row label and row content
            row_content = ' | '.join(symbol_map[cell] for cell in row)
            print(f"{i} | {row_content} |")
            print('  ' + '----' * 3)



    