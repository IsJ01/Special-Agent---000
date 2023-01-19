import pygame
# данный файл предназначен для хранения в себе групп спрайтов


all_sprites = pygame.sprite.Group()  # почти все спрайты
hero_group = pygame.sprite.Group()  # группа главного героя
robot_group = pygame.sprite.Group()  # группа робото героя
platforms = pygame.sprite.Group()  # группа платформ героя
tablets = pygame.sprite.Group()  # группа табличек героя
bullets = pygame.sprite.Group()  # группа пуль героя
doc = pygame.sprite.Group()  # группа документа героя
guns = pygame.sprite.Group()  # группа пистолета
buttons = pygame.sprite.Group()  # группа кнопок
inputs = pygame.sprite.Group()  # группа кнопок
drugs = pygame.sprite.Group()  # группа лекарств