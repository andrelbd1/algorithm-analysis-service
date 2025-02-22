import logging
from abc import abstractmethod

from src.common import Singleton


log = logging.getLogger(__file__)


class BaseCode(metaclass=Singleton):
    name = 'base'

    @abstractmethod
    def run(self, params: dict):
        raise NotImplementedError('run() is missing code.')
