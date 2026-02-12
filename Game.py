from Board import Board
from Move import Move

class Game:
    def __init__(self, pits=6, seeds=4):
        """Initialize the Kalaha game.
        
        Args:
            pits (int): Number of pits per player (excluding store)
            seeds (int): Initial number of seeds per pit
        """
        self.board = Board(pits, seeds)
        self.current_player = 0  # Player 0 starts
        self.game_over = False
    
    def reset(self):
        """Reset the game to initial state."""
        self.board.reset()
        self.current_player = 0
        self.game_over = False
    
    def get_state(self):
        """Return the current state of the game."""
        return {
            'board': self.board.get_state(),
            'current_player': self.current_player,
            'game_over': self.game_over
        }
    
    def set_state(self, state):
        """Set the game state from a state dictionary."""
        self.board.set_state(state['board'])
        self.current_player = state['current_player']
        self.game_over = state['game_over']
    
    def clone(self):
        """Create a deep copy of the game."""
        game_copy = Game(self.board.pits, self.board.seeds)
        game_copy.set_state(self.get_state())
        return game_copy
    
    def get_possible_moves(self):
        """Return list of valid moves for current player."""
        if self.game_over:
            return []
        
        valid_moves = []
        start_idx = 0 if self.current_player == 0 else self.board.pits + 1
        
        for i in range(self.board.pits):
            if self.board[start_idx + i] > 0:
                valid_moves.append(i)
                
        return valid_moves
    
    def make_move(self, pit_idx):
        """Make a move in the game.
        
        Args:
            pit_idx (int): Index of the pit to pick seeds from (0-indexed for each player)
            
        Returns:
            bool: True if the move was valid and executed, False otherwise
        """
        if self.game_over:
            return False
        
        move = Move(self.current_player, pit_idx)
        
        # Check if the move is valid
        if not move.validate(self.board):
            return False
        
        # Execute the move
        free_turn = move.execute(self.board)
        
        # Check if the game is over
        if self.board.is_player_side_empty(0) or self.board.is_player_side_empty(1):
            self.board.collect_remaining_seeds()
            self.game_over = True
            free_turn = False
        
        # Switch player if no free turn
        if not free_turn:
            self.current_player = 1 - self.current_player
            
        return True
    
    def get_winner(self):
        """Return the winner of the game or None if the game is not over."""
        if not self.game_over:
            return None
            
        player1_score = self.board[self.board.pits]
        player2_score = self.board[2 * self.board.pits + 1]
        
        if player1_score > player2_score:
            return 0
        elif player2_score > player1_score:
            return 1
        else:
            return -1  # Draw
    
    def print_board(self):
        """Print the current state of the board."""
        self.board.print()
        print(f"Current player: {self.current_player + 1}")
        
    def can_capture(self, pit):
        """Check if a move from the given pit will result in a capture."""
        # Calculate actual board index
        actual_idx = pit if self.current_player == 0 else pit + self.board.pits + 1
        
        # Get the number of seeds in the pit
        seeds = self.board[actual_idx]
        
        if seeds == 0:
            return False
            
        # Calculate where the last seed will land
        current_idx = actual_idx
        opponent_store = self.board.get_player_store(1 - self.current_player)
        
        for _ in range(seeds):
            current_idx = (current_idx + 1) % (2 * self.board.pits + 2)
            if current_idx == opponent_store:
                current_idx = (current_idx + 1) % (2 * self.board.pits + 2)
        
        # Check if last seed lands in an empty pit on player's side
        is_player_side = False
        if self.current_player == 0:
            is_player_side = 0 <= current_idx < self.board.pits
        else:
            is_player_side = self.board.pits + 1 <= current_idx < 2 * self.board.pits + 1
            
        if is_player_side and self.board[current_idx] == 0:
            opposite_idx = self.board.get_opposite_pit(current_idx)
            return opposite_idx is not None and self.board[opposite_idx] > 0
            
        return False
