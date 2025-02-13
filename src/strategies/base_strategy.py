from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """Abstract base class for all betting strategies."""
    
    def __init__(self):
        self.decision_rule = None
        
    @abstractmethod
    def determine_bet(self, game, budget):
        """Determines the bet amount for the next hand."""
        pass
        
    @abstractmethod
    def decide(self, player_hand, game, budget):
        """Makes a decision for the current hand."""
        pass

    def explain_decision(self, decision, player_hand, dealer_up_card):
        """Explains the reasoning behind a decision."""
        return f"Made decision '{decision}' with hand value {player_hand.get_value()} against dealer's {dealer_up_card}" 