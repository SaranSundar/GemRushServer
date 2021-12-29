from enum import Enum


class Tier(str, Enum):
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    BLUE = 'BLUE'

    def __str__(self):
        return self.name
