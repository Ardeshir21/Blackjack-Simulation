# Blackjack Strategy Simulator

A sophisticated Python-based Blackjack simulator for analyzing and comparing different betting strategies. This project demonstrates object-oriented design, strategy pattern implementation, and advanced data analysis techniques.

## 🎯 Features

- **Multiple Strategy Support**
  - Basic Strategy (standard blackjack play)
  - Aggressive Strategy (high-risk, high-reward)
  - Conservative Strategy (risk-averse approach)
  - Extensible framework for custom strategies

- **Configurable Simulation Parameters**
  - Number of rounds
  - Initial budgets
  - Minimum bet amounts
  - Strategy-specific parameters

- **Comprehensive Analytics**
  - Win/loss statistics
  - Budget history tracking
  - Hand-by-hand analysis
  - Strategy performance comparison

- **Rich Reporting**
  - Excel reports with detailed round data
  - Budget history plots
  - Strategy comparison summaries
  - Performance metrics


# 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/blackjack-simulator.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .


# Run with default configuration
blackjack

# Run with verbose output
blackjack -v

# Use custom configuration file
blackjack -c my_config.yaml
```

# 📦 Basic Usage

```bash
# Run with default configuration
blackjack

# Run with verbose output
blackjack -v

# Use custom configuration file
blackjack -c my_config.yaml
```

# 📦 Configuration

The configuration file (`config.yaml`) allows you to customize the simulation parameters. Here's an example configuration:


# 🛠️ Technical Implementation

## Design Patterns
- **Strategy Pattern**: For implementing different betting strategies
- **Decorator Pattern**: For game state tracking and logging
- **Factory Pattern**: For card and deck management

## Key Technologies
- **Python 3.7+**
- **Pandas**: For data analysis and Excel report generation
- **Matplotlib**: For visualization
- **PyYAML**: For configuration management

## 📊 Reports Generated

### 1. Excel Report (`round_info.xlsx`)
- Detailed round-by-round data
- Player decisions and outcomes
- Bet amounts and results
- Hand compositions

### 2. Budget History Plot
- Visual representation of each player's budget over time
- Trend analysis
- Strategy comparison

### 3. Summary Report
- Overall statistics
- Win/loss ratios
- Blackjack frequency
- Average bet sizes
- Maximum winning/losing streaks

## 📁 Project Structure

```
blackjack-simulator/
├── src/
│   ├── game/
│   │   ├── __init__.py
│   │   ├── blackjack.py      # Main game controller and CLI
│   │   ├── card.py           # Card representation
│   │   ├── dealer.py         # Dealer logic
│   │   ├── deck.py           # Deck management
│   │   ├── hand.py           # Hand representation
│   │   └── player.py         # Player logic
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py      # Abstract base class for strategies
│   │   ├── basic_strategy.py     # Standard blackjack strategy
│   │   ├── aggressive_strategy.py # High-risk strategy
│   │   └── conservative_strategy.py # Low-risk strategy
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── statistics.py      # Analytics and reporting
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── decorators.py      # Game state tracking decorators
│   │
│   └── __init__.py
│
├── config.yaml                # Simulation configuration
├── pyproject.toml            # Project metadata and dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
└── results/                 # Generated reports (gitignored)
    ├── round_info.xlsx      # Detailed game data
    ├── budget_history.png   # Budget visualization
    └── summary_report.txt   # Strategy comparison 
```


# 🧪 Development Features

- **Modular Design**: Easy to extend and modify
- **Type Hints**: For better code documentation
- **Comprehensive Logging**: For debugging and analysis
- **Configuration Management**: YAML-based configuration
- **Error Handling**: Robust error checking and reporting

## 🔧 Extending the Simulator

### Adding New Strategies

1. Create a new strategy class in `src/strategies/`:

```python
from .base_strategy import BaseStrategy
from src.utils.decorators import decision_modifier_decorator

class MyCustomStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.name = "My Custom Strategy"
        
    @decision_modifier_decorator
    def decide(self, player_hand, game, budget):
        # Implement your strategy logic here
        pass
        
    def determine_bet(self, game, budget):
        # Implement your betting logic here
        pass
```

2. Add the new strategy to the configuration file (`config.yaml`):

```yaml
players:
  - name: "Custom Player"
    strategy: "MyCustomStrategy"
    initial_budget: 1000

strategies:
  MyCustomStrategy:
    description: "My custom strategy implementation"
    # Add any strategy-specific parameters
```