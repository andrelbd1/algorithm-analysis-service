import logging
from datetime import datetime

from src.config import ApplicationConfig
from src.common.functions import format_datetime, format_to_alphanumeric
from src.models.tb_report import Report

from . import ControllerDefault
from .algorithm import ControllerAlgorithm
from .payload import ControllerPayload

log = logging.getLogger(__file__)
config_app = ApplicationConfig()


class ControllerReport(ControllerDefault):

    @property
    def __controller_algorithm(self):
        return ControllerAlgorithm()

    @property
    def __controller_payload(self):
        return ControllerPayload()

    # @property
    # def __controller_result(self):
    #     return ControllerResult()

    def __extract_criteria_to_process(self, dict_entity_index):
        pass

    def __get_instance(self, report_id):
        obj = None
        for item in self._orm.session.query(Report).filter_by(report_id=report_id,
                                                              enabled=True):
            obj = item
        return obj

    def add(self, params):
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

    def process_report(self, params):
        report_id = params.get("report_id")
        report = self.__get_instance(report_id)
        self._validate_object(report_id, report)
        report.set_status_to_progressing()
        self._orm.object_commit(report)
        # report_data = report.get()
        # TODO ...
        report.set_status_to_done()
        self._orm.object_commit(report)

    def set_warning_report(self, params):
        report_id = params.get("report_id")
        warning = params.get("warning")
        report = self.__get_instance(report_id)
        self._validate_object(report_id, report)
        report.set_status_to_warning(warning)
        self._orm.object_commit(report)

    def set_error_report(self, params):
        report_id = params.get("report_id")
        error = params.get("error")
        report = self.__get_instance(report_id)
        self._validate_object(report_id, report)
        report.set_status_to_error(error)
        self._orm.object_commit(report)

    def db_disconnect(self):
        self._orm_disconnect()
