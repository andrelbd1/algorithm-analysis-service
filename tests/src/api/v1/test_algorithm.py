import json

import mock

from tests import BaseTestClassTornado


class TestViewAlgorithm(BaseTestClassTornado):

    def setUp(self):
        super(BaseTestClassTornado, self).setUp()
        self._url = "/v1/algorithm"
        self._header = {'Content-Type': 'application/json'}

    @mock.patch("src.api.v1.algorithm.ControllerAlgorithm")
    def test_get(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
                "total_items": 1,
                "algorithms": [
                    {
                    "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                    "name": "Factorial",
                    "description": "A function that multiplies a positive integer by all the positive integers that are less than or equal to it",
                    "input": [
                        {
                        "input_id": "0192919b-2501-585f-1492-4f5d22c98267",
                        "name": "factorial number",
                        "input_type": "integer",
                        "description": "number to calculate factorial"
                        }
                    ]
                    }
                ]
            })
        url = self._url + "?amount=20&page=0&search_by=algorithm_id&value=0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.algorithm.ControllerAlgorithm")
    def test_get_search_by_null_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&value=0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 422)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.algorithm.ControllerAlgorithm")
    def test_get_amount_invalid(self, mock_controller):
        url = self._url + "?amount=-20&page=0&search_by=algorithm_id&value=0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.algorithm.ControllerAlgorithm")
    def test_get_page_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=2.2&search_by=algorithm_id&value=0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 422)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.algorithm.ControllerAlgorithm")
    def test_delete(self, mock_controller):
        url = self._url + "/0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='DELETE')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().delete.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

