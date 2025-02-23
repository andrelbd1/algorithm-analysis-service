import logging

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class CountNodes(BaseEvaluation):
    name = 'Count Nodes'

    def run(self, code: BaseCode, params: dict) -> dict:
        result = {'value': None, 'unit': None}
        # TODO: Implement the process function
        return result
