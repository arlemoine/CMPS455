import random

class PlayerType:
    HUMAN = 1
    AI = 2


class Player:
    def __init__(self, name: str, playerType: PlayerType = PlayerType.HUMAN):
        self.name = name
        self.type = playerType


if __name__ == '__main__':
    player1 = Player("Johnny", PlayerType.AI)
    
    print(player1.type)
