import random

computersNumber = random.randint(1,100)
foundTheAnswer = False
print("I'm thinking of a number between 1 and 100.")

while foundTheAnswer is False:
    print("Take a guess...")
    userGuess = int(input())
    if userGuess > computersNumber:
        print("Lower...")
    elif userGuess < computersNumber:
        print("Higher...")
    elif userGuess == computersNumber:
        print("That's it!")
        foundTheAnswer = True

