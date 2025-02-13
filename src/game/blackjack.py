from .deck import Deck
from .player import Player
from .dealer import Dealer
from ..utils.decorators import round_info_decorator


class Game:
    """Main game controller class."""
    
    def __init__(self, players, verbose=False, minimum_bet=10):
        self.minimum_bet = minimum_bet
        self.deck = Deck()
        self.players = players
        self.dealer = Dealer()
        self.round_number = 0
        self.round_info_list = []
        self.verbose = verbose
        self.game_over = False
        
        for player in self.players:
            player.game = self
            
    @round_info_decorator
    def start_game(self):
        """Runs a single round of the game."""
        self.round_number += 1
        self._reset_hands()
        self._check_deck()
        self._place_bets()
        self._deal_initial_cards()
        self._play_hands()
        self._play_dealer_hand()
        self._settle_bets()
        
    def run_simulation(self, num_games):
        """Runs multiple rounds of the game."""
        for round_num in range(num_games):
            if self.game_over:
                break
            if self.verbose and round_num % 10 == 0:  # Print progress every 10 rounds
                print(f"Playing round {round_num + 1}/{num_games}")
            self.start_game()
        return self.summarize_round_info_list()

    def _reset_hands(self):
        """Reset all hands for a new round."""
        self.dealer.reset_hand()
        for player in self.players:
            player.reset_hand()
            
    def _check_deck(self):
        """Check if deck needs to be reshuffled."""
        if len(self.deck.cards) < (len(self.players) + 1) * 6:
            self.deck.reset()
            
    def _place_bets(self):
        """Have all players place their bets."""
        for player in self.players:
            player.place_bet()
            
    def _deal_initial_cards(self):
        """Deal initial cards to all players and dealer."""
        self.dealer.deal_cards(self.players, self.deck)
            
    def _play_hands(self):
        """Play out each player's hands."""
        max_decisions_per_hand = 5  # Reduced to 5 as that should be maximum needed
        
        for player in self.players:
            if self.verbose:
                print(f"\n=== {player.name}'s turn ===")
                
            for hand_index, hand in enumerate(player.hands):
                decisions_made = 0
                if self.verbose:
                    print(f"\nHand {hand_index + 1}: {', '.join(str(card) for card in hand.cards)}")
                    print(f"Hand value: {hand.get_value()}")
                    print(f"Dealer shows: {self.dealer.hand.cards[0]}")
                
                while hand.can_hit and decisions_made < max_decisions_per_hand:
                    decision, rule = player.make_decision(hand)
                    hand.decision_list.append((decision, rule))
                    decisions_made += 1
                    
                    if self.verbose:
                        print(f"Decision {decisions_made}: {decision} (Rule: {rule})")
                    
                    if decision == "hit":
                        new_card = self.deck.deal_card()
                        hand.add_card(new_card)
                        if self.verbose:
                            print(f"Drew: {new_card}")
                            print(f"New hand: {', '.join(str(card) for card in hand.cards)}")
                            print(f"New value: {hand.get_value()}")
                        
                        if hand.is_bust():
                            hand.can_hit = False
                            hand.result = "lose"
                            if self.verbose:
                                print("Bust!")
                                
                    elif decision == "stand":
                        hand.can_hit = False
                        if self.verbose:
                            print("Standing")
                            
                    elif decision == "double down":
                        if self.verbose:
                            print(f"Double down with current bet: {hand.bet}")
                        player.double_down(hand)
                        
                    elif decision == "split":
                        if self.verbose:
                            print("Splitting pair")
                        player.split_hand(hand)
                        
                if decisions_made >= max_decisions_per_hand:
                    hand.can_hit = False
                    print(f"\nWARNING: Hand forced to end after {max_decisions_per_hand} decisions")
                    print(f"Final hand state: {', '.join(str(card) for card in hand.cards)}")
                    print(f"Decision history: {hand.decision_list}")
            
    def _play_dealer_hand(self):
        """Play out the dealer's hand."""
        self.dealer.play(self.deck)
            
    def _settle_bets(self):
        """Settle all bets based on hand results."""
        dealer_value = self.dealer.hand.get_value()
        dealer_bust = self.dealer.hand.is_bust()
        
        for player in self.players:
            for hand in player.hands:
                if hand.result == "lose":  # Already determined (e.g., bust)
                    continue
                    
                if hand.is_blackjack():
                    hand.result = "win"
                    player.win(hand.bet * 2.5)  # Blackjack pays 3:2
                elif dealer_bust:
                    hand.result = "win"
                    player.win(hand.bet * 2)
                else:
                    player_value = hand.get_value()
                    if player_value > dealer_value:
                        hand.result = "win"
                        player.win(hand.bet * 2)
                    elif player_value < dealer_value:
                        hand.result = "lose"
                    else:
                        hand.result = "push"
                        player.win(hand.bet)  # Return original bet
                        
    def summarize_round_info_list(self):
        """Returns a summary of all rounds played."""
        return {
            'total_rounds': len(self.round_info_list),
            'final_budgets': {player.name: player.budget for player in self.players}
        }

def main():
    """Command line entry point for running blackjack simulations."""
    import argparse
    import yaml
    from pathlib import Path
    from ..strategies import (
        BasicStrategy, 
        AggressiveStrategy, 
        ConservativeStrategy
    )
    from ..analysis import BlackjackAnalytics
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run Blackjack simulation with different strategies.')
    parser.add_argument('-c', '--config', type=str, default='config.yaml', 
                       help='Path to configuration file')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Override config verbose setting')
    args = parser.parse_args()
    
    # Load configuration
    config_path = Path(args.config)
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Create strategy instances
    strategy_classes = {
        'BasicStrategy': BasicStrategy,
        'AggressiveStrategy': AggressiveStrategy,
        'ConservativeStrategy': ConservativeStrategy
    }
    
    # Create players from config
    players = []
    for player_config in config['players']:
        strategy_class = strategy_classes[player_config['strategy']]
        strategy = strategy_class()
        
        # Configure strategy if parameters exist
        if player_config['strategy'] in config['strategies']:
            strategy_params = config['strategies'][player_config['strategy']]
            for param, value in strategy_params.items():
                if param != 'description' and hasattr(strategy, param):
                    setattr(strategy, param, value)
        
        player = Player(
            name=player_config['name'],
            budget=player_config['initial_budget'],
            strategy=strategy
        )
        players.append(player)
    
    # Create game with configuration
    game = Game(
        players=players,
        verbose=args.verbose or config['simulation']['verbose'],
        minimum_bet=config['game']['minimum_bet']
    )
    
    # Run analysis
    analytics = BlackjackAnalytics(game)
    results = analytics.run_simulation(num_rounds=config['simulation']['num_rounds'])
    
    # Generate reports
    output_dir = config['simulation']['output_dir']
    analytics.plot_budget_history(output_dir)
    analytics.generate_summary_report(output_dir)
    analytics.export_results(f"{output_dir}/round_info.xlsx")
    
    return results

if __name__ == "__main__":
    main() 