import mock
from tornado.web import Application
import asyncio
from src.server import ApiServer
from tests import BaseTestClass


class TestServer(BaseTestClass):

    """Class for test the methods module server."""

    @mock.patch('src.server.HTTPServer')
    @mock.patch('src.server.asyncio.Event')
    def test_server(self, mock_event, mock_httpserver):
        mock_result = mock.AsyncMock()
        mock_result.return_value = "teste"
        mock_event().wait.return_value = mock_result()
        server = ApiServer()
        asyncio.run(server.start())
        self.assertTrue(mock_event().wait.called)
        self.assertIsInstance(server.make_app(), Application)

    # @mock.patch('src.server.HTTPServer')
    # @mock.patch('src.server.asyncio.Event')
    # @mock.patch('src.server.ElasticAPM', mock.MagicMock())
    # def test_server(self, mock_event, mock_httpserver):
    #     mock_result = mock.AsyncMock()
    #     mock_result.return_value = "teste"
    #     mock_event().wait.return_value = mock_result()
    #     server = ApiServer()
    #     asyncio.run(server.start())
    #     self.assertTrue(mock_event().wait.called)
    #     self.assertIsInstance(server.make_app(), Application)
    
    @mock.patch("src.server.tornado.process.fork_processes")
    @mock.patch("src.server.bind_sockets")
    def test_bind_port(self, mock_bind_sockets, mock_fork_process):
        server = ApiServer()
        server.bind_port()
        self.assertTrue(mock_bind_sockets.called)
        self.assertTrue(mock_fork_process.called)
    
    # @mock.patch('src.server.config_app')
    # @mock.patch('src.server.ElasticAPM')
    # def test_add_apm(self, mock_apm, mock_config_app):
    #     mock_config_app.ELASTIC_APM_SERVER_URL = "https://elastic"
    #     mock_app = mock.MagicMock()
    #     server = ApiServer()
    #     server.add_apm(mock_app)
    #     self.assertTrue(mock_apm.called)