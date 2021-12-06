from pathlib import Path

class map:

    def __init__(self):
        x = 1000
        y = 1000
        self.map = [[0 for _ in range(x)] for _ in range(y)]

    def addLine(self, start, end):
        x1 = int(start[0])
        y1 = int(start[1])
        x2 = int(end[0])
        y2 = int(end[1])

        if x1 == x2:
            if y1 < y2:
                for i in range(y1, y2 + 1):
                    self.map[x1][i] = self.map[x1][i] + 1
            else: 
                for i in range(y2, y1 + 1):
                    self.map[x1][i] = self.map[x1][i] + 1
        elif y1 == y2:
            if x1 < x2:
                for i in range(x1, x2 + 1):
                    self.map[i][y1] = self.map[i][y1] + 1
            else: 
                for i in range(x2, x1 + 1):
                    self.map[i][y1] = self.map[i][y1] + 1

    def countMultiple(self):
        sum = 0
        for row in self.map:
            for point in row:
                if point > 1:
                    sum += 1
        return sum

m = map()

p = Path('input.txt')
with p.open() as f:
    while line := f.readline():
        line = line.lstrip().replace('\n', '')
        parts = line.split(' -> ')
        start = parts[0].split(',')
        end = parts[1].split(',')
        m.addLine(start, end)

print(m.countMultiple())
