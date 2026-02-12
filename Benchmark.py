import time
import random
from Game import Game
from AI import KalahaAI, RandomKalahaAI

def benchmark_ai(ai1, ai2, num_games=50, verbose=False):
    """Run AI vs AI benchmark matches and collect performance statistics.

    Args:
        ai1: First AI instance.
        ai2: Second AI instance.
        num_games (int): Number of matches to simulate.
        verbose (bool): Whether to print detailed game results.
    
    Returns:
        dict: Dictionary containing benchmark statistics.
    """
    ai1_wins = 0
    ai2_wins = 0
    draws = 0
    total_moves = 0
    total_time_ai1 = 0
    total_time_ai2 = 0
    game_lengths = []
    
    ai1_scores = []
    ai2_scores = []
    
    # Track captures and extra turns
    ai1_captures = 0
    ai2_captures = 0
    ai1_extra_turns = 0
    ai2_extra_turns = 0

    for game_num in range(num_games):
        if verbose:
            print(f"Game {game_num+1}/{num_games}")
            
        game = Game()
        move_count = 0
        
        # Track game-specific stats
        game_ai1_captures = 0
        game_ai2_captures = 0
        game_ai1_extra_turns = 0
        game_ai2_extra_turns = 0

        while not game.game_over:
            current_ai = ai1 if game.current_player == 0 else ai2
            current_player = game.current_player
            
            start_move_time = time.time()
            move = current_ai.get_best_move(game)
            end_move_time = time.time()

            if current_ai == ai1:
                total_time_ai1 += (end_move_time - start_move_time)
            else:
                total_time_ai2 += (end_move_time - start_move_time)

            if move is None:
                break  # No more valid moves
                
            # Check if move will result in capture
            if game.can_capture(move):
                if current_player == 0:
                    game_ai1_captures += 1
                else:
                    game_ai2_captures += 1
            
            # Store the player before the move
            previous_player = game.current_player
            
            # Execute the move
            game.make_move(move)
            
            # Check if player got an extra turn
            if game.current_player == previous_player and not game.game_over:
                if previous_player == 0:
                    game_ai1_extra_turns += 1
                else:
                    game_ai2_extra_turns += 1
            
            move_count += 1

        # Update game stats
        ai1_captures += game_ai1_captures
        ai2_captures += game_ai2_captures
        ai1_extra_turns += game_ai1_extra_turns
        ai2_extra_turns += game_ai2_extra_turns
        
        # Get final scores
        player1_score = game.board[game.board.pits]
        player2_score = game.board[2 * game.board.pits + 1]
        ai1_scores.append(player1_score)
        ai2_scores.append(player2_score)
        
        # Determine winner
        winner = game.get_winner()
        if winner == 0:
            ai1_wins += 1
        elif winner == 1:
            ai2_wins += 1
        else:
            draws += 1

        total_moves += move_count
        game_lengths.append(move_count)
        
        if verbose:
            print(f"  Game {game_num+1} - Winner: {'Player 1' if winner == 0 else 'Player 2' if winner == 1 else 'Draw'}")
            print(f"  Score: Player 1: {player1_score}, Player 2: {player2_score}")
            print(f"  Moves: {move_count}, Captures: P1={game_ai1_captures}, P2={game_ai2_captures}")
            print(f"  Extra turns: P1={game_ai1_extra_turns}, P2={game_ai2_extra_turns}")
            print()

    # Calculate additional statistics
    avg_game_length = total_moves / num_games if num_games > 0 else 0
    avg_ai1_score = sum(ai1_scores) / num_games if num_games > 0 else 0
    avg_ai2_score = sum(ai2_scores) / num_games if num_games > 0 else 0
    
    # Average move time (handle case where no moves were made)
    avg_time_ai1 = total_time_ai1 / total_moves if total_moves > 0 else 0
    avg_time_ai2 = total_time_ai2 / total_moves if total_moves > 0 else 0
    
    # Calculate standard deviation of game lengths
    mean_length = avg_game_length
    variance = sum((length - mean_length) ** 2 for length in game_lengths) / num_games if num_games > 0 else 0
    std_dev_length = variance ** 0.5
    
    # Print benchmark results
    print("-" * 80)
    print(f"AI 1: {ai1.__class__.__name__} (Depth {ai1.max_depth})")
    print(f"AI 2: {ai2.__class__.__name__} (Depth {ai2.max_depth})")
    print("-" * 80)
    print(f"Games played: {num_games}")
    print(f"AI 1 wins: {ai1_wins} ({ai1_wins / num_games:.2%})")
    print(f"AI 2 wins: {ai2_wins} ({ai2_wins / num_games:.2%})")
    print(f"Draws: {draws} ({draws / num_games:.2%})")
    print()
    print(f"Average game length: {avg_game_length:.2f} moves (std dev: {std_dev_length:.2f})")
    print(f"Total moves: {total_moves}")
    print()
    print(f"AI 1 avg score: {avg_ai1_score:.2f}")
    print(f"AI 2 avg score: {avg_ai2_score:.2f}")
    print()
    print(f"AI 1 captures: {ai1_captures} (avg: {ai1_captures/num_games:.2f} per game)")
    print(f"AI 2 captures: {ai2_captures} (avg: {ai2_captures/num_games:.2f} per game)")
    print()
    print(f"AI 1 extra turns: {ai1_extra_turns} (avg: {ai1_extra_turns/num_games:.2f} per game)")
    print(f"AI 2 extra turns: {ai2_extra_turns} (avg: {ai2_extra_turns/num_games:.2f} per game)")
    print()
    print(f"AI 1 avg move time: {avg_time_ai1:.4f} sec")
    print(f"AI 2 avg move time: {avg_time_ai2:.4f} sec")
    print("-" * 80)
    
    return {
        'ai1_wins': ai1_wins,
        'ai2_wins': ai2_wins,
        'draws': draws,
        'win_rate_ai1': ai1_wins / num_games if num_games > 0 else 0,
        'win_rate_ai2': ai2_wins / num_games if num_games > 0 else 0,
        'avg_game_length': avg_game_length,
        'avg_score_ai1': avg_ai1_score,
        'avg_score_ai2': avg_ai2_score,
        'avg_time_ai1': avg_time_ai1,
        'avg_time_ai2': avg_time_ai2,
        'captures_ai1': ai1_captures,
        'captures_ai2': ai2_captures,
        'extra_turns_ai1': ai1_extra_turns,
        'extra_turns_ai2': ai2_extra_turns
    }


# Define custom AI variants for testing
class StoreWeightedAI(KalahaAI):
    """AI that puts higher priority on storing seeds."""
    def _evaluate(self, game):
        board = game.board
        
        # If game is over, assign large values based on the winner
        if game.game_over:
            winner = game.get_winner()
            if winner == game.current_player:
                return 1000
            elif winner is not None:
                return -1000
            else:
                return 0
        
        # Store values (even higher priority)
        player_store = board[board.get_player_store(game.current_player)]
        opponent_store = board[board.get_player_store(1 - game.current_player)]
        
        # Seeds in pits
        player_seeds = sum(board[i] for i in board.get_player_pits_range(game.current_player))
        opponent_seeds = sum(board[i] for i in board.get_player_pits_range(1 - game.current_player))
        
        # Extra turn opportunities
        extra_turns = 0
        for pit in range(game.board.pits):
            actual_idx = pit if game.current_player == 0 else pit + game.board.pits + 1
            if actual_idx + board[actual_idx] == board.get_player_store(game.current_player):
                extra_turns += 1
        
        # Capturing moves
        capture_score = 0
        for pit in range(game.board.pits):
            if game.can_capture(pit):
                capture_score += 1
        
        # Heavily weight the store difference
        return (
            15 * (player_store - opponent_store) +  # Increased from 10 to 15
            2 * (player_seeds - opponent_seeds) +
            4 * extra_turns +
            6 * capture_score
        )

class ExtraTurnPrioritizedAI(KalahaAI):
    """AI that prioritizes moves that lead to extra turns."""
    def _evaluate(self, game):
        board = game.board
        
        # If game is over, assign large values based on the winner
        if game.game_over:
            winner = game.get_winner()
            if winner == game.current_player:
                return 1000
            elif winner is not None:
                return -1000
            else:
                return 0
        
        # Store values
        player_store = board[board.get_player_store(game.current_player)]
        opponent_store = board[board.get_player_store(1 - game.current_player)]
        
        # Seeds in pits
        player_seeds = sum(board[i] for i in board.get_player_pits_range(game.current_player))
        opponent_seeds = sum(board[i] for i in board.get_player_pits_range(1 - game.current_player))
        
        # Extra turn opportunities (heavily weighted)
        extra_turns = 0
        for pit in range(game.board.pits):
            actual_idx = pit if game.current_player == 0 else pit + game.board.pits + 1
            if actual_idx + board[actual_idx] == board.get_player_store(game.current_player):
                extra_turns += 1
        
        # Capturing moves
        capture_score = 0
        for pit in range(game.board.pits):
            if game.can_capture(pit):
                capture_score += 1
        
        # Heavily weight extra turns
        return (
            10 * (player_store - opponent_store) +
            2 * (player_seeds - opponent_seeds) +
            10 * extra_turns +  # Increased from 4 to 10
            6 * capture_score
        )

class CapturePrioritizedAI(KalahaAI):
    """AI that prioritizes capturing opponent's seeds."""
    def _evaluate(self, game):
        board = game.board
        
        # If game is over, assign large values based on the winner
        if game.game_over:
            winner = game.get_winner()
            if winner == game.current_player:
                return 1000
            elif winner is not None:
                return -1000
            else:
                return 0
        
        # Store values
        player_store = board[board.get_player_store(game.current_player)]
        opponent_store = board[board.get_player_store(1 - game.current_player)]
        
        # Seeds in pits
        player_seeds = sum(board[i] for i in board.get_player_pits_range(game.current_player))
        opponent_seeds = sum(board[i] for i in board.get_player_pits_range(1 - game.current_player))
        
        # Extra turn opportunities
        extra_turns = 0
        for pit in range(game.board.pits):
            actual_idx = pit if game.current_player == 0 else pit + game.board.pits + 1
            if actual_idx + board[actual_idx] == board.get_player_store(game.current_player):
                extra_turns += 1
        
        # Capturing moves (heavily weighted)
        capture_score = 0
        for pit in range(game.board.pits):
            if game.can_capture(pit):
                capture_score += 1
        
        # Heavily weight capture opportunities
        return (
            10 * (player_store - opponent_store) +
            2 * (player_seeds - opponent_seeds) +
            4 * extra_turns +
            12 * capture_score  # Increased from 6 to 12
        )

class NoMoveOrderingAI(KalahaAI):
    """AI without move ordering optimization."""
    def _order_moves(self, game, moves):
        """Return moves without any ordering."""
        return moves  # No sorting, just return the original moves


def main():
    """Main function to run benchmarks."""
    # Configure the number of games for each benchmark
    games_per_benchmark = 50
    
    print("=" * 80)
    print("KALAHA AI BENCHMARK SUITE")
    print("=" * 80)
    print(f"Games per benchmark: {games_per_benchmark}")
    print()
    
    # Store results for later analysis
    all_results = {}
    
    # 1. Search Depth Comparison
    print("\n1. SEARCH DEPTH COMPARISON\n")
    depths = [3, 5, 7, 9]  # Test different search depths
    
    for i, depth1 in enumerate(depths):
        for depth2 in depths[i+1:]:
            print(f"Testing Depth {depth1} vs Depth {depth2}")
            ai1 = KalahaAI(max_depth=depth1)
            ai2 = KalahaAI(max_depth=depth2)
            results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
            all_results[f"Depth {depth1} vs Depth {depth2}"] = results
    
    # 2. Evaluation Function Comparison
    print("\n2. EVALUATION FUNCTION COMPARISON\n")
    
    # Default vs Store-Weighted
    print("Default AI vs Store-Weighted AI")
    ai1 = KalahaAI(max_depth=5)
    ai2 = StoreWeightedAI(max_depth=5)
    results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
    all_results["Default vs Store-Weighted"] = results
    
    # Default vs Extra Turn-Oriented
    print("Default AI vs Extra Turn-Oriented AI")
    ai1 = KalahaAI(max_depth=5)
    ai2 = ExtraTurnPrioritizedAI(max_depth=5)
    results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
    all_results["Default vs Extra Turn-Oriented"] = results
    
    # Default vs Capture-Oriented
    print("Default AI vs Capture-Oriented AI")
    ai1 = KalahaAI(max_depth=5)
    ai2 = CapturePrioritizedAI(max_depth=5)
    results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
    all_results["Default vs Capture-Oriented"] = results
    
    # 3. Move Ordering Efficiency
    print("\n3. MOVE ORDERING EFFICIENCY\n")
    
    print("AI with Move Ordering vs AI without Move Ordering")
    ai1 = KalahaAI(max_depth=5)
    ai2 = NoMoveOrderingAI(max_depth=5)
    results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
    all_results["Move Ordering vs No Move Ordering"] = results
    
    # 4. Randomness Effect
    print("\n4. RANDOMNESS EFFECT\n")
    
    print("Deterministic AI vs Random AI")
    ai1 = KalahaAI(max_depth=5)
    ai2 = RandomKalahaAI(max_depth=5)
    results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
    all_results["Deterministic vs Random"] = results
    
    # 5. Head-to-Head champion tournament
    print("\n5. CHAMPION TOURNAMENT\n")
    
    # Create the champions with equal depths
    depth = 5
    champions = [
        ("Default", KalahaAI(max_depth=depth)),
        ("Store-Weighted", StoreWeightedAI(max_depth=depth)),
        ("Extra-Turn", ExtraTurnPrioritizedAI(max_depth=depth)),
        ("Capture", CapturePrioritizedAI(max_depth=depth)),
        ("Random", RandomKalahaAI(max_depth=depth))
    ]
    
    # Tournament results
    tournament_results = {name: {"wins": 0, "games": 0} for name, _ in champions}
    
    print(f"Running tournament with {len(champions)} AI variants...")
    
    # Play all combinations
    for i, (name1, ai1) in enumerate(champions):
        for j, (name2, ai2) in enumerate(champions):
            if i >= j:  # Skip self-matches and repeated matches
                continue
                
            print(f"{name1} vs {name2}")
            results = benchmark_ai(ai1, ai2, num_games=games_per_benchmark)
            
            # Update tournament results
            tournament_results[name1]["wins"] += results["ai1_wins"]
            tournament_results[name2]["wins"] += results["ai2_wins"]
            tournament_results[name1]["games"] += games_per_benchmark
            tournament_results[name2]["games"] += games_per_benchmark
    
    # Print tournament rankings
    print("\nTOURNAMENT RANKINGS")
    print("-" * 50)
    print(f"{'AI Type':<20} {'Win Rate':<10} {'Wins':<8} {'Games':<8}")
    print("-" * 50)
    
    # Sort by win rate
    sorted_results = sorted(
        tournament_results.items(),
        key=lambda x: x[1]["wins"] / x[1]["games"] if x[1]["games"] > 0 else 0,
        reverse=True
    )
    
    for name, stats in sorted_results:
        win_rate = stats["wins"] / stats["games"] if stats["games"] > 0 else 0
        print(f"{name:<20} {win_rate:.4f}    {stats['wins']:<8} {stats['games']:<8}")
    
    print("\nBenchmark completed!")


if __name__ == "__main__":
    main()