from .base_strategy import BaseStrategy
from ..utils.decorators import decision_modifier_decorator

class CardCountingStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        
    def determine_bet(self, game, budget):
        true_count = game.deck.counter.count / 5  # Approximate decks remaining
        if true_count > 2:
            return min(budget * 0.1, game.minimum_bet * 2)
        return game.minimum_bet 