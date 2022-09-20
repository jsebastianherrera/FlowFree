from random import randint


class Point:
    def __init__(self, colour: int, x: int, y: int, main=True, random=False):
        self.colour = colour
        if random:
            x, y = self._randomize_point(x, y)
        self.x = x
        self.y = y
        self.main = main

    def __str__(self):
        return '('+str(self.x)+','+str(self.y) + ',' + str(self.colour)+')'

    def __eq__(self, o):
        if self.x == o.x and self.y == o.y:
            return True
        else:
            return False

    def _randomize_point(self, row, col) -> tuple[int, int]:
        return randint(0, row-1), randint(0, col - 1)
