import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
ROWS, COLS = 8, 8
SCALE_FACTOR = 4, 5
SQUARE_SIZE = SCREEN_WIDTH//ROWS
IMAGE_SIZE = (SQUARE_SIZE*SCALE_FACTOR[0])//SCALE_FACTOR[1], (SQUARE_SIZE*SCALE_FACTOR[0])//SCALE_FACTOR[1]
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
texture01 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "white_piece.png")), IMAGE_SIZE)
texture02 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "black_piece.png")), IMAGE_SIZE)
texture03 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "texture01.png")), (SQUARE_SIZE, SQUARE_SIZE))
texture04 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(r'Assets', "texture02.png")), (SQUARE_SIZE, SQUARE_SIZE)), 90)
texture05 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "white_piece_king.png")), IMAGE_SIZE)
texture06 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "black_piece_king.png")), IMAGE_SIZE)
