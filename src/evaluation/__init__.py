import logging

from src.common import Singleton

from .base import BaseEvaluation
from .count_edges import CountEdges
from .count_nodes import CountNodes
from .detect_cycle import DetectCycle
from .memory_consume import MemoryConsume
from .running_time import RunningTime


log = logging.getLogger(__file__)


__all__ = ["CountEdges", "CountNodes", "DetectCycle", "MemoryConsume", "RunningTime"]


class Evaluation:

    @staticmethod
    def get_instance(name: str) -> BaseEvaluation:
        for evaluation_class in BaseEvaluation.__subclasses__():
            if evaluation_class.name == name:
                return evaluation_class()
        raise NotImplementedError(f'{name} is a missing evaluation.')
