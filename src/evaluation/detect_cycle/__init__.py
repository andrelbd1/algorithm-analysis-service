import logging
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class DetectCycle(BaseCode):
    name = 'Detect Cycle'

    def process(self, params: dict):
        result = {'value': None,
                  'unit': None,
                  'message': None,
                  }
        # TODO: Implement the process function
        return result
