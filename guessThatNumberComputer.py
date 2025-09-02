import random

foundTheAnswer = False

def requestInput(message):
    waiting = True
    while waiting:
        print(message)
        try:
            userInput = int(input("\t"))
            waiting = False
        except:
            print("That's not valid. Try again.")
    return userInput

userNumber = requestInput("Come up with a number for me to guess!")

print("What is the range I should use to guess?")
lo = requestInput("From the number")
hi = requestInput("To the number")

if userNumber < lo or userNumber > hi:
    print("You cheated! I'm done!")
    exit()

while foundTheAnswer == False:
    computerGuess = random.randint(lo, hi)

    if computerGuess > userNumber:
        correctDirection = 0
        hi = computerGuess
    elif computerGuess < userNumber:
        correctDirection = 1
        lo = computerGuess
    elif computerGuess == userNumber:
        correctDirection = 2
        foundTheAnswer = True

    print(f"Is your number {computerGuess}?")
    response = requestInput("[0] Lower... [1] Higher... [2] That's it!")
    
    if response != correctDirection:
        print("You cheated! I'm done!")
        exit()

print("Yes! That was fun! Take care!")
