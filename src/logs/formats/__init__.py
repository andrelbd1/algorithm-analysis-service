from datetime import datetime, timezone
import logging
import os
import socket
import uuid

ENV = os.environ.get("ENV", "local")
PROJECT_NAME = os.environ.get("PROJECT_NAME")
PROJECT_VERSION = os.environ.get("VERSION", "1.0.0")
PROJECT_TYPE = os.environ.get("PROJECT_TYPE", "api")


class JsonFormatterDefault(logging.Formatter):
    """
    Format logs for send to StackDriver.
    exmple to use:
    logger.info('sent to log stack', extra={'msisdn': msisdn, 'carrier': 'carrier'})
    """

    def __valiate_register(self, field, record):
        value = ""
        if hasattr(record, field):
            value = getattr(record, field)
        return value

    def __unique_id(self, record):
        unique_id = self.__valiate_register("unique_id", record)
        if not unique_id:
            unique_id = str(uuid.uuid4())
        return unique_id

    def __individual_id(self, record):
        individual_id = self.__valiate_register("individual_id", record)
        if not individual_id:
            individual_id = str(uuid.uuid4())
        return individual_id

    def __log_level_name(self, record):
        value = self.__valiate_register("logging_level", record)
        if not value:
            value = record.levelname
        return value

    def _default_format_message(self, record):
        message = {
            'loggingLevel': self.__log_level_name(record),
            'message': record.message,
            'header': {
                'environment': ENV,
                'projectName': PROJECT_NAME,
                'semanticVersion': PROJECT_VERSION,
                'projectType': PROJECT_TYPE,
            },
            'instanceId': socket.gethostname(),
            'uniqueId': self.__unique_id(record),
            'individualId': self.__individual_id(record),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'stackTrace': record.exc_text,
        }
        return message
