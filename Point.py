class Point:
    def __init__(self, colour: int, x: int, y: int, main=True):
        self.colour = colour
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
