from .base_strategy import BaseStrategy
from src.utils.decorators import decision_modifier_decorator

class AggressiveStrategy(BaseStrategy):
    """Aggressive betting and playing strategy."""
    
    def __init__(self):
        super().__init__()
        self.name = "Aggressive Strategy"
        self.description = "High-risk high-reward strategy with progressive betting"
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        
    def determine_bet(self, game, budget):
        """Progressive betting system."""
        base_bet = game.minimum_bet
        if self.consecutive_wins > 0:
            return min(base_bet * (2 ** self.consecutive_wins), budget * 0.25)
        return base_bet
        
    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        """Aggressive playing decisions."""
        player_value = player_hand.get_value()
        dealer_up_card = game.dealer.hand.cards[0].blackjack_value()
        
        # Track the reason for the decision
        reason = ""
        decision = None
        
        # Only split if we have fewer than 4 hands total and it makes strategic sense
        if player_hand.can_split() and budget >= player_hand.bet and len(game.players[0].hands) < 4:
            card_value = player_hand.cards[0].blackjack_value()
            if card_value in [8, 11]:  # Only split Aces and 8s
                decision = "split"
                reason = f"Splitting pair of {player_hand.cards[0].rank}s (Aggressive strategy splits Aces and 8s)"
            elif card_value <= 7:  # Maybe split low cards against dealer's weak cards
                if dealer_up_card <= 6:
                    decision = "split"
                    reason = f"Splitting pair of {player_hand.cards[0].rank}s against dealer's weak card"
        
        # If we haven't decided to split, make hitting/standing decision
        if not decision:
            if player_value <= 16:
                decision = "hit"
                reason = f"Hitting on {player_value} (Aggressive strategy hits on 16 or lower)"
            elif player_value == 17 and player_hand.is_soft:
                decision = "hit"
                reason = "Hitting on soft 17 (Aggressive strategy)"
            else:
                decision = "stand"
                reason = f"Standing on {player_value}"
        
        if game.verbose:
            print(f"Strategy reasoning: {reason}")
            
        return decision 