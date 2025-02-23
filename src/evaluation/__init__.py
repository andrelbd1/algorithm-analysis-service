import logging

from src.common import Singleton

from .base import BaseEvaluation
# from .count_edges import CountEdges
# from .count_nodes import CountNodes
# from .detect_cycle import DetectCycle
# from .memory_consume import MemoryConsume
from .running_time import RunningTime


log = logging.getLogger(__file__)


__all__ = ["RunningTime"]


class Evaluation:

    @staticmethod
    def get_instance(params: dict) -> BaseEvaluation:
        name = params.get('name')
        for evaluation_class in BaseEvaluation.__subclasses__():
            if code_class.name == name:
                return code_class()
        raise NotImplementedError(f'{name} is a missing evaluation.')
