from random import randint


class Point:
    def __init__(self, colour: int, size: int, flag=True):
        self.colour = colour
        x, y = self._randomize_point(size)
        self.x = x
        self.y = y
        self.main = flag

    def __str__(self):
        return '('+str(self.x)+','+str(self.y) + ',' + str(self.colour)+')'

    def __eq__(self, o):
        if self.x == o.x and self.y == o.y:
            return True
        else:
            return False

    def _randomize_point(self, size) -> tuple[int, int]:
        return randint(0, size - 1), randint(0, size - 1)
