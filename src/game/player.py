from src.utils.decorators import round_info_decorator
from src.game.hand import Hand

class Player:
    """Represents a player in the game."""
    
    def __init__(self, name, budget, strategy):
        self.name = name
        self.budget = budget
        self.strategy = strategy
        self.hands = []
        self.game = None
        self.initial_bet = None
        
    def place_bet(self):
        """Places initial bet for the round."""
        bet_amount = self.strategy.determine_bet(self.game, self.budget)
        if bet_amount:
            self.budget -= bet_amount
            self.initial_bet = bet_amount
            
    def make_decision(self, hand):
        """Makes a decision for the current hand."""
        return self.strategy.decide(hand, self.game, self.budget)
        
    def double_down(self, hand):
        """Executes a double down action."""
        self.budget -= hand.bet
        hand.bet *= 2
        hand.add_card(self.game.deck.deal_card())
        hand.can_hit = False
        hand.is_double_down = True
        
    def split_hand(self, hand):
        """Splits a pair into two hands."""
        if hand.can_split() and len(self.hands) < 3 and not hand.ace_split:
            second_hand = Hand()
            second_hand.bet = hand.bet
            self.budget -= hand.bet
            
            if hand.cards[0].blackjack_value() == 11:
                hand.ace_split = True
                second_hand.ace_split = True
                
            second_hand.add_card(hand.cards.pop())
            second_hand.add_card(self.game.deck.deal_card())
            self.hands.append(second_hand)
            hand.add_card(self.game.deck.deal_card())
            
    def win(self, amount):
        """Updates budget after winning."""
        self.budget += amount
        
    def lose(self):
        """Updates budget after losing."""
        pass
        
    def reset_hand(self):
        """Resets player's hands for new round."""
        self.hands = []
        self.initial_bet = None 