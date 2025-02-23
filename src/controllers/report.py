import logging
from datetime import datetime

from src.codes import Codes
from src.common.functions import format_datetime, format_to_alphanumeric, validate_object
from src.config import ApplicationConfig
from src.evaluation import Evaluation
from src.models.tb_report import Report

from . import ControllerDefault
from .algorithm import ControllerAlgorithm
from .criteria import ControllerCriteria
from .payload import ControllerPayload
from .result import ControllerResult

log = logging.getLogger(__file__)
config_app = ApplicationConfig()


class ControllerReport(ControllerDefault):

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

    def __get_instance(self, report_id: str) -> Report:
        """
        Retrieve an instance of the Report with the specified report_id.

        Args:
            report_id (str): The unique identifier of the report to retrieve.

        Returns:
            Report: The Report instance with the specified report_id if found and enabled, otherwise None.
        """
        obj = None
        for item in self._orm.session.query(Report).filter_by(report_id=report_id,
                                                              enabled=True):
            obj = item
        return obj

    def add(self, params: dict) -> str:
        """
        Adds a new report with the given parameters.

        Args:
            params (dict): A dictionary containing the parameters for the report.
                           Expected keys include "algorithm_id" and optionally "report_alias".

        Returns:
            str: The ID of the newly created report.

        Raises:
            KeyError: If "algorithm_id" is not present in params.
            Exception: If there is an error during the report creation process.
        """
        algorithm = self.__controller_algorithm.get_instance(params["algorithm_id"])
        report_alias = f"Report_{datetime.now(config_app.TIMEZONE_VAN).strftime(format_datetime())}"
        report_alias = format_to_alphanumeric(params.get('report_alias', report_alias))
        params.update({
            "report_alias": report_alias,
            "algorithm": algorithm,
        })
        report = Report()
        report.add(params)
        report_id = str(report.report_id)
        if self.__controller_payload.add(params, report) is False:
            report.set_status_to_error("Invalid payload")
        self._orm.object_commit(report)
        self._orm_disconnect()
        return report_id

    def process_report(self, params: dict):
        report_id = params.get("report_id")
        report = self.__get_instance(report_id)
        validate_object(report_id, report)
        report.set_status_to_progressing()
        self._orm.object_commit(report)
        report_data = report.get()
        algorithm = report_data['algorithm']
        payload = report_data['payload']
        criteria = self.__controller_criteria.get_criteria_by_algorithm_id(algorithm['algorithm_id'])
        for c in criteria:
            log.info(f"processing criteria of {c['criteria_name']}")
            code = Codes.get_instance(algorithm)
            result_id = self.__controller_result.add(report_data)
            evaluation = Evaluation.get_instance(criteria)
            evaluation.process(code, payload, result_id)
        report.set_status_to_done()
        self._orm.object_commit(report)

    def set_warning_report(self, params: dict):
        """
        Sets the status of a report to warning with the provided warning message.

        Args:
            params (dict): A dictionary containing the following keys:
                - report_id: The ID of the report to update.
                - warning: The warning message to set for the report.

        Raises:
            ValueError: If the report_id is not found or the report object is invalid.
        """
        report_id = params.get("report_id")
        warning = params.get("warning")
        report = self.__get_instance(report_id)
        validate_object(report_id, report)
        report.set_status_to_warning(warning)
        self._orm.object_commit(report)

    def set_error_report(self, params: dict):
        """
        Sets the status of a report to error with the provided error message.

        Args:
            params (dict): A dictionary containing the following keys:
                - "report_id": The ID of the report to update.
                - "error": The error message to set for the report.

        Raises:
            ValueError: If the report_id is not found or invalid.
        """
        report_id = params.get("report_id")
        error = params.get("error")
        report = self.__get_instance(report_id)
        validate_object(report_id, report)
        report.set_status_to_error(error)
        self._orm.object_commit(report)

    def db_disconnect(self):
        self._orm_disconnect()
