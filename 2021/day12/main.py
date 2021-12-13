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

    def find_routes(self, curr_route):
        verticies = self.path_map[curr_route[-1]].copy()
        for vertex in verticies:
            if self.is_small(vertex) and \
                vertex in curr_route:
                continue
            route = curr_route.copy()
            route.append(vertex)
            if vertex == 'end':
                self.routes.append(route)
                continue
            self.find_routes(route)

    def __init__(self, paths) -> None:
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
G = Graph(M)
assert len(G.routes) == 5333
print(len(G.routes))
