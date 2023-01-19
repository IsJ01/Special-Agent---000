import pygame
from groups import doc, all_sprites
from settings import *
from load_image import load_image


# на данном классе внимание заострать не стану, ибо это тоже самое,
# что и Tablet, но вместо нового уровня завершает игру
class Secret(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(doc, all_sprites)
        self.image = load_image('doc.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * tile_width, y * tile_height
        self.pos = (x, y)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = (x, y)