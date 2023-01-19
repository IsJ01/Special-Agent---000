import pygame
from load_image import load_image
from bullet import Bullet
from groups import platforms, all_sprites, hero_group, tablets, doc, guns, drugs
from settings import *


# класс игрока
class Player(pygame.sprite.Sprite):
    # класс принимает в конструктор класса x, y, level, группу.
    def __init__(self, x, y, level, *group):
        super().__init__(*group)
        # self.cur_frame - переменная, в которой хранится номер нынешнего фрейма.
        self.cur_frame = 0
        # эти image переменные хранят в себе текстуры игрока и игрока при движении
        self.image_s = load_image('Hero.png', -1)
        self.image_m = load_image('Hero_move.png', -1)
        self.image_m2 = load_image('Hero_move2.png', -1)
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
        # создание прямоугольника
        self.rect = self.image.get_rect()
        # тут задаются координаты.
        self.rect.x, self.rect.y = x * tile_width, y * tile_height - 10
        # создание переменной класса clock
        self.clock = pygame.time.Clock()
        # переменная итераций
        self.iteration = 0
        self.pos = [int(self.rect.x / tile_width), int(self.rect.y / tile_width)]
        # скорость по y координате
        self.Y_speed = 0
        # скорость по x
        self.speed = 2
        # переменная уровня
        self.level = level
        # пиксели, пройденные при прыжке
        self.jump_px = 0
        # здоровье игрока
        self.xp = 20
        # очки игрока
        self.score = 0
        # урон игрока
        self.damage = 2

    def get_score(self):
        return self.score

    # метод, стреляющий пулями, принимающий на себя позицию для стрельбы
    def shoot(self, pos):
        Sound = pygame.mixer.Sound('data/shoot.mp3')
        Sound.play()
        # создание объекта класса bullet
        bullet = Bullet(self.rect.x, self.rect.y)
        # вызыв метода, определяющий цель для пули
        bullet.setGoal(pos, self)

    # метод перемещающий игрока
    def move(self, x, y):
        self.pos = [x, y]

    # метод гравитации
    def gravity(self):
        # увеличение y координаты на self.Y_speed
        self.rect.y += self.Y_speed
        # проверка в случае, если скорость меньше 0
        if self.Y_speed < 0:
            # увеличение количества пикселей, которые прошел игрок при прыжке
            self.jump_px += abs(self.Y_speed)
            # проверка если количество пикселей больше 119 или игрок столкнулся
            # с блоком, то скорость мы меняем на 10, а количество пикселей
            # обнуляем и выходим из цикла
            for sprite in platforms:
                if self.jump_px >= 120:
                    self.Y_speed = 10
                    self.jump_px = 0
                    break
                elif pygame.sprite.collide_mask(self, sprite):
                    self.rect.y = sprite.rect.bottom
                    self.Y_speed = 10
                    self.jump_px = 0
                    break
        # если скорость больше 0, то мы падаем вниз, до тех пор пока игрок
        # не оказывается на полу и координату y меняем на y координату блока,
        # которая минусуется на высоту игрока и выходим из цикла
        if self.Y_speed > 0:
            for sprite in platforms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.y = sprite.rect.top - self.rect.height
                    break

    # метод, проверяющий на то, стоит ли игрок у лекарства
    def at_drug(self):
        if drugs.sprites():
            for sprite in drugs.sprites():
                if pygame.sprite.collide_mask(self, sprite):
                    sprite.heal_(self)
                    sprite.kill()
                    return True

    # метод, проверяющий на то, стоит ли игрок у документа
    def at_doc(self):
        if doc.sprites():
            if pygame.sprite.spritecollideany(self, doc):
                return True

    # метод, проверяющий на то, стоит ли игрок у таблички
    def at_tablet(self):
        if pygame.sprite.spritecollideany(self, tablets):
            return True

    def at_gun(self):
        if guns.sprites():
            if pygame.sprite.spritecollideany(self, guns):
                return True

    # метод update
    def update(self):
        key = pygame.key.get_pressed()
        # если нажата клавиша d, то мы перемещаемся вправо
        if key[pygame.K_d]:
            # мы проверяем перемещаем персонажа, и если он столкнулся с блоком,
            # то перемещаем его назад
            self.rect.x += self.speed
            for sprite in platforms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.x = sprite.rect.left - tile_width
            # изображение меняется на следующий фрейм
            self.image = self.frames[self.cur_frame]
            # номер фрейма тоже меняется
            self.cur_frame = (self.cur_frame + 1) % 3
        # тут функционал тот же, что и у клавиши влево
        if key[pygame.K_a]:
            self.rect.x -= self.speed
            for sprite in platforms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.x = sprite.rect.right - 10
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
                self.image.set_colorkey(-1)
                self.cur_frame = (self.cur_frame + 1) % 3
        # если клавиша space нажата, то мы проверяем игрока
        # на возможность прыгнуть вверх и если это так, то скорость меняется на -10
        if key[pygame.K_SPACE]:
            self.rect.y += 1
            for sprite in platforms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.y = sprite.rect.top - tile_height - 10
                    self.Y_speed = -10
                    break
        # если количество итераций кратно 6, то мы вызываем метод self.clock.tick(10)
        if self.iteration % 6 == 0:
            self.clock.tick(10)
        # счетчик итераций увеличивается
        self.iteration += 1
        # вызов метода gravity
        self.gravity()
        # устанавливаем fps
        self.clock.tick(FPS)