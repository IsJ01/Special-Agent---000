import pygame
from settings import *
from groups import drugs
from load_image import load_image


# данный класс нужен для того, чтобы игрок мог вылечить себя
class Drug(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(drugs)
        self.image = load_image('medicine.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height
        self.pos = (x, y)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = (x, y)

    def get_pos(self):
        return self.pos

    # метод, лечащий игрока
    def heal_(self, hero):
        if hero.xp <= 12:
            hero.xp += 8
        else:
            hero.xp += 20 - hero.xp