import logging
from src.codes.base import BaseCode

log = logging.getLogger(__file__)


class Dijkstra(BaseCode):
    name = 'Dijkstra'

    def __init__(self):
        self.inf = float('inf')
        self.graph = []
        self.n_vertices = len(self.graph)

    def __print_distance(self, dist, target=None, show_print: bool=False):
        if target:
            if show_print:
                print("distance:", dist[target])
            return dist[target]
        if show_print:
            print("Vertex \t Distance from Source")
            for node in range(self.n_vertices):
                print(node, "\t\t", dist[node])

    def __print_path(self, path: list, target: int):
        queue = [target]
        build_path = []
        while True:
            prev = queue.pop(0)
            build_path.append(prev)
            if path[prev] is None:
                break
            queue.append(path[prev])
        build_path.reverse()
        print("path:", " -> ".join([str(i) for i in build_path]))

    def __min_distance(self, dist: list, visited: list) -> int:
        minimum = self.inf  # Initialize minimum distance for next node
        for v in range(self.n_vertices):  # get nearest vertex not visited
            if dist[v] < minimum and visited[v] is False:
                minimum = dist[v]
                min_index = v

        return min_index

    def run(self, params: dict):  # O(n2)
        self.graph = params("graph")
        self.n_vertices = len(self.graph)
        src = params.get("src")
        target = params.get("target")
        show_print = params.get("show_print")
        visited = [False] * self.n_vertices
        dist = [self.inf] * self.n_vertices
        dist[src] = 0
        path_prev = {src: None}
        for _ in range(self.n_vertices):
            # Get the minimum distance vertex not visited yet.
            # u is always equal to src in first iteration.
            u = self.__min_distance(dist, visited)
            visited[u] = True
            # Update distance value of the adjacent vertices
            for v in range(self.n_vertices):
                if (self.graph[u][v] > 0 and  # Check if has edge
                        visited[v] is False and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    path_prev.update({v: u})
        if show_print:
            self.__print_path(path_prev, target)
        return self.__print_distance(dist, target, show_print)
