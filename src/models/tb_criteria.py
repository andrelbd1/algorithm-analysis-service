from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel

config_app = ApplicationConfig()


class Criteria(BaseModel):
    __tablename__ = "criteria"
    criteria_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    __table_args__ = (
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __name(self):
        return self.name

    @__name.setter
    def __name(self, value):
        validate_param("name", value, "str")
        self.name = value

    @property
    def __description(self):
        return self.description

    @__description.setter
    def __description(self, value):
        self.description = value

    def __set_params(self, params):
        self.__set_name(params.get("name"))
        self.__set_description(params.get("description"))

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "criteria_id": str(self.criteria_id),
            "name": self.__name,
            "description": self.__description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "enabled": self.enabled,
        }
