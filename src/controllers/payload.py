from src.config import ApplicationConfig
from src.models.tb_payload import Payload
from src.models.tb_report import Report

from . import ControllerDefault
from .input import ControllerInput

config_app = ApplicationConfig()


class ControllerPayload(ControllerDefault):

    @property
    def __controller_input(self):
        return ControllerInput()

    def __get_instance(self, p_id: str) -> Payload:
        """
        Retrieve an instance of the Payload model based on the given payload ID.

        Args:
            p_id (str): The ID of the payload to retrieve.

        Returns:
            Payload: The instance of the Payload model if found and enabled, otherwise None.
        """
        query = self._orm.session.query(Payload).filter_by(payload_id=p_id,
                                                           enabled=True)
        result = None
        for item in query:
            result = item
        return result

    def __is_payload_valid(self, inputs: list, payload: list) -> bool:
        """
        Validates the payload against the required inputs and their types.

        Args:
            inputs (list): A list of dictionaries where each dictionary contains 'input_id' and 'input_type'.
            payload (list): A list of dictionaries where each dictionary contains 'id' and 'value'.

        Returns:
            bool: True if the payload is valid, False otherwise.

        Raises:
            ValueError: If the payload contains invalid or missing inputs.
        """
        required_inputs = {i['input_id']: False for i in inputs}
        type_inputs = {i['input_id']: i['input_type'] for i in inputs}
        try:
            for p in payload:
                if p.get('id') not in required_inputs:
                    continue
                p_value = p.get('value', '')
                match type_inputs.get(p.get('id')):
                    case 'bool' | 'boolean':
                        if p_value.strip().lower() not in ['true', 'false']:
                            raise ValueError("Payload validation failed due to invalid input.")
                    case 'float':
                        float(p_value.strip())
                    case 'int' | 'integer':
                        int(p_value.strip())
                    case _:
                        continue
                required_inputs[p['id']] = True
            if any(value is False for value in required_inputs.values()):
                raise ValueError("Payload validation failed due to missing inputs.")
            return True
        except ValueError:
            return False

    def add(self, params: dict, report: Report) -> bool:
        """
        Adds a payload to the report if the input parameters are valid.

        Args:
            params (dict): A dictionary containing the parameters for the payload.
                           Expected keys are "algorithm_id" and "input".
            report (Report): The report object to which the payload will be added.

        Returns:
            bool: True if the payload is valid and added successfully, False otherwise.
        """
        is_valid = False
        if (algorithm_id := params.get("algorithm_id")):
            inputs = self.__controller_input.get_input_by_algorithm_id(algorithm_id)
            if (is_valid := self.__is_payload_valid(inputs, params.get("input"))):
                for i in params.get("input"):
                    p = {'input_value': i.get('value'),
                         'report': report,
                         'input': self.__controller_input.get_instance(i.get('id')),
                         }
                    payload = Payload()
                    payload.add(p)
                    self._orm.object_commit(payload)
        return is_valid
