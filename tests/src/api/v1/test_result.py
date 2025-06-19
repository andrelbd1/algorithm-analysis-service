import json

import mock

from tests import BaseTestClassTornado


class TestViewResult(BaseTestClassTornado):

    def setUp(self):
        super(BaseTestClassTornado, self).setUp()
        self._url = "/v1/result/evaluation-report/algorithm/0192919b-2501-2fea-a93d-5d5541c4002b/criteria/001fe2d3-09a5-4bc0-b891-45d475a4b1bc/input/0192919b-2501-585f-1492-4f5d22c98267"
        self._header = {'Content-Type': 'application/json'}


    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get(self, mock_controller):
        mock_controller().report.return_value = json.dumps({
            "total_items": 1,
            "report": [
                {
                "input_value": "5",
                "average": "0.000002165000000000000000",
                "unit": "secs"
                }
            ]
            })
        url = self._url + "?amount=20&page=0"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().report.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)


    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get_page_invalid(self, mock_controller):
        url = self._url + "?amount=2&page=-1"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().report.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)


    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get_amount_invalid(self, mock_controller):
        url = self._url + "?amount=2.2&page=0"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().report.called)
        self.assertEqual(response.code, 422)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get_algorithm_invalid(self, mock_controller):
        url = "/v1/result/evaluation-report/algorithm/invalid-id/criteria/001fe2d3-09a5-4bc0-b891-45d475a4b1bc/input/0192919b-2501-585f-1492-4f5d22c98267"
        url += "?amount=20&page=0"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().report.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get_criteria_invalid(self, mock_controller):
        url = "/v1/result/evaluation-report/algorithm/0192919b-2501-2fea-a93d-5d5541c4002b/criteria/invalid_id/input/0192919b-2501-585f-1492-4f5d22c98267"
        url += "?amount=20&page=0"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().report.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.result.ControllerResult")
    def test_get_input_invalid(self, mock_controller):
        url = "/v1/result/evaluation-report/algorithm/0192919b-2501-2fea-a93d-5d5541c4002b/criteria/0192919b-2501-585f-1492-4f5d22c98267/input/invalid_id"
        url += "?amount=20&page=0"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().report.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)