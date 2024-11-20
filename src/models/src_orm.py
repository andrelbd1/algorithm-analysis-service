from src.common import Singleton
from src.config import ApplicationConfig

from .orm import Orm

config_app = ApplicationConfig()


class OrmConnect(metaclass=Singleton):

    def __init__(self):
        self.__orm = Orm(database=config_app.connection_string(),
                         timeout=config_app.TIMEOUT_RECONNECT_POSTGRE,
                         pool_size=config_app.POLL_SIZE_POSTGRE)

    @property
    def orm(self):
        return self.__orm
