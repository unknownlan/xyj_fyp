import pygame
from .constants import *
from copy import deepcopy


class Piece(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.color = color
        self.row = row
        self.col = col
        self.x, self.y = 0, 0
        self.calc_pos()
        self.king = False
        if self.color == WHITE:
            self.image = texture01
        else:
            self.image = texture02
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.sprite_group = pygame.sprite.GroupSingle()
        self.sprite_group.add(self)

    def calc_pos(self):
        self.x = int(SQUARE_SIZE*(self.col+0.5))
        self.y = int(SQUARE_SIZE*(self.row+0.5))

    def make_king(self):
        self.king = True

    def draw_piece(self, win):
        self.sprite_group.draw(win)
        self.sprite_group.update()

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
        self.sprite_group.update()

    def update(self):
        if self.king:
            if self.color == WHITE:
                self.image = texture05
            elif self.color == BLACK:
                self.image = texture06
        self.rect.center = self.x, self.y
## start of code i wrote
    def __repr__(self):
        # return self.color
        return f"Piece(color={self.color}, row={self.row}, col={self.col})"
## end of code i wrote
    def __str__(self):
        return f"{self.color}, {self.row}, {self.col}"

    def copy(self):
        copyobj = Piece(self.row, self.col, self.color)
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj
