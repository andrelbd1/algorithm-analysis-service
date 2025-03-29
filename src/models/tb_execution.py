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
STATUS_DONE = config_app.STATUS_DONE
STATUS_ERROR = config_app.STATUS_ERROR
STATUS_PROCESSING = config_app.STATUS_PROCESSING
STATUS_QUEUE = config_app.STATUS_QUEUE
STATUS_WARNING = config_app.STATUS_WARNING


class Execution(BaseModel):
    __tablename__ = "execution"
    execution_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    algorithm_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(20), nullable=False)
    alias = Column(String(100))
    message = Column(Text)
    algorithm = relationship("Algorithm")
    __table_args__ = (
        Index("idx_execution_algorithm", algorithm_id),
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
    def __alias(self):
        return self.alias

    @__alias.setter
    def __alias(self, value):
        self.alias = value

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
        self.__alias = params.get("alias")
        self.__set_algorithm(params.get("algorithm"))

    def __parser_payload(self):
        payload = []
        if self.payload:
            for item_object in self.payload:
                item = item_object.get()
                payload.append({"payload_id": item.get("payload_id", ""),
                                "input": item.get("input", ""),
                                "input_value": item.get("input_value", ""),
                                "enabled": item.get("enabled", "")
                                })
        return payload

    def __parser_result(self):
        result = []
        if self.result:
            for item_object in self.result:
                item = item_object.get()
                result.append({"criteria": item.get("criteria", {}).get("name", ""),
                               "value": item.get("value", ""),
                               "unit": item.get("unit", ""),
                               "status": item.get("status", ""),
                               "message": item.get("message", ""),
                               "enabled": item.get("enabled", "")
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
            "execution_id": str(self.execution_id),
            "algorithm_id": str(self.algorithm_id),
            "status": self.__status,
            "alias": self.__execution_alias,
            "message": self.__message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "enabled": self.enabled,
            "algorithm": self.algorithm.get(),
            "payload": payload,
            "result": result,
        }
