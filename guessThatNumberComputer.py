import random

print("Come up with a number for me to guess!")

userNumber = int(input())
foundTheAnswer = False

print("What is the range I should use to guess?")
lo = int(input("From the number "))
hi = int(input("To the number "))

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
    print("[0] Lower... [1] Higher... [2] That's it!")
    response = int(input("\t"))
    
    if response != correctDirection:
        print("You cheated! I'm done!")
        exit()

print("Yes! That was fun! Take care!")
