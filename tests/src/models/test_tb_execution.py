import mock
from src.exceptions import ParamInvalid
from src.models.tb_algorithm import Algorithm
from src.models.tb_execution import (Execution, STATUS_DONE, STATUS_ERROR,
                                     STATUS_PROCESSING, STATUS_QUEUE, STATUS_WARNING)
from tests import BaseTestClass

class TestExecution(BaseTestClass):

    @property
    def __execution(self):
        return Execution()
    
    def test_add_get(self):
        params = {
            "algorithm": Algorithm(),
            "alias": "mock_alias",
        }
        get_payload = {
            "payload_id": "mock_payload_id",
            "input": "mock_input",
            "input_value": "mock_input_value",
            "enabled": "mock_enabled"
        }
        get_result = {
            "criteria": {"name": "mock_name"},
            "value": "mock_value",
            "unit": "mock_unit",
            "status": "mock_status",
            "message": "mock_message",
            "enabled": "mock_enabled",
        }
        mock_payload = mock.MagicMock()
        mock_payload.get.return_value = get_payload
        mock_result = mock.MagicMock()
        mock_result.get.return_value = get_result
        execution = self.__execution
        execution.add(params)
        execution.payload = [mock_payload]
        execution.result = [mock_result]
        result = execution.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("alias"), params.get("alias"))
        self.assertEqual(result.get("status"), STATUS_QUEUE)
        self.assertEqual(result.get("payload"), [get_payload])
        self.assertIsNotNone(result.get("result"))
        self.assertIn("execution_id", result)
        self.assertIn("algorithm_id", result)

    def test_add_algorithm_null(self):
        params = {
            "algorithm": None
        }
        execution = self.__execution
        with self.assertRaises(ParamInvalid):
            execution.add(params)

    def test_add_algorithm_invalid(self):
        params = {
            "algorithm": Execution()
        }
        execution = self.__execution
        with self.assertRaises(ParamInvalid):
            execution.add(params)

    def test_update(self):
        params = {
            "algorithm": Algorithm(),
            "alias": "mock_alias",
        }
        execution = self.__execution
        execution.update(params)
        result = execution.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("alias"), params.get("alias"))
        self.assertIn("execution_id", result)
        self.assertIn("algorithm_id", result)

    def test_set_to_progressing(self):
        execution = self.__execution
        execution.algorithm = Algorithm()
        execution.set_status_to_progressing()
        result = execution.get()
        self.assertEqual(result["status"], STATUS_PROCESSING)

    def test_set_status_to_done(self):
        execution = self.__execution
        execution.algorithm = Algorithm()
        execution.set_status_to_done()
        result = execution.get()
        self.assertEqual(result["status"], STATUS_DONE)

    def test_set_status_to_warning(self):
        execution = self.__execution
        execution.algorithm = Algorithm()
        message = 'mock_warning_message'
        execution.set_status_to_warning(message)
        result = execution.get()
        self.assertEqual(result["status"], STATUS_WARNING)
        self.assertEqual(result["message"], message)

    def test_set_status_to_error(self):
        execution = self.__execution
        execution.algorithm = Algorithm()
        message = 'mock_warning_message'
        execution.set_status_to_error(message)
        result = execution.get()
        self.assertEqual(result["status"], STATUS_ERROR)
        self.assertEqual(result["message"], message)
