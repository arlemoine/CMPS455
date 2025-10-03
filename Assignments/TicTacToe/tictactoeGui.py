import pygame as pg


# Define constants
WINDOWSIZE = 600
STATUSBAR_HEIGHT = 80
SCREEN_HEIGHT = WINDOWSIZE + STATUSBAR_HEIGHT
SQUARESIZE = WINDOWSIZE // 3
MARKER_SIZE = int(SQUARESIZE * 0.8)  # Size for scaled image
KEY_SIZE = int(SQUARESIZE * 0.3)

BLACK = (0, 0, 0)  # Black
WHITE = (255, 255, 255)  # White
DARK_GRAY = (30, 30, 30)
BLUE = (10, 50, 150)
ORANGE = (200, 80, 0)


class TicTacToeGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOWSIZE, SCREEN_HEIGHT))
        pg.display.set_caption("Tic-Tac-Toe")
        self.FONT = pg.font.SysFont("Arial", 32)

        # Load game assets
        try:
            # Load and scale background image
            bg_img = pg.image.load('img/board_art.png').convert()
            self.background = pg.transform.scale(
                bg_img, (WINDOWSIZE, WINDOWSIZE))
            # Load, scale, and fit X image
            x_img = pg.image.load('img/letter_x.png').convert_alpha()
            self.x_marker = pg.transform.scale(
                x_img, (MARKER_SIZE, MARKER_SIZE))
            # Load, scale, and fit O image
            o_img = pg.image.load('img/letter_o.png').convert_alpha()
            self.o_marker = pg.transform.scale(
                o_img, (MARKER_SIZE, MARKER_SIZE))
            # Load, scale, and fit key images
            key1_png = pg.image.load('img/key_1.png').convert_alpha()
            self.key1_img = pg.transform.scale(
                key1_png, (KEY_SIZE, KEY_SIZE))
            key2_png = pg.image.load('img/key_2.png').convert_alpha()
            self.key2_img = pg.transform.scale(
                key2_png, (KEY_SIZE, KEY_SIZE))
            keyQ_png = pg.image.load('img/key_q.png').convert_alpha()
            self.keyQ_img = pg.transform.scale(
                keyQ_png, (KEY_SIZE, KEY_SIZE))
            keySPACE_png = pg.image.load('img/key_space.png').convert_alpha()
            self.keySPACE_img = pg.transform.scale(
                keySPACE_png, (KEY_SIZE * 2, KEY_SIZE))
        except pg.error as e:
            print(f"Error loading image: {e}")
            
    def drawStatusBar(self, game, controller):
        pg.draw.rect(self.screen, (50, 50, 50), (0, 0, WINDOWSIZE, STATUSBAR_HEIGHT))

        # Score box
        score_bg_color = DARK_GRAY
        score_bg_rect = pg.Rect(20, 20, 210, 40) 
        pg.draw.rect(self.screen, score_bg_color, score_bg_rect, border_radius=10)
        
        # Individual score boxes
        team1_rect = pg.Rect(30, 25, 90, 30)
        team2_rect = pg.Rect(130, 25, 90, 30)
        pg.draw.rect(self.screen, BLUE, team1_rect, border_radius=10)  # team 1 color
        pg.draw.rect(self.screen, ORANGE, team2_rect, border_radius=10) # team 2 color
        
        # Render scores
        score1_text = self.FONT.render(str(controller.scores[0]), True, WHITE)
        score2_text = self.FONT.render(str(controller.scores[1]), True, WHITE)
        self.screen.blit(score1_text, (team1_rect.centerx - score1_text.get_width() // 2, team1_rect.centery - score1_text.get_height() // 2))
        self.screen.blit(score2_text, (team2_rect.centerx - score2_text.get_width() // 2, team2_rect.centery - score2_text.get_height() // 2))

    def statusMessage(self, message):
        messageText = self.FONT.render(message, True, WHITE)
        self.screen.blit(messageText, (WINDOWSIZE - messageText.get_width() - 20, STATUSBAR_HEIGHT // 2 - messageText.get_height() // 2))


    def drawMenu(self):
        """Draws the main menu screen."""
        # Background
        pg.draw.rect(self.screen, WHITE, (0, 0, WINDOWSIZE, SCREEN_HEIGHT))
    
        # Title
        title_text = self.FONT.render("TIC-TAC-TOE", True, BLACK)
        self.screen.blit(title_text, (WINDOWSIZE // 2 - title_text.get_width() // 2, 50))
    
        # Player vs AI option with key image
        y_pos = 200
        self.screen.blit(self.key1_img, (WINDOWSIZE // 2 - 200, y_pos))
        option_text = self.FONT.render("Player vs AI", True, BLACK)
        self.screen.blit(option_text, (WINDOWSIZE // 2 - 100, y_pos + self.key1_img.get_height() // 4))
    
        # Player vs Player option with key image
        y_pos = 300
        self.screen.blit(self.key2_img, (WINDOWSIZE // 2 - 200, y_pos))
        option_text = self.FONT.render("Player vs Player", True, BLACK)
        self.screen.blit(option_text, (WINDOWSIZE // 2 - 100, y_pos + self.key2_img.get_height() // 4))
    
        # Quit option with Q key image
        y_pos = 400
        self.screen.blit(self.keyQ_img, (WINDOWSIZE // 2 - 200, y_pos))
        option_text = self.FONT.render("Quit (At any time)", True, BLACK)
        self.screen.blit(option_text, (WINDOWSIZE // 2 - 100, y_pos + self.keyQ_img.get_height() // 4))
    
        pg.display.flip()

    def drawMarkers(self, game):  # Using 'thisCase' convention
        offset_margin = SQUARESIZE * 0.1  # Small margin to center the image
        
        for row in range(3):
            for col in range(3):
                # Calculate the top-left corner position for blitting
                x_pos = col * SQUARESIZE + offset_margin
                y_pos = row * SQUARESIZE + STATUSBAR_HEIGHT+ offset_margin

                # Player 1 is 'X' (1)
                if game.board[row][col] == 1:
                    self.screen.blit(self.x_marker, (x_pos, y_pos))

                # Player 2 is 'O' (-1)
                elif game.board[row][col] == -1:
                    self.screen.blit(self.o_marker, (x_pos, y_pos))
            
    def render(self, game, controller):
        # --- Drawing Logic based on State ---
        self.drawStatusBar(game, controller)
        if game.gameState == 1: # MENU
            self.drawMenu()
        elif game.gameState == 2: # PLAYING
            self.screen.blit(self.background, (0, STATUSBAR_HEIGHT))
            self.drawMarkers(game)
            if game.whosTurn == 1:
                self.statusMessage("Player 1, your turn.")
            if game.whosTurn == -1:
                if game.gameMode == 2:
                    self.statusMessage("Player 2, your turn.")
                if game.gameMode == 1:
                    self.statusMessage("Waiting for AI...")
        elif game.gameState == 3: # GAMEOVER
            self.drawMarkers(game)
            if game.winner == 1:
                message = "Player 1 (X) wins!"
            elif game.winner == 2:
                message = "Player 2 (O) wins!"
            elif game.winner == 3:
                message = "It's a tie!"
            else:
                message = "Game over!"
                
            # Draw game outcome text over the final board state
            self.statusMessage(message)
            
            box_width = 470
            box_height = 100
            box_x = WINDOWSIZE // 2 - box_width // 2
            box_y = 450
            
            # Draw white rectangle
            pg.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height))
            # Draw black border
            pg.draw.rect(self.screen, BLACK, (box_x, box_y, box_width, box_height), 2)
        
            # Render "Press " text
            press_text = self.FONT.render("Press ", True, BLACK)
            text_x = box_x + 20
            text_y = box_y + (box_height - press_text.get_height()) // 2
            self.screen.blit(press_text, (text_x, text_y))
        
            # Blit spacebar image
            key_x = text_x + press_text.get_width() + 10  # small gap
            key_y = box_y + (box_height - self.keySPACE_img.get_height()) // 2
            self.screen.blit(self.keySPACE_img, (key_x, key_y))
        
            # Render " for new game" text
            newgame_text = self.FONT.render(" for new game", True, BLACK)
            newgame_x = key_x + self.keySPACE_img.get_width() + 10
            newgame_y = box_y + (box_height - newgame_text.get_height()) // 2
            self.screen.blit(newgame_text, (newgame_x, newgame_y))        
        
        pg.display.flip()


if __name__ == '__main__':
    game1 = TicTacToeGUI()
    game1.runGameLoop()
