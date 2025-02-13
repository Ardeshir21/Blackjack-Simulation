import random
from .card import Card

class Counter:
    """Keeps track of card counting metrics."""
    def __init__(self):
        self.count = 0
        
    def update(self, card):
        """Updates running count based on card value."""
        value = card.blackjack_value()
        if value >= 10:
            self.count -= 1
        elif value <= 6:
            self.count += 1

class Deck:
    """Represents a deck of playing cards."""
    
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.counter = Counter()
        self.reset()
        
    def reset(self):
        """Resets the deck to its initial state."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        
        self.cards = []
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
        
        self.shuffle()
        self.counter.count = 0
        
    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)
        
    def deal_card(self):
        """Deals one card from the deck."""
        if not self.cards:
            self.reset()
        
        card = self.cards.pop()
        self.counter.update(card)
        return card
        
    def total_deck_value(self):
        """Returns total value of remaining cards."""
        return sum(card.blackjack_value() for card in self.cards) 