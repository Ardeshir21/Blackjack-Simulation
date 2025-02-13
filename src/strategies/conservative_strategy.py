from .base_strategy import BaseStrategy
from src.utils.decorators import decision_modifier_decorator

class ConservativeStrategy(BaseStrategy):
    """Very conservative strategy focusing on capital preservation."""
    
    def __init__(self):
        super().__init__()
        self.name = "Conservative Strategy"
        self.description = "Risk-averse strategy focusing on capital preservation"
        
    def determine_bet(self, game, budget):
        """Minimal betting approach."""
        if budget < game.minimum_bet * 20:  # Stop if low on funds
            return None
        return game.minimum_bet
        
    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        """Conservative playing decisions."""
        player_value = player_hand.get_value()
        dealer_up_card = game.dealer.hand.cards[0].blackjack_value()
        
        # Never split
        if player_value >= 12:
            return "stand"
        return "hit" 