import logging

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class CountNodes(BaseEvaluation):
    name = 'Count Nodes'

    def run(self, code: BaseCode, params: dict) -> dict:
        """
        Given a graph, count the number of nodes.

        Args:
            code (BaseCode): An instance of a class that inherits from BaseCode, which contains the code to be executed.
            params (dict): A dictionary of parameters, expected to contain a 'graph' key with the graph data.

        Returns:
            dict: A dictionary containing the number of nodes with keys 'value' and 'unit' (set to 'node(s)').
        """
        graph = params.get('graph', [])
        result = {'value': f'{len(graph)}', 'unit': 'node(s)'}
        return result
