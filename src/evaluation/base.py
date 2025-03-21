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
        """
        Loads and processes a payload list into a dictionary of parameters.

        Args:
            payload (list): A list of dictionaries, where each dictionary contains
                            'input', 'input_type', and 'input_value' keys.

        Returns:
            dict: A dictionary where the keys are the 'name' from each 'input'
                  dictionary and the values are the corresponding 'input_value'
                  converted to the appropriate type based on 'input_type'.
        """
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
        """
        Processes the given code and payload, and updates the result status.

        Args:
            code (BaseCode): The code to be evaluated.
            payload (list): The payload containing parameters for running the code.
            result_id (str): The unique identifier for the result.

        Raises:
            Exception: If an error occurs during the evaluation process.

        The method performs the following steps:
        1. Initializes the result dictionary with the result_id.
        2. Sets the progress status of the result.
        3. Loads the parameters from the payload.
        4. Runs the evaluation with the given code and parameters.
        5. Updates the result dictionary with the evaluation value, unit, and message.
        6. Sets the done status of the result.
        7. If an error occurs, logs the error, updates the result dictionary with the error message, and sets the error status.
        """
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
