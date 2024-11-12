from tic_tac_toe import TicTacToe
from ai_player import TicTacToeAI
import torch

def main():
    game = TicTacToe()
    ai = TicTacToeAI()
    ai.load_state_dict(torch.load('tic_tac_toe_ai.pth', weights_only=True))
    player = 1  # Player is 1 (X), AI is -1 (O)
    game.currentWinner = None

    while True:
        print("Player is X's and AI is O's.")
        game.print_board()
        if game.currentWinner is not None or game.is_full():
            print("Game over.")
            break

        if player == 1:
            # Player's turn
            move = input("Enter your move (row,col): ")
            try:
                row, col = map(int, move.strip().split(','))
                if not game.make_move(row, col, player):
                    print("Invalid move. Try again.")
                    continue
            except Exception as e:
                print("Invalid input. Enter row and column numbers separated by a comma.")
                continue
        else:
            # AI's turn
            row, col = ai.select_move(game.board * player)
            game.make_move(row, col, player)
            print(f"AI placed at position ({row}, {col})")

        player *= -1  # Switch turn

        game.print_board()
        if game.currentWinner == 1:
            print("You win!")
        elif game.currentWinner == -1:
            print("AI wins!")
        else:
            print("It's a tie!")

if __name__ == '__main__':
    main()
