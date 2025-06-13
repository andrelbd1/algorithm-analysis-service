from src.config import ApplicationConfig
from src.models.tb_input import Input
from src.models.tb_payload import Payload
from src.models.tb_execution import Execution

from . import ControllerDefault
from .input import ControllerInput

config_app = ApplicationConfig()


class ControllerPayload(ControllerDefault):

    @property
    def __controller_input(self):
        return ControllerInput()

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

    def __query_payload_by_execution_id(self, execution_id: str):
        return self._orm.session.query(Input.input_type,
                                       Input.name,
                                       Payload.input_value) \
                                       .join(Payload, Input.input_id == Payload.input_id) \
                                       .filter(Payload.execution_id == execution_id,
                                               Payload.enabled.is_(True))

    def get_payload_by_execution_id(self, execution_id: str) -> list[dict]:
        """
        Retrieve payload details associated with a specific execution ID.

        Args:
            execution_id (str): The ID of the execution for which to retrieve payload details.

        Returns:
            list: A list of dictionaries, each containing the following keys:
        """
        query = self.__query_payload_by_execution_id(execution_id)
        payload = []
        for i in query:
            payload.append({"type": str(i[0]),
                            "name": i[1],
                            "value": i[2],
                            })
        self._orm.remove_session()
        return payload

    def add(self, params: dict, execution: Execution) -> bool:
        """
        Adds a payload to the execution if the input parameters are valid.

        Args:
            params (dict): A dictionary containing the parameters for the payload.
                           Expected keys are "algorithm_id" and "input".
            execution (Execution): The execution object to which the payload will be added.

        Returns:
            bool: True if the payload is valid and added successfully, False otherwise.
        """
        is_valid = False
        if (algorithm_id := params.get("algorithm_id")):
            inputs = self.__controller_input.get_input_by_algorithm_id(algorithm_id)
            if (is_valid := self.__is_payload_valid(inputs, params.get("input"))):
                for i in params.get("input"):
                    p = {'input_value': i.get('value'),
                         'execution': execution,
                         'input': self.__controller_input.get_instance(i.get('id')),
                         }
                    payload = Payload()
                    payload.add(p)
                    self._orm.object_commit(payload)
        return is_valid
