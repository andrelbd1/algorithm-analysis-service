from sqlalchemy import Column, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.exceptions import ParamInvalid
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel
from .tb_report import Report
from .tb_criteria import Criteria

config_app = ApplicationConfig()


class Result(BaseModel):
    __tablename__ = "result"
    result_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    report_id = Column(UUID(as_uuid=True), nullable=False)
    criteria_id = Column(UUID(as_uuid=True), nullable=False)
    value = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    message = Column(Text)
    report = relationship("Report", backref="payload")
    criteria = relationship("Criteria")
    __table_args__ = (
        Index("idx_result_report", report_id),
        Index("idx_result_criteria", criteria_id),
        ForeignKeyConstraint(
            [report_id], ["{}.report.report_id".format(config_app.DB_SCHEMA)]
        ),
        ForeignKeyConstraint(
            [criteria_id], ["{}.criteria.criteria_id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __value(self):
        return self.value

    @__value.setter
    def __value(self, value):
        validate_param("value", value, "str")
        self.value = value

    @property
    def __status(self):
        return self.status

    @__status.setter
    def __status(self, value):
        validate_param("status", value, "str")
        self.status = value

    @property
    def __message(self):
        return self.message

    @__message.setter
    def __message(self, value):
        self.message = value

    def __set_report(self, value):
        if not isinstance(value, Report):
            raise ParamInvalid("Value invalid to Report")
        self.report = value

    def __set_criteria(self, value):
        if not isinstance(value, Criteria):
            raise ParamInvalid("Value invalid to Input")
        self.criteria = value

    def __set_params(self, params):
        self.__value = params.get("input_value")
        self.__status = params.get("input_value")
        self.__set_report(params.get("report"))
        self.__set_criteria(params.get("criteria"))

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "result_id": str(self.result_id),
            "report_id": str(self.report_id),
            "criteria_id": str(self.criteria_id),
            "value": self.__value,
            "status": self.__status,
            "message": self.__message,
            "criteria": self.criteria.get(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
