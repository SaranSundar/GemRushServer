from enum import Enum


class CardColor(str, Enum):
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    WHITE = 'WHITE'
    BLACK = 'BLACK'

    def __str__(self):
        return self.name
