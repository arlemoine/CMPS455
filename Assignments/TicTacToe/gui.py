import pygame as pg
from logic import TicTacToeGame as game

# Define constants
WINDOWSIZE = 600
BLACK = (0, 0, 0) # Black
WHITE = (255, 255, 255) # White
SQUARESIZE = WINDOWSIZE // 3
MARKER_SIZE = int(SQUARESIZE * 0.8) # Size for scaled image

class TicTacToeGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOWSIZE, WINDOWSIZE))
        pg.display.set_caption("Tic-Tac-Toe")
        
        self.game = game()
        self.game.gameRunning = True
        self.game.gameState = "MENU"       # State: "MENU", "PLAYING", or "GAMEOVER"
        self.game.gameMode = 0             # 1: P vs AI, 2: P vs P
        self.FONT = pg.font.SysFont("Arial", 32)
        
        # Load game assetsco
        try:
            # Load and scale background image
            bg_img = pg.image.load('img/board_art.png').convert()
            self.background = pg.transform.scale(bg_img, (WINDOWSIZE, WINDOWSIZE))
            # Load, scale, and fit X image
            x_img = pg.image.load('img/letter_x.png').convert_alpha()
            self.x_marker = pg.transform.scale(x_img, (MARKER_SIZE, MARKER_SIZE))
             # Load, scale, and fit O image
            o_img = pg.image.load('img/letter_o.png').convert_alpha()
            self.o_marker = pg.transform.scale(o_img, (MARKER_SIZE, MARKER_SIZE))
        except pg.error as e:
            print(f"Error loading image: {e}")
            self.game.gameRunning = False

    def resetGame(self):
            """Resets the model and state to start a new game."""
            self.game = game() # New game model
            self.game.gameMode = self.game.gameMode     # Set gameMode on the model
            self.game.gameState = "PLAYING"

    def drawGrid(self): 
        self.screen.blit(self.background, (0, 0))

    def drawMenu(self):
        """Draws the main menu screen."""
        self.screen.blit(self.background, (0, 0))
        
        title_text = self.FONT.render("TIC-TAC-TOE", True, WHITE)
        self.screen.blit(title_text, (WINDOWSIZE // 2 - title_text.get_width() // 2, 50))
        
        text_1 = self.FONT.render(" [1] Player vs AI", True, WHITE)
        self.screen.blit(text_1, (WINDOWSIZE // 2 - text_1.get_width() // 2, 200))

        text_2 = self.FONT.render(" [2] Player vs Player", True, WHITE)
        self.screen.blit(text_2, (WINDOWSIZE // 2 - text_2.get_width() // 2, 300))

        quit_text = self.FONT.render(" [Q] Quit", True, WHITE)
        self.screen.blit(quit_text, (WINDOWSIZE // 2 - quit_text.get_width() // 2, 450))

        pg.display.flip()

    def aiTurn(self):
        """Executes the AI's move."""
        if self.game.gameState != "PLAYING" or self.game.whosTurn != -1:
            return

        # 1. Get move from model
        row, col = self.game.aiMove() 
        
        # 2. Mark spot (returns 1 for win, 0 for ongoing)
        gameStatus = self.game.markSpot(row, col) 
        
        # 3. Check win/tie
        if gameStatus == 1:
            self.game.WINNER = "Player O (AI) wins! (Press SPACE for Menu)"
            self.game.gameState = "GAMEOVER"
        
        # 4. Advance turn and check for tie only if game is still running
        if self.game.gameState != "GAMEOVER":
            self.game.turnCounter += 1
            if self.game.turnCounter == 9:
                self.game.WINNER = "It's a Tie! (Press SPACE for Menu)"
                self.game.gameState = "GAMEOVER"
            else:
                self.game.whosTurn *= -1 # Switch back to Player X (human)

    def handleClick(self, pos):
        """Translate a player click into a move and trigger AI if needed."""
        row = pos[1] // SQUARESIZE
        col = pos[0] // SQUARESIZE
    
        # Block clicks if AI turn
        if self.game.gameMode == 1 and self.game.whosTurn == -1:
            return
    
        validChoice = self.game.validateChoice(row, col)
       if validChoice == 1:
           result = self.game.markSpot(row, col)
    
            # Update GUI message if game over
            if self.game.checkForWinConditional(row, col) == 1:
                winner_char = "X" if self.game.whosTurn == 1 else "O"
                self.game.WINNER = f"Player {winner_char} wins! (Press SPACE for Menu)"
                self.game.gameState = "GAMEOVER"
            elif self.game.turnCounter == 9:
                self.game.WINNER = "It's a Tie! (Press SPACE for Menu)"
                self.game.gameState = "GAMEOVER"
    
            # Trigger AI move if needed
            if self.game.gameMode == 1 and self.game.whosTurn == -1:
                self.aiTurn()

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
            while self.game.gameRunning:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.game.gameRunning = False
    
                    if event.type == pg.MOUSEBUTTONDOWN and self.game.gameState == "PLAYING":
                        self.handleClick(event.pos)
    
                    if event.type == pg.KEYDOWN:
                        if self.game.gameState == "MENU" or self.game.gameState == "GAMEOVER":
                            # Handle menu and game over screen inputs
                            if event.key == pg.K_1:
                                self.game.gameMode = 1
                                self.resetGame()
                            elif event.key == pg.K_2:
                                self.game.gameMode = 2
                                self.resetGame()
                            elif event.key == pg.K_q:
                                self.game.gameRunning = False
                            elif event.key == pg.K_SPACE and self.game.gameState == "GAMEOVER":
                                self.game.gameState = "MENU" # Return to menu
                # --- Drawing Logic based on State ---
                if self.game.gameState == "MENU":
                    self.drawMenu()
    
                elif self.game.gameState == "PLAYING" or self.game.gameState == "GAMEOVER":
                    self.drawGrid()
                    self.drawMarkers()
                    
                    if self.game.gameState == "GAMEOVER":
                        # Draw game outcome text over the final board state
                        final_text = self.FONT.render(self.game.WINNER, True, BLACK)
                        text_rect = final_text.get_rect(center=(WINDOWSIZE // 2, WINDOWSIZE // 2))
                        
                        # Draw a solid white box with a black border
                        pg.draw.rect(self.screen, (255, 255, 255), text_rect.inflate(20, 10), 0, 5)
                        pg.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10), 3, 5)
                        
                        self.screen.blit(final_text, text_rect)
                    
                    pg.display.flip()
    
            pg.quit()
        
        
if __name__ == '__main__':
    game1 = TicTacToeGUI()
    game1.runGameLoop()