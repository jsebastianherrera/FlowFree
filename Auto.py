import re
from queue import PriorityQueue
from colored import fg, attr, bg


class Node:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.constrained = 0

    def __str__(self):
        return f"Symbol:{self.symbol}({self.x},{self.y})"


class Graph:
    def __init__(self, number):
        self.graph = []
        self.rows = 0
        self.cols = 0
        self.colors = set(())
        self.eCount = 0
        self._fillGraphNodes(number)
        self.queue = PriorityQueue()
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

    def _readFile(self, number) -> str:
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

    def _makeQueue(self):
        if self.queue.qsize() > 0:
            self.queue = PriorityQueue()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.graph[i][j].symbol == "_":
                    self.graph[i][j].constrained = self._howConstrained(
                        self.graph[i][j], self._findNeighbors(i, j))
                    priorityNum = -self.graph[i][j].constrained
                    self.queue.put(
                        ((priorityNum, self.eCount), self.graph[i][j]))
                    self.eCount = self.eCount + 1

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

    def solvePuzzleSmart(self):
        self.count = 0
        print("Unsolved Puzzle:")
        self.printGraph()
        self._makeQueue()

        start = self.queue.get()[1]
        if self._solveSquareSmart(start):
            print("Solution:")
            self.printGraph()

        else:
            print("No Solution.")
        print("Assignments made: " + str(self.count))

    def _solveSquareSmart(self, current):
        self.printGraph()
        done = False
        x = current.x
        y = current.y
        nbors = self._findNeighbors(x, y)

        if self.graph[x][y].symbol != "_":
            done = self._solveSquareSmart(self.queue.get()[1])
        else:
            self.options = self._countColors(nbors, self.options)
            for i in self.options:
                self.graph[x][y].symbol = i
                self.count += 1
                valid = self._checkConstraints(x, y, nbors)

                if valid:
                    blankNum = True
                    for i in range(self.rows):
                        for j in range(self.cols):
                            if self.graph[i][j].symbol == "_":
                                blankNum = False
                                break
                    if self.queue.empty():
                        return True
                    elif blankNum:
                        done = True
                        return done
                    else:
                        self._makeQueue()
                        done = self._solveSquareSmart(
                            self.queue.get()[1])

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

    def printGraph(self):
        for i in range(self.rows):
            print("")
            for j in range(self.cols):
                symbol = ord(self.graph[i][j].symbol.lower())
                color = bg(symbol) + fg(symbol)
                reset = attr("reset")
                print(color + "XX" + reset, end="")
        print("\n")
