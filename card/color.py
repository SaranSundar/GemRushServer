from marshmallow_dataclass import dataclass as mmdc

# TODO: This was an enum, currently not being used


@mmdc
class TokenColor:
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
    GOLD = 'gold'


@mmdc
class CardColor:
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'
    BLACK = 'black'
