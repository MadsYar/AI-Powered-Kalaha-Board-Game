import time
from Player import Player_Human, Player_AI
from AI import KalahaAI

class UI:
    def __init__(self, game):
        """Initialize the game interface."""
        
        self.game = game
        self.players = [None, None]
        
    def setup_players(self, type):
        """Set up the players for the game."""

        for i, spec in enumerate(type):
        
            if spec == 'human':
                self.players[i] = Player_Human(i)
        
            elif isinstance(spec, tuple) and spec[0] == 'ai':
                self.players[i] = Player_AI(i, spec[1])
        
    def play(self):
        print("Welcome to Kalaha!")
        print("Enter 'q' to quit the game.")
        
        while not self.game.game_over:
            self.game.print_board()
            
            current_player = self.players[self.game.current_player]
            
            valid_move = self.game.get_possible_moves()
        
            if not valid_move:
                print(f"{current_player} has no valid moves!")
                break
            
            move = current_player.get_move(self.game)
            
            if move is None:
                print("The game has been quit")
                return
                
            self.game.make_move(move)
        
        # Game over
        self.game.print_board()
        self.announce_winner()
        
    def announce_winner(self):
        winner = self.game.get_winner()
        
        if winner == 0:
            print("Player 1 wins")
        
        elif winner == 1:
            print("Player 2 wins")
        
        else:
            print("Draw")
