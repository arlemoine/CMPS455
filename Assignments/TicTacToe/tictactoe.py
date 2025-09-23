import random

board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
rowSum = [0, 0, 0]
colSum = [0, 0, 0]
diagSum = [0, 0]

def printBoard():
    """
    Output: TicTacToe board to terminal output
    """
    print("\n\t|\t1\t|\t2\t|\t3\n--------------------------------------------------------\n", end="")
    for i in range(3):
        print(f"{chr(i+65)}", end="")
        for j in range(3):
            if board[i][j] == 0:
                print("\t|\t", end="")
            elif board[i][j] == 1:
                print("\t|\tX", end="")
            elif board[i][j] == -1:
                print("\t|\tO", end="")
            else:
                print("Board error (incorrect entry in board). Terminating...")
                return()
        print("\n--------------------------------------------------------")
    print()
    
def validateChoice(row, col, whosTurn):
    if whosTurn != 1 and whosTurn != -1:
        # Validate X (1) or O (-1) is used
        print("Invalid choice of X (1) or O (-1).")
        return -1
    elif row < 0 or row > 2 or col < 0 or col > 2:
    # Get row and column indeces and validate
        print("Invalid spot entered.")
        return -1
    elif board[row][col] != 0:
        # Validate spot is available
        print("Spot already taken.")
        return -1
    else: 
        return 1
    
def markSpot(whosTurn, gameMode):
    validatedMove = -1
    
    if gameMode == 1:
        if whosTurn == -1:
            row, col = aiMove()
            validatedMove = 1
    
    while validatedMove != 1:
        spot = getInput(whosTurn)
        row, col = spotToIndex(spot)
        validatedMove = validateChoice(row, col, whosTurn)     

    board[row][col] = whosTurn
        
    # Increment sums related to victory conditions
    rowSum[row] += whosTurn
    colSum[col] += whosTurn
    if row == col:
        diagSum[0] += whosTurn
    if row + col == 2:
        diagSum[1] += whosTurn
            
    # Check for win conditions
    winValue = 3 if whosTurn == 1 else -3
    winner = "X" if winValue == 3 else "O"
    
    if rowSum[row] == winValue:
        print(f"Player {winner} wins!")
        return 1
    elif colSum[col] == winValue:
        print(f"Player {winner} wins!")
        return 1
    elif row == col and diagSum[0] == winValue:
        print(f"Player {winner} wins!")
        return 1
    elif row + col == 2 and diagSum[1] == winValue:
        print(f"Player {winner} wins!")
        return 1
    else:
        return 0
        
def spotToIndex(spot):
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
                
def getInput(player):
    if player == 1:
        print("Player 1, make your move: ")
        return input()
    else:
        print("Player 2, make your move: ")
        return input()
    
def aiMove():
    # Obtain list of available spots on board
    freeSpots = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                freeSpots.append((i, j))       
    
    choice = random.choice(freeSpots)

    focusDirection, focusIndex = aiCheck()
    
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

def aiCheck():
    # Define focus points of the board based on game condition
    focusIndexOffense = -1
    focusDirectionOffense = ""
    focusIndexDefense = -1
    focusDirectionDefense = ""
    
    for i in range(3):
        if rowSum[i] == 2:
            focusIndexDefense = i
            focusDirectionDefense = "row"                
        if rowSum[i] == -2:
            focusIndexOffense = i
            focusDirectionOffense = "row"
    
    for i in range(3):
        if colSum[i] == -2:
            focusIndexOffense = i
            focusDirectionOffense = "col"
        if colSum[i] == 2:
            focusIndexDefense = i
            focusDirectionDefense = "col"
            
    for i in range(2):
        if diagSum[i] == -2:
            focusIndexOffense = i
            focusDirectionOffense = "diag"
        if diagSum[i] == 2:
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

def main():
    gameRunning = True
    whosTurn = 1
    turnCounter = 0
    printBoard()
    
    while True:
        try:
            gameMode = int(input("Choose game mode:\n\t[1] player vs AI\n\t[2] player vs player\n"))
            if gameMode != 1 and gameMode != 2:
                raise ValueError()
            break
        except:
            print("Invalid choice. Select again.")
    
    while gameRunning:
        marker = markSpot(whosTurn, gameMode)
        
        if marker == 1:
            gameRunning = False
            printBoard()
            break
        if marker == 0:
            whosTurn = whosTurn * -1
            turnCounter = turnCounter + 1
            printBoard()
        if marker == -1:
            print("Try again.")
        if turnCounter == 9:
            print("Tie! Game over!")
            printBoard()
            break

main()
