from dataclasses import dataclass

from enum import Enum

from serde import serialize, deserialize


@deserialize
@serialize
@dataclass
class TokenColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
    GOLD = 'gold'

@deserialize
@serialize
@dataclass
class CardColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
