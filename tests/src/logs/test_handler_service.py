from threading import Timer

import mock

from src.logs.formats.formatter_json import JsonFormatter
from src.logs.handler_service import HandlerService
from tests import BaseTestClass


class TestHandlerService(BaseTestClass):
    @property
    def __mock_record(self):

        mock_record = mock.MagicMock()
        mock_record.getMessage.return_value = "Error"
        mock_record.pathname = "teste"
        mock_record.lineno = "teste2"
        mock_record.exc_text = "21f3f21gs"
        mock_record.process = 14221
        mock_record.funcName = "CDB"
        mock_record.lineno = 10
        mock_record.pathname = "path"
        mock_record.logging_level = "EXCEPTION"
        mock_record.unique_id = ""
        mock_record.individual_id = ""
        mock_record.levelname = "CRITICAL"
        mock_record.client_id = 10
        return mock_record

    @property
    def __mock_not_logginlevel_record(self):

        mock_record = mock.MagicMock()
        mock_record.getMessage.return_value = "Error"
        mock_record.pathname = "teste"
        mock_record.lineno = "teste2"
        mock_record.exc_text = "21f3f21gs"
        mock_record.process = 14221
        mock_record.funcName = "CDB"
        mock_record.lineno = 10
        mock_record.pathname = "path"
        mock_record.logging_level = ""
        mock_record.unique_id = ""
        mock_record.individual_id = ""
        mock_record.levelname = "CRITICAL"
        mock_record.client_id = 10
        return mock_record

    @property
    def __handler_sb(self):

        handler = HandlerService(buffer_size=1)
        form = JsonFormatter()
        handler.setFormatter(form)
        return handler

    @mock.patch("src.logs.handler_service.RequestsApp")
    def test_emit(self, mock_request):

        self.__handler_sb.emit(self.__mock_record)
        self.assertTrue(mock_request().post.called)

    @mock.patch("src.logs.handler_service.RequestsApp")
    def test_not_loggin_level_emit(self, mock_request):

        self.__handler_sb.emit(self.__mock_not_logginlevel_record)
        self.assertTrue(mock_request().post.called)

    @mock.patch("src.logs.handler_service.RequestsApp")
    def test_emit_error_send_elastic(self, mock_request):
        mock_request().post.side_effect = Exception()
        handler = HandlerService(buffer_size=1)
        form = JsonFormatter()
        handler.setFormatter(form)
        handler.emit(self.__mock_record)

    # def test_emit_not_buffer(self):
    #     handler = HandlerService()
    #     form = JsonFormatter()
    #     handler.setFormatter(form)
    #     handler.emit(self.__mock_record)

    def test_emit_timer_is_alive(self):
        handler = HandlerService(buffer_size=1)
        handler._timer = Timer(2, handler.flush)
        handler._timer.setDaemon(True)
        handler._timer.start()
        form = JsonFormatter()
        handler.setFormatter(form)
        handler.emit(self.__mock_record)
