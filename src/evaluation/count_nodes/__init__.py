import logging
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class CountNodes(BaseCode):
    name = 'Count Nodes'

    def process(self, params: dict):
        result = {'value': None,
                  'unit': None,
                  'message': None,
                  }
        # TODO: Implement the process function
        return result
