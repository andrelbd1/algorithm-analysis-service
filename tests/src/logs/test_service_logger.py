
from src.logs.service_logger import LoggerService
from tests import BaseTestClass


class TestLoggerService(BaseTestClass):

    @property
    def log_gv(self):
        return LoggerService(__file__)

    def test_log_info(self):
        self.log_gv.info("Test Info")

    def test_log_error(self):
        self.log_gv.error("Test Info")

    def test_log_exception(self):
        self.log_gv.exception("Test Info")

    def test_log_debug(self):
        self.log_gv.debug("Test Info")

    def test_log_warning(self):
        self.log_gv.warning("Test Info")

    def test_log_health(self):
        self.log_gv.health("Test Info")
