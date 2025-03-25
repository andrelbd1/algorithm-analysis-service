import logging

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class CountEdges(BaseEvaluation):
    name = 'Count Edges'

    def run(self, code: BaseCode, params: dict) -> dict:
        """
        Given a graph, count the number of edges.

        Args:
            code (BaseCode): An instance of a class that inherits from BaseCode, which contains the code to be executed.
            params (dict): A dictionary of parameters, expected to contain a 'graph' key with the graph data.

        Returns:
            dict: A dictionary containing the number of edges with keys 'value' and 'unit' (set to 'edge(s)').
        """
        result = {'value': '0', 'unit': 'edge(s)'}
        graph = params.get('graph', [])
        result['value'] = f'{self.count_edges(graph)}'
        return result

    def count_edges(self, graph: list) -> int:
        edge_count = 0
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] > 0:
                    edge_count += 1
        return edge_count