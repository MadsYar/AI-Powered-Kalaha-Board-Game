class Board:
    def __init__(self, pits=6, seeds=4):
        """Initialize the Kalaha game board.
        
        Args:
            pits (int): Number of pits per player (excluding store)
            seeds (int): Initial number of seeds per pit
        """
        self.pits = pits
        self.seeds = seeds
        self.reset()
    
    def reset(self):
        """Reset the board to initial state."""
        # Board layout: [p1_pits, p1_store, p2_pits, p2_store]
        self.state = [self.seeds] * self.pits + [0] + [self.seeds] * self.pits + [0]
    
    def get_state(self):
        """Return the current state of the board."""
        return self.state.copy()
    
    def set_state(self, state):
        """Set the board state."""
        self.state = state.copy()
    
    def __getitem__(self, index):
        """Get the number of seeds at a specific position."""
        return self.state[index]
    
    def __setitem__(self, index, value):
        """Set the number of seeds at a specific position."""
        self.state[index] = value
    
    def get_player_store(self, player):
        """Get the store index for a player."""
        return self.pits if player == 0 else 2 * self.pits + 1
    
    def get_player_pits_range(self, player):
        """Get the range of indices for a player's pits."""
        if player == 0:
            return range(self.pits)
        else:
            return range(self.pits + 1, 2 * self.pits + 1)
            
    def get_opposite_pit(self, pit):
        """Get the opposite pit index for a given pit."""
        if 0 <= pit < self.pits or self.pits + 1 <= pit < 2 * self.pits + 1:
            return 2 * self.pits - pit
        return None
        
    def is_player_side_empty(self, player):
        """Check if all pits on a player's side are empty."""
        return all(self.state[i] == 0 for i in self.get_player_pits_range(player))
    
    def collect_remaining_seeds(self):
        """Collect all remaining seeds into each player's store."""
        # Collect player 1's seeds
        for i in range(self.pits):
            self.state[self.pits] += self.state[i]
            self.state[i] = 0
        
        # Collect player 2's seeds
        for i in range(self.pits + 1, 2 * self.pits + 1):
            self.state[2 * self.pits + 1] += self.state[i]
            self.state[i] = 0
          
    def print(self):
        """Print the current state of the board as a visual representation."""
        # Print player 2's pits indices
        print("\n        ", end="")
        for i in range(self.pits - 1, -1, -1):
            print(f" [{i}]  ", end="")
        print()
        
        # Create top border
        print("      ┌─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Print player 2's pits (in reverse order)
        print("      │", end="")
        for i in range(2 * self.pits, self.pits, -1):
            print(f"  {self.state[i]:2} │", end="")
        print()
        
        # Create middle section with stores
        print("┌─────┼─────┴─────┴─────┴─────┴─────┴─────┼─────┐")
        print(f"│ P2: │                                   │ P1: │")
        print(f"│ {self.state[2*self.pits+1]:2}  │                                   │ {self.state[self.pits]:2}  │")
        print("└─────┼─────┬─────┬─────┬─────┬─────┬─────┼─────┘")
        
        # Print player 1's pits
        print("      │", end="")
        # Print player 1's pits
        for i in range(self.pits):
            print(f"  {self.state[i]:2} │", end="")
        print()
        
        # Create bottom border
        print("      └─────┴─────┴─────┴─────┴─────┴─────┘")
        
        # Print pit numbers for reference
        print("        ", end="")
        for i in range(self.pits):
            print(f" [{i}]  ", end="")
        print("\n")