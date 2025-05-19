from src.config import ApplicationConfig
from tests import BaseTestClass


class TestConfig(BaseTestClass):

    @property
    def __application_config(self):
        return ApplicationConfig()
