from enum import IntEnum


class EndTurnAction(IntEnum):
    # Any action can get a noble if player chooses to at that turn
    BuyingCard = 1
    BuyingGoldToken = 2
    Buying3DifferentTokens = 3
    Buying2SameTokens = 4
    # When you can only buy 1 or 2 tokens cause you have 8 or 9
    BuyingLimitedTokens = 5

    def __str__(self):
        return self.name
