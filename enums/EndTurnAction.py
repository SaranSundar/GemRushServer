from enum import Enum


class EndTurnAction(str, Enum):
    # Any action can get a noble if player chooses to at that turn
    BuyingCard = 'BuyingCard'
    BuyingGoldToken = 'BuyingGoldToken'
    Buying3DifferentTokens = 'Buying3DifferentTokens'
    Buying2SameTokens = 'Buying2SameTokens'
    # When you can only buy 1 or 2 tokens because you have 8 or 9
    BuyingLimitedTokens = 'BuyingLimitedTokens'

    def __str__(self):
        return self.name
