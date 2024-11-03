from sqlalchemy import Column, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.functions import validate_param
from src.config import ApplicationConfig
from src.exceptions import ParamInvalid
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel
from .tb_language import Language

config_app = ApplicationConfig()


class Question(BaseModel):
    __tablename__ = "question"
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    language_id = Column(UUID(as_uuid=True))
    value = Column(String(50), nullable=False)
    language = relationship("Language")
    __table_args__ = (
        Index("idx_question_language", language_id),
        ForeignKeyConstraint(
            [language_id], ["{}.language.language_id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    @property
    def __question_id(self):
        return self.question_id

    @property
    def __value(self):
        return self.value

    @__value.setter
    def __value(self, value):
        validate_param("value", value, "str")
        self.value = value

    @property
    def __language(self):
        return self.language

    def __set_language(self, value):
        if not isinstance(value, Language):
            raise ParamInvalid("Value invalid to Language")
        self.language = value

    def __set_params(self, params):
        self.__value = params.get("value")
        self.__set_language(params.get("language"))

    def add(self, params):
        self.__enabled = True
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "question_id": str(self.__question_id),
            "language_id": str(self.language_id),
            "value": self.__value,
            "language": self.language.get(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
