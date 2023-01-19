import pygame
import os


# фунция загрузки изображения
def load_image(name, color_key=None):
    # полный путь в папку data
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            # если фона нет
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image