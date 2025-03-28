import logging
from datetime import datetime

from src.codes import Codes
from src.common.functions import (format_date, format_datetime, format_to_alphanumeric,
                                  result_json, validate_object)
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

    def __format_report(self, report) -> dict:
        """
        Formats a report dictionary into a structured format for output.

        Args:
            report (dict): The report data containing details about the algorithm, 
                           inputs, results, and metadata.

        Returns:
            dict: A formatted dictionary containing:
                - report_id (str): The unique identifier of the report.
                - report_input (dict): Details about the algorithm and its inputs, including:
                    - algorithm_id (str): The ID of the algorithm.
                    - algorithm_name (str): The name of the algorithm.
                    - input (list): A list of dictionaries representing enabled inputs, 
                      each containing:
                        - id (str): The input ID.
                        - name (str): The input name.
                        - value (str): The value of the input.
                    - report_alias (str): The alias of the report.
                - status (str): The current status of the report.
                - message (str): A message associated with the report.
                - request_date (str): The formatted creation date of the report.
                - result (list): A list of dictionaries representing enabled results, 
                  each containing:
                    - criteria (str): The criteria of the result.
                    - value (str): The value of the result.
                    - unit (str): The unit of the result value.
                    - message (str): A message associated with the result.
                    - status (str): The status of the result.
        """
        r_input = {
            "algorithm_id": report["algorithm_id"],
            "algorithm_name": report["algorithm"].get("name"),
            "input": [{'id': i.get('input', {}).get('input_id'),
                       'name': i.get('input', {}).get('name'),
                       'value': i.get('input_value')} for i in report["payload"] if i.get('enabled')],
            "report_alias": report['report_alias']
        }
        r_result = []
        if report["status"] == config_app.STATUS_DONE:
            r_result = [{'criteria': r.get('criteria'),
                         'value': r.get('value'),
                         'unit': r.get('unit'),
                         'message': r.get('message'),
                         'status': r.get('status')} for r in report["result"] if r.get('enabled')]
        return {
            "report_id": report["report_id"],
            "report_input": r_input,
            "status": report["status"],
            "message": report["message"],
            "request_date": report["created_at"].strftime(format_date()),
            "result": r_result
        }

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
        if self.__controller_payload.add(params, report) is False:
            report.set_status_to_error("Invalid payload")
        self._orm.object_commit(report)
        report_id = str(report.report_id)
        self._orm_disconnect()
        return report_id

    def get(self, p_id):
        """
        Retrieve and format a report based on the provided ID.

        Args:
            p_id (str): The ID of the report to retrieve.

        Returns:
            dict: A JSON-serializable dictionary containing the formatted report data.
                  The dictionary has the structure:
                  {
                      'reports': dict  # Formatted report data or an empty dictionary if not found.
                  }
        """
        report = {}
        obj = self.__get_instance(p_id)
        if obj:
            report = self.__format_report(obj.get())
        result = {'reports': report}
        self._orm_disconnect()
        return result_json(result)

    def process_report(self, params: dict):
        """
        Processes a report based on the provided parameters.

        Args:
            params (dict): A dictionary containing the parameters for processing the report.
                Expected keys:
                    - "report_id": The ID of the report to be processed.

        Raises:
            ValueError: If the report_id is not found or the report is invalid.

        Workflow:
            01. Retrieves the report instance using the report_id.
            02. Validates the report object.
            03. Sets the report status to "progressing".
            04. Commits the report object to the ORM.
            05. Retrieves the report data and associates it with the report.
            06. Retrieves the algorithm and payload from the report data.
            07. Gets the code instance for the algorithm.
            08. Setups the code instance for running.
            09. Fetches the criteria associated with the algorithm.
            10. Processes each criterion:
                - Logs the processing of the criterion.
                - Retrieves the criterion instance.
                - Adds the report data to the result controller and gets the result ID.
                - Processes the evaluation for the criterion.
            11. Sets the report status to "done".
            12. Commits the report object to the ORM.
        """
        report_id = params.get("report_id")
        report = self.__get_instance(report_id)
        validate_object(report_id, report)
        report.set_status_to_progressing()
        self._orm.object_commit(report)
        report_data = report.get()
        report_data['report'] = report
        algorithm = report_data['algorithm']
        payload = report_data['payload']
        code = Codes.get_instance(algorithm['name'])
        code.setup(payload)
        criteria = self.__controller_criteria.get_criteria_by_algorithm_id(algorithm['algorithm_id'])
        for c in criteria:
            log.info(f"processing criteria of {c['criteria_name']}")
            report_data['criteria'] = self.__controller_criteria.get_instance(c['criteria_id'])
            result_id = self.__controller_result.add(report_data)
            evaluation = Evaluation.get_instance(c['criteria_name'])
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
