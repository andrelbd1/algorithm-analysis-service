import mock
from src.config import ApplicationConfig
from tests import BaseTestClass


class TestConfig(BaseTestClass):

    @property
    def __application_config(self):
        return ApplicationConfig()

    @mock.patch("src.config.ApplicationConfig.SQLALCHEMY_POSTGRES", "mock_driver")    
    @mock.patch("src.config.ApplicationConfig.DB_USER", "mock_user")
    @mock.patch("src.config.ApplicationConfig.DB_PASSWORD", "mock_pass")
    @mock.patch("src.config.ApplicationConfig.DB_HOST", "mock_host")
    @mock.patch("src.config.ApplicationConfig.DB_PORT", "mock_port")
    @mock.patch("src.config.ApplicationConfig.DB_NAME", "mock_name")
    def test_connection_string(self):
        connect = self.__application_config.connection_string()
        self.assertEqual(connect, "mock_driver://mock_user:mock_pass@mock_host:mock_port/mock_name")

    @mock.patch("src.config.ApplicationConfig.SQLALCHEMY_POSTGRES", "mock_driver")    
    @mock.patch("src.config.ApplicationConfig.MIGRATION_USER", "mock_user")
    @mock.patch("src.config.ApplicationConfig.MIGRATION_PASSWORD", "mock_pass")
    @mock.patch("src.config.ApplicationConfig.DB_HOST", "mock_host")
    @mock.patch("src.config.ApplicationConfig.DB_PORT", "mock_port")
    @mock.patch("src.config.ApplicationConfig.DB_NAME", "mock_name")
    def test_connection_string_migration(self):
        connect = self.__application_config.connection_string_migration()
        self.assertEqual(connect, "mock_driver://mock_user:mock_pass@mock_host:mock_port/mock_name")