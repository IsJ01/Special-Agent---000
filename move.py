from camera import Camera
from settings import *
from groups import *
import pygame


# данная функция получает главного героя, перемещение, уровень, группы
def move(hero, movement, level, *groups):
    camera = Camera(level)
    # объект класса камеры
    x, y = hero.rect.x, hero.rect.y
    # в случае шага влево
    if movement == 'left':
        # мы проверяем есть ли стена впереди, подвинув игрока влево,
        # если да, то он отодвигается назад
        hero.rect.x -= hero.speed
        if not pygame.sprite.spritecollideany(hero, platforms):
            # перемещение героя
            hero.move(y / tile_height, (x - hero.speed) / tile_width)
            # обновление камеры
            camera.update(hero)
            # в цикле мы пробегаемся по группам
            for group in groups:
                # пробегамся по спрайтам групп
                for sprite in group:
                    # обновляем их
                    camera.apply(sprite, 3)
        else:
            hero.rect.x += hero.speed
    if movement == 'right':
        # здесь функционал такой, как и у шага влево.
        hero.rect.x += hero.speed
        if not pygame.sprite.spritecollideany(hero, platforms):
            hero.move(y / tile_height, (x + hero.speed) / tile_width)
            camera.update(hero)
            for group in groups:
                for sprite in group:
                    camera.apply(sprite, 4)
        else:
            hero.rect.x -= hero.speed