import logging

from src.common import Singleton

from .base import BaseCode
from .dijkstra import Dijkstra
from .factorial import Factorial

log = logging.getLogger(__file__)


__all__ = ["Dijkstra", "Factorial"]


class Codes:

    @staticmethod
    def get_instance(params):
        name = params.get('name')
        for code_class in BaseCode.__subclasses__():
            if code_class.name == name:
                return code_class()
        raise NotImplementedError(f'{name} is a missing code.')
