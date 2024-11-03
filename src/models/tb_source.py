from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel

config_app = ApplicationConfig()


class Source(BaseModel):
    __tablename__ = "source"
    source_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    value = Column(String(50), nullable=False)
    user_id = Column(String(50), nullable=False)
    alias = Column(String(50))
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
    def __user_id(self):
        return self.user_id

    @__user_id.setter
    def __user_id(self, value):
        validate_param("user_id", value, "str")
        self.user_id = value

    @property
    def __alias(self):
        return self.alias

    @__alias.setter
    def __alias(self, value):
        self.alias = value

    def __set_params(self, params):
        self.__value = params.get("value")
        self.__user_id = params.get("user_id")
        self.__alias = params.get("alias")

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "source_id": str(self.source_id),
            "value": self.__value,
            "code": self.__code,
            "alias": self.__alias,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
