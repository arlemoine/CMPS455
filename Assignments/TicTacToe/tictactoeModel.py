import random


class TicTacToe:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.rowSum = [0, 0, 0]
        self.colSum = [0, 0, 0]
        self.diagSum = [0, 0]
        self.gameRunning = True
        self.whosTurn = 1
        self.turnCounter = 0

    def printBoard(self):
        """
        Output: TicTacToe self.board to terminal output
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

    def spotToIndex(self, spot):
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

    def validateChoice(self, row, col):
        if self.whosTurn != 1 and self.whosTurn != -1:
            # Validate X (1) or O (-1) is used
            print("Invalid choice of X (1) or O (-1).")
            return -1
        elif row < 0 or row > 2 or col < 0 or col > 2:
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
                spot = input(1)
            row, col = self.spotToIndex(spot)
            validatedMove = self.validateChoice(row, col)
        return self.markSpot(row, col)

    def markSpot(self, row, col):
        self.board[row][col] = self.whosTurn
        # Increment sums related to victory conditions
        self.rowSum[row] += self.whosTurn
        self.colSum[col] += self.whosTurn
        if row == col:
            self.diagSum[0] += self.whosTurn
        if row + col == 2:
            self.diagSum[1] += self.whosTurn
        return self.checkForWinConditional(row, col)

    def checkForWinConditional(self, row, col):
        # Check for win conditions
        winValue = 3 if self.whosTurn == 1 else -3
        winner = "X" if winValue == 3 else "O"
        if self.rowSum[row] == winValue:
            print(f"Player {winner} wins!")
            return 1
        elif self.colSum[col] == winValue:
            print(f"Player {winner} wins!")
            return 1
        elif row == col and self.diagSum[0] == winValue:
            print(f"Player {winner} wins!")
            return 1
        elif row + col == 2 and self.diagSum[1] == winValue:
            print(f"Player {winner} wins!")
            return 1
        else:
            return 0

    def aiMove(self):
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

    def runCLI(self):
        self.printBoard()

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
                self.printBoard()
                break
            if marker == 0:
                self.whosTurn = self.whosTurn * -1
                self.turnCounter = self.turnCounter + 1
                print(self.turnCounter)
                self.printBoard()
                if self.turnCounter == 9:
                    print("Tie! Game over!")
                    break
            if marker == -1:
                print("Try again.")


if __name__ == '__main__':
    game = TicTacToe()
    game.runCLI()