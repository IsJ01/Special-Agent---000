from settings import *
from load_image import load_image
from groups import *
import pygame


# это небольшой класс Gun, то есть это пистолет, который главный
# герой может подобрать
class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(guns)
        self.image = load_image('gun.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * tile_width, y * tile_height + 15

    # данный метод принимает на себя стрелка, который поднял этот пистолет
    # и его урон увеличится на две единицы
    def pick_up(self, shooter):
        shooter.damage += 2
        self.kill()

    def move(self, x, y):
        self.rect.move_ip(x, y)