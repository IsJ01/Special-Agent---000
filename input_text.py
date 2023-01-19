import pygame
from groups import *


# класс поля ввода принимает на себя x, y, w, h, color
class Input(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, col, text):
        super().__init__(inputs)
        self.font = pygame.font.Font(None, 20)
        self.b_text = self.font.render(text, True, col)
        self.b_x = x
        self.b_y = y - 10
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.col = col
        self.text = text
        # эта переменная значит, что игрок пишет именно в этом спрайте
        self.cl = True
        for i in inputs:
            if i != self:
                i.cl = False

    # метод отрисовки
    def draw(self, sc):
        pygame.draw.rect(sc, self.col, (self.rect.x, self.rect.y, self.rect.w, 1), 1)
        sc.blit(self.b_text, (self.b_x, self.b_y))

    # метод проверяющий поле на нажатие
    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1) \
                and pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
            self.cl = True
            for i in inputs:
                if i != self:
                    i.cl = False

    # метод ввода букв
    def write_text(self, word):
        self.text += word
        self.b_text = self.font.render(self.text, True, self.col)
        if len(self.text) * 10 >= self.rect.w:
            self.rect.w = self.b_text.get_width()