from Game import Game
from UI import UI
from AI import KalahaAI, RandomKalahaAI

def main():
    """Main function to run the Kalaha game."""
    # Game settings
    pits = 6
    seeds = 4
    
    # Create game instance
    game = Game(pits=pits, seeds=seeds)
    
    # Create game interface
    ui = UI(game)
    
    # Ask for game mode
    while True:
        print("Choose game mode:")
        print("1. Human vs AI")
        print("2. AI vs AI (Deterministic)")
        print("3. AI vs AI (Random)")
        mode_choice = input("Your choice: ")
        
        if mode_choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    if mode_choice == '1':
        # Human vs AI mode
        while True:
            ai_player_choice = input("Choose AI player:\n1. AI plays as Player 1\n2. AI plays as Player 2\nYour choice: ")
            if ai_player_choice in ['1', '2']:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        # Set up players
        ai_engine = KalahaAI(max_depth=6)
        if ai_player_choice == '1':
            ui.setup_players([('ai', ai_engine), 'human'])
        else:
            ui.setup_players(['human', ('ai', ai_engine)])
    
    elif mode_choice == '2':
        # AI vs AI (Deterministic) mode
        print("Setting up AI vs AI game (deterministic)...")
        ai_engine1 = KalahaAI(max_depth=6)
        ai_engine2 = KalahaAI(max_depth=6)
        ui.setup_players([('ai', ai_engine1), ('ai', ai_engine2)])
    
    else:  # mode_choice == '3'
        # AI vs AI (Random) mode
        print("Setting up AI vs AI game with randomness...")
        
        # Use the RandomKalahaAI class from AI.py
        ai_engine1 = RandomKalahaAI(max_depth=5)
        ai_engine2 = RandomKalahaAI(max_depth=7)
        ui.setup_players([('ai', ai_engine1), ('ai', ai_engine2)])
    
    # Start the game
    ui.play()
    
    print("Thank you for playing!")

if __name__ == "__main__":
    main()