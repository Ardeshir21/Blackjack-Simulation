from .hand import Hand

class Dealer:
    """Represents the dealer in the game."""
    
    def __init__(self):
        self.hand = Hand()
        
    def deal_cards(self, players, deck):
        """Deals initial cards to all players and dealer."""
        for player in players:
            if player.initial_bet:
                initial_hand = Hand()
                initial_hand.bet = player.initial_bet
                initial_hand.add_card(deck.deal_card())
                initial_hand.add_card(deck.deal_card())
                player.hands.append(initial_hand)
                
        self.hand.add_card(deck.deal_card())
        self.hand.add_card(deck.deal_card())
        
    def play(self, deck):
        """Plays the dealer's hand according to casino rules."""
        while self.hand.get_value() < 17:
            self.hand.add_card(deck.deal_card())
            
    def reset_hand(self):
        """Resets the dealer's hand."""
        self.hand = Hand() 