import logging
from abc import abstractmethod

from src.codes.base import BaseCode
from src.controllers import ControllerDefault
from src.controllers.result import ControllerResult


log = logging.getLogger(__file__)


class BaseEvaluation(ControllerDefault):
    name = 'base'

    @property
    def __controller_result(self):
        return ControllerResult()

    def process(self, code: BaseCode, payload: dict, result_id: str):
        try:
            result = {'result_id': result_id}
            self.__controller_result.set_progress_result(result)
            evaluation = self.run(code, payload)
            result = {'value': evaluation.get('value'),
                      'unit': evaluation.get('unit'),
                      'message': evaluation.get('message'),
                      }
            self.__controller_result.set_done_result(result)
        except Exception as error:
            log.error(f'Error processing evaluation: {error}')
            result.update({'error': str(error)})
            self.__controller_result.set_error_result(result)

    @abstractmethod
    def run(self, code, payload: dict) -> dict:
        raise NotImplementedError('run() is a missing function.')
