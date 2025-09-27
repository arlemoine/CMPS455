import pygame
import tictactoeModel

# Define constants
WINDOWSIZE = 600
LINECOLOR = (0, 0, 0) # Black
BACKGROUNDCOLOR = (255, 255, 255) # White
SQUARESIZE = WINDOWSIZE // 3
MARKER_SIZE = int(SQUARESIZE * 0.8) # Size for the scaled image

class TicTacToeGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
        pygame.display.set_caption("Pygame Tic-Tac-Toe")
        self.game = tictactoeModel.TicTacToe()
        self.gameRunning = True 
        
        # NEW: Load and scale the background image
        try:
            bg_img = pygame.image.load('img/board_art.png').convert()
            self.background = pygame.transform.scale(bg_img, (WINDOWSIZE, WINDOWSIZE))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.gameRunning = False
        
        try:
            # Load X image and scale it to fit the grid square
            x_img = pygame.image.load('img/letter_x.png').convert_alpha()
            self.x_marker = pygame.transform.scale(x_img, (MARKER_SIZE, MARKER_SIZE))

            # Load O image and scale it
            o_img = pygame.image.load('img/letter_o.png').convert_alpha()
            self.o_marker = pygame.transform.scale(o_img, (MARKER_SIZE, MARKER_SIZE))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            print("Please ensure 'img/letter_x.png' and 'img/letter_o.png' are available.")
            self.gameRunning = False

    def drawGrid(self): # Using 'thisCase' convention
        # NEW: Draw the background image first
        self.screen.blit(self.background, (0, 0))

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
        offset_margin = SQUARESIZE * 0.1 # Small margin to center the image
        for row in range(3):
            for col in range(3):
                # Calculate the top-left corner position for blitting
                x_pos = col * SQUARESIZE + offset_margin
                y_pos = row * SQUARESIZE + offset_margin
                
                # Player 1 is 'X' (1)
                if self.game.board[row][col] == 1:
                    self.screen.blit(self.x_marker, (x_pos, y_pos))
                
                # Player 2 is 'O' (-1)
                elif self.game.board[row][col] == -1:
                    self.screen.blit(self.o_marker, (x_pos, y_pos))

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