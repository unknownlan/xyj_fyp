import pygame
import sys
import os

# Get the project root directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from GUI.textures import *
from GUI.constants import *
from GUI.button import Button, RadioGroupElement, RadioGroup


class GUI:
    s_h = SCREEN_HEIGHT
    s_w = SCREEN_WIDTH

    def __init__(self, win, last_winner=None):
        self.win = win
        self.quit = False
        self.play = 0
        self.white_selection = "Human"  
        self.black_selection = "Human"
        self.last_winner = last_winner
        self._init()
    
    ## start of code i wrote

    def _init(self):

        #play_button
        self.play_button = Button(self.win, (250, 350, 160, 50), state=0,
                                  color=WHITEW, corner_radius=10, hover_color=GREENW, disabled_color=GRAY,
                                  font=font_render('f_2', 30), font_values=("Play", 30, BLACK))
        
        #quit_button
        self.quit_button = Button(self.win, (550, 350, 160, 50),
                                  color=WHITEW, corner_radius=10, hover_color=REDW, disabled_color=GRAY,
                                  font=font_render('f_2', 30), font_values=("Quit", 30, BLACK))

        self.white_human = RadioGroupElement(self.win, 1, t_easy_d, t_easy, t_easy)
        self.white_kane = RadioGroupElement(self.win, 2, t_okay_d, t_okay, t_okay)
        self.white_abel = RadioGroupElement(self.win, 3, t_hard_d, t_hard, t_hard)
        self.white_selection_group = RadioGroup(
            [self.white_human, self.white_kane, self.white_abel], 100, 250, 120
        )

        self.black_human = RadioGroupElement(self.win, 4, t_easy_d, t_easy, t_easy)
        self.black_kane = RadioGroupElement(self.win, 5, t_okay_d, t_okay, t_okay)
        self.black_abel = RadioGroupElement(self.win, 6, t_hard_d, t_hard, t_hard)
        self.black_selection_group = RadioGroup(
            [self.black_human, self.black_kane, self.black_abel], 500, 250, 120
        )

    def draw(self):
        self.draw_window()

        # title
        title = font_render("f_2", 40)
        title_txt = "C H E C K E R S"
        title_w, title_h = title.size(title_txt)
        self.win.blit(
            title.render(title_txt, 1, WHITE), ((self.s_w - title_w) // 2, 50)
        )

        # left title
        left_title = font_render("f_2", 25)
        left_title_txt = "White Player:"
        self.win.blit(
            left_title.render(left_title_txt, 1, WHITE), (100, 200)
        )

        # right title 
        right_title = font_render("f_2", 25)
        right_title_txt = "Black Player:"
        self.win.blit(
            right_title.render(right_title_txt, 1, WHITE), (500, 200)
        )

        # draw buttons
        self.play_button.draw()
        self.quit_button.draw()
        self.white_selection_group.draw()
        self.black_selection_group.draw()

    ## end of code i wrote

    def update(self):
        pygame.display.update()

    def draw_window(self):
        self.win.blit(t_bg, (0, 0))

    def run(self):
        self.play_button_f()
        self.quit_button_f()
        self.radio_group_f()

        if (
            self.white_selection_group.selected is not None
            and self.black_selection_group.selected is not None
        ):
            self.play_button.state = 1
        else:
            self.play_button.state = 0

    def play_button_f(self):
        if self.play_button.get_action():
            self.play = 1

    def quit_button_f(self):
        if self.quit_button.get_action():
            self.quit = True

## start of code i wrote

    def radio_group_f(self):
        # update White Player 
        white_selected = self.white_selection_group.get_selected()
        if white_selected == 1:
            self.white_selection = "Human"
        elif white_selected == 2:
            self.white_selection = "Kane"
        elif white_selected == 3:
            self.white_selection = "Abel"

        # update Black Player
        black_selected = self.black_selection_group.get_selected()
        if black_selected == 4:
            self.black_selection = "Human"
        elif black_selected == 5:
            self.black_selection = "Kane"
        elif black_selected == 6:
            self.black_selection = "Abel"
            
    def return_v(self):
        
        print(f"White Selection: {self.white_selection}, Black Selection: {self.black_selection}")
      
        return self.white_selection, self.black_selection

def draw_text(surface, text, size, x, y, color=WHITE):
    """Helper functions for drawing text"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def show_game_result(surface, winner):
    """Show game results"""
    print(f"Showing game result for winner: {winner}")  # Debugging Information
    
    # Creating a semi-transparent background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    surface.blit(overlay, (0, 0))
    
    # show winner
    if winner == WHITE:
        text = "white wins!"
        print("Showing WHITE winner")
    elif winner == BLACK:
        text = "Black wins!"
        print("Showing BLACK winner")
    else:
        text = "No winner!"
        print("Showing DRAW")
    
    try:
        # Plotting the resultant text
        draw_text(surface, text, 72, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, RED)
        draw_text(surface, "press any key to continue...", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, WHITE)
        pygame.display.update()
        
        # Waiting for user keystrokes or timeout
        waiting = True
        start_time = pygame.time.get_ticks()
        while waiting:
            current_time = pygame.time.get_ticks()
            if current_time - start_time > 3000:  # 3s timeout
                break
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    
    except Exception as e:
        print(f"Error showing game result: {e}")
        import traceback
        traceback.print_exc()

def show_end_screen(winner):
    """Show game over page"""
    # create windows
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    
    # Create Button - Restart Button uses green colour
    restart_button = Button(WIN, (250, 400, 160, 50),
                          color=GREENW, corner_radius=10, hover_color=GREEN,
                          font=font_render('f_2', 30), font_values=("Restart", 30, WHITE))
    
    # Quit button red
    quit_button = Button(WIN, (550, 400, 160, 50),
                        color=REDW, corner_radius=10, hover_color=RED,
                        font=font_render('f_2', 30), font_values=("Quit", 30, WHITE))
    
    clock = pygame.time.Clock()
    FPS = 60
    
    while True:
        clock.tick(FPS)
        
        # white background
        WIN.fill(WHITE)
        
        # show text
        winner_text = "White win!" if winner == WHITE else "Black win!"
        winner_font = font_render("f_2", 72)
        winner_w, winner_h = winner_font.size(winner_text)
        WIN.blit(
            winner_font.render(winner_text, 1, BLACK),
            ((SCREEN_WIDTH - winner_w) // 2, 200)
        )
        
        # draw button
        restart_button.draw()
        quit_button.draw()
        
        # update
        pygame.display.update()
        
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # check action button
        if restart_button.get_action():
            return True
        if quit_button.get_action():
            pygame.quit()
            sys.exit()

def main_gui(last_winner=None):
    """Main GUI function"""
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Checkers - Select Players")
    
    gui = GUI(WIN, last_winner)
    clock = pygame.time.Clock()
    FPS = 60

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gui.draw()
        gui.run()
        gui.update()

        if gui.quit:
            pygame.quit()
            sys.exit()
        
        if gui.play:
            selections = gui.return_v()
            return selections

if __name__ == "__main__":
    main_gui()

## end of code i wrote