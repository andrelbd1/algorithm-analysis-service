import logging

from src.common import Singleton
from src.config import ApplicationConfig
from src.models.src_orm import OrmConnect

log = logging.getLogger(__file__)


class ControllerDefault(metaclass=Singleton):

    def __init__(self):
        self.__instance_orm = OrmConnect()

    @property
    def _orm(self):
        return self.__instance_orm.orm

    def _orm_disconnect(self):
        self._orm.remove_session()
