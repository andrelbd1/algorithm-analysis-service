import logging

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class CountEdges(BaseEvaluation):
    name = 'Count Edges'

    def run(self, code: BaseCode, params: dict) -> dict:
        result = {'value': None, 'unit': None}
        # TODO: Implement the process function
        return result
