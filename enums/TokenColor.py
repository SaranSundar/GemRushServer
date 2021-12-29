from enum import Enum


class TokenColor(str, Enum):
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    WHITE = 'WHITE'
    BLACK = 'BLACK'
    GOLD = 'GOLD'

    def __str__(self):
        return self.name
