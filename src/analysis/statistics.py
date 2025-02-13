import pandas as pd
import matplotlib.pyplot as plt
import os

class BlackjackAnalytics:
    def __init__(self, game):
        self.game = game
        
    def analyze_win_rate(self):
        """Analyzes win rate and returns statistics."""
        pass
        
    def plot_budget_history(self, output_dir):
        """Plots budget history for each player."""
        plt.figure(figsize=(12, 6))
        
        for player in self.game.players:
            budgets = [p['budget'] for round_info in self.game.round_info_list 
                      for p in round_info['players'] if p['name'] == player.name]
            plt.plot(budgets, label=player.name)
            
        plt.title('Player Budget History')
        plt.xlabel('Round')
        plt.ylabel('Budget')
        plt.legend()
        plt.grid(True)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.savefig(os.path.join(output_dir, 'budget_history.png'))
        plt.close()
        
    def generate_summary_report(self, output_dir):
        """Generates a summary report of the simulation."""
        summary = {
            'total_rounds': len(self.game.round_info_list),
            'players': []
        }
        
        for player in self.game.players:
            player_stats = {
                'name': player.name,
                'final_budget': player.budget,
                'total_hands': 0,
                'wins': 0,
                'losses': 0,
                'pushes': 0,
                'blackjacks': 0
            }
            
            for round_info in self.game.round_info_list:
                for p in round_info['players']:
                    if p['name'] == player.name:
                        for hand in p['hands']:
                            player_stats['total_hands'] += 1
                            if hand['result'] == 'win':
                                player_stats['wins'] += 1
                                if hand['is blackjack']:
                                    player_stats['blackjacks'] += 1
                            elif hand['result'] == 'lose':
                                player_stats['losses'] += 1
                            else:
                                player_stats['pushes'] += 1
                                
            summary['players'].append(player_stats)
            
        # Write summary to file
        with open(os.path.join(output_dir, 'summary_report.txt'), 'w') as f:
            f.write("Blackjack Simulation Summary\n")
            f.write("===========================\n\n")
            f.write(f"Total Rounds: {summary['total_rounds']}\n\n")
            
            for player in summary['players']:
                f.write(f"Player: {player['name']}\n")
                f.write(f"Final Budget: ${player['final_budget']}\n")
                f.write(f"Total Hands: {player['total_hands']}\n")
                f.write(f"Wins: {player['wins']} ({player['wins']/player['total_hands']*100:.1f}%)\n")
                f.write(f"Losses: {player['losses']} ({player['losses']/player['total_hands']*100:.1f}%)\n")
                f.write(f"Pushes: {player['pushes']} ({player['pushes']/player['total_hands']*100:.1f}%)\n")
                f.write(f"Blackjacks: {player['blackjacks']}\n\n")

    def get_strategy_statistics(self):
        """Calculate comprehensive statistics for a strategy."""
        game_data = self.game.round_info_list
        player_data = [p for game in game_data for p in game['players']]
        
        total_hands = sum(len(p['hands']) for p in player_data)
        wins = sum(sum(1 for h in p['hands'] if h['result'] == 'win') for p in player_data)
        blackjacks = sum(sum(1 for h in p['hands'] if h['is blackjack']) for p in player_data)
        busts = sum(sum(1 for h in p['hands'] if h['is bust']) for p in player_data)
        
        # Calculate consecutive wins
        max_consecutive_wins = 0
        current_consecutive_wins = 0
        for p in player_data:
            if any(h['result'] == 'win' for h in p['hands']):
                current_consecutive_wins += 1
                max_consecutive_wins = max(max_consecutive_wins, current_consecutive_wins)
            else:
                current_consecutive_wins = 0
        
        return {
            'Final Budget': player_data[-1]['budget'],
            'Total Hands': total_hands,
            'Win Rate': wins / total_hands if total_hands > 0 else 0,
            'Average Bet': sum(h['bet'] for p in player_data for h in p['hands']) / total_hands,
            'Largest Win': max((h['bet'] for p in player_data for h in p['hands'] if h['result'] == 'win'), default=0),
            'Largest Loss': max((h['bet'] for p in player_data for h in p['hands'] if h['result'] == 'lose'), default=0),
            'Blackjacks': blackjacks,
            'Busts': busts,
            'Max Consecutive Wins': max_consecutive_wins
        }

    def run_simulation(self, num_rounds):
        """Runs simulation and collects statistics."""
        return self.game.run_simulation(num_rounds)
        
    def export_results(self, filename='round_info.xlsx'):
        """Exports detailed round data to Excel."""
        df_player = pd.json_normalize(
            self.game.round_info_list, 
            ['players', 'hands'], 
            max_level=3,
            meta=['round number', ['players', 'name'], ['players', 'budget']]
        )
        
        df_dealer = pd.json_normalize(self.game.round_info_list)
        df_dealer.drop(['players'], axis=1, inplace=True)
        
        df = df_player.merge(df_dealer, on='round number', how='left')
        df = df.rename(columns=lambda x: x.split('.')[-1])
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_excel(filename, index=False) 