import logging
import random
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

    def __print_path(self, path: dict, target: int):
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
        self.graph = params.get("graph")
        self.n_vertices = len(self.graph)
        src = params.get("source")
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

    @staticmethod
    def setup(payload: list):
        """
        Generates an adjacency matrix representation of a worst-case graph for Dijkstra's algorithm.

        Args:
            payload (list): A list of dictionaries containing input parameters. 
                            The dictionary should have keys "input" and "input_value".
                            The "input" key should map to another dictionary with at least the key "name".
                            The "input_value" key should map to the value of the input parameter.
            num_nodes (int): Number of nodes in the graph.

        Note:
            The function modifies the input payload list in place by appending the generated graph,
            source node, and target node as new dictionaries.
        """
        for p in payload:
            p_input = p.get("input")
            if p_input.get("name") == "number of nodes":
                num_nodes = int(p.get("input_value"))
                break
        
        # Initialize an empty adjacency matrix
        graph = [[0] * num_nodes for _ in range(num_nodes)]

        # Create a complete undirected graph with random weights
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):  # Ensures undirected edges
                weight = random.randint(1, 100)  # Random weight between 1 and 100
                graph[i][j] = weight
                graph[j][i] = weight  # Mirror the weight for undirected property

        # Choose source as the first node (0) and target as the last node (num_nodes - 1)
        source = 0
        target = num_nodes - 1

        source_input = {'payload_id': None, "input_value": source, 'input':{
            'input_id': None,
            'name': 'source',
            'description': None,
            'input_type': 'integer',
        }}
        target_input = {'payload_id': None, "input_value": target, 'input':{
            'input_id': None,
            'name': 'target',
            'description': None,
            'input_type': 'integer',
        }}
        graph_input = {'payload_id': None, "input_value": graph, 'input':{
            'input_id': None,
            'name': 'graph',
            'description': None,
            'input_type': 'list',
        }}
        payload.append(source_input)
        payload.append(target_input)
        payload.append(graph_input)
