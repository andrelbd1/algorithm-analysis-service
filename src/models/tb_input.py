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


class Input(BaseModel):
    __tablename__ = "input"
    input_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    algorithm_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(50), nullable=False)
    input_type = Column(String(10), nullable=False)
    description = Column(Text)
    algorithm = relationship("Algorithm", backref="input")
    __table_args__ = (
        Index("idx_input_algorithm", algorithm_id),
        ForeignKeyConstraint(
            [algorithm_id], ["{}.algorithm.algorithm_id".format(config_app.DB_SCHEMA)]
        ),
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
    def __input_type(self):
        return self.input_type

    @__input_type.setter
    def __input_type(self, value):
        validate_param("input_type", value, "str")
        self.input_type = value

    @property
    def __description(self):
        return self.description

    @__description.setter
    def __description(self, value):
        self.description = value

    def __set_algorithm(self, value):
        if not isinstance(value, Algorithm):
            raise ParamInvalid("Value invalid to Algorithm")
        self.algorithm = value

    def __set_params(self, params):
        self.__name = params.get("name")
        self.__description = params.get("description")
        self.__input_type = params.get("input_type")
        self.__set_algorithm(params.get("algorithm"))

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "input_id": str(self.input_id),
            "name": self.__name,
            "description": self.__description,
            "input_type": self.__input_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "enabled": self.enabled,
        }
