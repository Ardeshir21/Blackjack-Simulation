class Hand:
    """Represents a hand of playing cards."""

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.can_hit = True
        self.is_double_down = False
        self.ace_split = False
        self.is_soft = False
        self.result = None
        self.decision_list = []
        
    def __str__(self):
        """Returns a string representation of the hand."""
        hand_str = f"\nCards in hand:\n{', '.join(map(str, self.cards))}\n"
        hand_str += f"Total value: {self.get_value()}\n"
        hand_str += f"Current bet: {self.bet}\n"
        return hand_str

    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def get_value(self):
        """Calculates the hand's value, considering aces."""
        total = 0
        num_aces = 0
        for card in self.cards:
            card_value = card.blackjack_value()
            total += card_value
            if card_value == 11:  # Ace
                num_aces += 1

        while total > 21 and num_aces > 0:
            total -= 10  # Change ace value to 1
            num_aces -= 1
    
        # Check if the hand is considered soft
        if num_aces > 0 and total <= 11:
            self.is_soft = True
        else:
            self.is_soft = False

        return total
   
    def can_split(self):
        """Determines if the hand can be split."""
        if len(self.cards) != 2:
            return False
       
        first_card_value = self.cards[0].blackjack_value()
        second_card_value = self.cards[1].blackjack_value()
       
        return first_card_value == second_card_value

    def is_blackjack(self):
        """Returns True if the hand is a blackjack."""
        return len(self.cards) == 2 and self.get_value() == 21

    def is_bust(self):
        """Returns True if the hand's value exceeds 21."""
        return self.get_value() > 21 