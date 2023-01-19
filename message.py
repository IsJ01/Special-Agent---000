import sys

from settings import *
import pygame


# эта функция выводит на экран сообщения во время самой игры
# перенос на слоги внимания не обращает
# фунция в остальном от фунции get_message не отличается
def message(screen, message):
    font = pygame.font.Font(None, 15)
    # текст с сообщениями
    text = []
    part_text = ''
    for i in range(1, len(message) + 1):
        part_text += message[i - 1]
        if i % 80 == 0:
            # перенос строки
            text.append(part_text)
            part_text = ''
        if i == len(message):
            text.append(part_text)
    text_coord = size[1] * 0.8 + 20
    for mes in text:
        string_rendered = font.render(mes, True, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False