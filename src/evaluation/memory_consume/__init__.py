import logging
from memory_profiler import memory_usage

from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

log = logging.getLogger(__file__)


class MemoryConsume(BaseEvaluation):
    name = 'Memory Consume'

    def run(self, code: BaseCode, params: dict) -> dict:
        result = {'value': None, 'unit': None}
        mem_usage = memory_usage((code.run, (params,)), interval=0.1)
        result.update({'value': f'{max(mem_usage):.7f}',
                       'unit': 'MiB',
                       })
        return result
