import logging
import time

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class RunningTime(BaseEvaluation):
    name = 'Running Time'

    def run(self, code: BaseCode, params: dict) -> dict:
        """
        Executes the provided code with given parameters and measures its running time.

        Args:
            code (BaseCode): An instance of BaseCode that has a run method to be executed.
            params (dict): A dictionary of parameters to be passed to the code's run method.

        Returns:
            dict: A dictionary containing the running time of the code execution with keys:
                - 'value': The running time as a string formatted to 7 decimal places.
                - 'unit': The unit of the running time, which is 'secs'.
        """
        result = {'value': None, 'unit': None}
        time_init = time.perf_counter()
        code.run(params)
        time_end = time.perf_counter()
        run_time = time_end-time_init
        result.update({'value': f'{run_time:.7f}',
                       'unit': 'secs',
                       })
        return result
