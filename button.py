import pygame
from groups import *


# класс кнопки принимает на себя x, y, w, h, color
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, col, text):
        super().__init__(buttons)
        font = pygame.font.Font(None, 20)
        self.b_text = font.render(text, True, col)
        self.b_x = x + (w - self.b_text.get_width()) // 2
        self.b_y = y + (h - self.b_text.get_height()) // 2
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.col = col

    # метод отрисовки
    def draw(self, sc):
        pygame.draw.rect(sc, self.col, self.rect, 1)
        sc.blit(self.b_text, (self.b_x, self.b_y))

    def run(self,  *args):
        if args:
            self.func(*args)
        else:
            self.func()

    # метод проверяющий кнопку на нажатие и выполняющий функцию
    def is_clicked(self, pos,):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1) \
                and pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
            return True

    # метод задающий функцию при нажатии и ее аргументы
    def clicked(self, func):
        self.func = func