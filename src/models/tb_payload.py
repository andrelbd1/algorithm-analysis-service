from sqlalchemy import Column, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.exceptions import ParamInvalid
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel
from .tb_execution import Execution
from .tb_input import Input

config_app = ApplicationConfig()


class Payload(BaseModel):
    __tablename__ = "payload"
    payload_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    execution_id = Column(UUID(as_uuid=True), nullable=False)
    input_id = Column(UUID(as_uuid=True), nullable=False)
    input_value = Column(String(50), nullable=False)
    execution = relationship("Execution", backref="payload")
    input_ref = relationship("Input")
    __table_args__ = (
        Index("idx_payload_execution", execution_id),
        Index("idx_payload_input", input_id),
        ForeignKeyConstraint(
            [execution_id], ["{}.execution.execution_id".format(config_app.DB_SCHEMA)]
        ),
        ForeignKeyConstraint(
            [input_id], ["{}.input.input_id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __input_value(self):
        return self.input_value

    @__input_value.setter
    def __input_value(self, value):
        validate_param("input_value", value, "str")
        self.input_value = value

    def __set_execution(self, value):
        if not isinstance(value, Execution):
            raise ParamInvalid("Value invalid to Execution")
        self.execution = value

    def __set_input_ref(self, value):
        if not isinstance(value, Input):
            raise ParamInvalid("Value invalid to Input")
        self.input_ref = value

    def __set_params(self, params):
        self.__input_value = params.get("input_value")
        self.__set_execution(params.get("execution"))
        self.__set_input_ref(params.get("input"))

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "payload_id": str(self.payload_id),
            "execution_id": str(self.execution_id),
            "input_id": str(self.input_id),
            "input_value": self.__input_value,
            "input": self.input_ref.get(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "enabled": self.enabled,
        }
