import curses
import re
import random
from Point import Point


class Grid:
    def __init__(self, flows=0, row=0, col=0, random_points=False):
        self._List = [i for i in range(4, 254)]
        self.flows = flows
        self.cont = 0
        self._enter = (False, None)
        self.rows = row
        self.cols = col
        self._points = {}
        self.starting_points = []
        self.grid = [[None for _ in range(self.rows)]
                     for _ in range(self.cols)]
        if random_points:
            self._colors = random.choices(self._List, k=flows)
            self._randomize_starting_points()
        else:
            list = [i for i in range(1, 19)]
            self._read_file(random.choice(list))
        self._init_grid()

    def _read_file(self, number):
        pattern = "[0-9]+"
        with open(f"puzzles/flowfree_{number}.txt") as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if i == 0:
                    splited = line.split(' ')
                    self.flows, self.rows, self.cols = (int(splited[0]),
                                                        int(splited[1]),
                                                        int(splited[2]))
                    self.grid = [[None for _ in range(
                        self.rows)]for _ in range(self.cols)]
                    self._colors = random.choices(self._List, k=self.flows)
                else:
                    j = re.findall(pattern, line)
                    c = list()
                    p1 = Point(self._colors[i-1], int(j[0]), int(j[1]))
                    p2 = Point(self._colors[i-1], int(j[2]), int(j[3]))
                    self.starting_points.append(p1)
                    self.starting_points.append(p2)
                    c.append((p1, False))
                    c.append((p2, False))
                    self._points[self._colors[i-1]] = c
                i += 1

    def print_grid(self, stdsrc, x, y):
        stdsrc.clear()
        hmax, wmax = stdsrc.getmaxyx()
        h = hmax//2 - self.rows
        w = wmax//2 - self.cols
        if self._enter[0]:
            stdsrc.addstr(1, 1, 'XXXXX',
                          curses.color_pair(self._enter[1].colour))
        stdsrc.addstr(h-2, w-2, '('+str(x)+','+str(y) + ')')
        stdsrc.addstr(
            h-2, w+2, ' | flows:('+str(self.cont)+','+str(self.flows) + ')')
        x_ = 0
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
    # Point None means that there is an empty place

    def clean_grid(self, colour):
        for i in range(self.rows):
            for j in range(self.cols):
                p: Point = self.grid[i][j]
                if p is not None:
                    if not p.main and p.colour == colour:
                        self.grid[i][j] = None
                    elif p.main:
                        new = list(map(lambda x: (x[0], False),
                                       self._points[p.colour]))
                        self._points[p.colour] = new

    def _check_grid(self):
        self.cont = 0
        for i in self._points.keys():
            if self._points[i][0][1] is True and self._points[i][1][1] is True:
                self.cont += 1

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
            p = Point(self._enter[1].colour, self.rows, self.cols, False)
            self.grid[i][j] = p
        else:
            if self._enter[0] and xy is not None:
                if xy.main and xy.colour == self._enter[1].colour:
                    if xy is not self._enter[1]:
                        t = self._points[xy.colour]
                        t[0] = (t[0][0], True)
                        t[1] = (t[1][0], True)
                        self._enter = (False, None)
                        self._points[xy.colour] = t
                    else:
                        i, j = X, Y
                elif not xy.main and xy.colour != self._enter[1].colour:
                    p = Point(self._enter[1].colour,
                              self.rows, self.cols, False)
                    self.grid[i][j] = p
                    self.clean_grid(xy.colour)
                else:
                    self.clean_grid(xy.colour)
                    i = self._enter[1].x
                    j = self._enter[1].y

        return i, j

    def grid_control(self, key, i, j):
        self._check_grid()
        if key == curses.KEY_UP and j > 0:
            i, j = self._grid_control_aux(i, j)
        elif key == curses.KEY_DOWN and j < self.rows-1:
            i, j = self._grid_control_aux(i, j, increase=True)
        elif key == curses.KEY_LEFT and i > 0:
            i, j = self._grid_control_aux(i, j, x=True)
        elif key == curses.KEY_RIGHT and i < self.cols-1:
            i, j = self._grid_control_aux(i, j, x=True, increase=True)
        elif key == 10:
            p: Point = self.grid[i][j]
            if p is not None and p.main:
                self._enter = (True, p)
                c = self._points[p.colour]
                if p.x == c[0][0].x and p.y == c[0][0].y:
                    c[0] = (c[0][0], True)
                else:
                    c[1] = (c[1][0], True)
                self._points[p.colour] = c
            else:
                self._enter = (False, None)
        return i, j

    def _init_grid(self):
        for p in self.starting_points:
            self.grid[p.x][p.y] = p

    def _randomize_starting_points(self) -> None:
        for i in range(self.flows):
            cont = 0
            c = list()
            while cont < 2:
                p = Point(self._colors[i], self.rows, self.cols, random=True)
                if p not in self.starting_points:
                    self.starting_points.append(p)
                    # Point , state ---> False: no connected
                    c.append((p, False))
                    cont += 1
            # first element
            self._points[c[0][0].colour] = c
