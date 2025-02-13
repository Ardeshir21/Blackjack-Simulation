import math

def round_info_decorator(start_game_func):
    def wrapper(self, *args, **kwargs):
        start_game_func(self, *args, **kwargs)
        
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
        
    return wrapper

def decision_modifier_decorator(decide_func):
    def wrapper(self, player_hand, *args, **kwargs):
        decision = decide_func(self, player_hand, *args, **kwargs)
        rule = f"Strategy: {self.name}"
        return (decision, rule)
    return wrapper 