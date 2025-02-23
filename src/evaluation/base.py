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

    def __load_payload(self, payload: list) -> dict:
        params = {}
        for item in payload:
            item_input = item.get('input')
            name = item_input.get('name')
            match item_input.get('input_type'):
                case 'int' | 'integer':
                    value = int(item.get('input_value'))
                case 'float':
                    value = float(item.get('input_value'))
                case 'str':
                    value = str(item.get('input_value'))
                case _:
                    value = item.get('input_value')
            params.update({name: value})
        return params

    def process(self, code: BaseCode, payload: list, result_id: str):
        try:
            result = {'result_id': result_id}
            self.__controller_result.set_progress_result(result)
            params = self.__load_payload(payload)
            evaluation = self.run(code, params)
            result.update({'value': evaluation.get('value'),
                           'unit': evaluation.get('unit'),
                           'message': evaluation.get('message'),
                           })
            self.__controller_result.set_done_result(result)
        except Exception as error:
            log.error(f'Error processing evaluation: {error}')
            result.update({'error': str(error)})
            self.__controller_result.set_error_result(result)

    @abstractmethod
    def run(self, code: BaseCode, payload: dict) -> dict:
        raise NotImplementedError('run() is a missing function.')
