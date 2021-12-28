from dataclasses import dataclass

from enum import Enum


@dataclass
class TokenColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
    GOLD = 'gold'

    def __hash__(self):
        return hash(str(self.RED)) ^ hash(str(self.GREEN)) ^ hash(str(self.BLUE)) ^ hash(str(self.WHITE)) ^ hash(str(self.BLACK)) ^ hash(
            str(self.GOLD))


@dataclass
class CardColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
