## start of code I  wrote 
import pygame
import sys
import os

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from GUI.gui import main_gui, show_end_screen
from main_board import main_board

def main():
    try:
        # init pygame
        pygame.init()
        
        last_winner = None
        
        while True:
            # get player
            selections = main_gui(last_winner)
            if selections:
                white_type, black_type = selections
                print(f"Selected players: White - {white_type}, Black - {black_type}")
                
                # start game
                winner = main_board(3, white_type=white_type, black_type=black_type)
                
                if winner is not None:
                    # show game end page
                    if show_end_screen(winner):
                        # If you choose to restart, update last_winner and continue the loop
                        last_winner = winner
                        pygame.quit()
                        pygame.init()
                        continue
                    else:
                        # If you choose to exit, end the programme
                        break
            
    except Exception as e:
        print(f"Game error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()

## end of code I  wrote 