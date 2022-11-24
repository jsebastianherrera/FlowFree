import re
import curses
from queue import PriorityQueue


class Node:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.constrained = 0

    def __str__(self):
        return f"Symbol:{self.symbol}({self.x},{self.y})"


class Graph:
    def __init__(self, number, stdscr):
        self._stdscr = stdscr
        self.graph = []
        self.rows = 0
        self.cols = 0
        self.colors = set(())
        self._fillGraphNodes(number)
        self.count = 0
        self.options = set(())
        self.colors.remove('_')
        for i in self.colors:
            self.options.add(i.lower())

    def _fillGraphNodes(self, number):
        matrix = self._readFile(number)
        for i in range(self.rows):
            data = []
            for j in range(self.cols):
                val = matrix[i][j]
                self.colors.add(val)
                data.append(Node(val, i, j))
            self.graph.append(data)

    def _readFile(self, number):
        matrix = [[]]
        pattern = "[0-9]+"
        with open(f"puzzles/flowfree_{number}.txt") as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if i == 0:
                    splitted = line.split(' ')
                    _, self.rows, self.cols = (int(splitted[0]),
                                               int(splitted[1]),
                                               int(splitted[2]))
                    matrix = [['_' for i in range(self.rows)]
                              for j in range(self.cols)]
                else:
                    j = re.findall(pattern, line)
                    x, y = int(j[0]), int(j[1])
                    x1, y1 = int(j[2]), int(j[3])
                    matrix[x][y] = chr(i+64)
                    matrix[x1][y1] = chr(i+64)
                i += 1
            return matrix
        return matrix

    def _getNext(self, x, y):
        if x == self.rows - 1 and y == self.cols - 1:
            return None
        elif x == self.rows - 1:
            return [0, y + 1]
        else:
            return [x + 1, y]

    def _countColors(self, nbors, options):
        temp = list()
        counts = PriorityQueue()
        reordered = list()
        for x in nbors:
            temp.append(x.symbol.lower())

        for x in options:
            counts.put((-temp.count(x), x))
        while not counts.empty():
            hi = counts.get()
            reordered.append(hi[1])

        return reordered

    def solver(self, x, y):
        done = False
        nextSquare = self._getNext(x, y)
        nbors = self._findNeighbors(x, y)
        self.printGrid(self._stdscr)
        if self.graph[x][y].symbol != "_" and nextSquare is not None:
            done = self.solver(nextSquare[0], nextSquare[1])
        else:
            for i in self.options:
                self.graph[x][y].symbol = i
                self.count += 1
                valid = self._checkConstraints(x, y, nbors)
                if valid:
                    if nextSquare is None:
                        return True
                    else:
                        done = self.solver(
                            nextSquare[0], nextSquare[1])
                        if done:
                            return done
            if not done:
                self.graph[x][y].symbol = '_'
        return done

    def _findNeighbors(self, x, y):
        nbors = list(())
        if x > 0:
            nbors.append(self.graph[x-1][y])
        if y > 0:
            nbors.append(self.graph[x][y-1])
        if x < self.rows - 1:
            nbors.append(self.graph[x+1][y])
        if y < self.cols - 1:
            nbors.append(self.graph[x][y+1])
        return nbors

    def _howConstrained(self, square, nbors):
        count = 0
        for i in self.options:
            if self._checkConstraints(square.x, square.y, nbors):
                count += 1
        return len(self.options) - count

    def _includesSquare(self, symbol, nbors):
        count = 0
        for i in nbors:
            if i.symbol == symbol:
                count += 1
        return count

    def _checkConstraints(self, x, y, nbors):
        valid = True
        nbors.append(self.graph[x][y])
        for j in nbors:
            if j.symbol == "_":
                continue
            cnbors = self._findNeighbors(j.x, j.y)
            if j.symbol.isupper():
                symbolCount = self._includesSquare(j.symbol.lower(), cnbors)
                blankCount = self._includesSquare("_", cnbors)
                if symbolCount > 1:
                    valid = False
                if blankCount == 0 and symbolCount != 1:
                    valid = False
            else:
                symbolCount = self._includesSquare(j.symbol, cnbors)
                symbolCount += self._includesSquare(j.symbol.upper(), cnbors)
                blankCount = self._includesSquare("_", cnbors)
                if symbolCount > 2:
                    valid = False
                if symbolCount == 1 and blankCount < 1:
                    valid = False
                if symbolCount == 0 and blankCount < 2:
                    valid = False
        return valid

    def printGrid(self, stdsrc):
        hmax, wmax = stdsrc.getmaxyx()
        h = hmax//2 - self.rows
        w = wmax//2 - self.cols
        x_ = 0
        for i in range(0, self.rows):
            y_ = 0
            for j in range(0, self.cols):
                if self.graph[i][j].symbol != "_":
                    text = self.graph[i][j].symbol.upper()
                    stdsrc.addstr(h+y_, w+x_, text.upper()+text.upper(),
                                  curses.color_pair(
                        ord(self.graph[i][j].symbol.lower())))
                else:
                    stdsrc.addstr(h+y_, w+x_, '__',
                                  curses.color_pair(2))
                y_ += 2
            x_ += 3
        stdsrc.refresh()
