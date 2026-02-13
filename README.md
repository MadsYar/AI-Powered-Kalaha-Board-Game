# Kalaha Board Game

A complete implementation of the classic **Kalaha** board game with an intelligent AI opponent powered by the MinMax algorithm with alpha-beta pruning.

## Project Overview

This project implements the traditional two-player Kalaha game (also known as Mancala) with:
- **Human vs AI gameplay**: Play against a computer opponent
- **AI vs AI battles**: Watch two AIs compete using different strategies
- **AI agent**: Implements MinMax search with alpha-beta pruning and strategic move ordering
- **Benchmarking**: Tools to evaluate and compare different AI strategies
- **Customizable game parameters**: Adjust pit counts, seed distribution, and search depth

## Game Rules

Kalaha is a turn-based strategy game played on a board with:
- **6 pits per player** (default, customizable)
- **4 seeds per pit** (default, customizable)
- **2 stores** (one for each player)

### How to Play:
1. Players take turns selecting a pit on their side
2. Seeds from the selected pit are distributed counter-clockwise, one seed per pit
3. If the last seed lands in the player's store, they get an extra turn
4. If the last seed lands in an empty pit on the player's side, they capture the opposite pit's seeds
5. The game ends when one player's side is empty
6. The player with the most seeds in their store wins

## Project Structure

```
.
├── Game.py           # Core game logic and state management
├── Board.py          # Board representation and operations
├── Move.py           # Move validation and execution
├── Player.py         # Player base class and implementations (Human, AI)
├── AI.py             # AI engine with MinMax and alpha-beta pruning
├── UI.py             # Game interface and display
├── Main.py           # Entry point and game setup
├── Benchmark.py      # AI benchmarking and comparison tools
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

### Key Components:

**Game.py** - Manages game state, turn logic, and win conditions

**Board.py** - Represents the board state and provides pit/store access methods

**Move.py** - Validates and executes moves, handles captures and extra turns

**AI.py** - Implements:
- `KalahaAI`: Standard AI with MinMax and alpha-beta pruning
- `RandomKalahaAI`: AI variant with randomized evaluations
- Custom AI variants for strategy testing

**Player.py** - Abstract player class with implementations for:
- `Player_Human`: Human input-based player
- `Player_AI`: AI-controlled player

**UI.py** - Handles game display and player interaction

**Benchmark.py** - Evaluation framework featuring:
- Depth comparison tests
- Evaluation function variants
- Move ordering efficiency analysis

## AI Algorithm Details

### MinMax with Alpha-Beta Pruning

The AI uses a recursive MinMax algorithm that:
1. Searches game states to a specified depth (default: 7)
2. Alternates between maximizing and minimizing players
3. Uses alpha-beta pruning to eliminate unnecessary branches
4. Implements move ordering to improve pruning efficiency

### Running the Game

```bash
python Main.py
```

Follow the prompts to:
1. Choose a game mode (Human vs AI, AI vs AI Deterministic, or AI vs AI Randomized)
2. If playing as human, choose which player you want to be
3. Make moves by entering pit numbers (0-5)
4. Type `q` to quit

### Running Benchmarks

```bash
python Benchmark.py
```

This runs a comprehensive benchmark suite comparing:
- Different search depths (3, 5, 7, 9)
- Different evaluation functions
- Move ordering efficiency
- Custom AI variants

### Evaluation Function

The evaluation function weighs different strategic aspects:
```
score = 8 * (player_store - opponent_store) +
        2 * (player_seeds - opponent_seeds) +
        5 * extra_turn_opportunities +
        14 * capture_score
```

- **Store difference (weight: 8)**: Highest priority - winning is about accumulating seeds
- **Board control (weight: 2)**: Sum of seeds on player's side
- **Extra turns (weight: 5)**: Opportunities to move again
- **Captures (weight: 14)**: Capturing opponent's seeds

## Configuration

You can customize game parameters in `Main.py` and `Game.py`:

```python
# Number of pits per player
pits = 6

# Initial seeds per pit
seeds = 4

# AI search depth
ai_depth = 6
```

## Example Session

```
Choose game mode:
1. Human vs AI
2. AI vs AI (Deterministic)
3. AI vs AI (Random)
Your choice: 1

Choose AI player:
1. AI plays as Player 1
2. AI plays as Player 2
Your choice: 2

        [5]  [4]  [3]  [2]  [1]  [0]
      ┌─────┬─────┬─────┬─────┬─────┬─────┐
      │   4 │   4 │   4 │   4 │   4 │   4 │
┌─────┼─────┴─────┴─────┴─────┴─────┴─────┼─────┐
│ P2: │                                   │ P1: │
│  0  │                                   │  0  │
└─────┼─────┬─────┬─────┬─────┬─────┬─────┼─────┘
      │   4 │   4 │   4 │   4 │   4 │   4 │
      └─────┴─────┴─────┴─────┴─────┴─────┘
        [0]  [1]  [2]  [3]  [4]  [5]

Current player: 1
Player 1: Choose a pit (0-5): 2
```
