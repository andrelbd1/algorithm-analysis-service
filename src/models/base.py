from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import declarative_base

from src.common.functions import date_utc_now

Base = declarative_base()


class BaseModel(Base):
    """Defaut Classe to tables of system."""

    __abstract__ = True
    __TYPE__ = "abstract"
    created_at = Column(DateTime,
                        default=date_utc_now)
    updated_at = Column(DateTime,
                        default=date_utc_now,
                        onupdate=date_utc_now)
    enabled = Column(Boolean,
                     nullable=False,
                     default=True)

    def set_enabled_to_false(self):
        self.__enabled = False
