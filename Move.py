class Move:
    def __init__(self, player, pit_index):
        """Initialize a move.
        
        Args:
            player (int): The player making the move (0 or 1)
            pit_index (int): The pit index selected by the player
        """
        self.player = player
        self.pit_index = pit_index
        
    def get_actual_index(self, board):
        """Get the actual index on the board based on player and pit index."""
        return self.pit_index if self.player == 0 else self.pit_index + board.pits + 1
        
    def validate(self, board):
        """Check if this is a valid move."""
        actual_idx = self.get_actual_index(board)
        
        # Check if the pit is within range and not empty
        if 0 <= self.pit_index < board.pits and board[actual_idx] > 0:
            return True
        return False
        
    def execute(self, board):
        """Execute the move on the board.
        
        Args:
            board (Board): The game board
            
        Returns:
            bool: True if player gets another turn, False otherwise
        """
        # Get actual board index
        actual_idx = self.get_actual_index(board)
        
        # Pick up seeds
        seeds_in_hand = board[actual_idx]
        board[actual_idx] = 0
        
        # Sow seeds
        current_idx = actual_idx
        opponent_store = board.get_player_store(1 - self.player)
        
        while seeds_in_hand > 0:
            current_idx = (current_idx + 1) % (2 * board.pits + 2)
            
            # Skip opponent's store
            if current_idx == opponent_store:
                continue
                
            # Place a seed
            board[current_idx] += 1
            seeds_in_hand -= 1
        
        # Check for capture: last seed was placed in an empty pit on player's side
        is_player_side = False
        if self.player == 0:
            is_player_side = 0 <= current_idx < board.pits
        else:
            is_player_side = board.pits + 1 <= current_idx < 2 * board.pits + 1
            
        if is_player_side and board[current_idx] == 1:
            opposite_idx = board.get_opposite_pit(current_idx)
            if opposite_idx is not None and board[opposite_idx] > 0:
                # Capture opponent's seeds
                player_store = board.get_player_store(self.player)
                board[player_store] += board[opposite_idx] + board[current_idx]
                board[opposite_idx] = 0
                board[current_idx] = 0
        
        # Check if last seed was placed in player's store (free turn)
        player_store = board.get_player_store(self.player)
        return current_idx == player_store
