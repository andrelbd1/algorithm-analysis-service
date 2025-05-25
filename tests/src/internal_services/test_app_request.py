import mock

from src.exceptions import (ErrorPartnerGreaterEqual400,
                            ErrorPartnerGreaterEqual500)
from src.internal_services.app_request import RequestsApp
from tests import BaseTestClass


class ServiceRequestsApp(BaseTestClass):

    def setUp(self):
        self._url = "www.tests.com"

    @property
    def requests(self):
        return RequestsApp()

    @mock.patch('src.internal_services.app_request.requests')
    def test_request_post(self, requests_mock):
        requests_mock.post.return_value = self._mock_response()
        response = self.requests.post(self._url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('src.internal_services.app_request.requests')
    def test_request_get(self, requests_mock):
        requests_mock.get.return_value = self._mock_response()
        response = self.requests.get(self._url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('src.internal_services.app_request.requests')
    def test_request_delete(self, requests_mock):
        requests_mock.delete.return_value = self._mock_response()
        response = self.requests.delete(self._url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('src.internal_services.app_request.requests')
    def test_request_put(self, requests_mock):
        requests_mock.put.return_value = self._mock_response()
        response = self.requests.put(self._url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('src.internal_services.app_request.requests')
    def test_error_validate_response_500(self, requests_mock):
        requests_mock.delete.return_value = self._mock_response(status=500)
        with self.assertRaises(ErrorPartnerGreaterEqual500):
            self.requests.delete(self._url)

    @mock.patch('src.internal_services.app_request.requests')
    def test_error_validate_response_400(self, requests_mock):
        requests_mock.delete.return_value = self._mock_response(status=400)
        with self.assertRaises(ErrorPartnerGreaterEqual400):
            self.requests.delete(self._url)
