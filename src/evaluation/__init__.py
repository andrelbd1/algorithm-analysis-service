import logging

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
        """
        Retrieve an instance of a subclass of BaseEvaluation by its name.

        Args:
            name (str): The name of the evaluation class to retrieve.

        Returns:
            BaseEvaluation: An instance of the evaluation class with the specified name.

        Raises:
            NotImplementedError: If no subclass with the specified name is found.
        """
        for evaluation_class in BaseEvaluation.__subclasses__():
            if evaluation_class.name == name:
                return evaluation_class()
        raise NotImplementedError(f'{name} is a missing evaluation.')
