import logging
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class RunningTime(BaseCode):
    name = 'Running Time'

    def process(self, params: dict):
        pass
