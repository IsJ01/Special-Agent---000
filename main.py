import pygame
from load_image import load_image
from level import load_level, generate_level, maps
from groups import *
from start_screen import start_screen
from move import move
from settings import *
from get_message import get_message
from message import message
import sqlite3


def kill_sprites():
    for sprite in platforms:
        sprite.kill()
    for sprite in hero_group:
        sprite.kill()
    for sprite in tablets:
        sprite.kill()
    for sprite in bullets:
        sprite.kill()
    for sprite in robot_group:
        sprite.kill()
    for sprite in doc:
        sprite.kill()
    for sprite in robot_group:
        sprite.kill()
    for sprite in drugs:
        sprite.kill()
    for sprite in guns:
        sprite.kill()



# в файле main выполняется сама игра
# в переменной SCORE хранятся очки игрока
SCORE = 0
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Спец Агент 000')
pygame_icon = pygame.image.load('icon.ico')
pygame.display.set_icon(pygame_icon)
running = True
clock = pygame.time.Clock()
level = load_level(maps.pop(0))
background = load_image('background.png')
player, x, y = generate_level(level)
key = pygame.key.get_pressed()
# вызов start_screen
name = start_screen(screen)
# получение разговоров персонажа из файла plot.txt в папке data и в дальнейшем
with open('data/plot.txt', encoding='utf-8') as file:
    messages = [i.replace('\n', '') for i in file.read().split('.')]
with sqlite3.connect('game.db') as con:
    cur = con.cursor()
while running:
    # если здоровье игрока меньше 1, то выводится экран поражения
    if player.xp <= 0:
        if name:
            old_score = cur.execute(f'SELECT score from score WHERE name = "{name}"').fetchall()[0][0]
            if old_score < SCORE + player.score:
                cur.execute(f'UPDATE score SET score = {SCORE + player.score} WHERE name = "{name}"')
                con.commit()
        get_message(screen, [':(', f'Счет: {SCORE + player.score}'], 'black')
        # удаление лишних спрайтов
        kill_sprites()
        maps = ['map.map', 'map2.map', 'map3.map']
        level = load_level(maps.pop(0))
        player, x, y = generate_level(level)
        SCORE = 0
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.at_drug()  # если игрок возле лекарства, то он лечится
        if guns.sprites():
            if player.at_gun():
                guns.sprites()[0].pick_up(player)
        # если игрок возле документа, то все спрайты удаляются и выводится экран победы
        if doc.sprites():
            if player.at_doc():
                kill_sprites()
                if name:
                    # добавление рекорда, если тот больше предыдущего
                    old_score = cur.execute(f'SELECT score from score WHERE name = "{name}"').fetchall()[0][0]
                    if old_score < SCORE + player.score:
                        cur.execute(f'UPDATE score SET score = {SCORE + player.score} WHERE name = "{name}"')
                        con.commit()
                get_message(screen, ['Поздравляем!', f'Счет: {SCORE + player.score}'], 'black', True)
                running = False
        # если игрок возле документа, то все спрайты удаляются и заменяются на новый спрайты следующего уровня
        if player.at_tablet():
            # если игрок на 3 уровне
            if maps[0] == 'map3.map':
                messages.append('...')
            # увеличение счетчика
            SCORE += player.get_score()
            kill_sprites()
            level = load_level(maps.pop(0))
            player, x, y = generate_level(level)
    # вызов функции move в случае нажатия клавиш
    if key[pygame.K_a]:
        move(player, 'left', level, platforms, tablets, robot_group, doc, guns, drugs)
    if key[pygame.K_d]:
        move(player, 'right', level, platforms, tablets, robot_group, doc, guns, drugs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # если нажата ЛКМ, то игрок начинает стрелять и воспроизводится звук выстрела
                player.shoot(event.pos)
    # в этом участке кода идет отрисовка и обновление спрайтов
    screen.blit(background, (0, 0))
    bullets.draw(screen)
    if bullets.sprites():
        for sprite in bullets.sprites():
            sprite.move()
    drugs.draw(screen)
    robot_group.draw(screen)
    robot_group.update()
    tablets.draw(screen)
    hero_group.draw(screen)
    hero_group.update()
    platforms.draw(screen)
    doc.draw(screen)
    doc.update()
    guns.draw(screen)
    guns.update()
    for sprite in buttons:
        sprite.draw(screen)
    pygame.display.flip()
    # а тут выводятся сообщения
    if messages:
        message(screen, messages.pop(0))
    clock.tick(FPS)
pygame.quit()