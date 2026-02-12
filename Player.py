import abc

class Player(abc.ABC):
    def __init__(self, player_number):
        """Initialize the player."""

        self.player_number = player_number
        
    @abc.abstractmethod
    def get_move(self, game):
        """Get a move from the player.
        
        Args:
            game: The current game state
            
        Returns:
            int: The index of the pit to choose
        """
        pass
        
    def __str__(self):
        return f"Player {self.player_number + 1}"


class Player_Human(Player):

    def get_move(self, game):
        valid_moves = game.get_possible_moves()
        
        while True:
            try:
                user_input = input(f"{self}: Choose a pit (0-{game.board.pits-1}): ")
                
                if user_input.lower() == 'q':
                    return None
                    
                move = int(user_input)

                if move in valid_moves:
                    return move
                else:
                    print(f"This is not possible. What you can do is: {valid_moves}")
            
            except ValueError:
                print("Please enter a valid number or q to quit.")


class Player_AI(Player):
    
    def __init__(self, player_number, ai_engine):
        super().__init__(player_number)
        self.ai_engine = ai_engine
        
    def get_move(self, game):
        move = self.ai_engine.get_best_move(game)

        if move is not None:
            print(f"{self} selects pit {move}")
        
        return move
        
    def __str__(self):
        return f"AI (Player {self.player_number + 1})"
