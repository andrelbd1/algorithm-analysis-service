import logging

from src.common import Singleton
from src.config import ApplicationConfig
from src.controllers.report import ControllerReport

from . import celery_seedz

log = logging.getLogger(__file__)

config_app = ApplicationConfig()


@celery_seedz.task(bind=True, queue=config_app.QUEUE_PROCESS_REPORT)
def process_report(self, **params: dict):
    """
    Processes a report asynchronously.

    This Celery task processes a report based on the provided parameters.
    It logs the progress and handles any exceptions that occur during the process.

    Args:
        self (Task): The Celery task instance.
        **params (dict): A dictionary of parameters required for processing the report. Expected keys include:
            - individual_id (str): The ID of the individual.
            - unique_id (str): A unique identifier for the report.

    Raises:
        Exception: If an error occurs during the report processing, it is logged, and the error is set in the report.

    Logs:
        Logs the completion of the report or any exceptions that occur,
        along with the provided individual_id and unique_id.
    """
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


def queue_process_report(params: dict):
    """
    Queue the process_report task with the given parameters.

    This function uses Celery to asynchronously queue the process_report task.

    Args:
        params (dict): A dictionary of parameters to pass to the process_report task.
    """
    process_report.delay(**params)
