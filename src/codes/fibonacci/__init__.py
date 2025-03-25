import logging
from src.codes.base import BaseCode

log = logging.getLogger(__file__)


class Fibonacci(BaseCode):
    name = 'Fibonacci sequence'

    def run(self, params: dict):
        key = "fibonacci number"
        n = params.get(key)
        match n:
            case 0 | 1:
                return n
            case _:
                return self.run({key: n - 1}) + self.run({key: n - 2})
