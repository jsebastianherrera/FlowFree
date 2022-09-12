import curses
from Point import Point


class Grid:
    def __init__(self, rows: int, col: int):
        self.flows = 0
        self._enter = (False, None)
        self.rows = rows
        self.cols = col
        self._points = {}
        self.starting_points = []
        self.grid = [[None for _ in range(self.rows)]
                     for _ in range(self.cols)]
        self._randomize_starting_points()
        self._init_grid()

    def print_grid(self, stdsrc, x, y):
        stdsrc.clear()
        hmax, wmax = stdsrc.getmaxyx()
        h = hmax//2 - self.cols
        w = wmax//2 - self.rows
        if self._enter[0]:
            stdsrc.addstr(1, 1, 'XXXXX',
                          curses.color_pair(self._enter[1].colour))
        stdsrc.addstr(h-2, w-2, '('+str(x)+','+str(y) + ')')
        stdsrc.addstr(
            h-2, w+2, ' | flows:('+str(self.flows)+','+str(self.rows) + ')')
        x_ = 0
        y_ = 0
        for i in range(0, self.rows):
            y_ = 0
            for j in range(0, self.cols):
                if self.grid[i][j] is None:
                    if x == i and y == j:
                        stdsrc.addstr(h+y_, w+x_, "00",
                                      curses.color_pair(3))
                    else:
                        stdsrc.addstr(h+y_, w+x_, "00",
                                      curses.color_pair(2))
                else:
                    stdsrc.addstr(
                        h+y_, w+x_,
                        "00", curses.color_pair(self.grid[i][j].colour))
                y_ += 2
            x_ += 3
        stdsrc.refresh()

    def clean_grid(self, colour=2):
        if colour > 2:
            for i in range(self.rows):
                for j in range(self.cols):
                    xy = self.grid[i][j]
                    if xy is not None and xy.colour == colour and not xy.main:
                        self.grid[i][j] = None
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    xy = self.grid[i][j]
                    if xy is not None and not xy.main:
                        if not self._points[xy.colour][0][0]:
                            if not self._points[xy.colour][0][1]:
                                self.grid[i][j] = None

    def _check_grid(self):
        self.flows = 0
        for i in self._points.keys():
            if self._points[i][0][1] is True and self._points[i][1][1] is True:
                self.flows += 1

    def _grid_control_aux(self, i, j, x=False, increase=False):
        X, Y = i, j
        if not x and not increase:
            j -= 1
        elif not x and increase:
            j += 1
        elif x and not increase:
            i -= 1
        else:
            i += 1
        xy = self.grid[i][j]
        if self._enter[0] and xy is None:
            p = Point(self._enter[1].colour, i, j, False)
            self.grid[i][j] = p
        else:
            if self._enter[0] and xy is not None:
                if xy.main:
                    if xy.colour == self._enter[1].colour:
                        t = self._points[xy.colour]
                        t[0] = (t[0][0], True)
                        t[1] = (t[1][0], True)
                        self._enter = (False, None)
                        self._points[xy.colour] = t
                        self._check_grid()
                    else:
                        i, j = X, Y
                elif not xy.main and xy.colour != self._enter[1].colour:
                    p = Point(self._enter[1].colour, i, j, False)
                    self.grid[i][j] = p
                    self.clean_grid(xy.colour)
                else:
                    self.clean_grid(xy.colour)
                    i = self._enter[1].x
                    j = self._enter[1].y

        return i, j

    def grid_control(self, key, i, j):
        if key == curses.KEY_UP and j > 0:
            i, j = self._grid_control_aux(i, j)
        elif key == curses.KEY_DOWN and j < self.rows-1:
            i, j = self._grid_control_aux(i, j, increase=True)
        elif key == curses.KEY_LEFT and i > 0:
            i, j = self._grid_control_aux(i, j, x=True)
        elif key == curses.KEY_RIGHT and i < self.rows-1:
            i, j = self._grid_control_aux(i, j, x=True, increase=True)
        elif key == 10:
            if self.grid[i][j] is not None and self.grid[i][j].main:
                self._enter = (True, self.grid[i][j])
                t = self._points[self._enter[1].colour]
                try:
                    index = t.index((self._enter[1], False))
                    t[index] = (t[index][0], True)
                except:
                    pass
                self._points[self._enter[1].colour] = t
            else:
                self._enter = (False, None)
                self.clean_grid()
        return i, j

    def _init_grid(self):
        for p in self.starting_points:
            self.grid[p.x][p.y] = p

    def _randomize_starting_points(self) -> None:
        for i in range(2):
            cont = 0
            c = list()
            while cont < 2:
                p = Point(i+4, self.rows, self.cols)
                if p not in self.starting_points:
                    self.starting_points.append(p)
                    c.append((p, False))
                    cont += 1
            self._points[c[0][0].colour] = c
