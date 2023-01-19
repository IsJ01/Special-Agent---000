from settings import *


# это класс камеры, которая следит за персонажем, двигая блоки в противоположную сторону движения персонажа.
class Camera:
    def __init__(self, level):
        self.level = level
        self.dx = 0
        self.dy = 0

    def apply(self, obj, m):
        if m == 3:
            # перемещение влево
            obj.move(-self.dx, 0)
        if m == 4:
            # перемещение вправо
            obj.move(self.dx, 0)

    def update(self, target):
        # отступ по x координате равен скорости персонажа умноженую на 3 раза
        self.dx = -target.speed * 3