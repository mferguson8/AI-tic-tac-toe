import torch
import torch.nn as nn
import torch.nn.functional as F

class TicTacToeAI(nn.Module):
    def __init__(self):
        super(TicTacToeAI, self).__init__()
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 9)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x  # Raw scores for each position

    def select_move(self, board_state):
        self.eval()
        with torch.no_grad():
            board_tensor = torch.FloatTensor(board_state.flatten()).unsqueeze(0)
            logits = self.forward(board_tensor)
            # Mask invalid moves
            mask = (board_state.flatten() != 0)
            logits[0][mask] = -float('inf')
            probs = F.softmax(logits, dim=1)
            move = torch.argmax(probs, dim=1).item()
            row, col = divmod(move, 3)
            return row, col
