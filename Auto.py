import re
from queue import PriorityQueue


def includesSquare(symbol, nbors):
    count = 0
    for i in nbors:
        if i.symbol == symbol:
            count += 1
    return count


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
        self.graph = []  # double array of squares
        self.xdim = 0  # x-dimension
        self.ydim = 0  # y-dimension
        self.colors = set(())  # all colors included in the graph
        self.eCount = 0
        self._fillGraphNodes(number)
        self.squaresByConst = PriorityQueue()  # queue for smart alg
        self.count = 0  # number of assignments
        self.options = set(())  # domains
        self.colors.remove('_')
        for i in self.colors:  # create a list of lower case colors available
            self.options.add(i.lower())

    def _fillGraphNodes(self, number):
        matrix = self._readFile(number)
        for i in range(self.xdim):
            data = []
            for j in range(self.ydim):
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
                    _, self.xdim, self.ydim = (int(splitted[0]),
                                               int(splitted[1]),
                                               int(splitted[2]))
                    matrix = [['_' for i in range(self.xdim)]
                              for j in range(self.ydim)]
                else:
                    j = re.findall(pattern, line)
                    x, y = int(j[0]), int(j[1])
                    x1, y1 = int(j[2]), int(j[3])
                    matrix[x][y] = chr(i+64)
                    matrix[x1][y1] = chr(i+64)
                i += 1
            return matrix
        return matrix

    def makeQueue(self):
        # set constraints and set up max priority queue
        if self.squaresByConst.qsize() > 0:
            self.squaresByConst = PriorityQueue()
        for i in range(self.xdim):
            for j in range(self.ydim):
                if self.graph[i][j].symbol == "_":
                    self.graph[i][j].constrained = self.howConstrained(
                        self.graph[i][j], self.findNeighbors(i, j))
                    priorityNum = -self.graph[i][j].constrained
                    # set up as max priority queue instead of min
                    self.squaresByConst.put(
                        ((priorityNum, self.eCount), self.graph[i][j]))
                    self.eCount = self.eCount + 1

    # get a list of possible colors organized by how often they appear in nbors
    def countColors(self, nbors, options):
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

    def solvePuzzleSmart(self):  # uses the smart algorithm to solve the puzzle
        self.count = 0

        print("Unsolved Puzzle:")
        self.printGraph()
        self.makeQueue()

        start = self.squaresByConst.get()[1]
        # solve and determine if solution exists
        if self.solveSquareSmart(start):
            print("Solution:")
            self.printGraph()

        else:
            print("No Solution.")
        print("Assignments made: " + str(self.count))

    def solveSquareSmart(self, current):
        done = False  # keeps track of whether constraints are violated
        x = current.x
        y = current.y
        nbors = self.findNeighbors(x, y)

        # recurzive version
        if self.graph[x][y].symbol != "_":  # not a filled square and not the last square
            print("hi")
            done = self.solveSquareSmart(self.squaresByConst.get()[1])
        else:  # this square must be blank
            # reorganize the colors prioritizing most occuring in nbors
            self.options = self.countColors(nbors, self.options)
            for i in self.options:  # loop through all possible colors, checking validity of each one
                self.graph[x][y].symbol = i
                self.count += 1
                # make sure this doesn't violate any constraints
                valid = self.checkConstraints(x, y, nbors)

                if valid:
                    blankNum = True  # means there are no blanks in the grid
                    for i in range(self.xdim):
                        for j in range(self.ydim):
                            if self.graph[i][j].symbol == "_":
                                blankNum = False  # found a blank
                                break
                    if self.squaresByConst.empty():  # we've reached a solution, so return
                        return True
                    elif blankNum:
                        done = True
                        return done
                    else:
                        # update Constraints
                        self.makeQueue()
                        # recursively call the solve method on the next square
                        done = self.solveSquareSmart(
                            self.squaresByConst.get()[1])

                        if done:  # end if we've reached a solution
                            return done
            if not done:  # rewrite over the symbol as blank of none of this options are valid
                self.graph[x][y].symbol = '_'
        return done  # return solution or not

    def findNeighbors(self, x, y):  # returns all neighbors of a square in a list
        nbors = list(())
        if x > 0:
            nbors.append(self.graph[x-1][y])
        if y > 0:
            nbors.append(self.graph[x][y-1])
        if x < self.xdim - 1:
            nbors.append(self.graph[x+1][y])
        if y < self.ydim - 1:
            nbors.append(self.graph[x][y+1])
        return nbors

        # determines how constrained by finding number of non-blank neighbors
    def howConstrained(self, square, nbors):
        count = 0
        for i in self.options:
            if self.checkConstraints(square.x, square.y, nbors):
                count += 1
        return len(self.options) - count

    def checkConstraints(self, x, y, nbors):
        valid = True  # check that placing this value in this square doesn't violate any neighboring constraints
        nbors.append(self.graph[x][y])
        for j in nbors:  # includes this square and all 4 of its neighbors
            if j.symbol == "_":  # ignore blank spaces
                continue
            cnbors = self.findNeighbors(j.x, j.y)
            if j.symbol.isupper():  # Make sure endpoints don't have more than one matching color coming out of them and that if it doesn't have any, that it has at least one blank adjacent square
                symbolCount = includesSquare(j.symbol.lower(), cnbors)
                blankCount = includesSquare("_", cnbors)
                if symbolCount > 1:  # more than one of same color connecting
                    valid = False
                if blankCount == 0 and symbolCount != 1:  # no available ways to connect to endpoint
                    valid = False
            else:  # Symbol is not an endpoint, but we have to make sure it's not blocked in by other colors either
                symbolCount = includesSquare(j.symbol, cnbors)
                symbolCount += includesSquare(j.symbol.upper(), cnbors)
                blankCount = includesSquare("_", cnbors)
                if symbolCount > 2:  # too many of same color connecting
                    valid = False
                if symbolCount == 1 and blankCount < 1:  # not enough blank spaces to connect
                    valid = False
                if symbolCount == 0 and blankCount < 2:  # not enough blank spaces to connect
                    valid = False
        return valid

    def printGraph(self):
        for i in range(self.xdim):
            line = ""
            for j in range(self.ydim):
                line += self.graph[i][j].symbol
            print(line)
