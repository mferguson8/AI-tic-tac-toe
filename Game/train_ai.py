import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from tic_tac_toe import TicTacToe
from ai_player import TicTacToeAI

def generate_training_data(num_samples):
    X = []
    y = []
    game = TicTacToe()

    for _ in range(num_samples):
        game.reset()
        board_states = []
        moves = []
        player = 1  # Start with player

        while True:
            available = game.available_moves()
            if not available or game.currentWinner is not None:
                break

            move = np.random.choice(len(available))
            row, col = available[move]
            game.make_move(row, col, player)
            board_states.append(game.board.copy())
            moves.append((row, col))

            player *= -1  # Switch player

        # Assign labels (1 if win, 0 otherwise)
        label = 1 if game.currentWinner == -1 else 0

        for state, move in zip(board_states, moves):
            if game.board[move[0], move[1]] == -1:
                X.append(state.flatten())
                y_label = np.zeros(9)
                y_label[move[0] * 3 + move[1]] = label
                y.append(y_label)

    return np.array(X), np.array(y)

def train_ai_model():
    model = TicTacToeAI()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    X_train, y_train = generate_training_data(1000)
    X_train = torch.FloatTensor(X_train)
    y_train = torch.LongTensor(np.argmax(y_train, axis=1))

    epochs = 10
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = loss_fn(outputs, y_train)
        loss.backward()
        optimizer.step()
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')

    # Save the trained model
    torch.save(model.state_dict(), 'tic_tac_toe_ai.pth')

if __name__ == '__main__':
    train_ai_model()
