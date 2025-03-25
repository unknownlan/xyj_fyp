## start of code i wrote
import pygame
import sys
import os
from Checkers.constants import *
from Checkers.board import *
from Checkers.piece import *
from Checkers.game import *
from Checkers.kane_algo import minimax, move_minimax
from Checkers.abel_algo import AbelPPOAI
from CheckersEnv import CheckersEnv
from GUI.gui import show_game_result
from stable_baselines3 import PPO
import time

def get_mouse_pos(pos):
    x, y = pos
    row = int(y // SQUARE_SIZE)
    col = int(x // SQUARE_SIZE)
    return row, col

def main_board(diff:int, white_type="Kane", black_type="Kane", callback=None):
    # Make sure pygame is initialised
    if not pygame.get_init():
        pygame.init()
    
    # Creating a game window
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Checkers - Game")
    
    # Creating a Game Example
    game = Game(WIN, white_type=white_type, black_type=black_type)
    clock = pygame.time.Clock()
    FPS = 60
    run = True
    
    print(f"Game started with White: {white_type}, Black: {black_type}")
    print(f"Initial turn: {'BLACK' if game.turn == BLACK else 'WHITE'}")

    # Ensure that the first drawing
    game.update()
    pygame.display.update()

    while run:
        clock.tick(FPS)
        
        # Check if the game is over
        winner = game.winner()
        if winner is not None:
            print(f"Game over! Winner: {'WHITE' if winner == WHITE else 'BLACK'}")
            # Last update shows
            game.update()
            pygame.display.update()
            pygame.time.delay(500)  # short delay
            return 'WHITE' if winner == WHITE else 'BLACK'

        # Handling user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ((game.turn == WHITE and white_type == "Human") or 
                    (game.turn == BLACK and black_type == "Human")):
                    pos = pygame.mouse.get_pos()
                    row, col = get_mouse_pos(pos)
                    game.select(row, col)

        # AI move logic
        if game.turn == WHITE and white_type != "Human":
            print("\nWhite AI's turn")
            start_time = time.time()
            success = handle_ai_move(game, diff)
            if not success:
                print("White AI failed to move")
            
            # Record thinking time
            if callback:
                callback(start_time, 'WHITE')
            
        elif game.turn == BLACK and black_type != "Human":
            print("\nBlack AI's turn")
            start_time = time.time()
            success = handle_ai_move(game, diff)
            if not success:
                print("Black AI failed to move")
            
            # Record thinking time
            if callback:
                callback(start_time, 'BLACK')

        # Update Display
        game.update()
        pygame.display.update()

    return None

def handle_ai_move(game, depth):
    """Handling AI's Action Logic"""
    print(f"\nHandling AI move for {'BLACK' if game.turn == BLACK else 'WHITE'}")
    
    # Check for legal movement
    if not game.check_valid_moves():
        print("No valid moves available")
        game.change_turn()
        return False

    # Perform AI movement
    success = False
    try:
        if game.turn == WHITE:
            if game.white_type == "Kane":
                success = game.kane_ai_move()
            elif game.white_type == "Abel":
                success = game.abel_ai_move(game.white_ai)
        elif game.turn == BLACK:
            if game.black_type == "Kane":
                success = game.kane_ai_move()
            elif game.black_type == "Abel":
                success = game.abel_ai_move(game.black_ai)

        if not success:
            print("AI failed to make a valid move")
            game.board.print_board_state()
    except Exception as e:
        print(f"Error during AI move: {e}")
        import traceback
        traceback.print_exc()
    
    return success

if __name__ == "__main__":
    from GUI.gui import main_gui
    white_selection, black_selection = main_gui()
    main_board(3, white_type=white_selection, black_type=black_selection)

## end of code i wrote