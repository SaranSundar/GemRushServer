from enum import Enum


class CardColor(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'

    def __str__(self):
        return self.value
