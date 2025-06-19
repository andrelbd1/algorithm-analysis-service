import json
import logging
from datetime import datetime
from sqlalchemy import DateTime, String, and_, func, null, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.cursor import LegacyCursorResult

from src.codes import Codes
from src.common.functions import (format_date, format_datetime, format_to_alphanumeric,
                                  result_json, validate_object)
from src.config import ApplicationConfig
from src.evaluation import Evaluation
from src.models.tb_algorithm import Algorithm
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution
from src.models.tb_input import Input
from src.models.tb_payload import Payload
from src.models.tb_result import Result

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

    def __add_multiple_filters(self, params: dict, query):
        """
        Adds multiple filters to a query based on the provided parameters.

        This method processes a set of predefined filter keys and applies the corresponding
        filtering logic to the query object. The filters are applied using SQLAlchemy expressions.

        Args:
            params (dict): A dictionary containing filter parameters. The keys should match
                the predefined filter names, and the values should be the filter criteria.
                Supported keys include:
                    - "execution_id": Filters by execution ID(s).
                    - "algorithm_id": Filters by algorithm ID(s).
                    - "alias": Filters by execution alias using a case-insensitive partial match.
                    - "execution_status": Filters by execution status (converted to uppercase).
                    - "result_status": Filters by result status (converted to uppercase).
                    - "request_date": Filters by execution creation date (start and end of the day).
                    - "created_at": Filters by execution creation date (start and end of the day).
            query (SQLAlchemy Query): The query object to which the filters will be applied.

        Returns:
            SQLAlchemy Query: The modified query object with the applied filters.

        Notes:
            - For "execution_id", "algorithm_id" and "execution_status",
              multiple values can be provided separated by semicolons (e.g., "value1;value2").
            - For "request_date" and "created_at", the date is parsed and used to filter
              records within the start and end of the specified day.
            - The method uses SQLAlchemy's `and_` and `in_` constructs for combining filters.
        """
        filter_value = []
        filters = ["execution_id", "algorithm_id", "alias", "execution_status", "request_date", "created_at"]
        for value in filters:
            if (result_param := params.get(value)) is None:
                continue
            match value:
                case "execution_id" | "algorithm_id" | "execution_status":
                    if value in ["execution_status"]:
                        value = "status"
                        result_param = result_param.upper()
                    new_result = [item.strip() for item in result_param.split(";")]
                    filter_value.append(getattr(Execution, value).in_(new_result))
                case "request_date" | "created_at":
                    start = datetime.strptime(result_param, format_date())
                    start = datetime.combine(start, datetime.min.time())
                    end = datetime.strptime(result_param, format_date())
                    end = datetime.combine(end, datetime.max.time())
                    filter_value.append(Execution.created_at.between(start, end))
                case "alias":
                    filter_value.append(func.lower(Execution.alias).like("%{}%".format(result_param.strip().lower())))
                case _:
                    continue
        return query.where(and_(*filter_value))

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

    def __get_options_search(self, params: dict) -> LegacyCursorResult:
        """
        Retrieves a list of executions based on the provided search criteria.

        Args:
            params (dict): A dictionary of parameters used to filter and paginate the query.
                Expected keys include:
                    - "amount" (int, optional): The number of records to retrieve. Defaults to 0.
                    - "page" (int, optional): The page number for pagination. Defaults to 0.
                    - Additional keys for filtering are passed to `__add_multiple_filters`.

        Returns:
            sqlalchemy.engine.ResultProxy: The result of the executed query, containing the requested
            execution options and a count of total records.

        Notes:
            - The query retrieves execution details, including algorithm, input, payload, criteria,
              and result information.
            - Filters are applied to ensure only enabled records are included.
            - Pagination is implemented using the "amount" and "page" parameters.
            - The query uses a Common Table Expression (CTE) for modularity and includes a union
              to combine the data query with a count query.
        """
        amount = params.get("amount", 0)
        page = params.get("page", 0)
        data_query = select(func.row_number().over(order_by=Execution.execution_id).label('id'),
                            Execution.execution_id, Execution.algorithm_id, Algorithm.name.label("algorithm_name"),
                            Execution.alias, Execution.status, Execution.message, Execution.created_at
                            ). \
            join(Algorithm, Execution.algorithm_id == Algorithm.algorithm_id). \
            filter(Execution.enabled.is_(True), Algorithm.enabled.is_(True))
        data_query = self.__add_multiple_filters(params, data_query)
        data_query = data_query.order_by(Execution.created_at.desc(), Execution.execution_id.desc())
        data_query = data_query.limit(amount).offset(page * amount)
        data_query = data_query.cte("data_query")
        count_query = select(func.count(func.distinct(Execution.execution_id)).label("total_executions")). \
            join(Algorithm, Execution.algorithm_id == Algorithm.algorithm_id). \
            filter(Execution.enabled.is_(True), Algorithm.enabled.is_(True))
        count_query = self.__add_multiple_filters(params, count_query)
        count = select(count_query.c.total_executions.label("id"),
                       null().cast(UUID).label("execution_id"), null().cast(UUID).label("algorithm_id"),
                       null().cast(String).label("algorithm_name"), null().cast(UUID).label("input_id"),
                       null().cast(String).label("input_name"), null().cast(String).label("input_value"),
                       null().cast(String).label("alias"), null().cast(String).label("status"),
                       null().cast(String).label("message"), null().cast(DateTime).label("created_at"),
                       null().cast(String).label("criteria_name"), null().cast(String).label("value"),
                       null().cast(String).label("unit"), null().cast(String).label("result_message"),
                       null().cast(String).label("result_status")).limit(1).cte("count")
        smt = select(data_query.c.id, data_query.c.execution_id, data_query.c.algorithm_id,
                     data_query.c.algorithm_name, Payload.input_id, Input.name.label("input_name"),
                     Payload.input_value, data_query.c.alias, data_query.c.status, data_query.c.message,
                     data_query.c.created_at, Criteria.name.label("criteria_name"), Result.value,
                     Result.unit, Result.message.label("result_message"), Result.status.label("result_status")
                     ). \
            join(Payload, data_query.c.execution_id == Payload.execution_id, isouter=True). \
            join(Input, Payload.input_id == Input.input_id, isouter=True). \
            join(Result, data_query.c.execution_id == Result.execution_id, isouter=True). \
            join(Criteria, Result.criteria_id == Criteria.criteria_id, isouter=True). \
            filter(Criteria.enabled.is_(True) | (Criteria.enabled.is_(None)),
                   Payload.enabled.is_(True) | (Payload.enabled.is_(None)),
                   Input.enabled.is_(True) | (Input.enabled.is_(None)),
                   Result.enabled.is_(True) | (Result.enabled.is_(None))
                   ). \
            union_all(select(count.c.id, count.c.execution_id, count.c.algorithm_id,
                             count.c.algorithm_name, count.c.input_id, count.c.input_name,
                             count.c.input_value, count.c.alias, count.c.status, count.c.message,
                             count.c.created_at, count.c.criteria_name, count.c.value,
                             count.c.unit, count.c.result_message, count.c.result_status))
        return self._orm.execute_query(smt)

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

    def db_disconnect(self):
        self._orm_disconnect()

    def get(self, p_id) -> dict:
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
        execution = []
        if (obj := self.__get_instance(p_id)):
            execution.append(self.__format_result(obj.get()))
        result = {'executions': execution}
        self._orm_disconnect()
        return result_json(result)

    def list_objects(self, kwargs: dict) -> str:
        """
        Lists execution objects based on the provided search criteria.

        Args:
            kwargs (dict): A dictionary of search parameters which may include:
                - "amount" (int): The number of items to return per page (default is 20).
                - "page" (int): The page number to return (default is 0).
                - "execution_id": Filters by execution ID(s).
                - "algorithm_id": Filters by algorithm ID(s).
                - "alias": Filters by execution alias using a case-insensitive partial match.
                - "execution_status": Filters by execution status (converted to uppercase).
                - "request_date": Filters by execution creation date (start and end of the day).

        Returns:
            str: A JSON string containing the total number of items and a list of executions with their details.
        """
        query = self.__get_options_search(kwargs)
        list_execution = []
        previous_execution_id = None
        for execution in query:
            if execution[1] is None:
                total_items = execution[0]
                break
            execution_result = {
                "criteria": execution[11],
                "value": execution[12],
                "unit": execution[13],
                "message": execution[14],
                "status": execution[15],
            }
            if previous_execution_id == execution[1]:
                list_execution[-1]["result"].append(execution_result)
                continue
            previous_execution_id = execution[1]
            execution_input = {
                "id": str(execution[4]),
                "name": execution[5],
                "value": execution[6]
            }
            list_execution.append({
                "execution_id": str(execution[1]),
                "payload": {
                    "algorithm_id": str(execution[2]),
                    "algorithm_name": execution[3],
                    "input": [execution_input],
                    "alias": execution[7]
                },
                "status": execution[8],
                "message": execution[9],
                "request_date": str(execution[10]),
                "result": [execution_result]
                }),
        result = {"total_items": total_items,
                  "executions": list_execution}
        self._orm_disconnect()
        return json.dumps(result_json(result))

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

    def set_enabled_to_false(self, p_id):
        """
        Disables the execution instance associated with the given primary ID.

        Args:
            p_id: The primary identifier of the execution instance to be disabled.

        Raises:
            ValidationError: If the execution instance corresponding to p_id is invalid.
        """
        execution = self.__get_instance(p_id)
        validate_object(p_id, execution)
        execution.set_enabled_to_false()
        self._orm.object_commit(execution)
        self._orm_disconnect()

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
