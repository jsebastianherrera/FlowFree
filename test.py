import re
from pprint import pprint as pp
pattern = "[0-9]+"
points = list()
flows, row, col = 0, 0, 0
with open("puzzles/flowfree_example1.txt") as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        if i == 0:
            splited = line.split(' ')
            flows, row, col = splited[0], splited[1], splited[2]
        else:
            j = re.findall(pattern, line)
            points.append(((int(j[0]), int(j[1])), (int(j[2]), int(j[3]))))
        i += 1
    print(flows, row, col)
    pp(points)

mat = [[0 for i in range(0, int(row))] for _ in range(0, int(col))]
i = 1
for k in points:
    p1, p2 = k[0], k[1]
    print(p1[0])
    mat[p1[0]][p1[1]] = i
    mat[p2[0]][p2[1]] = i
    i += 1

pp(mat)
