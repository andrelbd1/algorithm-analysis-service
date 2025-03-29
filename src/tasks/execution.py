import logging

from src.common import Singleton
from src.config import ApplicationConfig
from src.controllers.execution import ControllerExecution

from . import celery_app

log = logging.getLogger(__file__)

config_app = ApplicationConfig()


@celery_app.task(bind=True, queue=config_app.QUEUE_EXECUTION)
def process_algorithm(self, **params: dict):
    """
    Processes an algorithm asynchronously.

    This Celery task processes a algorithm based on the provided parameters.
    It logs the progress and handles any exceptions that occur during the process.

    Args:
        self (Task): The Celery task instance.
        **params (dict): A dictionary of parameters required for processing the algorithm. Expected keys include:
            - individual_id (str): The ID of the individual.
            - unique_id (str): A unique identifier for the execution.

    Raises:
        Exception: If an error occurs during the algorithm processing, it is logged, and the error is set in the execution.

    Logs:
        Logs the completion of the execution or any exceptions that occur,
        along with the provided individual_id and unique_id.
    """
    try:
        extra = {
            "individual_id": params.get("individual_id"),
            "unique_id": params.get("unique_id")
        }
        controller = ControllerExecution()
        controller.run(params)
        log.info("Execution is done", extra=extra)
    except Exception as error:
        log.exception(str(error), extra=extra)
        params.update({'error': str(error)})
        controller.set_error_execution(params)
        Singleton.drop()
        raise error
    finally:
        controller.db_disconnect()


def queue_execution(params: dict):
    """
    Queue the process_execution task with the given parameters.

    This function uses Celery to asynchronously queue the process_execution task.

    Args:
        params (dict): A dictionary of parameters to pass to the process_execution task.
    """
    process_algorithm.delay(**params)
