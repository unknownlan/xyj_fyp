import pygame
import pygame.gfxdraw
from .textures import *
from .constants import *


class Button(pygame.sprite.Sprite):
    def __init__(self, win, metrics,
                 color=None, hover_color=None, disabled_color=None,
                 texture=None, hover_texture=None, disabled_texture=None,
                 corner_radius=0, state=True,
                 font="Arial", font_values=("Sample Text", 20, BLACK)):
        super().__init__()
        self.win = win
        self.action = False
        self.state = state
        self.color = color
        self.disabled_color = disabled_color
        self.button_color = color
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.x, self.y, self.w, self.h = metrics
        self.image = texture
        self.texture = texture
        self.hover_texture = hover_texture
        self.disabled_texture = disabled_texture
        if texture is not None:
            self.rect = self.image.get_rect()
        elif color is not None:
            self.rect = pygame.Rect(metrics, border_radius=self.corner_radius)
        self.rect.center = self.x, self.y
        self.fonttxt, self.fontsize, self.fontcolor = font_values
        if isinstance(font, pygame.font.FontType):
            self.font = font
        else:
            self.font = pygame.font.SysFont(font, self.fontsize)
        self.font_surf = self.font.render(self.fonttxt, 1, self.fontcolor)
        self.font_rect = self.font_surf.get_rect(center=self.rect.center)
        self.pressed = False
        self.sprite_group = pygame.sprite.GroupSingle()
        self.sprite_group.add(self)

    def draw(self):
        self.state_check()
        if self.image is not None:
            self.win.blit(self.image, self.rect)
        elif self.color is not None:
            self.draw_rounded_rect()
        self.font_draw()
        self.update()

    def update(self):
        self.check_click()

    def font_draw(self):
        self.win.blit(self.font_surf, self.font_rect)

    def draw_rounded_rect(self):
        surface, rect, color, corner_radius = self.win, self.rect, self.color, self.corner_radius
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(
                f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        # need to use anti aliasing circle drawing routines to smooth the corners
        pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius,
                                color)
        pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius,
                                color)

        pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius,
                                     color)
        pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius,
                                     color)
        pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1,
                                     corner_radius, color)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        return mx, my

    def check_click(self):
        mouse_pos = self.get_mouse_pos()
        self.action = False
        if self.state:
            if self.rect.collidepoint(mouse_pos):
                self.color = self.hover_color
                self.image = self.hover_texture
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                elif (not pygame.mouse.get_pressed()[0]) and self.pressed:
                    self.action = True
                    self.pressed = False
            else:
                self.color = self.button_color
                self.image = self.texture

    def get_action(self):
        return self.action

    def state_check(self):
        if not self.state:
            self.color = self.disabled_color
            self.image = self.disabled_texture
        else:
            self.color = self.color
            self.image = self.texture


class RadioGroupElement(pygame.sprite.Sprite):
    def __init__(self, win, idnum, base_texture, select_texture, hover_texture):
        super().__init__()
        self.win = win
        self.id = idnum
        self.texture = base_texture
        self.hover_texture = hover_texture
        self.select_texture = select_texture
        self.image = self.texture
        self.rect = self.image.get_rect()
        self.sprite_group = pygame.sprite.GroupSingle()
        self.pressed = False
        self.selected = False
        self.sprite_group.add(self)

    def draw(self, pos):
        self.rect.center = pos
        self.sprite_group.draw(self.win)
        self.update()

    def update(self):
        self.check_click()
        self.check_selection()

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        return mx, my

    def check_click(self):
        mouse_pos = self.get_mouse_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.hover_texture
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif (not pygame.mouse.get_pressed()[0]) and self.pressed:
                self.selected = not self.selected
                self.pressed = False
        else:
            self.image = self.texture

    def check_selection(self):
        if self.selected:
            self.image = self.select_texture

    def __repr__(self):
        return self.id


class RadioGroup:
    def __init__(self, elements, x, y, padding):
        self.elements = []
        for element in elements:
            if isinstance(element, RadioGroupElement):
                self.elements.append(element)
        self.x, self.y = x, y
        self.padding = padding
        self.selected = None

    def draw(self):
        self.update()
        for index, element in enumerate(self.elements):
            element.draw((self.x+self.padding*index, self.y))

    def update(self):
        self.check_selection()

    def check_selection(self):
        select_state = [x.selected for x in self.elements]
        if True not in select_state:
            self.selected = None
        for element in self.elements:
            if element.pressed:
                self.selected = element
                for e in self.elements:
                    if e != element:
                        e.selected = False

    def get_selected(self):
        if self.selected is not None:
            return self.selected.id
        return None