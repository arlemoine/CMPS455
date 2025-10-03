import random
import pygame as pg
import tictactoeModel as model
import tictactoeGui as gui
import time


class Controller:
    def __init__(self, name: str = "Default"):
        self.name = name
        self.scores = [0, 0]
        self.controllerRunning = True
        self.gameMode = 0
        
    def takeTurn(self, gameModel, row, col):
        validChoice = gameModel.validateChoice(row, col)
        if validChoice == 1:
            # markSpot now returns 0 (continue), 1 (win), or 2 (tie)
            gameModel.markSpot(row, col)
            gameStatus = gameModel.winCheck(row, col)
            print(f"gameStatus: {gameStatus}")
            if gameStatus == 1 or gameStatus == 2: # Win or Tie
                gameModel.gameState = model.GameState.GAMEOVER
            else: 
                # Only switch turn if the game is still PLAYING
                gameModel.nextTurn()
        
    def handleEvents(self, gameModel, gameGui):
        # Monitor for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameModel.gameRunning = False
                self.controllerRunning = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if gameModel.gameState == model.GameState.PLAYING:
                    # Register a click, validate choice, mark spot, and check for win
                    pos_x, pos_y = event.pos
                    row = (pos_y - gui.STATUSBAR_HEIGHT) // gui.SQUARESIZE
                    col = pos_x // gui.SQUARESIZE
                    self.takeTurn(gameModel, row, col)
                    return
            elif event.type == pg.KEYDOWN:
                if gameModel.gameState != model.GameState.PLAYING:
                    # Handle menu and game over screen inputs
                    if event.key == pg.K_1:
                        self.gameMode = model.GameMode.PVAI
                        gameModel.gameMode = self.gameMode
                        gameModel.gameState = model.GameState.PLAYING
                    elif event.key == pg.K_2:
                        self.gameMode = model.GameMode.PVP
                        gameModel.gameMode = self.gameMode
                        gameModel.gameState = model.GameState.PLAYING
                    elif event.key == pg.K_SPACE:
                        if gameModel.gameState == model.GameState.GAMEOVER:
                            gameModel.gameRunning = False
                if event.key == pg.K_q:
                    gameModel.gameRunning = False
                    self.controllerRunning = False

        if gameModel.gameState == model.GameState.PLAYING:
            if gameModel.gameMode == model.GameMode.PVAI and gameModel.whosTurn == -1:
                time.sleep(2)
                row, col = gameModel.aiMove()
                self.takeTurn(gameModel, row, col)
                
        if gameModel.gameState == model.GameState.MENU:
            if self.gameMode != 0:
                gameModel.gameState = model.GameState.PLAYING

    def newGame(self):
        clock = pg.time.Clock()
        gameModel = model.TicTacToeGame(model.GameMode.PVAI)
        gameGui = gui.TicTacToeGUI()
        gameGui.render(gameModel, self) 
        
        if self.gameMode != 0:
            gameModel.gameMode = self.gameMode
        
        while gameModel.gameRunning:
            self.handleEvents(gameModel, gameGui)
            # gameGui.screen.fill((0, 0, 0))
            gameGui.render(gameModel, self)
            clock.tick(60)

        if gameModel.winner == 1:
            self.scores[0] += 1
        if gameModel.winner == 2:
            self.scores[1] += 1
            
        print(f"Winner: {gameModel.winner}")
        
    def newGameLoop(self):
        while self.controllerRunning:
            self.newGame()
        pg.quit()

if __name__ == '__main__':
    game = Controller()
    game.newGameLoop()
