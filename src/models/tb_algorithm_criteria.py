from sqlalchemy import Column, ForeignKeyConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config import ApplicationConfig
from src.exceptions import ParamInvalid
from src.internal_services.app_ulid import AppUlid

from .base import BaseModel
from .tb_algorithm import Algorithm
from .tb_criteria import Criteria

config_app = ApplicationConfig()


class AlgorithmCriteria(BaseModel):

    __tablename__ = "algorithm_criteria"
    algorithm_criteria_id = Column(UUID(as_uuid=True), primary_key=True, default=AppUlid.ulid_to_uuid)
    algorithm_id = Column(UUID(as_uuid=True), nullable=False)
    criteria_id = Column(UUID(as_uuid=True), nullable=False)
    algorithm = relationship("Algorithm")
    criteria = relationship("Criteria")
    __table_args__ = (
        Index("idx_algorithm_criteria_algorithm", algorithm_id),
        Index("idx_criteria_algorithm_criteria", criteria_id),
        ForeignKeyConstraint(
            [algorithm_id], ["{}.algorithm.algorithm_id".format(config_app.DB_SCHEMA)]
        ),
        ForeignKeyConstraint(
            [criteria_id], ["{}.criteria.criteria_id".format(config_app.DB_SCHEMA)]
        ),
        {"schema": config_app.DB_SCHEMA},
    )

    def __set_algorithm(self, value):
        if not isinstance(value, Algorithm):
            raise ParamInvalid("Value invalid to Algorithm")
        self.algorithm = value

    def __set_criteria(self, value):
        if not isinstance(value, Criteria):
            raise ParamInvalid("Value invalid to Criteria")
        self.criteria = value

    def __set_params(self, params):
        self.__set_algorithm(params.get("algorithm"))
        self.__set_criteria(params.get("criteria"))

    def add(self, params):
        self.__set_params(params)

    def update(self, params):
        self.__set_params(params)

    def get(self):
        return {
            "acceptance_criteria_id": str(self.acceptance_criteria_id),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
