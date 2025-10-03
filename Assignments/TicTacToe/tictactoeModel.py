import random


class GameState:
    MENU = 1
    PLAYING = 2
    GAMEOVER = 3
    
    
class GameMode:
    PVAI = 1   
    PVP = 2
 


class GameWinner:
    PENDING = 0
    PLAYER1 = 1
    PLAYER2 = 2
    TIE = 3


class TicTacToeGame:
    def __init__(self, gameMode: GameMode):
        # General
        self.gameRunning = True
        self.gameState = GameState.MENU
        self.gameMode = gameMode
        self.winner = GameWinner.PENDING
        self.whosTurn = 1
        self.turnCounter = 0
        
        # Board status
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.rowSum = [0, 0, 0]
        self.colSum = [0, 0, 0]
        self.diagSum = [0, 0]

    def validateChoice(self, row, col):
        """
        Validate choice of row and column selection.
        
        :param row: Targeted row
        :type row: int
        :param col: Targeted column
        :type col: int
        :return: 1 (valid), -1 (invalid)
        :rtype: int
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            # Get row and column indeces and validate
            print("Invalid spot entered.")
            return -1
        elif self.board[row][col] != 0:
            # Validate spot is available
            print("Spot already taken.")
            return -1
        else:
            return 1

    def getInput(self):
        """
        Retrieve input from either a human player or AI player and mark a spot on the game board.
        
        :return: 0 (no win yet), 1 (winner found)
        :rtype: int
        """
        validatedMove = -1
        if self.gameMode == 1:
            if self.whosTurn == -1:
                row, col = self.aiMove()
                validatedMove = 1
        while validatedMove != 1:
            if self.whosTurn == 1:
                print("Player 1, make your move: ")
                spot = input()
            else:
                print("Player 2, make your move: ")
                spot = input()
            row, col = self.cliSpotToIndex(spot)
            validatedMove = self.validateChoice(row, col)
        return self.markSpot(row, col)

    def markSpot(self, row, col):
        """
        Mark spot on the game board as taken and increment arrays for row/column/diagonal sums.
        
        :param row: Targeted row
        :type row: int
        :param col: Targeted column
        :type col: int
        :return: 0 (no win yet), 1 (winner found)
        :rtype: int
        """
        # Mark spot on the board
        self.board[row][col] = self.whosTurn
        
        # Increment sums related to victory conditions
        self.rowSum[row] += self.whosTurn
        self.colSum[col] += self.whosTurn
        if row == col:
            self.diagSum[0] += self.whosTurn
        if row + col == 2:
            self.diagSum[1] += self.whosTurn
        
        # Advance turn counter and check for tie
        self.turnCounter += 1
        print(self.turnCounter)
            
    def winCheck(self, row, col):
        """
        Determine if a winner is found, targeting the given row and column as the source for checks.
        
        :param row: Target row
        :type row: int
        :param col: Target column
        :type col: int
        :return: 0 (no win yet), 1 (winner found)
        :rtype: int
        """
        # Check for win conditions
        winValue = 3 if self.whosTurn == 1 else -3     
        status = 0
                
        if self.whosTurn == 1:
            potentialWinner = GameWinner.PLAYER1
        else:
            potentialWinner = GameWinner.PLAYER2
            
        # Check for tie game
        if self.turnCounter == 9:
            self.winner = GameWinner.TIE
            self.gameState = GameState.GAMEOVER
            status = 2
        
        if self.rowSum[row] == winValue:
            self.winner = potentialWinner
            print(f"Player {self.winner} wins!")
            status = 1
        if self.colSum[col] == winValue:
            self.winner = potentialWinner
            print(f"Player {self.winner} wins!")
            status = 1
        if row == col and self.diagSum[0] == winValue:
            self.winner = potentialWinner
            print(f"Player {self.winner} wins!")
            status = 1
        if row + col == 2 and self.diagSum[1] == winValue:
            self.winner = potentialWinner
            print(f"Player {self.winner} wins!")
            status = 1

        print(f"whosTurn: {self.whosTurn}\nwinValue: {winValue}\nstatus: {status}\n")
        return status
            
    def nextTurn(self):
        self.whosTurn *= -1
        
    def aiMove(self):
        """
        Choose a spot on the board for the AI player.
        
        :return: row, column chosen by AI
        :rtype: int, int
        """
        # Obtain list of available spots on self.board
        freeSpots = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    freeSpots.append((i, j))

        choice = random.choice(freeSpots)

        focusDirection, focusIndex = self.aiCheck()

        if focusDirection == "row":
            for i in freeSpots:
                if i[0] == focusIndex:
                    choice = i
        if focusDirection == "col":
            for i in freeSpots:
                if i[1] == focusIndex:
                    choice = i
        if focusDirection == "diag":
            if focusIndex == 0:
                for i in freeSpots:
                    if i[0] == i[1]:
                        choice = i
            if focusIndex == 1:
                for i in freeSpots:
                    if i[0] + i[1] == 2:
                        choice = i

        return choice[0], choice[1]

    def aiCheck(self):
        """
        Determine if a particular spot on the game board should be targeted by the AI's next move to win the game or defend from a loss.
        
        :return: focusDirection (row, column, or diagonal), focusIndex
        :rtype: String, int
        """
        # Define focus points of the self.board based on game condition
        focusIndexOffense = -1
        focusDirectionOffense = ""
        focusIndexDefense = -1
        focusDirectionDefense = ""

        for i in range(3):
            if self.rowSum[i] == 2:
                focusIndexDefense = i
                focusDirectionDefense = "row"
            if self.rowSum[i] == -2:
                focusIndexOffense = i
                focusDirectionOffense = "row"

        for i in range(3):
            if self.colSum[i] == -2:
                focusIndexOffense = i
                focusDirectionOffense = "col"
            if self.colSum[i] == 2:
                focusIndexDefense = i
                focusDirectionDefense = "col"

        for i in range(2):
            if self.diagSum[i] == -2:
                focusIndexOffense = i
                focusDirectionOffense = "diag"
            if self.diagSum[i] == 2:
                focusIndexDefense = i
                focusDirectionDefense = "diag"

        if focusDirectionOffense == "":
            focusDirection = focusDirectionDefense
        else:
            focusDirection = focusDirectionOffense

        if focusDirection == focusDirectionOffense:
            focusIndex = focusIndexOffense
        else:
            focusIndex = focusIndexDefense

        return focusDirection, focusIndex

    def cliPrintBoard(self):
        """
        Print current state of game board to output terminal.
        
        :return: None
        :rtype: None
        """
        print("\n\t|\t1\t|\t2\t|\t3\n--------------------------------------------------------\n", end="")
        for i in range(3):
            print(f"{chr(i+65)}", end="")
            for j in range(3):
                if self.board[i][j] == 0:
                    print("\t|\t", end="")
                elif self.board[i][j] == 1:
                    print("\t|\tX", end="")
                elif self.board[i][j] == -1:
                    print("\t|\tO", end="")
                else:
                    print("Board error (incorrect entry in self.board). Terminating...")
                    return ()
            print("\n--------------------------------------------------------")
        print()

    def cliSpotToIndex(self, spot):
        """
        Convert player choice for spot chosen into indeces to be used by the program.
        
        :param spot: Choice requested by player on game board location in the format of <LETTER><NUMBER> coinciding with row and column of the game board.
        :type spot: String
        :raises ValueError: ValueError
        :return: row and column indeces
        :rtype: int, int
        """
        # Validate spot
        try:
            # Check for valid number of characters
            if len(spot) != 2:
                raise ValueError("variable 'spot' must be 2 characters")

            row = ord(spot[0]) - 65
            col = int(spot[1]) - 1
        except ValueError as e:
            print(f"Error: {e}")
        return row, col

    def cliRun(self):
        """
        Run the CLI version of the game.
        
        :raises ValueError: ValueError
        :return: None
        :rtype: None
        """
        self.cliPrintBoard()

        while True:
            try:
                self.gameMode = int(
                    input("Choose game mode:\n\t[1] player vs AI\n\t[2] player vs player\n"))
                if self.gameMode != 1 and self.gameMode != 2:
                    raise ValueError()
                break
            except:
                print("Invalid choice. Select again.")

        while self.gameRunning:
            marker = self.getInput()

            if marker == 1:
                self.gameRunning = False
                self.cliPrintBoard()
                break
            if marker == 0:
                self.whosTurn = self.whosTurn * -1
                self.turnCounter = self.turnCounter + 1
                self.cliPrintBoard()
                if self.turnCounter == 9:
                    print("Tie! Game over!")
                    break
            if marker == -1:
                print("Try again.")


if __name__ == '__main__':
    game = TicTacToeGame()
    game.cliRun()
