import os
import sqlite3
import subprocess
import sys
import tkinter
import tkinter.ttk as ttk
import pygame

from button import Button
from get_message import get_message
from groups import inputs, buttons
from input_text import Input
from load_image import load_image

with sqlite3.connect('game.db') as con:
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS score (id INTEGER,'
                'name TEXT,'
                'score INTEGER)')
    con.commit()


# функция, выводящая рекорды игроков
def show_statistics():
    # запуск файла
    subprocess.run('statistic_of_game.exe')


# функция, удаляющая из базы игрока
def clear(name):
    with sqlite3.connect('game.db') as con:
        cur = con.cursor()
        cur.execute(f'DELETE from score WHERE name = "{name}"')
        con.commit()


# функция, выводящая нас из начального меню и добавляющая игрока в базу (если он ввел имя)
def stop(name):
    if name:
        with sqlite3.connect('game.db') as con:
            cur = con.cursor()
            names = cur.execute('SELECT name FROM score').fetchall()
            new_id = len(cur.execute('SELECT * FROM score').fetchall()) + 1
            if name not in [i[0] for i in names]:
                cur.execute(f'INSERT INTO score VALUES ({new_id}, "{name}", 0)')
                con.commit()
    for i in buttons:
        i.kill()
    for i in inputs:
        i.kill()


# функция, вызывающая начальное окно
def start_screen(screen):
    font = pygame.font.Font(None, 20)
    # вызов функции get_message с предупреждением
    get_message(screen, ['Warning!',
                         'Данная игра не создана с целью кого-либо унизить или оскорбить,',
                         ' любые совпадения имен, локаций или событий случайны.',
                         'Автор не несет ответсвенность за действия игроков,',
                         ' и вообще он за все хорошее и против всего плохого.'], 'red', True)
    screen.fill('black')
    # вызов функции get_message с названием игры
    get_message(screen, ['Спец Агент 000'], 'black', True)
    screen.fill('black')
    # вызов функции get_message с управлением
    get_message(screen, ['Управление',
                         'A - влево',
                         'D - вправо',
                         'W - перейти на новый уровень',
                         'SPACE - прыжок',
                         'ЛКМ - стрелять'], 'yellow', True)
    # вызов функции с инструкциями
    get_message(screen, ['Для перехода на новый уровень вы должны',
                         'подойти к табличке нажав клавишу W'], 'yellow', True)
    # вызов с пожеланием удачи.
    get_message(screen, ['Удачи'], 'yellow', True)
    screen.blit(load_image('background.png'), (0, 0))
    get_message(screen, ['Введите свое имя'], 'yellow')
    input_ = Input(200, 240, 50, 30, (0, 0, 0), '')
    button = Button(200, 250, 50, 30, (0, 0, 0), 'OK')
    button.clicked(stop)
    button3 = Button(200, 290, 200, 30, (0, 0, 0), 'Статистика')
    button3.clicked(show_statistics)
    button2 = Button(200, 330, 200, 30, (0, 0, 0), 'Удалить из списка')
    button2.clicked(clear)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_.is_clicked(event.pos)
                # проверка кнопок на нажатие и выполнение действий в случае нажатия
                if button3.is_clicked(event.pos):
                    button3.run()
                if button2.is_clicked(event.pos):
                    button2.run(input_.text)
                if button.is_clicked(event.pos):
                    button.run(input_.text)
                    running = False
            if event.type == pygame.KEYDOWN:
                if input_.cl:
                    if event.key != pygame.K_BACKSPACE:
                        input_.write_text(event.unicode)
                    else:
                        if input_.text:
                            screen.blit(load_image('background.png'), (0, 0))
                            input_.text = input_.text[:-1]
                            input_.write_text('')
        get_message(screen, ['Введите свое имя'], 'yellow')
        for i in buttons:
            i.draw(screen)
        for i in inputs:
            i.draw(screen)
        pygame.display.flip()
    screen.fill('black')
    return input_.text