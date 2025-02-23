import logging
from src.codes.base import BaseCode

log = logging.getLogger(__file__)


class Factorial(BaseCode):
    name = 'Factorial'

    def run(self, params: dict):
        n = params.get("factorial number")
        match n:
            case 0 | 1:
                return 1
            case _:
                return n * self.run({"factorial number": n - 1})
