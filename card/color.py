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


@dataclass
class CardColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
