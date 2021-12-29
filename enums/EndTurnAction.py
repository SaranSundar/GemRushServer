from enum import Enum


class EndTurnAction(str, Enum):
    # Any action can get a noble if player chooses to at that turn
    BuyingCard = 1
    BuyingGoldToken = 3
    Buying3DifferentTokens = 4
    Buying2SameTokens = 5
    BuyingAndReturningTokens = 6
    BuyingLimitedTokens = 7

    def __str__(self):
        return self.value
