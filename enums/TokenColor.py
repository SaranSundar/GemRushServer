from enum import Enum


class TokenColor(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
    GOLD = 'gold'

    def __str__(self):
        return self.value
