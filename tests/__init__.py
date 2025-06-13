from unittest import TestCase

import mock
from tornado.testing import AsyncHTTPTestCase

from src.server import ApiServer

class BaseTestClassTornado(AsyncHTTPTestCase):

    # @mock.patch('src.server.ElasticAPM', mock.MagicMock())
    def get_app(self):
        server = ApiServer()
        app = server.make_app()
        # app.settings.update({"apm_elastic": mock.MagicMock()})
        return app

class BaseTestClass(TestCase):

    @staticmethod
    def _mock_response(status=200, content="CONTENT", json_data=None, raise_for_status=None):
        """
            since we typically test a bunch of different
            requests calls for a service, we are going to do
            a lot of mock responses, so its usually a good idea
            to have a helper function that builds these things
            """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)
        return mock_resp