import random

computersNumber = random.randint(1,100)
foundTheAnswer = False
print("I'm thinking of a number between 1 and 100.")

while foundTheAnswer is False:
    print("Take a guess...")
    try:
        userGuess = int(input())
    except:
        print("That's not a valid choice. Try again.")
        continue
    
    if userGuess < 1 or userGuess > 100:
        print("I said between 1 and 100, try again.")
    elif userGuess > computersNumber:
        print("Lower...")
    elif userGuess < computersNumber:
        print("Higher...")
    elif userGuess == computersNumber:
        print("That's it!")
        foundTheAnswer = True

