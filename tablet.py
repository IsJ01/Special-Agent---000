import pygame
from settings import *
from groups import tablets
from load_image import load_image


# данный класс нужен для того, чтобы игрок мог перейти на новый
# уровень и в остальном фунционале идентичен классу Tile
class Tablet(pygame.sprite.Sprite):
    def __init__(self, x, y, F):
        super().__init__(tablets)
        self.image = load_image('tablet.png')
        if F < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image.set_colorkey(-1)
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height
        self.pos = (x, y)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = (x, y)

    def get_pos(self):
        return self.pos