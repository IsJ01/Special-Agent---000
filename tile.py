import pygame
from groups import platforms, all_sprites
from settings import *
from load_image import load_image


# один из гланых классов - класс блоков
class Tile(pygame.sprite.Sprite):
    # конструктор принимает на себя режим, и координаты
    def __init__(self, mode, x, y):
        self.mode = mode
        super().__init__(platforms, all_sprites)
        self.mods = {'wall': 'wall2.png', 'platform': 'texture1.png',
                     'box': 'box.png', 'design': 'design.png', 'design2': 'texture2.png',
                     'ceiling': 'ceiling.png', 'troll': 'troll.png', 'void': 'void.png'}
        # получение изображения
        self.image = load_image(self.mods[mode])
        self.image = pygame.transform.scale(self.image, (30, 30))
        # сжатие в случае, если размер больше 30px
        self.image.set_colorkey(-1)
        self.rect = self.image.get_rect()
        # получение координат
        self.rect.x, self.rect.y = x * tile_width, y * tile_height
        self.pos = (x, y)

    # метод перемещает данный блок
    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = (x, y)

    # метод возвращает координаты
    def get_pos(self):
        return self.pos