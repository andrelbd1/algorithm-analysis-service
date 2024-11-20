
from . import JsonFormatterDefault


class JsonFormatter(JsonFormatterDefault):
    """
    Format logs for send to StackDriver.
    exmple to use:
    logger.info('sent to log stack', extra={'msisdn': msisdn, 'carrier': 'carrier'})
    """

    def format(self, record):
        super(JsonFormatter, self).format(record)
        return self._default_format_message(record)
