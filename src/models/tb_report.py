from sqlalchemy import Column, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.exceptions import ParamInvalid
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel
from .tb_algorithm import Algorithm

config_app = ApplicationConfig()
STATUS_DONE = 'DONE'
STATUS_ERROR = 'ERROR'
STATUS_PROCESSING = 'PROCESSING'
STATUS_QUEUE = "QUEUE"
STATUS_WARNING = 'WARNING'


class Report(BaseModel):
    __tablename__ = "report"
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    algorithm_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(20), nullable=False)
    report_alias = Column(String(100))
    message = Column(Text)
    algorithm = relationship("Algorithm")
    __table_args__ = (
        Index("idx_report_algorithm", algorithm_id),
        ForeignKeyConstraint(
            [algorithm_id], ["{}.algorithm.algorithm_id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __status(self):
        return self.status

    @__status.setter
    def __status(self, value):
        validate_param("status", value, "str")
        self.status = value

    @property
    def __report_alias(self):
        return self.report_alias

    @__report_alias.setter
    def __report_alias(self, value):
        self.report_alias = value

    @property
    def __message(self):
        return self.message

    @__message.setter
    def __message(self, value):
        self.message = value

    def __set_algorithm(self, value):
        if not isinstance(value, Algorithm):
            raise ParamInvalid("Value invalid to Algorithm")
        self.algorithm = value

    def __set_params(self, params):
        self.__report_alias = params.get("report_alias")
        self.__set_algorithm(params.get("algorithm"))

    def __parser_payload(self):
        payload = []
        if self.payload:
            for item_object in self.payload:
                item = item_object.get()
                payload.append({"payload_id": item.get("payload_id", ""),
                                "input": item.get("input", ""),
                                "input_value": item.get("input_value", "")})
        return payload

    def __parser_result(self):
        result = []
        if self.result:
            for item_object in self.result:
                item = item_object.get()
                result.append({"criteria": item.get("criteria", ""),
                               "value": item.get("value", ""),
                               "status": item.get("status", ""),
                               "message": item.get("message", ""),
                               })
        return result

    def add(self, params):
        self.__enabled = True
        self.__status = STATUS_QUEUE
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def set_status_to_progressing(self):
        self.__status = STATUS_PROCESSING

    def set_status_to_done(self):
        self.__status = STATUS_DONE

    def set_status_to_warning(self, message):
        self.__status = STATUS_WARNING
        self.__message = message

    def set_status_to_error(self, message):
        self.__status = STATUS_ERROR
        self.__message = message

    def get(self):
        payload = self.__parser_payload()
        result = self.__parser_result()
        return {
            "report_id": str(self.report_id),
            "algorithm_id": str(self.algorithm_id),
            "status": self.__status,
            "report_alias": self.__report_alias,
            "message": self.__message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "algorithm": self.algorithm.get(),
            "payload": payload,
            "result": result
        }
