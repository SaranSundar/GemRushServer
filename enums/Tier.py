from enum import Enum


class Tier(str, Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    def __str__(self):
        return self.value
