import logging

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class DetectCycle(BaseEvaluation):
    name = 'Detect Cycle'

    def run(self, code: BaseCode, params: dict) -> dict:
        """
        Executes the cycle detection algorithm on the provided code and parameters.

        Args:
            code (BaseCode): The code object to be analyzed.
            params (dict): A dictionary of parameters, expected to contain a 'graph' key with the graph data.

        Returns:
            dict: A dictionary with the result of the cycle detection. 
                  'value' will be 'Cycle detected' if a cycle is found, otherwise 'No cycle detected'.
                  'unit' will be None.
        """
        result = {'value': 'No cycle detected', 'unit': None}
        graph = params.get('graph', [])
        if self.is_cyclic(graph):
            result['value'] = 'Cycle detected'
        return result

    def is_cyclic(self, graph):
        visited = [False] * len(graph)
        rec_stack = [False] * len(graph)

        for node in range(len(graph)):
            if not visited[node]:
                if self.is_cyclic_util(graph, node, visited, rec_stack):
                    return True
        return False

    def is_cyclic_util(self, graph, v, visited, rec_stack):
        visited[v] = True
        rec_stack[v] = True

        for neighbour in range(len(graph)):
            if graph[v][neighbour] > 0:
                if not visited[neighbour]:
                    if self.is_cyclic_util(graph, neighbour, visited, rec_stack):
                        return True
                elif rec_stack[neighbour]:
                    return True

        rec_stack[v] = False
        return False