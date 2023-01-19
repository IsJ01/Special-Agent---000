from player import Player
from groups import hero_group, all_sprites
from secret_documents import Secret
from tile import Tile
from tablet import Tablet
from robot import Robot
from gun import Gun
from drug import Drug


# список с названиями файлов уровней
maps = ['map.map', 'map2.map', 'map3.map']


# загрузка уровня в папке data
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    # выравнивание уровня
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


# создание уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # здесь # - это блок пола, @ - игрок, С - потолок, w - стена, S - документы, D - табличка вправо,
            # d - табличка влево, R - робот, B - коробка, p - платформа, T - тролл фейс, c - тоже платформа,
            # v - пустота.
            if level[y][x] == '#':
                Tile('platform', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y, level, hero_group, all_sprites)
            elif level[y][x] == 'C':
                Tile('ceiling', x, y)
            elif level[y][x] == 'w':
                Tile('wall', x, y)
            elif level[y][x] == 'S':
                Secret(x, y)
            elif level[y][x] == 'D':
                Tablet(x, y, 1)
            elif level[y][x] == 'd':
                Tablet(x, y, -1)
            elif level[y][x] == 'R':
                Robot(x, y, level)
            elif level[y][x] == 'B':
                Tile('box', x, y)
            elif level[y][x] == 'p':
                Tile('design2', x, y)
            elif level[y][x] == 'T':
                Tile('troll', x, y)
            elif level[y][x] == 'c':
                Tile('design', x, y)
            elif level[y][x] == 'v':
                Tile('void', x, y)
            elif level[y][x] == 'G':
                Gun(x, y)
            elif level[y][x] == 'M':
                Drug(x, y)
    return new_player, x, y