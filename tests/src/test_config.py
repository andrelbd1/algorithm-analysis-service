import os
import importlib
import mock
import src.config
from tests import BaseTestClass


class TestConfig(BaseTestClass):

    @property
    def __application_config(self):
        return src.config.ApplicationConfig()

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

    @mock.patch.dict(os.environ, {"CELERY_GET_BROKER": "REDIS",
                                  "REDIS_HOST": "mock_host",
                                  "REDIS_PORT": "mock_port",})
    def test_broker_redis(self):
        importlib.reload(src.config)
        res = self.__application_config.broker_url
        self.assertEqual(res, "redis://mock_host:mock_port")

    @mock.patch.dict(os.environ, {"CELERY_GET_BROKER": "RABBITMQ",
                                  "RABBITMQ_HOST": "mock_host",
                                  "RABBITMQ_USER": "mock_user",
                                  "RABBITMQ_PASSWORD": "mock_pass",
                                  "RABBITMQ_PORT": "mock_port"})
    def test_broker_rabbitmq(self):
        importlib.reload(src.config)
        res = self.__application_config.broker_url
        self.assertEqual(res, "pyamqp://mock_user:mock_pass@mock_host:mock_port//")

    @mock.patch.dict(os.environ, {"CELERY_GET_BROKER": "SQS",
                                  "SQS_URL": "mock_sqs_url",
                                  "SQS_AWS_REGION": "mock_sqs_region",
                                  "SQS_ACCESS_KEY": "mock_sqs_access_key",
                                  "SQS_SECRET_KEY": "mock_sqs_secret_key"})
    def test_broker_sqs(self):
        importlib.reload(src.config)
        res = self.__application_config.broker_url
        self.assertEqual(res, "sqs://mock_sqs_access_key:mock_sqs_secret_key@")
