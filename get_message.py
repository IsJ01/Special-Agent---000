from settings import *
from load_image import load_image
import sys
import pygame
# функция предназанченная для вывода какой-либо информации на пустой экран.


# аргументы: экран, список с сообщениями и цвет текста
def get_message(sc, mess, col, run=False):
    if run:
        sc.blit(load_image('background.png'), (0, 0))
    # создание шрифта
    font = pygame.font.Font(None, 20)
    running = True
    # начальная позиция по y координате
    text_y = size[1] // 2 - 40
    # мы пробегаемся по списку и отрисовываем текст
    for mes in mess:
        # текст
        string_rendered = font.render(mes, True, pygame.Color(col))
        intro_rect = string_rendered.get_rect()
        # настройка координат
        intro_rect.x = (size[0] - intro_rect.w) // 2
        intro_rect.y = text_y
        text_y += 20
        sc.blit(string_rendered, intro_rect)
    pygame.display.flip()
    # в данном цикле игра ожидает пока игрок не нажмет мышкой по экрану, либо не выйдет из игры.
    if run:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
        sc.fill('black')