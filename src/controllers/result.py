import json
import logging
from sqlalchemy import String, and_, func, null, select, Integer, Numeric
from sqlalchemy.engine.cursor import LegacyCursorResult
from datetime import datetime

from src.common.functions import format_date, result_json, validate_object
from src.config import ApplicationConfig
from src.models.tb_algorithm import Algorithm
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution
from src.models.tb_input import Input
from src.models.tb_payload import Payload
from src.models.tb_result import Result

from . import ControllerDefault

log = logging.getLogger(__file__)
config_app = ApplicationConfig()


class ControllerResult(ControllerDefault):

    def __add_multiple_filters(self, params: dict, query):
        """
        Applies multiple filters to a SQLAlchemy query based on provided parameters.

        Args:
            params (dict): A dictionary containing filter parameters. Supported keys are
                "algorithm_id", "criteria_id", "alias", "request_date", and "created_at".
                - "algorithm_id" and "criteria_id" expect semicolon-separated values.
                - "alias" expects a string for case-insensitive partial matching.
                - "request_date" and "created_at" expect a date string in the format specified by `format_date()`.
            query: The initial SQLAlchemy query object to which filters will be applied.

        Returns:
            The SQLAlchemy query object with the applied filters.

        Notes:
            - For "algorithm_id" and "criteria_id", filters are applied using the `in_` operator.
            - For "alias", a case-insensitive LIKE filter is used.
            - For "request_date" and "created_at", a date range filter is applied for the entire day.
            - Only parameters present in `params` are used for filtering.
        """
        filter_value = []
        filters = ["algorithm_id", "criteria_id", "alias", "request_date", "created_at"]
        for value in filters:
            if (result_param := params.get(value)) is None:
                continue
            match value:
                case "algorithm_id":
                    new_result = [item.strip() for item in result_param.split(";")]
                    filter_value.append(getattr(Execution, value).in_(new_result))
                case "criteria_id":
                    new_result = [item.strip() for item in result_param.split(";")]
                    filter_value.append(getattr(Criteria, value).in_(new_result))
                case "input_id":
                    new_result = [item.strip() for item in result_param.split(";")]
                    filter_value.append(getattr(Input, value).in_(new_result))
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

    def __get_instance(self, p_id: str) -> Result:
        """
        Retrieve an instance of the Result model based on the given result ID.

        Args:
            p_id (str): The ID of the result to retrieve.

        Returns:
            Result: The instance of the Result model if found and enabled, otherwise None.
        """
        query = self._orm.session.query(Result).filter_by(result_id=p_id,
                                                          enabled=True)
        result = None
        for item in query:
            result = item
        return result

    def __make_report(self, params: dict) -> LegacyCursorResult:
        """
        Generates a paginated report of average result values grouped by input value and unit.
        Args:
            params (dict): Dictionary containing filter and pagination parameters. Expected keys include:
                - "amount" (int): Number of records per page.
                - "page" (int): Page number (zero-based).
                - "algorithm_id": Filters by algorithm ID(s).
                - "criteria_id": Filters by criteria_id ID(s).
                - "input_id": Filters by input ID(s).
                - Additional filter parameters as alias and request_date.
        Returns:
            LegacyCursorResult: The result of the executed query, including paginated average values and a count of total groups.
        The report aggregates results by input value and unit, computes the average for each group, and supports pagination.
        """
        amount = params.get("amount", 0)
        page = params.get("page", 0)
        data_query = select(func.row_number().over(order_by=Execution.execution_id).label('id'),
                            func.cast(Payload.input_value, Integer).label('input_value'),
                            Result.unit, func.cast(Result.value, Numeric).label('value')
                            ). \
            join(Payload, Execution.execution_id == Payload.execution_id). \
            join(Input, Input.input_id == Payload.input_id). \
            join(Algorithm, Execution.algorithm_id == Algorithm.algorithm_id). \
            join(Result, Result.execution_id == Execution.execution_id). \
            join(Criteria, Criteria.criteria_id == Result.criteria_id). \
            filter(Execution.enabled.is_(True), Algorithm.enabled.is_(True),
                   Result.status == config_app.STATUS_DONE)
        data_query = self.__add_multiple_filters(params, data_query)
        data_query = data_query.order_by(func.cast(Payload.input_value, Integer).asc())
        data_query = data_query.cte("data_query")
        group_query = select(func.row_number().over(order_by=data_query.c.input_value).label('id'),
                             data_query.c.input_value.label('input_value'), data_query.c.unit.label('unit'),
                             func.avg(data_query.c.value).label('average')). \
            group_by(data_query.c.input_value, data_query.c.unit). \
            order_by(data_query.c.input_value). \
            limit(amount).offset(page * amount). \
            cte("group_query")
        count = select(func.count(func.distinct(group_query.c.id)).label("id"),
                       null().cast(Integer).label("input_value"), null().cast(String).label("unit"),
                       null().cast(Numeric).label("average"))
        smt = select(group_query.c.id, group_query.c.input_value,
                     group_query.c.average, group_query.c.unit). \
            union_all(select(count.c.id, count.c.input_value,
                             count.c.average, count.c.unit))
        return self._orm.execute_query(smt)

    def report(self, kwargs: dict) -> str:
        """
        Generates a report of algorithm executions based on provided search criteria.

        Args:
            kwargs (dict): Dictionary of search parameters, which may include:
                - amount (int, optional): Number of items per page. Defaults to 20.
                - page (int, optional): Page number for pagination. Defaults to 0.
                - algorithm_id (int or list[int]): Filter by one or more algorithm IDs.
                - criteria_id (int or list[int]): Filter by one or more criteria IDs.
                - input_id (int or list[int]): Filter by one or more input IDs.
                - alias (str, optional): Case-insensitive partial match for execution alias.
                - request_date (str or datetime, optional): Filter by execution creation date (start and end of the day).

        Returns:
            str: JSON-encoded string containing:
                - total_items (int): Total number of matching executions.
                - report (list[dict]): List of execution details, each with:
                    - input_value (str): The input value used in the execution.
                    - average (str): The average result for the input value.
                    - unit (str): The unit of measurement for the result.
        """
        report_result = []
        query = self.__make_report(kwargs)
        for report in query:
            if report[1] is None:
                total_items = report[0]
                break
            report_result.append({
                "input_value": str(report[1]),
                "average": str(report[2]),
                "unit": report[3]
            })
        result = {"total_items": total_items,
                  "report": report_result}
        self._orm_disconnect()
        return json.dumps(result_json(result))

    def add(self, params: dict) -> str:
        result = Result()
        result.add(params)
        self._orm.object_commit(result)
        result_id = str(result.result_id)
        self._orm_disconnect()
        return result_id

    def set_done_result(self, params: dict):
        result_id = params.get("result_id")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_done(params)
        self._orm.object_commit(result)
        self._orm_disconnect()

    def set_progress_result(self, params: dict):
        result_id = params.get("result_id")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_progressing()
        self._orm.object_commit(result)
        self._orm_disconnect()

    def set_warning_result(self, params: dict):
        result_id = params.get("result_id")
        warning = params.get("warning")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_warning(warning)
        self._orm.object_commit(result)
        self._orm_disconnect()

    def set_error_result(self, params: dict):
        result_id = params.get("result_id")
        error = params.get("error")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_error(error)
        self._orm.object_commit(result)
        self._orm_disconnect()
