import logging
import logging.config
import os
import pytz

from kombu import Exchange, Queue
from dotenv import load_dotenv

from src.logs.service_logger import LoggerService


class ApplicationConfig:
    load_dotenv(override=True)
    BASE_PATH = os.environ.get("BASE_PATH", "/")
    ENV = os.environ.get("ENV", "local")
    PROJECT_NAME = os.environ.get("PROJECT_NAME", "algorithm-analysis-service")
    PROJECT_TYPE = os.environ.get("PROJECT_TYPE", "api")
    NAME = os.environ.get("ELASTIC_APM_SERVICE_NAME", "Algorithm Analysis Service")
    VERSION = os.environ.get('VERSION', '1.0.0')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SQLALCHEMY_POSTGRES = "postgresql+psycopg2"

    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "dev")
    DB_SCHEMA = os.environ.get("DB_SCHEMA", "service_algorithm_analysis")

    TIMEOUT_RECONNECT_POSTGRES = int(os.getenv('TIMEOUT_RECONNECT_POSTGRES', 30))
    AMOUNT_PROCESS_API = int(os.environ.get("AMOUNT_PROCESS_API", 1))
    POLL_SIZE_POSTGRES = int(os.getenv('POLL_SIZE_POSTGRES', 30))
    PORT_API = os.environ.get("PORT_API", 8000)

    ELASTIC_HOST = os.environ.get("ELASTIC_HOST", "")
    INDEX_LOG_ELASTIC = os.environ.get("INDEX_LOG_ELASTIC", "service_logs")
    ELASTIC_APM_SERVER_URL = os.environ.get("ELASTIC_APM_SERVER_URL", "")
    ELASTIC_APM_SECRET_TOKEN_APM = os.environ.get("ELASTIC_APM_SECRET_TOKEN_APM", "")
    DEBUG_ELASTIC_APM = bool(os.environ.get("DEBUG_ELASTIC_APM", "true"))

    MIGRATION_USER = os.environ.get("MIGRATION_USER", "postgres")
    MIGRATION_PASSWORD = os.environ.get("MIGRATION_PASSWORD", "postgres")
    MAX_BUFFER_SIZE = int(os.environ.get("MAX_BUFFER_SIZE", 10_485_760_000))

    STATUS_DONE = 'DONE'
    STATUS_ERROR = 'ERROR'
    STATUS_PROCESSING = 'PROCESSING'
    STATUS_QUEUE = "QUEUE"
    STATUS_WARNING = 'WARNING'

    TIMEZONE_APP = os.environ.get("TIMEZONE_APP", "America/Vancouver")
    TIME_CRON_PROCESS_EXECUTION = os.environ.get("TIME_CRON_PROCESS_EXECUTION", 1)
    TIMEZONE_VAN = pytz.timezone(TIMEZONE_APP)
    QUEUE_EXECUTION = os.environ.get("QUEUE_EXECUTION", PROJECT_NAME+"_execution")
    QUEUE_CRON = os.environ.get("QUEUE_CRON", PROJECT_NAME+"_cron")
    CELERY_GET_BROKER = os.environ.get("CELERY_GET_BROKER")
    broker_transport_options: dict = {}

    if CELERY_GET_BROKER == "RABBITMQ":
        RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
        RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "admin")
        RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "admin")
        RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")
        broker_url = "pyamqp://{user}:{passw}@{host}:{port}//".format(
            user=RABBITMQ_USER,
            passw=RABBITMQ_PASSWORD,
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
        )
    elif CELERY_GET_BROKER == "REDIS":
        REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
        REDIS_PORT = os.environ.get("REDIS_PORT", "6379/0")
        broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    elif CELERY_GET_BROKER == "SQS":
        SQS_URL = os.environ.get("SQS_URL")
        SQS_AWS_REGION = os.environ.get('SQS_AWS_REGION', 'us-east-1')
        SQS_ACCESS_KEY = os.environ.get('SQS_ACCESS_KEY')
        SQS_SECRET_KEY = os.environ.get('SQS_SECRET_KEY')
        CELERY_BROKER_TRANSPORT_OPTIONS = {
            "region": SQS_AWS_REGION,
            "predefined_queues": {
                QUEUE_EXECUTION: {  # SQS queue name
                    "url": SQS_URL,
                },
                QUEUE_CRON: {
                    "url": SQS_URL,
                }
            },
        }
        if SQS_ACCESS_KEY and SQS_SECRET_KEY:
            _ = CELERY_BROKER_TRANSPORT_OPTIONS['predefined_queues'][QUEUE_EXECUTION]
            _.update({"access_key_id": SQS_ACCESS_KEY, "secret_access_key": SQS_SECRET_KEY})
            _ = CELERY_BROKER_TRANSPORT_OPTIONS['predefined_queues'][QUEUE_CRON]
            _.update({"access_key_id": SQS_ACCESS_KEY, "secret_access_key": SQS_SECRET_KEY})
        broker_url = f'sqs://{SQS_ACCESS_KEY}:{SQS_SECRET_KEY}@' if SQS_ACCESS_KEY and SQS_SECRET_KEY else 'sqs://'
        broker_transport_options = CELERY_BROKER_TRANSPORT_OPTIONS
    backend = None
    broker_connection_retry = True
    broker_connection_retry_on_startup = True
    name_cron = QUEUE_CRON
    task_create_missing_queues = False
    task_serializer = "json"
    task_soft_time_limit = int(os.getenv("TASK_SOFT_TIME_LIMIT", 30_000_000_000_000))
    task_time_limit = 30_000_000_000_000_000
    task_acks_late = True
    worker_prefetch_multiplier = 1
    timezone = TIMEZONE_APP
    imports = (
        "src.tasks.cron_schedule",
        "src.tasks.execution",
    )
    beat_schedule = {
        "cron_to_proces__scheduled_execution": {
            "task": "src.tasks.cron_schedule.execution",
            "schedule": TIME_CRON_PROCESS_EXECUTION * 60,
            "options": {"queue": QUEUE_CRON},
        },
    }
    task_queues = (
        Queue(
            QUEUE_EXECUTION,
            Exchange(QUEUE_EXECUTION),
            routing_key=QUEUE_EXECUTION,
        ),
        Queue(
            QUEUE_CRON,
            Exchange(QUEUE_CRON),
            routing_key=QUEUE_CRON,
        ),
    )
    task_default_queue = QUEUE_EXECUTION
    APPLICATION_SETTINGS = {
        "ELASTIC_APM":
        {
            "SERVICE_NAME": PROJECT_NAME + '-' + ENV,
            "SECRET_TOKEN": ELASTIC_APM_SECRET_TOKEN_APM,
            "Debug": DEBUG_ELASTIC_APM,
            "SERVER_URL": ELASTIC_APM_SERVER_URL
        }
    }
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%s'
            },
            'json': {
                'class': 'src.logs.formats.formatter_json.JsonFormatter',
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
        },
        'handlers': {
            'service_logger': {
                'class': 'src.logs.handler_service.HandlerService',
                'host': ELASTIC_HOST,
                'es_index_name': INDEX_LOG_ELASTIC,
                'use_ssl': True,
                'level': 'INFO',
                'formatter': 'json',
            },
            'dev_null': {
                'class': 'logging.NullHandler'
            },
            'stdout_logger': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'level': "INFO",
                'handlers': ['stdout_logger'],
                'propagate': False,
            },
        },
    }
    logging.setLoggerClass(LoggerService)
    logging.config.dictConfig(LOGGING)

    @classmethod
    def connection_string(cls):
        return f"{cls.SQLALCHEMY_POSTGRES}://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def connection_string_migration(cls):
        return f"{cls.SQLALCHEMY_POSTGRES}://{cls.MIGRATION_USER}:{cls.MIGRATION_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
