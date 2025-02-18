import logging

from src.common import Singleton
from src.config import ApplicationConfig
from src.controllers.report import ControllerReport

from . import celery_seedz

log = logging.getLogger(__file__)

config_app = ApplicationConfig()


@celery_seedz.task(bind=True, queue=config_app.QUEUE_PROCESS_REPORT)
def process_report(self, **params):
    try:
        extra = {
            "individual_id": params.get("individual_id"),
            "unique_id": params.get("unique_id")
        }
        controller = ControllerReport()
        controller.process_report(params)
        log.info("Report is done", extra=extra)
    except Exception as error:
        log.exception(str(error), extra=extra)
        params.update({'error': str(error)})
        controller.set_error_report(params)
        Singleton.drop()
        raise error
    finally:
        controller.db_disconnect()


def queue_process_report(params):
    process_report.delay(**params)
