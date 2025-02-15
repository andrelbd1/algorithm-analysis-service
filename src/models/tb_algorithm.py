from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel

config_app = ApplicationConfig()


class Algorithm(BaseModel):
    __tablename__ = "algorithm"
    algorithm_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    source = Column(String(50))
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

    @property
    def __source(self):
        return self.source

    @__source.setter
    def __source(self, value):
        self.source = value

    def __set_params(self, params):
        self.__set_name(params.get("name"))
        self.__set_description(params.get("description"))
        self.__set_source(params.get("source"))

    def __parser_input(self):
        result = []
        if self.result:
            for item_object in self.input:
                item = item_object.get()
                result.append({"input_id": item.get("input_id", ""),
                               "name": item.get("name", ""),
                               "input_type": item.get("input_type", ""),
                               "description": item.get("description", ""),
                               })
        return result

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        inputs = self.__parser_input()
        return {
            "algorithm_id": str(self.algorithm_id),
            "name": self.__name,
            "description": self.__description,
            "source": self.__source,
            "input": inputs,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
