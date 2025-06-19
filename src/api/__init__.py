import logging
from functools import wraps
from http import HTTPStatus

from tornado.web import RequestHandler
from webargs import fields
from webargs.tornadoparser import HTTPError

from src.common import Singleton
from src.common.functions import log_extra, uuid_4, validate_field_null, validate_non_negative_integer
from src.exceptions import AppError

logger = logging.getLogger(__name__)


class InternalRequestHandler(RequestHandler):

    param_search_by = {
        "search_by": fields.Str(required=True, validate=validate_field_null),
        "value": fields.Str(dump_default=""),
        "page": fields.Int(required=True, dump_default=0, validate=validate_non_negative_integer),
        "amount": fields.Int(required=True, dump_default=20, validate=validate_non_negative_integer),
    }

    def __message_default(self, status_code, message):
        self.set_status(status_code)
        self.write(message)
        self.finish()

    def _secure_filename(self, filename):
        filename = filename.replace("..", "")
        filename = filename.replace("/", "")
        filename = filename.replace(".", "")
        return "upload_" + filename

    def error(self, status_code, message):
        result = {"status": "fail", "message": message}
        self.__message_default(status_code, result)

    def initialize(self):
        self.set_header("Content-Type", "application/json")
        self._log_extra = {}

    def options(self, *args):
        self.set_status(204)
        self.finish()

    def prepare(self):
        unique_id = self.request.headers.get("X-Request-Id", uuid_4())
        individual_id = self.request.headers.get("X-Individual-Id", uuid_4())
        self._log_extra = log_extra(individual_id, unique_id)

    def success(self, result):
        status_code = HTTPStatus.OK if result is not None else HTTPStatus.CREATED
        message = result if result is not None else ""
        self.__message_default(status_code, message)

    @classmethod
    def api_method_wrapper(cls, function):
        p_method = function

        @wraps(p_method)
        async def _execute_method(
            self: InternalRequestHandler, *path_parameter, **kwargs
        ):
            """Execute method of instance."""
            # apm = self.settings.get("apm_elastic")
            try:
                result = await p_method(self, *path_parameter, **kwargs)
                self.success(result)
            except HTTPError as error:
                # apm.client.capture_message(str(error))
                logger.error(str(error))
                self.error(error.status_code, error.messages)
            except AppError as error:
                # apm.client.capture_message(str(error))
                logger.error(str(error))
                self.error(error.status, str(error))
            except Exception as error:
                # apm.client.capture_exception()
                Singleton.drop()
                logger.exception(str(error))
                self.error(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error")

        return _execute_method
