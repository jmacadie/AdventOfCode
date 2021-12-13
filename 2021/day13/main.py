class Origami:

    MAX = 2000

    def add_point(self, point):
        x, y = [int(i) for i in point.split(',')]
        self.map[y][x] = 1
        self.max_x = max(self.max_x, x + 1)
        self.max_y = max(self.max_y, y + 1)

    def trim_map(self):
        self.map = self.map[:self.max_y]
        for y in range(self.max_y):
            self.map[y] = self.map[y][:self.max_x]

    def fold_x(self, at):
        lower = max(2 * at - self.max_x + 1, 0)
        for x in range(lower, at):
            for y in range(self.max_y):
                self.map[y][x] = min(self.map[y][x] + self.map[y][2 * at - x], 1)

    def fold_y(self, at):
        lower = max(2 * at - self.max_y + 1, 0)
        for x in range(self.max_x):
            for y in range(lower, at):
                self.map[y][x] = min(self.map[y][x] + self.map[2 * at - y][x], 1)

    def do_fold(self, fold):
        dim, at = fold.split('=')
        at = int(at)
        if dim == 'x':
            self.fold_x(at)
            self.max_x = at
        elif dim == 'y':
            self.fold_y(at)
            self.max_y = at
        self.trim_map()

    def count_dots(self):
        sum_dots = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                sum_dots += self.map[y][x]
        return sum_dots

    def __init__(self, points, folds):
        self.map = [[0 for _ in range(self.MAX)] for _ in range(self.MAX)]
        self.max_x = 0
        self.max_y = 0
        self.fold1_dots = 0
        for point in points:
            self.add_point(point)
        self.trim_map()
        for fold in folds:
            self.do_fold(fold)
            if self.fold1_dots == 0:
                self.fold1_dots = self.count_dots()

    def print_out(self):
        for y in range(self.max_y):
            line_out = ''
            for x in range(self.max_x):
                if self.map[y][x] == 0:
                    line_out += ' '
                else:
                    line_out += '#'
            print(line_out)

P = []
F = []
P_SEC = True
for line in open('input.txt', encoding='UTF-8'):
    if line == '\n':
        P_SEC = False
    elif P_SEC:
        P.append(line.replace('\n', '').strip())
    else:
        line = line.replace('\n', '').strip()
        _, line = line.split('along ')
        F.append(line)
O = Origami(P, F)
assert O.fold1_dots == 655
print(O.fold1_dots)
O.print_out()
