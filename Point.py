from random import randint


class Point:
    def __init__(self, colour: int, rows, cols, flag=True):
        self.colour = colour
        if flag:
            x, y = self._randomize_point(rows, cols)
            self.x = x
            self.y = y
            self.main = True
        else:
            self.x = rows
            self.y = cols
            self.main = False

    def __str__(self):
        return '('+str(self.x)+','+str(self.y) + ',' + str(self.colour)+')'

    def __eq__(self, o):
        if self.x == o.x and self.y == o.y and self.colour == o.colour:
            return True
        else:
            return False

    def _randomize_point(self, rows, cols) -> tuple[int, int]:
        return randint(0, rows - 1), randint(0, cols - 1)
