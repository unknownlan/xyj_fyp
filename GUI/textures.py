import pygame
import os
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.font.init()

# Use Pygame's default system fonts instead of custom font files
def font_render(file_code=None, size=40):
    return pygame.font.SysFont(None, size)  # None means the default system font

def texture_resize(texture, factor):
    ratio = texture.get_width(), texture.get_height()
    size = int(factor * ratio[0]), int(factor * ratio[1])
    return pygame.transform.scale(texture, size)

factor1 = 0.4

# Load and resize textures
t_bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bg.png')), (SCREEN_WIDTH, SCREEN_HEIGHT))
t_easy = texture_resize(pygame.image.load(os.path.join("Assets", 'human.png')), factor1)
t_okay = texture_resize(pygame.image.load(os.path.join("Assets", 'kane.png')), factor1)
t_hard = texture_resize(pygame.image.load(os.path.join("Assets", 'abel.png')), factor1)
t_easy_d = texture_resize(pygame.image.load(os.path.join("Assets", 'human_d.png')), factor1)
t_okay_d = texture_resize(pygame.image.load(os.path.join("Assets", 'kane_d.png')), factor1)
t_hard_d = texture_resize(pygame.image.load(os.path.join("Assets", 'abel_d.png')), factor1)
