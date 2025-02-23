import logging
import time

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class RunningTime(BaseEvaluation):
    name = 'Running Time'

    def run(self, code: BaseCode, params: dict) -> dict:
        result = {'value': None, 'unit': None}
        time_init = time.perf_counter()
        code.run(params)
        time_end = time.perf_counter()
        run_time = time_end-time_init
        result.update({'value': f'{run_time:.7f}',
                       'unit': 'secs',
                       })
        return result
