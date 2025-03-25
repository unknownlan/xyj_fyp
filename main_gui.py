## start of code i wrote
import pygame, sys
from GUI.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from GUI.textures import *
from GUI.gui import GUI


def main_gui():
    FPS = 60
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Checkers")
    main_gui = GUI(WIN)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if main_gui.quit or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if main_gui.play:
            print(f"Play button clicked. White: {main_gui.white_selection}, Black: {main_gui.black_selection}")
            run = False
        main_gui.run()
        main_gui.draw()
        main_gui.update()

    # return main_gui.difficulty
    return main_gui.white_selection, main_gui.black_selection
    


if __name__ == '__main__':
    selections = main_gui()
    print(f"Returned players: White - {selections[0]}, Black - {selections[1]}")
## end of code i wrote