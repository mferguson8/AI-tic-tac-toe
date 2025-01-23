import pygame
import sys
from tic_tac_toe import TicTacToe
from ai_player import TicTacToeAI
import torch

class TicTacToeGUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.LINE_WIDTH = 15
        self.CELL_SIZE = self.WIDTH // 3
        
        # Colors
        self.BG_COLOR = (28, 170, 156)
        self.LINE_COLOR = (23, 145, 135)
        self.X_COLOR = (84, 84, 84)
        self.O_COLOR = (242, 235, 211)
        
        # Setup display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tic Tac Toe vs AI')
        self.screen.fill(self.BG_COLOR)
        
        # Game state
        self.game = TicTacToe()
        self.ai = TicTacToeAI()
        self.ai.load_state_dict(torch.load('tic_tac_toe_ai.pth'))
        self.player = 1  # X starts
        
        # Draw initial grid
        self.draw_grid()
        
    def draw_grid(self):
        # Vertical lines
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.CELL_SIZE, 0), 
                        (self.CELL_SIZE, self.HEIGHT), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.CELL_SIZE * 2, 0), 
                        (self.CELL_SIZE * 2, self.HEIGHT), self.LINE_WIDTH)
        
        # Horizontal lines
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, self.CELL_SIZE), 
                        (self.WIDTH, self.CELL_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, self.CELL_SIZE * 2), 
                        (self.WIDTH, self.CELL_SIZE * 2), self.LINE_WIDTH)
    
    def draw_X(self, row, col):
        # Calculate position
        x = col * self.CELL_SIZE
        y = row * self.CELL_SIZE
        
        # Draw X
        offset = 50
        pygame.draw.line(self.screen, self.X_COLOR, 
                        (x + offset, y + offset), 
                        (x + self.CELL_SIZE - offset, y + self.CELL_SIZE - offset), 
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.X_COLOR, 
                        (x + offset, y + self.CELL_SIZE - offset), 
                        (x + self.CELL_SIZE - offset, y + offset), 
                        self.LINE_WIDTH)
    
    def draw_O(self, row, col):
        # Calculate position
        x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        
        # Draw O
        radius = self.CELL_SIZE // 3
        pygame.draw.circle(self.screen, self.O_COLOR, (x, y), radius, self.LINE_WIDTH)
    
    def draw_board(self):
        for row in range(3):
            for col in range(3):
                if self.game.board[row, col] == 1:
                    self.draw_X(row, col)
                elif self.game.board[row, col] == -1:
                    self.draw_O(row, col)
    
    def get_cell_from_mouse(self, mouse_pos):
        x, y = mouse_pos
        row = y // self.CELL_SIZE
        col = x // self.CELL_SIZE
        return int(row), int(col)
    
    def show_winner_message(self, winner):
        font = pygame.font.Font(None, 40)
        if winner == 1:
            text = "You win!"
            color = self.X_COLOR
        elif winner == -1:
            text = "AI wins!"
            color = self.O_COLOR
        else:
            text = "It's a tie!"
            color = self.LINE_COLOR
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.WIDTH/2, self.HEIGHT/2 - 20))
        
        # Add "Play Again?" message
        play_again_surface = font.render("Click to Play Again", True, color)
        play_again_rect = play_again_surface.get_rect(center=(self.WIDTH/2, self.HEIGHT/2 + 20))
        
        # Draw semi-transparent background
        s = pygame.Surface((self.WIDTH, 100))
        s.set_alpha(128)
        s.fill(self.BG_COLOR)
        self.screen.blit(s, (0, self.HEIGHT/2 - 50))
        
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(play_again_surface, play_again_rect)
        pygame.display.flip()
        
        # Wait for click or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    return True
        return False

    def reset_game(self):
        self.game = TicTacToe()
        self.player = 1
        self.screen.fill(self.BG_COLOR)
        self.draw_grid()
        pygame.display.flip()

    def run(self):
        while True:
            game_over = False
            
            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        row, col = self.get_cell_from_mouse(mouse_pos)
                        
                        # Player's turn
                        if self.player == 1:
                            if self.game.make_move(row, col, self.player):
                                self.draw_board()
                                pygame.display.flip()
                                
                                if self.game.currentWinner or self.game.is_full():
                                    game_over = True
                                    if self.show_winner_message(self.game.currentWinner):
                                        self.reset_game()
                                    continue
                                
                                # AI's turn
                                self.player = -1
                                row, col = self.ai.select_move(self.game.board * self.player)
                                self.game.make_move(row, col, self.player)
                                self.draw_board()
                                pygame.display.flip()
                                
                                if self.game.currentWinner or self.game.is_full():
                                    game_over = True
                                    if self.show_winner_message(self.game.currentWinner):
                                        self.reset_game()
                                    continue
                                self.player = 1
                
                pygame.display.flip()

if __name__ == '__main__':
    game = TicTacToeGUI()
    game.run() 