from collections import Counter

class Graph:

    def add_one_path(self, v_1, v_2):
        if v_1 not in list(self.path_map.keys()):
            self.path_map[v_1] = []
        paths = self.path_map[v_1]
        paths.append(v_2)
        self.path_map[v_1] = paths

    def add_path(self, start, end):
        self.add_one_path(start, end)
        self.add_one_path(end, start)

    def is_small(self, vertex):
        return vertex == vertex.lower()

    def is_small_bad(self, vertex, route):
        if self.part == 1:
            return vertex in route
        if self.part == 2:
            if vertex == 'start':
                return True
            caves = Counter(route)
            for k, v in caves.items():
                if self.is_small(k):
                    if v > 1:
                        return vertex in route
            return False

    def find_routes(self, curr_route):
        verticies = self.path_map[curr_route[-1]].copy()
        for vertex in verticies:
            if self.is_small(vertex) and \
                self.is_small_bad(vertex, curr_route):
                continue
            route = curr_route.copy()
            route.append(vertex)
            if vertex == 'end':
                self.routes.append(route)
                continue
            self.find_routes(route)

    def __init__(self, paths, part) -> None:
        self.part = part
        self.path_map = {}
        self.routes = []
        for path in paths:
            start, end = path.split('-')
            self.add_path(start, end)
        for _, value in self.path_map.items():
            value = value.sort()
        self.find_routes(['start'])

    def print_map(self):
        print(self.path_map)

M = []
for line in open('input.txt', encoding='UTF-8'):
    M.append(line.replace('/n', '').strip())

G = Graph(M, 1)
assert len(G.routes) == 5333
print(len(G.routes))

G = Graph(M, 2)
assert len(G.routes) == 146553
print(len(G.routes))
