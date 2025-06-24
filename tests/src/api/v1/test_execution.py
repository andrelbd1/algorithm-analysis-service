import json

import mock

from tests import BaseTestClassTornado


class TestViewExecution(BaseTestClassTornado):

    def setUp(self):
        super(BaseTestClassTornado, self).setUp()
        self._url = "/v1/execution"
        self._header = {'Content-Type': 'application/json'}

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get(self, mock_controller):
        mock_controller().get.return_value = json.dumps({
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "/0195dfda-3263-82cc-6b25-9a302b1df9b5"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().get.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_execution_id(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&execution_id=0195dfda-3263-82cc-6b25-9a302b1df9b5"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_two_execution_ids(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&execution_id=0195dfda-3263-82cc-6b25-9a302b1df9b5;0195dfda-3263-82cc-6b25-9a302b1df9b6"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)
    
    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_algorithm_id(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&algorithm_id=0192919b-2501-2fea-a93d-5d5541c4002b"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_two_algorithm_ids(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&algorithm_id=0195dfda-3263-82cc-6b25-9a302b1df9b5;0195dfda-3263-82cc-6b25-9a302b1df9b6"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_alias(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&alias=Execution_2024_07_18_11_27_07"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_status_DONE(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&status=DONE"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_status_DONE_and_QUEUE(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
            "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&result_status=DONE;QUEUE"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)
    
    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_request_date(self, mock_controller):
        mock_controller().list_objects.return_value = json.dumps({
        "total_items": 1,
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "?amount=20&page=0&request_date=2025-03-29"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().list_objects.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_page_invalid(self, mock_controller):
        url = self._url + "?amount=2&page=-1&execution_id=21d88834-5021-5fff-a66f-0069f40ec3e7"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_amount_invalid(self, mock_controller):
        url = self._url + "?amount=2.2&page=0&execution_id=21d88834-5021-5fff-a66f-0069f40ec3e7"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 422)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_execution_id_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&execution_id=wrong"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_execution_status_queue_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&execution_status=queue"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_result_status_queue_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&execution_status=queue"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_execution_id_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&execution_id=123456"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_algorithm_id_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&algorithm_id=123456"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_list_objects_request_date_invalid(self, mock_controller):
        url = self._url + "?amount=20&page=0&request_date=2024-02-31"
        response = self.fetch(url, headers=self._header, method='GET')
        result = json.loads(response.body.decode())
        self.assertFalse(mock_controller().list_objects.called)
        self.assertEqual(response.code, 400)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_delete(self, mock_controller):
        url = self._url + "/21d88834-5021-5fff-a66f-0069f40ec3e7"
        response = self.fetch(url, headers=self._header, method='DELETE')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().set_enabled_to_false.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_get_id(self, mock_controller):
        mock_controller().get.return_value = json.dumps({
            "executions": [
                {
                    "execution_id": "0195dfda-3263-82cc-6b25-9a302b1df9b5",
                    "payload": {
                        "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                        "algorithm_name": "Factorial",
                        "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                        ],
                        "alias": "Execution_2024_07_18_11_27_07"
                    },
                    "status": "DONE",
                    "message": None,
                    "request_date": "2025-03-29 03:02:53",
                    "result": [
                        {
                        "criteria": "Running Time",
                        "value": "0.0000324",
                        "unit": "secs",
                        "message": None,
                        "status": "DONE"
                        }
                    ]
                }
            ]
        })
        url = self._url + "/0195dfda-3263-82cc-6b25-9a302b1df9b5"
        response = self.fetch(url, headers=self._header, method="OPTIONS")
        self.assertEqual(response.code, 204)

    @mock.patch("src.api.v1.execution.queue_execution")
    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_post(self, mock_controller, mock_task):
        url = self._url
        payload = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41",
        }
        mock_controller().add.return_value = {"id": "21d88834-5021-5fff-a66f-0069f40ec3e7"}
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        result = json.loads(response.body.decode())
        self.assertTrue(mock_controller().add.called)
        self.assertTrue(mock_task.called)
        self.assertEqual(response.code, 200)
        self.assertIsInstance(result, dict)
        self.assertIsNotNone(result["id"])        

    def test_post_algorithm_id_null(self):
        url = self._url
        payload = {
            "algorithm_id": None,
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41",
        }
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        self.assertEqual(response.code, 422)

    def test_post_algorithm_id_invalid_uuid(self):
        url = self._url
        payload = {
            "algorithm_id": "0192919b-2501-585f-1492-4f5d2",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41",
        }
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        self.assertEqual(response.code, 400)

    def test_post_input_null(self):
        url = self._url
        payload = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": None,
            "alias": "Execution_2025_01_01_16_06_41",
        }
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        self.assertEqual(response.code, 422)

    def test_post_input_empty_list(self):
        url = self._url
        payload = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [],
            "alias": "Execution_2025_01_01_16_06_41",
        }
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        self.assertEqual(response.code, 422)

    @mock.patch("src.api.v1.execution.ControllerExecution")
    def test_exception_post(self, mock_controller):
        url = self._url
        payload = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41",
        }
        mock_controller().add.side_effect = Exception("Interno Server errror")
        response = self.fetch(url, body=json.dumps(payload), headers=self._header, method='POST')
        self.assertTrue(mock_controller().add.called)
        self.assertEqual(response.code, 500)
    