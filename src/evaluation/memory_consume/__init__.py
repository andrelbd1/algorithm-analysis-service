import logging
from memory_profiler import memory_usage

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class MemoryConsume(BaseEvaluation):
    name = 'Memory Consume'

    def run(self, code: BaseCode, params: dict) -> dict:
        """
        Executes the given code and measures its memory usage.

        Args:
            code (BaseCode): An instance of a class that inherits from BaseCode, which contains the code to be executed.
            params (dict): A dictionary of parameters to be passed to the code's run method.

        Returns:
            dict: A dictionary containing the maximum memory usage with keys 'value' (as a string formatted to 7 decimal places) 
                  and 'unit' (set to 'MiB').
        """
        result = {'value': None, 'unit': None}
        mem_usage = memory_usage((code.run, (params,)), interval=0.1)
        result.update({'value': f'{max(mem_usage):.7f}',
                       'unit': 'MiB',
                       })
        return result
