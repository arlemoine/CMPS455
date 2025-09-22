board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
rowSum = [0, 0, 0]
colSum = [0, 0, 0]
diagSum = [0, 0]

def printBoard():
    """
    Output: TicTacToe board to terminal output
    """
    print(f"\n\t|\t1\t|\t2\t|\t3\n----------------------------\n", end="")
    for i in range(3):
        print(f"{chr(i+65)}", end="")
        for j in range(3):
            if board[i][j] == 0:
                print(f"\t|\t", end="")
            elif board[i][j] == 1:
                print(f"\t|\tX", end="")
            elif board[i][j] == -1:
                print(f"\t|\tO", end="")
            else:
                print("Board error (incorrect entry in board). Terminating...")
                return()
        print(f"\n----------------------------")
    print()
    
def markSpot(spot, choiceStr):
    """
    Input: spot (2 char string with {A,B,C}{1,2,3}), choice (expects 1 or -1)
    Output: -1 if error present
    """
    # Validate choice
    choice = int(choiceStr)
    if choice != 1 and choice != -1:
        print("Invalid choice of X (1) or O (-1)")
        return -1
    
    # Obtain row and column indeces
    row, col = spotToIndex(spot)

    # Assign choice to spot if not taken
    if board[row][col] == 0:
        board[row][col] = choice
        printBoard()
        
        # Increment sums related to victory conditions
        rowSum[row] += choice
        colSum[col] += choice
        if row == col:
            diagSum[0] += choice
        if row + col == 2:
            diagSum[1] += choice
            
        # Check for win conditions
        winValue = 3 if choice == 1 else -3
        winner = "X" if winValue == 3 else "O"
        
        if rowSum[row] == winValue:
            print(f"Player {winner} wins!")
            return 1

        if rowSum[col] == winValue:
            print(f"Player {winner} wins!")
            return 1
        
        if row == col and diagSum[0] == winValue:
            print(f"Player {winner} wins!")
            return 1
        
        if row + col == 2 and diagSum[1] == winValue:
            print(f"Player {winner} wins!")
            return 1
        
        return 0
    else:
        print("That spot is already taken.")
        return -1
        
def spotToIndex(spot):
    # Validate spot
    try:
        # Check for valid number of characters
        if len(spot) != 2:
            raise ValueError("variable 'spot' must be 2 characters")
            
        row = ord(spot[0]) - 65
        col = int(spot[1]) - 1
        
        # Check for valid index
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise ValueError("variable 'spot' has invalid entry")
    except ValueError as e:
        print(f"Error occurred: {e}")
        return -1
    
    return row, col
                
def getInput(player):
    if player == 1:
        return input(f"Player 1, make your move: ")
    else:
        return input(f"Player 2, make your move: ")
    
def aiMove():
    freeSpots = []
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                freeSpots.append((i, j))
    
    randomChoice = random.choice(freeSpots)

    # TESTING            
    print(f"freeSpots = {freeSpots}")
    print(f"randomChoice = {randomChoice}")
    

def main():
    gameRunning = True
    whosTurn = 1
    turnCounter = 0
    while gameRunning:
        printBoard()
        marker = markSpot(getInput(whosTurn), whosTurn)
        
        if marker == 1:
            gameRunning = False
            break
        if marker == 0:
            whosTurn = whosTurn * -1
            turnCounter = turnCounter + 1
        if marker == -1:
            print("Try again.")
        if turnCounter == 9:
            print("Tie! Game over!")
            break
        aiMove()

main()