class KalahaAI:
    def __init__(self, max_depth=7):
        """Initialize the AI with a maximum search depth.
        
        Args:
            max_depth (int): Maximum depth for the MinMax algorithm
        """
        self.max_depth = max_depth
    
    def get_best_move(self, game):
        """Return the best move for the current player using MinMax with alpha-beta pruning.
        
        Args:
            game (Game): The current game state
            
        Returns:
            int: The index of the best pit to choose
        """
        valid_moves = game.get_possible_moves()
        
        if not valid_moves:
            return None
        
        # Order moves to improve efficiency
        ordered_moves = self._order_moves(game, valid_moves)
            
        best_move = ordered_moves[0]
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in ordered_moves:
            # Create a copy of the game to simulate the move
            game_copy = game.clone()
            game_copy.make_move(move)
            
            # If player gets another turn, continue searching from their perspective
            if game_copy.current_player == game.current_player:
                value = self._min_max(game_copy, self.max_depth - 1, alpha, beta, True)
            else:
                value = self._min_max(game_copy, self.max_depth - 1, alpha, beta, False)
                
            if value > best_value:
                best_value = value
                best_move = move
                
            alpha = max(alpha, best_value)
            
        return best_move
    
    def _order_moves(self, game, moves):
        """Order moves to improve alpha-beta pruning efficiency.
        Prioritize moves that land in store (extra turn) or might capture.
        
        Args:
            game (Game): Current game state
            moves (list): List of possible moves
            
        Returns:
            list: Ordered list of moves
        """
        scored_moves = []
        board = game.board
        
        for move in moves:
            score = 0
            game_copy = game.clone()
            
            # Calculate actual board index
            actual_idx = move if game_copy.current_player == 0 else move + board.pits + 1
            seeds = game_copy.board[actual_idx]
            
            # Check if this might land in the store (extra turn)
            player_store = board.get_player_store(game_copy.current_player)
            
            # Calculate where the last seed will land
            last_idx = actual_idx
            seeds_to_distribute = seeds
            
            while seeds_to_distribute > 0:
                last_idx = (last_idx + 1) % (2 * board.pits + 2)
                # Skip opponent's store
                opponent_store = board.get_player_store(1 - game_copy.current_player)
                if last_idx == opponent_store:
                    continue
                seeds_to_distribute -= 1
            
            # Check if last seed lands in store (extra turn)
            if last_idx == player_store:
                score += 10  # Highly prioritize extra turns
            
            # Check if this might lead to a capture
            is_player_side = False
            if game_copy.current_player == 0:
                is_player_side = 0 <= last_idx < board.pits
            else:
                is_player_side = board.pits + 1 <= last_idx < 2 * board.pits + 1
                
            if is_player_side and game_copy.board[last_idx] == 0:
                opposite_idx = board.get_opposite_pit(last_idx)
                if opposite_idx is not None:
                    score += game_copy.board[opposite_idx]  # Prioritize by capture value
                    
            scored_moves.append((move, score))
            
        # Sort moves by score in descending order
        return [move for move, score in sorted(scored_moves, key=lambda x: x[1], reverse=True)]
    
    def _min_max(self, game, depth, alpha, beta, maximizing):
        """MinMax algorithm with alpha-beta pruning.
        
        Args:
            game (Game): The current game state
            depth (int): Current depth in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing (bool): True if maximizing player, False if minimizing
            
        Returns:
            float: The evaluation of the best move
        """
        # Check if game is over or maximum depth reached
        if game.game_over or depth == 0:
            return self._evaluate(game)
            
        valid_moves = game.get_possible_moves()
        
        if not valid_moves:
            return self._evaluate(game)
        
        # Order moves for better pruning
        ordered_moves = self._order_moves(game, valid_moves)
            
        if maximizing:
            value = float('-inf')
            for move in ordered_moves:
                game_copy = game.clone()
                game_copy.make_move(move)
                
                # Check if we stay with the same player
                if game_copy.current_player == game.current_player:
                    # If we get another turn, continue maximizing
                    child_value = self._min_max(game_copy, depth - 1, alpha, beta, True)
                else:
                    # Otherwise, switch to minimizing
                    child_value = self._min_max(game_copy, depth - 1, alpha, beta, False)
                    
                value = max(value, child_value)
                alpha = max(alpha, value)
                
                if beta <= alpha:
                    break  # Beta cut-off
                    
            return value
        else:
            value = float('inf')
            for move in ordered_moves:
                game_copy = game.clone()
                game_copy.make_move(move)
                
                # Check if we stay with the same player
                if game_copy.current_player == game.current_player:
                    # If opponent gets another turn, continue minimizing
                    child_value = self._min_max(game_copy, depth - 1, alpha, beta, False)
                else:
                    # Otherwise, switch to maximizing
                    child_value = self._min_max(game_copy, depth - 1, alpha, beta, True)
                    
                value = min(value, child_value)
                beta = min(beta, value)
                
                if beta <= alpha:
                    break  # Alpha cut-off
                    
            return value
    
    def _evaluate(self, game):
        """Evaluate the current game state with optimized weightings."""
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

        # Store values (highest priority)
        player_store = board[board.get_player_store(game.current_player)]
        opponent_store = board[board.get_player_store(1 - game.current_player)]

        # Seeds in pits (control of board)
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

        #Weighted evaluation
        return (
            8 * (player_store - opponent_store) +
            2 * (player_seeds - opponent_seeds) +
            5 * extra_turns +
            14 * capture_score 
        )

class RandomKalahaAI(KalahaAI):
    """KalahaAI variant that adds randomness to evaluations."""
    
    def _evaluate(self, game):
        import random
        # Get the base evaluation
        base_eval = super()._evaluate(game)
        # Add a small random factor
        return base_eval + random.uniform(-1.0, 1.0)
