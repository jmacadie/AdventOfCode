class OctoGrid:

    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(list(lines[0]))
        self.map = []
        self.tot_flashes = 0
        self.flashed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.step_flashes = 0
        for row in lines:
            row = [int(i) for i in list(row)]
            assert len(row) == self.width
            self.map.append(row)

    def get_point_val(self, point):
        return self.map[point[1]][point[0]]

    def increment_point_val(self, point):
        self.map[point[1]][point[0]] += 1

    def reset_point_val(self, point):
        self.map[point[1]][point[0]] = 0

    def in_bounds(self, point):
        if point[0] < 0 or point[1] < 0:
            return False
        if point[0] >= self.width or point[1] >= self.height:
            return False
        return True

    def get_adjacent_points(self, point):
        i = point[0]
        j = point[1]
        points = []
        for new_point in [
            [i + 1, j],
            [i + 1, j + 1],
            [i,     j + 1],
            [i - 1, j + 1],
            [i - 1, j],
            [i - 1, j - 1],
            [i,     j - 1],
            [i + 1, j - 1]]:
            if self.in_bounds(new_point):
                points.append(new_point)
        return points

    def already_flashed(self, point):
        return self.flashed[point[1]][point[0]]

    def try_flash(self, point):
        if not self.already_flashed(point):
            self.flashed[point[1]][point[0]] = True
            self.step_flashes += 1
            self.trigger_adjacent(point)

    def trigger_adjacent(self, point):
        for new_point in self.get_adjacent_points(point):
            self.increment_point_val(new_point)
            if self.get_point_val(new_point) > 9:
                self.try_flash(new_point)

    def increment_all(self):
        for i in range(self.width):
            for j in range(self.height):
                self.increment_point_val([i, j])

    def test_flash_all(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.get_point_val([i, j]) > 9:
                    self.try_flash([i, j])

    def reset_all(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.get_point_val([i, j]) > 9:
                    self.reset_point_val([i, j])

    def add_step(self):
        self.flashed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.step_flashes = 0
        self.increment_all()
        self.test_flash_all()
        self.reset_all()
        self.tot_flashes += self.step_flashes

    def all_flashed(self):
        return True if self.step_flashes == (self.width * self.height) else False

    def print_map(self):
        for row in range(self.height):
            print(''.join([str(i) for i in self.map[row]]))
        print('')

M = []
for line in open('input.txt', encoding='UTF-8'):
    M.append(line.replace('\n', '').strip())
OG = OctoGrid(M)
for x in range(10000):
    OG.add_step()
    if x == 99:
        assert OG.tot_flashes == 1697
        print(OG.tot_flashes)
    if OG.all_flashed():
        break
assert x + 1 == 344
print(x + 1)
