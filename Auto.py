from colored import fg, attr, bg
import re
import random


class Auto:
    def __init__(self):
        self.grid = [[]]
        self.startNodes = {}
        self.endNodes = {}
        self.allNodes = []
        self.distances = {}
        self._read_file(random.choice([i for i in range(1, 22)]))
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self._init()
        self._sortNodes()

    def _read_file(self, number):
        pattern = "[0-9]+"
        with open(f"puzzles/flowfree_{number}.txt") as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if i == 0:
                    splited = line.split(' ')
                    rows, cols = int(splited[1]), int(splited[2])
                    self.grid = [[-1 for i in range(cols+2)]
                                 for j in range(rows+2)]
                else:
                    j = re.findall(pattern, line)
                    x1, y1 = int(j[0])+1, int(j[1])+1
                    x2, y2 = int(j[2])+1, int(j[3])+1
                    self.grid[x1][y1] = i
                    self.grid[x2][y2] = i
                i += 1
            for i in range(1, rows+1):
                for j in range(1, cols+1):
                    if self.grid[i][j] == -1:
                        self.grid[i][j] = 0

    def _init(self):
        for row in range(1, self.rows-1):
            for column in range(1, self.cols-1):
                color = self.grid[row][column]
                if color > 0:
                    if color in self.startNodes:
                        self.endNodes[color] = [row, column]
                        self.distances[color] = abs(
                            row-self.startNodes[color][0])
                        + abs(column-self.startNodes[color][1])
                    else:
                        self.startNodes[color] = [row, column]
                    self.allNodes.append([row, column, color])

    def _sortNodes(self):
        self.sortedNodes = []
        keys = list(self.distances)
        for i in range(0, len(self.distances)):
            min = self.distances[keys[0]]
            for key in self.distances:
                if self.distances[key] < min:
                    min = self.distances[key]
            self.sortedNodes.append(key)
            self.distances.pop(key)

    def drawGrid(self):
        for row in range(1, self.rows-1):
            print('')
            for column in range(1, self.cols-1):
                pos = self.grid[row][column]
                color = bg(pos) + fg(pos)
                reset = attr('reset')
                print(color + 'XX' + reset, end='')
        print('\n\n')

    def _checkGrid(self):
        for row in range(1, self.rows-1):
            for column in range(1, self.cols-1):
                if self.grid[row][column] > 0:
                    color = self.grid[row][column]
                    if (self.grid[row+1][column] > 0 and
                            self.grid[row+1][column] != color):
                        if (self.grid[row-1][column] > 0 and
                                self.grid[row-1][column] != color):
                            if (self.grid[row][column+1] > 0 and
                                    self.grid[row][column+1] != color):
                                if (self.grid[row][column-1] > 0 and
                                        self.grid[row][column-1] != color):
                                    return False
                    if (self.grid[row+1][column] == color and
                        self.grid[row-1][column] == color and
                            self.grid[row][column+1] == color):
                        return False
                    elif (self.grid[row+1][column] == color and
                          self.grid[row-1][column] == color and
                          self.grid[row][column-1] == color):
                        return False
                    elif (self.grid[row+1][column] == color and
                          self.grid[row][column+1] == color and
                          self.grid[row][column-1] == color):
                        return False
                    elif (self.grid[row-1][column] == color and
                          self.grid[row][column+1] == color and
                          self.grid[row][column-1] == color):
                        return False
        return True

    def _solved(self):
        for row in range(1, self.rows-1):
            for column in range(1, self.cols-1):
                if self.grid[row][column] == 0:
                    return False
        return True

    def solvePuzzle(self):
        self.drawGrid()
        if not self._checkGrid():
            return False

        if self._solved():
            return True

        for color in self.sortedNodes:
            startNode = self.startNodes[color]
            endNode = self.endNodes[color]
            if (abs(endNode[0] - startNode[0]) +
                    abs(endNode[1] - startNode[1]) > 1):
                directions = []
                if self.grid[startNode[0]][startNode[1]+1] == 0:
                    if endNode[1] > startNode[1]:
                        directions.insert(0, "right")  # Higher Priority
                    else:
                        directions.append("right")  # Lower Priority!
                if self.grid[startNode[0]][startNode[1]-1] == 0:
                    if endNode[1] < startNode[1]:
                        directions.insert(0, "left")  # Higher Priority
                    else:
                        directions.append("left")  # Lower Priority!
                if self.grid[startNode[0]+1][startNode[1]] == 0:
                    if endNode[0] > startNode[0]:
                        directions.insert(0, "down")  # Higher Priority
                    else:
                        directions.append("down")  # Lower Priority!
                if self.grid[startNode[0]-1][startNode[1]] == 0:
                    if endNode[0] < startNode[0]:
                        directions.insert(0, "up")  # Higher Priority
                    else:
                        directions.append("up")  # Lower Priority!

                if len(directions) == 0:
                    return False
                for direction in directions:
                    if direction == "right":
                        startNode[1] += 1
                        self.grid[startNode[0]][startNode[1]] = color
                        if self.solvePuzzle():
                            return True
                        else:
                            self.grid[startNode[0]][startNode[1]] = 0
                            startNode[1] -= 1

                    elif direction == "left":
                        startNode[1] -= 1
                        self.grid[startNode[0]][startNode[1]] = color
                        if self.solvePuzzle():
                            return True
                        else:
                            self.grid[startNode[0]][startNode[1]] = 0
                            startNode[1] += 1
                    elif direction == "up":
                        startNode[0] -= 1
                        self.grid[startNode[0]][startNode[1]] = color
                        if self.solvePuzzle():
                            return True
                        else:
                            self.grid[startNode[0]][startNode[1]] = 0
                            startNode[0] += 1
                    elif direction == "down":
                        startNode[0] += 1
                        self.grid[startNode[0]][startNode[1]] = color
                        if self.solvePuzzle():
                            return True
                        else:
                            self.grid[startNode[0]][startNode[1]] = 0
                            startNode[0] -= 1
                return False
