import logging
from datetime import datetime

from src.codes import Codes
from src.common.functions import (format_date, format_datetime, format_to_alphanumeric,
                                  result_json, validate_object)
from src.config import ApplicationConfig
from src.evaluation import Evaluation
from src.models.tb_execution import Execution

from . import ControllerDefault
from .algorithm import ControllerAlgorithm
from .criteria import ControllerCriteria
from .payload import ControllerPayload
from .result import ControllerResult

log = logging.getLogger(__file__)
config_app = ApplicationConfig()


class ControllerExecution(ControllerDefault):

    @property
    def __controller_algorithm(self):
        return ControllerAlgorithm()

    @property
    def __controller_criteria(self):
        return ControllerCriteria()

    @property
    def __controller_payload(self):
        return ControllerPayload()

    @property
    def __controller_result(self):
        return ControllerResult()

    def __format_result(self, execution) -> dict:
        """
        Formats a execution dictionary into a structured format for output.

        Args:
            execution (dict): The execution data containing details about the algorithm,
                           inputs, results, and metadata.

        Returns:
            dict: A formatted dictionary containing:
                - execution_id (str): The unique identifier of the execution.
                - payload (dict): Details about the algorithm and its inputs, including:
                    - algorithm_id (str): The ID of the algorithm.
                    - algorithm_name (str): The name of the algorithm.
                    - input (list): A list of dictionaries representing enabled inputs,
                      each containing:
                        - id (str): The input ID.
                        - name (str): The input name.
                        - value (str): The value of the input.
                    - alias (str): The alias of the execution.
                - status (str): The current status of the execution.
                - message (str): A message associated with the execution.
                - request_date (str): The formatted creation date of the execution.
                - result (list): A list of dictionaries representing enabled results,
                  each containing:
                    - criteria (str): The criteria of the result.
                    - value (str): The value of the result.
                    - unit (str): The unit of the result value.
                    - message (str): A message associated with the result.
                    - status (str): The status of the result.
        """
        r_payload = {
            "algorithm_id": execution["algorithm_id"],
            "algorithm_name": execution["algorithm"].get("name"),
            "input": [{'id': i.get('input', {}).get('input_id'),
                       'name': i.get('input', {}).get('name'),
                       'value': i.get('input_value')} for i in execution["payload"] if i.get('enabled')],
            "alias": execution['alias']
        }
        r_result = [{'criteria': r.get('criteria'),
                     'value': r.get('value'),
                     'unit': r.get('unit'),
                     'message': r.get('message'),
                     'status': r.get('status')} for r in execution["result"] if r.get('enabled')]
        return {
            "execution_id": execution["execution_id"],
            "payload": r_payload,
            "status": execution["status"],
            "message": execution["message"],
            "request_date": execution["created_at"].strftime(format_datetime()),
            "result": r_result
        }

    def __get_instance(self, execution_id: str) -> Execution:
        """
        Retrieve an instance of the Execution with the specified execution_id.

        Args:
            execution_id (str): The unique identifier of the execution to retrieve.

        Returns:
            Execution: The Execution instance with the specified execution_id if found and enabled, otherwise None.
        """
        obj = None
        for item in self._orm.session.query(Execution).filter_by(execution_id=execution_id,
                                                                 enabled=True):
            obj = item
        return obj

    def add(self, params: dict) -> str:
        """
        Adds a new execution with the given parameters.

        Args:
            params (dict): A dictionary containing the parameters for the execution.
                           Expected keys include "algorithm_id" and optionally "alias".

        Returns:
            str: The ID of the newly created execution.

        Raises:
            KeyError: If "algorithm_id" is not present in params.
            Exception: If there is an error during the execution creation process.
        """
        algorithm = self.__controller_algorithm.get_instance(params["algorithm_id"])
        alias = f"Execution_{datetime.now(config_app.TIMEZONE_VAN).strftime(format_datetime())}"
        alias = format_to_alphanumeric(params.get('alias', alias))
        params.update({
            "alias": alias,
            "algorithm": algorithm,
        })
        execution = Execution()
        execution.add(params)
        if self.__controller_payload.add(params, execution) is False:
            execution.set_status_to_error("Invalid payload")
        self._orm.object_commit(execution)
        execution_id = str(execution.execution_id)
        self._orm_disconnect()
        return execution_id

    def get(self, p_id):
        """
        Retrieve and format a execution based on the provided ID.

        Args:
            p_id (str): The ID of the execution to retrieve.

        Returns:
            dict: A JSON-serializable dictionary containing the formatted execution data.
                  The dictionary has the structure:
                  {
                      'executions': dict  # Formatted execution data or an empty dictionary if not found.
                  }
        """
        execution = {}
        obj = self.__get_instance(p_id)
        if obj:
            execution = self.__format_result(obj.get())
        result = {'executions': execution}
        self._orm_disconnect()
        return result_json(result)

    def run(self, params: dict):
        """
        Run an algorithm based on the provided parameters.

        Args:
            params (dict): A dictionary containing the parameters for processing the algorithm.
                Expected keys:
                    - "execution_id": The ID of the execution to be processed.

        Raises:
            ValueError: If the execution_id is not found or the execution is invalid.

        Workflow:
            01. Retrieves the execution instance using the execution_id.
            02. Validates the execution object.
            03. Sets the execution status to "progressing".
            04. Commits the execution object to the ORM.
            05. Retrieves the execution data and associates it with the execution.
            06. Retrieves the algorithm and payload from the execution data.
            07. Gets the code instance for the algorithm.
            08. Setups the code instance for running.
            09. Fetches the criteria associated with the algorithm.
            10. Processes each criterion:
                - Logs the processing of the criterion.
                - Retrieves the criterion instance.
                - Adds the execution data to the result controller and gets the result ID.
                - Processes the evaluation for the criterion.
            11. Sets the execution status to "DONE".
            12. Commits the execution object to the ORM.
        """
        execution_id = params.get("execution_id")
        execution = self.__get_instance(execution_id)
        validate_object(execution_id, execution)
        execution.set_status_to_progressing()
        self._orm.object_commit(execution)
        execution_data = execution.get()
        execution_data['execution'] = execution
        algorithm = execution_data['algorithm']
        payload = execution_data['payload']
        code = Codes.get_instance(algorithm['name'])
        code.setup(payload)
        criteria = self.__controller_criteria.get_criteria_by_algorithm_id(algorithm['algorithm_id'])
        for c in criteria:
            log.info(f"processing criteria of {c['criteria_name']}")
            execution_data['criteria'] = self.__controller_criteria.get_instance(c['criteria_id'])
            result_id = self.__controller_result.add(execution_data)
            evaluation = Evaluation.get_instance(c['criteria_name'])
            evaluation.process(code, payload, result_id)
        execution.set_status_to_done()
        self._orm.object_commit(execution)

    def set_warning_execution(self, params: dict):
        """
        Sets the status of a execution to warning with the provided warning message.

        Args:
            params (dict): A dictionary containing the following keys:
                - execution_id: The ID of the execution to update.
                - warning: The warning message to set for the execution.

        Raises:
            ValueError: If the execution_id is not found or the execution object is invalid.
        """
        execution_id = params.get("execution_id")
        warning = params.get("warning")
        execution = self.__get_instance(execution_id)
        validate_object(execution_id, execution)
        execution.set_status_to_warning(warning)
        self._orm.object_commit(execution)

    def set_error_execution(self, params: dict):
        """
        Sets the status of a execution to error with the provided error message.

        Args:
            params (dict): A dictionary containing the following keys:
                - "execution_id": The ID of the execution to update.
                - "error": The error message to set for the execution.

        Raises:
            ValueError: If the execution_id is not found or invalid.
        """
        execution_id = params.get("execution_id")
        error = params.get("error")
        execution = self.__get_instance(execution_id)
        validate_object(execution_id, execution)
        execution.set_status_to_error(error)
        self._orm.object_commit(execution)

    def db_disconnect(self):
        self._orm_disconnect()
