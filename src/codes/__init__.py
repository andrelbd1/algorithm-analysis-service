import logging

from src.common import Singleton

from .base import BaseCode
from .dijkstra import Dijkstra
from .factorial import Factorial

log = logging.getLogger(__file__)


__all__ = ["Dijkstra", "Factorial"]


class Codes:

    @staticmethod
    def get_instance(name: str) -> BaseCode:
        """
        Retrieve an instance of a subclass of BaseCode by its name.

        Args:
            name (str): The name of the subclass to instantiate.

        Returns:
            BaseCode: An instance of the subclass with the specified name.

        Raises:
            NotImplementedError: If no subclass with the specified name is found.
        """
        for code_class in BaseCode.__subclasses__():
            if code_class.name == name:
                return code_class()
        raise NotImplementedError(f'{name} is a missing code.')
