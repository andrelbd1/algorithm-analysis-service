from sqlalchemy import Column, String, Date, Text
from sqlalchemy.dialects.postgresql import UUID

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel

config_app = ApplicationConfig()
STATUS_DESIGNING = 'DESIGNING'
STATUS_OPEN = 'OPEN'
STATUS_DONE = 'DONE'
STATUS_CANCELED = 'CANCELED'


class Questionnaire(BaseModel):
    __tablename__ = "questionnaire"
    questionnaire_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    value = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    __table_args__ = (
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
    def __description(self):
        return self.description

    @__description.setter
    def __description(self, value):
        self.description = value

    @property
    def __status(self):
        return self.status

    @__status.setter
    def __status(self, value):
        self.status = value

    @property
    def __start_date(self):
        return self.start_date

    @__start_date.setter
    def __start_date(self, value):
        validate_param("start_date", value)
        self.start_date = value

    @property
    def __end_date(self):
        return self.end_date

    @__end_date.setter
    def __end_date(self, value):
        self.end_date = value

    def __set_params(self, params):
        self.__value = params.get("value")
        self.__description = params.get("description")
        self.__status = params.get("status")
        self.__start_date = params.get("start_date")
        self.__end_date = params.get("end_date")

    def add(self, params):
        self.__enabled = True
        self.__status = STATUS_DESIGNING
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def set_status_to_open(self):
        self.__status = STATUS_OPEN

    def set_status_to_done(self):
        self.__status = STATUS_DONE

    def set_status_to_canceled(self):
        self.__status = STATUS_CANCELED

    def get(self):
        return {
            "language_id": str(self.questionnaire_id),
            "value": self.__value,
            "description": self.__description,
            "status": self.__status,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
