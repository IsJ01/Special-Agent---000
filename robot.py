import pygame
from bullet import Bullet
from load_image import load_image
from groups import robot_group, hero_group, platforms
from settings import *


# это класс робота
class Robot(pygame.sprite.Sprite):
    # класс принимает в конструктор класса x, y, level
    def __init__(self, x, y, level):
        super().__init__(robot_group)
        # self.cur_frame - переменная, в которой хранится номер нынешнего фрейма.
        self.cur_frame = 0
        # эти image переменные хранят в себе текстуры игрока и игрока при движении
        self.image = load_image('robot.png', -1)
        self.image_s = load_image('robot.png', -1)
        self.image_m = load_image('robot_move.png', -1)
        self.image_m2 = load_image('robot_move_2.png', -1)
        self.image_s = pygame.transform.scale(self.image_s, (40, 40))
        self.image_m = pygame.transform.scale(self.image_m, (40, 40))
        self.image_m2 = pygame.transform.scale(self.image_m2, (40, 40))
        self.image_s.set_colorkey(-1)
        self.image_m.set_colorkey(-1)
        self.image_m2.set_colorkey(-1)
        # список с фреймами.
        self.frames = [self.image_s, self.image_m, self.image_m2]
        # тут задается изображение
        self.image = self.frames[0]
        self.image.set_colorkey(-1)
        # создание прямоугольника
        self.rect = self.image.get_rect()
        # тут задаются координаты.
        self.rect.x, self.rect.y = x * tile_width, y * tile_height - 10
        # создание переменной класса clock
        self.clock = pygame.time.Clock()
        # переменная итераций
        self.iteration = 0
        self.pos = [int(self.rect.x / tile_width), int(self.rect.y / tile_width)]
        # скорость
        self.speed = 2
        # переменная уровня
        self.level = level
        # здоровье
        self.xp = 20
        # шаг
        self.F = 1
        self.clock = pygame.time.Clock()
        # скорость Y
        self.Y_speed = 10
        # урон
        self.damage = 3

    # метод, передвигающий робота
    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = (x, y)

    # метод стреляющий в цель
    def shoot(self, pos):
        Sound = pygame.mixer.Sound('data/shoot.mp3')
        Sound.play()
        bullet = Bullet(self.rect.x, self.rect.y)
        bullet.setGoal(pos, self)

    # метод гравитации
    def gravity(self):
        # робот падает вниз, если под ним нет блоков
        self.rect.y += self.Y_speed
        if self.Y_speed > 0:
            for sprite in platforms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.y = sprite.rect.top - tile_height - 10

    # это тоже метод move только он перемещает робота при виде игрока
    def move_(self, F):
        self.image = self.frames[self.cur_frame]
        self.rect.x += F
        self.cur_frame += 1
        self.cur_frame %= 3

    # метод update
    def update(self):
        # re_image - это отзеркаленое изображение
        self.re_image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
        self.re_image.set_colorkey(-1)
        # x - переменная для поиска игрока
        x = 20
        # see - переменная показывающая, видит ли робот игрока или нет.
        see = False
        # 7 - поле зрения игрока
        for i in range(7):
            try:
                # если x координата плюс x деленной на ширину блоков будет равнятся
                # x координате игрока деленной на ширину блоков и разница в высоте не более 60,
                # то робот его увидит, если нет, то x увеличивается на 20
                if (self.rect.x + x) // tile_width == hero_group.sprites()[0].rect.x // tile_width\
                        and abs(self.rect.y - hero_group.sprites()[0].rect.y) <= 60 and x:
                    see = True
                    self.F = 10
                    self.image = self.frames[self.cur_frame]
                    break
                x += 20
            except IndexError:
                pass
        # тут в случае, если робот не увидил в правом направлении, робот будет искать его в левои
        if not see:
            x = 20
            for i in range(7):
                try:
                    if (self.rect.x - x) // tile_width == hero_group.sprites()[0].rect.x // tile_width\
                            and abs(self.rect.y - hero_group.sprites()[0].rect.y) <= 60:
                        self.F = -10
                        see = True
                        self.image = self.re_image
                        break
                    x += 20
                except IndexError:
                    pass
        # если робот увидит игрока, то каждые пять итераций
        # он будет двигаться в его сторону, если расстояние между ними больше 89, а также стрелять в него
        if see:
            if self.iteration % 5 == 0:
                if self.F > 0:
                    self.shoot([self.rect.x + x, self.rect.y])
                else:
                    self.shoot([self.rect.x - x, self.rect.y])
            if x >= 90:
                self.move_(self.F)
        self.gravity()
        self.iteration += 1
        self.clock.tick(FPS)