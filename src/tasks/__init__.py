import logging.config
import warnings

from celery import Celery, signals
# from elasticapm import Client, instrument
# from elasticapm.contrib.celery import (
#     register_exception_tracking,
#     register_instrumentation,
# )

from src.config import ApplicationConfig
from src.logs.service_logger import LoggerService

warnings.filterwarnings('ignore')

# def config_apm(project_type):

#     if project_type == "api":
#         return

#     instrument()
#     apm_client = Client(
#         server_url=config_app.ELASTIC_HOST,
#         service_name=config_app.ELASTIC_APM_SERVICE_NAME_WORKER,
#     )
#     register_exception_tracking(apm_client)
#     register_instrumentation(apm_client)


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    config_app.LOGGING.update({"disable_existing_loggers": False})
    logging.config.dictConfig(config_app.LOGGING)
    logging.setLoggerClass(LoggerService)


config_app = ApplicationConfig()

celery_app = Celery(config_app.PROJECT_NAME)
celery_app.config_from_object(config_app)

# config_apm(config_app.PROJECT_TYPE)
