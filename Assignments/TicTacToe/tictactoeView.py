# tictactoeView.py
import pygame
from tictactoeModel import TicTacToe # Renamed import: game_logic -> tictactoeModel

# Define constants
WINDOWSIZE = 600
LINECOLOR = (0, 0, 0) # Black
BACKGROUNDCOLOR = (255, 255, 255) # White
SQUARESIZE = WINDOWSIZE // 3

class TicTacToeGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
        pygame.display.set_caption("Pygame Tic-Tac-Toe")
        self.game = TicTacToe()
        self.gameRunning = True # Using 'thisCase' convention

    def drawGrid(self): # Using 'thisCase' convention
        self.screen.fill(BACKGROUNDCOLOR)
        # Draw vertical and horizontal lines
        pygame.draw.line(self.screen, LINECOLOR, (SQUARESIZE, 0), (SQUARESIZE, WINDOWSIZE), 5)
        pygame.draw.line(self.screen, LINECOLOR, (SQUARESIZE * 2, 0), (SQUARESIZE * 2, WINDOWSIZE), 5)
        pygame.draw.line(self.screen, LINECOLOR, (0, SQUARESIZE), (WINDOWSIZE, SQUARESIZE), 5)
        pygame.draw.line(self.screen, LINECOLOR, (0, SQUARESIZE * 2), (WINDOWSIZE, SQUARESIZE * 2), 5)

    def handleClick(self, pos): # Using 'thisCase' convention
        x, y = pos
        col = x // SQUARESIZE
        row = y // SQUARESIZE
        if self.game.board[row][col] == 0:
            self.game.markSpot(row, col)
            # Check for game end condition (Model should return a status)
            if self.game.checkForWinConditional(row, col) or self.game.turnCounter >= 9:
                 self.gameRunning = False
            if self.gameRunning:
                self.game.turnCounter += 1
                self.game.whosTurn *= -1
        else:
            print("Spot already taken.") 

    def drawMarkers(self): # Using 'thisCase' convention
        for row in range(3):
            for col in range(3):
                center_x = col * SQUARESIZE + SQUARESIZE // 2
                center_y = row * SQUARESIZE + SQUARESIZE // 2
                if self.game.board[row][col] == 1:
                    # Draw 'X' 
                    offset = 50
                    pygame.draw.line(self.screen, LINECOLOR, 
                                     (center_x - offset, center_y - offset), 
                                     (center_x + offset, center_y + offset), 8)
                    pygame.draw.line(self.screen, LINECOLOR, 
                                     (center_x + offset, center_y - offset), 
                                     (center_x - offset, center_y + offset), 8)
                elif self.game.board[row][col] == -1:
                    # Draw 'O' 
                    radius = SQUARESIZE // 3
                    pygame.draw.circle(self.screen, LINECOLOR, (center_x, center_y), radius, 8)

    def runGameLoop(self): 
        while self.gameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRunning = False
                # Handle mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(event.pos)
            # 1. Drawing: Draw the static grid
            self.drawGrid()
            # 2. Drawing: Draw the dynamic markers (X's and O's)
            self.drawMarkers()
            # 3. Update the display to show the changes
            pygame.display.flip()
        pygame.quit()
        
        
if __name__ == '__main__':
    game = TicTacToeGUI()
    game.runGameLoop()