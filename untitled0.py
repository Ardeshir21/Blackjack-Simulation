# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:43:19 2024

@author: User
"""

import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = [Card(rank, suit) for _ in range(num_decks) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.cards)
        self.cards_left = len(self.cards)

    def draw_card(self):
        card = self.cards.pop()
        self.cards_left -= 1
        return card

class Player:
    def __init__(self, name, budget):
        self.name = name
        self.hand = []
        self.budget = budget
        self.bet = 0

    def receive_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def calculate_hand_value(self):
        values = [10 if card.rank in ['J', 'Q', 'K'] else int(card.rank) if card.rank.isdigit() else 11 for card in self.hand]
        num_aces = sum(1 for card in self.hand if card.rank == 'A')

        while num_aces > 0 and sum(values) > 21:
            values[values.index(11)] = 1
            num_aces -= 1

        return sum(values)

class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer', 0)

    def draw_additional_card(self, deck):
        while self.calculate_hand_value() < 17:
            self.receive_card(deck.draw_card())

class BlackjackGame:
    def __init__(self, num_players=1, initial_budget=1000):
        self.deck = Deck()
        self.players = [Player('You', initial_budget)] + [Player(f'Dummy Player {i+1}', 1000) for i in range(num_players-1)]
        self.dealer = Dealer()
        self.threshold_to_restart = self.deck.num_decks * 26

    def deal_initial_cards(self):
        for _ in range(2):
            for player in [self.dealer] + self.players:
                player.receive_card(self.deck.draw_card())

    def calculate_winner(self):
        dealer_score = self.dealer.calculate_hand_value()

        for player in self.players:
            player_score = player.calculate_hand_value()

            if player_score > 21 or (dealer_score <= 21 and dealer_score >= player_score):
                player.budget -= player.bet
            else:
                player.budget += player.bet * 2  # Player wins

            player.clear_hand()

    def run(self):
        while self.deck.cards_left > self.threshold_to_restart:
            self.deal_initial_cards()

            for player in self.players:
                # For simplicity, let's assume each player bets 10 units
                player.bet = 10

                while player.calculate_hand_value() < 21:
                    player.receive_card(self.deck.draw_card())

            self.dealer.draw_additional_card(self.deck)
            self.calculate_winner()

        print("Game over. Final budgets:")
        for player in self.players:
            print(f"{player.name}: {player.budget}")

# Example usage:
num_dummy_players = 2  # You can change the number of dummy players as needed
game = BlackjackGame(num_players=num_dummy_players + 1)  # +1 for the user
game.run()
