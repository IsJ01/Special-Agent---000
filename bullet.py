import pygame
from groups import bullets, robot_group, hero_group, platforms
from settings import *


# класс bullet является классом пуль
class Bullet(pygame.sprite.Sprite):
    # конструктор принимает на себя координаты
    def __init__(self, x, y):
        super().__init__(bullets)
        # тут создаются прямоугольник, изображение оранжевого цвета
        self.rect = pygame.Rect(x + tile_width / 2, y + tile_height / 2, 1, 1)
        self.image = pygame.Surface((1, 1))
        self.image.fill('orange')
        self.pos = None
        self.entity = None
        # переменная хранящая в себе скорость шага
        self.F = 0
        self.clock = pygame.time.Clock()
        # количетсво пройденных пикселей
        self.px = 0

    # метод, получающий координаты цели и стреляющий объект
    def setGoal(self, pos, entity):
        self.entity = entity
        self.pos = pos
        # в случае если цель правее, то шаг равен 3, в противном случае -3
        if self.rect.x < pos[0]:
            self.F = 3
        if self.rect.x > pos[0]:
            self.F = -3

    # фунция перемещения пули
    def move(self):
        # само перемещение пули
        self.rect.move_ip(self.F, 0)
        # увеличение px на F
        self.px += self.F
        # мы пробегаемся в цикле по группам роботов и игрока и если тип группы
        # не такой, как у self.entity, то мы пробегаемся по его спрайтам и
        # если пуля достигает спрайта, то его здоровье уменьшается
        # на damage стреляющего объекта, но если xp спрайта меньше 1,
        # то он исчезает и если стреляющим был игрок, то его очки увеличивается на 1
        for group in robot_group, hero_group:
            if group not in self.entity.groups():
                for sp in group:
                    if pygame.sprite.collide_mask(self, sp):
                        sp.xp -= self.entity.damage
                        if sp.xp <= 0:
                            if self.entity is hero_group.sprites()[0]:
                                self.entity.score += 1
                            sp.kill()
                        self.kill()
        # но если пуля попадет в блок или она попадет в точку,
        # в которую направлялась пуля, либо путь будет равен 300, то она пропадет
        if self.rect.x // 10 * 10 == self.pos[0] // 10 * 10 or\
                pygame.sprite.spritecollideany(self, platforms) or abs(self.px) == 150:
            self.kill()