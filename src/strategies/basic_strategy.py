import math
from .base_strategy import BaseStrategy
from ..utils.decorators import decision_modifier_decorator

class BasicStrategy(BaseStrategy):
    """Conservative basic strategy following standard blackjack rules."""
    
    def __init__(self):
        super().__init__()
        self.name = "Basic Strategy"
        self.description = "Conservative strategy following standard blackjack rules"
        
    def determine_bet(self, game, budget):
        """Consistent minimum betting."""
        return game.minimum_bet
        
    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        """Standard basic strategy decisions."""
        player_value = player_hand.get_value()
        dealer_up_card = game.dealer.hand.cards[0].blackjack_value()
        
        if player_hand.can_split() and budget >= player_hand.bet:
            if player_hand.cards[0].blackjack_value() in [8, 11]:  # Split 8s and Aces
                return "split"
                
        if player_hand.is_soft:  # Hand with Ace counted as 11
            if player_value <= 17:
                return "hit"
            return "stand"
            
        if player_value <= 11:
            return "hit"
        elif player_value == 12:
            return "stand" if dealer_up_card in [4,5,6] else "hit"
        elif 13 <= player_value <= 16:
            return "stand" if dealer_up_card <= 6 else "hit"
        return "stand" 