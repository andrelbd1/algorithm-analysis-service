import logging
from src.codes.base import BaseCode

log = logging.getLogger(__file__)


class Fibonacci(BaseCode):
    name = 'Fibonacci'

    def run(self, params: dict):
        n = params.get("fibonacci number")
        match n:
            case 0 | 1:
                return n
            case _:
                return self.run({"fibonacci number": n - 1}) + self.run({"fibonacci number": n - 2})
