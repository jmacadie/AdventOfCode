class HeightMap:

    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(list(lines[0]))
        self.map = []
        for row in lines:
            row = [int(i) for i in list(row)]
            assert len(row) == self.width
            self.map.append(row)

    def get_point_val(self, point):
        return self.map[point[1]][point[0]]

    def in_bounds(self, point):
        if point[0] < 0 or point[1] < 0:
            return False
        if point[0] >= self.width or point[1] >= self.height:
            return False
        return True

    def get_adjacent_points(self, point):
        i = point[0]
        j = point[1]
        return [[i + 1, j], [i, j + 1], [i - 1, j], [i, j - 1]]

    def is_low_point(self, i, j):
        val = self.get_point_val([i, j])
        for point in self.get_adjacent_points([i, j]):
            if self.in_bounds(point) and self.get_point_val(point) <= val:
                return False
        return True

    def risk_level(self, i, j):
        if self.is_low_point(i, j):
            return self.map[j][i] + 1
        return 0

    def already_included(self, new_point, curr_basin_points):
        for point in curr_basin_points:
            if point[0] == new_point[0] and point[1] == new_point[1]:
                return True
        return False

    def check_basin_point(self, i, j, curr_basin_points):
        if self.map[j][i] < 9:
            curr_basin_points.append([i, j])
            if i > 0 and not self.already_included([i - 1, j], curr_basin_points):
                curr_basin_points = self.check_basin_point(i - 1, j, curr_basin_points)
            if j > 0 and not self.already_included([i, j - 1], curr_basin_points):
                curr_basin_points = self.check_basin_point(i, j - 1, curr_basin_points)
            if i < (self.width - 1) and not self.already_included([i + 1, j], curr_basin_points):
                curr_basin_points = self.check_basin_point(i + 1, j, curr_basin_points)
            if j < (self.height - 1) and not self.already_included([i, j + 1], curr_basin_points):
                curr_basin_points = self.check_basin_point(i, j + 1, curr_basin_points)
        return curr_basin_points

    def get_basin_size(self, i, j):
        basin_points = self.check_basin_point(i, j, [])
        return len(basin_points)

M = []
for line in open('input.txt'):
    M.append(line.replace('\n', '').strip())
HM = HeightMap(M)
OUT = 0
S = []
for x in range(HM.width):
    for y in range(HM.height):
        if HM.is_low_point(x, y):
            OUT += HM.risk_level(x, y)
            size = HM.get_basin_size(x, y)
            S.append(size)
S.sort()
print(OUT)
print(S[-1] * S[-2] * S[-3])

