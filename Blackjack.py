# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:00:39 2024

@author: Ardeshir
"""
#%%
import random
import math
from pandas import json_normalize

def print_verbose(*args, verbose=False, **kwargs):
        """Prints information only if verbose is True."""
        if verbose:
            print(*args, **kwargs)
            
             
class Card:
    """Represents a single playing card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a string representation of the card."""
        return f"{self.rank} of {self.suit}"

    def blackjack_value(self):
        """Returns the blackjack value of the card."""
        if self.rank in ("Jack", "Queen", "King"):
            return 10
        elif self.rank == "Ace":
            return 11
        else:
            return int(self.rank)


class Counter:
    def __init__(self):
        self.count = 0

    def update_count(self, card): # Hi-Lo Counting
        # Update count based on the card
        if card.rank in ['2', '3', '4', '5', '6']:
            self.count += 1
        elif card.rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.count -= 1

    def reset_count(self):
        self.count = 0
      
        
class Deck:
    """Represents a deck of playing cards."""

    SUITS = ["Spades", "Hearts", "Diamonds", "Clubs"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, num_decks=6): # Create a list of Card object to shape the required Deck
        self.cards = []
        for _ in range(num_decks):
            for suit in self.SUITS:
                for rank in self.RANKS:
                    self.cards.append(Card(suit, rank))
                    
        self.initial_total_deck_value = sum(card.blackjack_value() for card in self.cards)
        self.initial_total_deck_cards = len(self.cards)
        self.counter = Counter()

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals a card from the top of the deck."""
        if not self.cards:
            raise IndexError("Deck is empty")
        
        dealt_card = self.cards.pop() # Deal the last card from Deck
        
        # Keep the Count of dealt cards
        self.counter.update_count(dealt_card)
        return dealt_card

    def total_deck_value(self):
        """Returns the total blackjack value of all cards in the deck."""
        return sum(card.blackjack_value() for card in self.cards)
    

class Hand:
   """Represents a hand of playing cards."""

   def __init__(self):
       self.cards = []
       self.bet = 0  # Initialize bet to 0
       self.can_hit = True  # Flag for doubling down or any other situations
       self.is_double_down = False
       self.ace_split = False # The hand is a result Ace split
       self.is_soft = False # Indicates if it is a soft hand
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
        """Determines if the hand can be split, considering the specified rules."""
        if len(self.cards) != 2:
            return False  # Only hands with two cards can be split
       
        first_card_value = self.cards[0].blackjack_value()
        second_card_value = self.cards[1].blackjack_value()
       
        if first_card_value != second_card_value:
            return False  # Cards must have the same value
       
        return True

   def is_blackjack(self):
       """Returns True if the hand is a blackjack (Ace + 10-value card)."""
       return len(self.cards) == 2 and self.get_value() == 21

   def is_bust(self):
       """Returns True if the hand's value exceeds 21."""
       return self.get_value() > 21


class Player:
    """Represents a player in a blackjack game."""

    def __init__(self, name, budget, strategy):
        self.name = name
        self.budget = budget
        self.strategy = strategy
        self.hands = []  # List to hold multiple hands
        self.game = None  # Store the game reference
        self.initial_bet = None

    def place_bet(self):
        """Places a bet on specific hand based on the player's strategy."""
        bet_amount = self.strategy.determine_bet(self.game, self.budget)
        
        # Player has decided to play in this round
        if bet_amount:
            self.budget -= bet_amount
            self.initial_bet = bet_amount
    
    def make_decision(self, hand):
        """Makes a decision based on the player's strategy."""
        decision = self.strategy.decide(hand, self.game, self.budget) # Tuple ('hit', 'R3')
        return decision
    
    def double_down(self, hand):
        """Doubles the player's bet and draws one more card."""
        self.budget -= hand.bet
        hand.bet *= 2
        hand.add_card(self.game.deck.deal_card()) # get a card fron game's deck
        hand.can_hit = False  # Force the player to stand after doubling down
        hand.is_double_down = True
    
    def split_hand(self, hand):
        if hand.can_split() and len(self.hands) < 3 and not hand.ace_split:
            second_hand = Hand()
            second_hand.bet = hand.bet # place same bet as the first hand
            self.budget -= hand.bet
            
            # If the current split is about Aces
            if hand.cards[0].blackjack_value() == 11:
                hand.ace_split = True
                second_hand.ace_split = True
            
            # draw cards from deck
            second_hand.add_card(hand.cards.pop())
            second_hand.add_card(self.game.deck.deal_card())  # Add one more card to second hand
            self.hands.append(second_hand)  # Add the split hand to the list
            hand.add_card(self.game.deck.deal_card()) # Add one more card to first hand
            

    def win(self, amount):
        """Updates the player's budget after winning."""
        self.budget += amount

    def lose(self):
        """Updates the player's budget after losing."""
        pass # No need to adjust the budget as during betting the bet amount was already deducted. 

    def reset_hand(self):
        """Resets the player's hand for a new round."""
        self.hands = []
        self.initial_bet = None


class Dealer:
   """Represents the dealer in a blackjack game."""

   def __init__(self):
       self.hand = Hand()

   def deal_cards(self, players, deck):
       """Deals initial cards to players and the dealer."""
       for player in players:
           if player.initial_bet: # Player is playing in this round and has placed intial bet
               initial_hand = Hand() # Create the first hand
               initial_hand.bet = player.initial_bet
               initial_hand.add_card(deck.deal_card())
               initial_hand.add_card(deck.deal_card())
               player.hands.append(initial_hand) 

       self.hand.add_card(deck.deal_card())
       self.hand.add_card(deck.deal_card())  # One card hidden

   def play(self, deck):
       """Implements the dealer's fixed rules for drawing cards."""
       while self.hand.get_value() < 17:
           self.hand.add_card(deck.deal_card())
           print_verbose(f"Dealer hits and gets {self.hand.cards[-1]}")

   def reveal_hand(self):
       """Shows the dealer's complete hand."""
       print_verbose("\nDealer's hand:")
       print_verbose(*self.hand.cards, sep="\n")

   def reset_hand(self):
       """Resets the dealer's hand for a new round."""
       self.hand = Hand()


def round_info_decorator(start_game_func):
    def wrapper(self, *args, **kwargs):

        # Call the original start_game method
        start_game_func(self, *args, **kwargs)

        # Store information about the completed round
        round_info = {
            'round number': self.round_number,
            'players': [
                {
                    'name': player.name,
                    'budget': player.budget,
                    'hands': [
                        {
                            'cards': [str(card) for card in hand.cards],
                            'decisions': hand.decision_list,
                            'bet': hand.bet,
                            'cards value': hand.get_value(),
                            'is blackjack': hand.is_blackjack(),
                            'is double down': hand.is_double_down,
                            'is ace split': hand.ace_split,
                            'is bust': hand.is_bust(),
                            'result': hand.result
                        }
                        for hand in player.hands
                    ]
                }
                for player in self.players
            ],
            'dealer': {
                'cards': [str(card) for card in self.dealer.hand.cards],
                'value': self.dealer.hand.get_value(),
                'is_bust': self.dealer.hand.is_bust(),
            },
            
            'deck': {
                'cards_remaining': len(self.deck.cards),
                'cards_total_value': self.deck.total_deck_value(),
                'cards_running_count': self.deck.counter.count,
                'cards_true_count': math.floor(self.deck.counter.count/5),
            }      
        }

        self.round_info_list.append(round_info)
        for player in self.players:
            print_verbose(f"{player.name}'s remaining budget is {player.budget}")


    return wrapper



def decision_modifier_decorator(decide_func):
    def wrapper(self, player_hand, *args, **kwargs):

        # Call the original start_game method
        player_decision = decide_func(self, player_hand, *args, **kwargs)

        # Initialize the modified_decision with the original decision
        modified_decision = player_decision

        # Check the decision and modify it according to Blackjack Rules
        if player_decision == 'hit':
            if not player_hand.can_hit:
                modified_decision = 'stand'
                
        if player_decision == 'split': 
            if not player_hand.can_split():
                modified_decision = 'hit'  # You might want to modify this based on your rules
        
        return (modified_decision, self.decision_rule)
    
    return wrapper


class Game:
    """Represents a single game of blackjack."""
    def __init__(self, players, verbose=False):
        self.minimum_bet = 10
        self.deck = Deck()
        self.players = players
        self.dealer = Dealer()
        self.round_number = 0
        self.round_info_list = [] # accumulate the rounds information
        self.verbose = verbose # each round information gets printed
        self.game_over = False # If no one has any budget left
        
        # assign the current game object to each player object
        for player in self.players:
            player.game = self
           
    @round_info_decorator
    def start_game(self):
        """Starts a single game of blackjack."""
        
        self.round_number += 1
        
        # Reset hands for the next game
        for player in self.players:
            player.reset_hand()
        self.dealer.reset_hand()
        
        # Check the Decks status       
        if len(self.deck.cards) < random.uniform(0.7, 0.9) * self.deck.initial_total_deck_cards: # 70% or more decks remaining then reset Deck
            self.deck = Deck() # Renew the whole deck
            
        # Shuffle the deck
        self.deck.shuffle()

        # Place bets
        for player in self.players:
            if player.budget > self.minimum_bet:
                player.place_bet()
                
        # Deal initial cards
        self.dealer.deal_cards(self.players, self.deck)
                      
        # Check if all player has been lost their whole budget i.e. no hand was dealt to anyone
        if all([len(player.hands) == 0 for player in self.players]):
                self.game_over = True 
                
        # Show initial hands
        print_verbose("\nDealer's hand:")
        print_verbose(self.dealer.hand.cards[0])  # Show only one dealer card
        for player in self.players:
            for hand in player.hands:
                print_verbose(f"\n{player.name}'s hand:")
                print_verbose(*hand.cards, sep="\n")

        # Player turns
        for player in self.players:
            for hand in player.hands:  # Iterate through each hand
                # if the hand is a double down
                if not hand.can_hit:
                    continue
                
                # Check for blackjack
                if hand.is_blackjack():
                   print_verbose(f"\n{player.name} has blackjack!")
                   continue  # Move to the next player
                        
                while True:
                    decision_and_rule = player.make_decision(hand)
                    decision = decision_and_rule[0] # first argument of tuple
                    hand.decision_list.append(decision_and_rule) # add decision and strategy rule to the hand
                    
                    if decision == "hit":
                        hand.add_card(self.deck.deal_card())
                        print_verbose(f"\n{player.name} hits and gets {hand.cards[-1]}")
                        
                        # Unable the player to hit more than one card on Ace splits
                        if hand.ace_split:
                            hand.can_hit = False
                        
                        if hand.is_bust():
                            hand.can_hit = False
                            print_verbose(f"\n{player.name} busts!")
                            break
                        
                    elif decision == "stand":
                        print_verbose(f"\n{player.name} stands.")
                        break
                    
                    elif decision == "double down":
                        print_verbose(f"\n{player.name} double down and gets {hand.cards[-1]}.")
                        player.double_down(hand)
                        break
                    
                    elif decision=="split":
                        print_verbose(f"\n{player.name} split hand of {hand.cards[-1]}")
                        player.split_hand(hand)
                        break
                    
                    else:
                        raise ValueError("Invalid decision")

        # Dealer's turn
        self.dealer.reveal_hand()
        self.dealer.play(self.deck)
        if self.dealer.hand.is_bust():
            print_verbose("Dealer busts!")

        # Determine winners
        for player in self.players:
            for hand in player.hands:  # Iterate through each hand
                if not hand.is_bust():
                    # Payout for Blackjack
                    if hand.is_blackjack():
                        hand.result = 'win'
                        player.win(hand.bet * 2.5)
                        print_verbose(f"\n{player.name} wins by Blackjack!")
                    elif self.dealer.hand.is_bust() or hand.get_value() > self.dealer.hand.get_value():
                        hand.result = 'win'
                        player.win(hand.bet * 2) # Double down hand's bet were updated before
                        print_verbose(f"\n{player.name} wins!")
                    elif hand.get_value() == self.dealer.hand.get_value():
                        hand.result = 'push'
                        player.win(hand.bet)  # Push (applies to both regular and double down)
                        print_verbose(f"\n{player.name} pushes.")
                    else: # dealer's hand has higher value
                        hand.result = 'lose'
                        player.lose()
                        print_verbose(f"\n{player.name} loses.")      
                else: # hand is bust
                    hand.result = 'lose'
                    player.lose()
                    
    def run_simulation(self, num_games):
            for _ in range(num_games):
                if self.game_over:
                    break
                self.start_game()
                
            return self.summarize_round_info_list()


    def summarize_round_info_list(self):
      """ Summarizes the final results of a list of round information dictionaries. """
    
      player_summaries = {}
    
      for round_info in self.round_info_list:
        for player in round_info["players"]:
          player_name = player["name"]
          if player_name not in player_summaries:
            player_summaries[player_name] = {
              "wins": 0,
              "losses": 0,
              "pushes": 0,
              # "budget_history": [],
            }
            
          # player_summaries[player_name]["budget_history"].append(player["budget"])
          
          for hand in player["hands"]:
            if hand["result"] == "win":
              player_summaries[player_name]["wins"] += 1
            elif hand["result"] == "lose":
              player_summaries[player_name]["losses"] += 1
            elif hand["result"] == "push":
              player_summaries[player_name]["pushes"] += 1
    
      return player_summaries                
        
    def export_game(self):
        # Plater, Convert round_info_list to a DataFrame
        df_player = json_normalize(self.round_info_list, ['players', 'hands'], max_level=3, 
                                   meta=['round number', ['players', 'name'], 
                                         ['players', 'budget']])
        
        # Dealer, Convert round_info_list to a DataFrame
        df_dealer_and_cards = json_normalize(self.round_info_list)
        df_dealer_and_cards.drop(['players'], axis=1, inplace=True)
        
        # Join the two daraframes
        df = df_player.merge(df_dealer_and_cards, on='round number', how='left')
        df = df.rename(columns=lambda x: x.split('.')[-1])  # Remove prefix from column names
        
        df.plot.line(x='round number', y='budget')
        
        # Specify the Excel file path
        excel_file_path = 'round_info.xlsx'
        
        # Write the DataFrame to an Excel file
        df.to_excel(excel_file_path, index=False)        

                
class BasicStrategy:
    """Implements a basic blackjack strategy.
        Use self.decision_rule for any return, so that it's possible to trace the rules. 
    """
    def __init__(self, with_card_counting=False, accuracy=1.0):
       self.decision_rule = None # Keep decision_rule to analyze later
        
    def determine_bet(self, game, budget):
        """Returns a bet amount or None which means that player is not playing in this round."""
        # Calculate % of the budget
        risk_amount = budget * 0.05
        
        # Round up to the nearest multiple of 5
        bet_amount = math.ceil(risk_amount / 10) * 10
        if bet_amount >= game.minimum_bet:
            return int(bet_amount)
        
    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        """Decides based on basic strategy rules."""   
        print(math.floor(game.deck.counter.count/5.0))
        player_hand_value = player_hand.get_value()
        dealer_card_value = game.dealer.hand.cards[0].blackjack_value()
           
        # Double down 
        if player_hand_value == 9 and dealer_card_value >= 3 and dealer_card_value <= 6 and budget >= player_hand.bet:
            self.decision_rule = 'R1'
            return "double down"
        elif player_hand_value <= 11:
            self.decision_rule = 'R2'
            return "hit"  # Always hit on 11 or less
        elif player_hand_value >= 17:
            self.decision_rule = 'R3'
            return "stand"  # Always stand on 17 or more
        elif player_hand_value == 12:
            if dealer_card_value >= 4 and dealer_card_value <= 6:
                self.decision_rule = 'R4'
                return "stand"
            else:
                self.decision_rule = 'R5'
                return "hit"
        # Split
        elif player_hand.can_split() and budget >= player_hand.bet:
            if (
                player_hand.cards[0].rank == "Ace" or  # Always split aces
                player_hand.cards[0].blackjack_value() in [8, 9]  # Split 8s and 9s against any dealer card
            ):
                self.decision_rule = 'R6'
                return "split"
            elif dealer_card_value in (2, 3, 7, 8, 9, 10):  # Don't split against strong dealer cards
                self.decision_rule = 'R7'
                return "stand"
            else:  # Split other pairs based on dealer card
                self.decision_rule = 'R8'
                return "split"
            
        # ... (more rules for other hand values and dealer cards)
        # Default to stand for remaining cases
        self.decision_rule = 'R9'
        return "stand"

class NewStartegy_1(BasicStrategy):

    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        """Decides based on basic strategy rules."""   
        
        player_hand_value = player_hand.get_value()
        dealer_card_value = game.dealer.hand.cards[0].blackjack_value()
           
        # Double down 
        if player_hand_value == 9 and dealer_card_value >= 3 and dealer_card_value <= 6 and budget >= player_hand.bet:
            self.decision_rule = 'R1'
            return "double down"
        elif player_hand_value <= 11:
            self.decision_rule = 'R2'
            return "hit"  # Always hit on 11 or less
        elif player_hand_value >= 17:
            self.decision_rule = 'R3'
            return "stand"  # Always stand on 17 or more
        elif player_hand_value == 12:
            self.decision_rule = 'R4'
            return "stand"

        # Split
        elif player_hand.can_split() and budget >= player_hand.bet:
            if (
                player_hand.cards[0].rank == "Ace" or  # Always split aces
                player_hand.cards[0].blackjack_value() in [8, 9]  # Split 8s and 9s against any dealer card
            ):
                self.decision_rule = 'R6'
                return "split"
            elif dealer_card_value in (2, 3, 7, 8, 9, 10):  # Don't split against strong dealer cards
                self.decision_rule = 'R7'
                return "stand"
            else:  # Split other pairs based on dealer card
                self.decision_rule = 'R8'
                return "split"
            
        # ... (more rules for other hand values and dealer cards)
        # Default to stand for remaining cases
        self.decision_rule = 'R9'
        return "stand"
    
#%%

# Create a player with a budget of $100 and using the basic strategy
ardeshir = Player(name="Ardeshir", budget=300, strategy=BasicStrategy())
# parisa = Player(name="Parisa", budget=100, strategy=BasicStrategy())

# Create a game with the player
game = Game(players=[ardeshir])

# Start simulation of the game
result = game.run_simulation(200)

game.export_game()


#%%

# Check if you can double down after split
