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
        
        # Game State Variables
        self.game = tictactoeModel.TicTacToe()
        self.gameRunning = True
        self.gameState = "MENU"       # State: "MENU", "PLAYING", or "GAMEOVER"
        self.gameMode = 0             # 1: P vs AI, 2: P vs P
        self.FONT = pygame.font.SysFont("Arial", 40)
        self.WINNER = ""
        
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

    def resetGame(self):
            """Resets the model and state to start a new game."""
            self.game = tictactoeModel.TicTacToe() # New game model
            self.game.gameMode = self.gameMode     # IMPORTANT: Manually set gameMode on the model
            self.gameState = "PLAYING"
            self.WINNER = ""
            
            # If AI is Player O (-1) and starts first (not likely for X always starting as 1)
            # We assume Player X (1) always starts first, so no initial AI move is needed.


    def drawGrid(self): # Using 'thisCase' convention
        # NEW: Draw the background image first
        self.screen.blit(self.background, (0, 0))

    def drawMenu(self):
        """Draws the main menu screen."""
        self.screen.blit(self.background, (0, 0))
        
        title_text = self.FONT.render("TIC-TAC-TOE", True, (0, 0, 0))
        self.screen.blit(title_text, (WINDOWSIZE // 2 - title_text.get_width() // 2, 50))
        
        text_1 = self.FONT.render(" [1] Player vs AI", True, (50, 50, 50))
        self.screen.blit(text_1, (WINDOWSIZE // 2 - text_1.get_width() // 2, 200))

        text_2 = self.FONT.render(" [2] Player vs Player", True, (50, 50, 50))
        self.screen.blit(text_2, (WINDOWSIZE // 2 - text_2.get_width() // 2, 300))

        quit_text = self.FONT.render(" [Q] Quit", True, (150, 0, 0))
        self.screen.blit(quit_text, (WINDOWSIZE // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()

    def aiTurn(self):
        """Executes the AI's move."""
        if self.gameState != "PLAYING" or self.game.whosTurn != -1:
            return

        # 1. Get move from model
        row, col = self.game.aiMove() 
        
        # 2. Mark spot (returns 1 for win, 0 for ongoing)
        gameStatus = self.game.markSpot(row, col) 
        
        # 3. Check win/tie
        if gameStatus == 1:
            self.WINNER = "Player O (AI) wins! (Press SPACE for Menu)"
            self.gameState = "GAMEOVER"
        
        # 4. Advance turn and check for tie only if game is still running
        if self.gameState != "GAMEOVER":
            self.game.turnCounter += 1
            if self.game.turnCounter == 9:
                self.WINNER = "It's a Tie! (Press SPACE for Menu)"
                self.gameState = "GAMEOVER"
            else:
                self.game.whosTurn *= -1 # Switch back to Player X (human)

    def handleClick(self, pos):
            """Handles player move and checks game status."""
            x, y = pos
            col = x // SQUARESIZE
            row = y // SQUARESIZE
            
            # Block interaction during AI's turn
            if self.gameMode == 1 and self.game.whosTurn == -1:
                return
    
            # Validate spot is available
            if self.game.board[row][col] == 0:
                
                # 1. Mark spot (returns 1 for win, 0 for ongoing)
                gameStatus = self.game.markSpot(row, col)
                
                # 2. Check for win
                if gameStatus == 1:
                    winner_char = "X" if self.game.whosTurn == 1 else "O"
                    self.WINNER = f"Player {winner_char} wins! (Press SPACE for Menu)"
                    self.gameState = "GAMEOVER"
                     
                # 3. Advance turn and check for tie only if game is still running
                if self.gameState != "GAMEOVER":
                    self.game.turnCounter += 1
                    
                    if self.game.turnCounter == 9:
                        self.WINNER = "It's a Tie! (Press SPACE for Menu)"
                        self.gameState = "GAMEOVER"
                    else:
                        self.game.whosTurn *= -1
                        
                        # 4. If P vs AI, trigger AI move immediately
                        if self.gameMode == 1 and self.game.whosTurn == -1:
                            self.aiTurn()
            # else: Spot already taken (no need for print in GUI unless debugging)


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
    
                    if event.type == pygame.MOUSEBUTTONDOWN and self.gameState == "PLAYING":
                        self.handleClick(event.pos)
    
                    if event.type == pygame.KEYDOWN:
                        if self.gameState == "MENU" or self.gameState == "GAMEOVER":
                            # Handle menu and game over screen inputs
                            if event.key == pygame.K_1:
                                self.gameMode = 1
                                self.resetGame()
                            elif event.key == pygame.K_2:
                                self.gameMode = 2
                                self.resetGame()
                            elif event.key == pygame.K_q:
                                self.gameRunning = False
                            elif event.key == pygame.K_SPACE and self.gameState == "GAMEOVER":
                                self.gameState = "MENU" # Return to menu
    
    
                # --- Drawing Logic based on State ---
    
                if self.gameState == "MENU":
                    self.drawMenu()
    
                elif self.gameState == "PLAYING" or self.gameState == "GAMEOVER":
                    self.drawGrid()
                    self.drawMarkers()
                    
                    if self.gameState == "GAMEOVER":
                        # Draw game outcome text over the final board state
                        final_text = self.FONT.render(self.WINNER, True, (255, 0, 0))
                        text_rect = final_text.get_rect(center=(WINDOWSIZE // 2, WINDOWSIZE // 2))
                        
                        # Draw a solid white box with a black border
                        pygame.draw.rect(self.screen, (255, 255, 255), text_rect.inflate(20, 10), 0, 5)
                        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10), 3, 5)
                        
                        self.screen.blit(final_text, text_rect)
                    
                    pygame.display.flip()
    
            pygame.quit()
        
        
if __name__ == '__main__':
    game = TicTacToeGUI()
    game.runGameLoop()