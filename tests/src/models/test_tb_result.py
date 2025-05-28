from src.exceptions import ParamInvalid
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution
from src.models.tb_result import (Result, STATUS_DONE, STATUS_ERROR,
                                  STATUS_PROCESSING, STATUS_QUEUE, STATUS_WARNING)
from tests import BaseTestClass

class TestResult(BaseTestClass):

    @property
    def __result(self):
        return Result()
    
    def test_add_get(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria": Criteria(),
        }
        result = self.__result
        result.add(params)
        result = result.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("value"), params.get("value"))
        self.assertEqual(result.get("unit"), params.get("unit"))
        self.assertEqual(result.get("status"), STATUS_QUEUE)
        self.assertEqual(result.get("message"), params.get("message"))
        self.assertIn("result_id", result)
        self.assertIn("execution_id", result)
        self.assertIn("criteria_id", result)

    def test_add_execution_null(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": None,
            "criteria": Criteria(),
        }
        result = self.__result
        with self.assertRaises(ParamInvalid):
            result.add(params)

    def test_add_execution_invalid(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Criteria(),
            "criteria": Criteria(),
        }
        result = self.__result
        with self.assertRaises(ParamInvalid):
            result.add(params)

    def test_add_criteria_null(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria": None,
        }
        result = self.__result
        with self.assertRaises(ParamInvalid):
            result.add(params)

    def test_add_criteria_invalid(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria": Execution(),
        }
        result = self.__result
        with self.assertRaises(ParamInvalid):
            result.add(params)

    def test_update(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria": Criteria(),
        }
        result = self.__result
        result.update(params)
        result = result.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("value"), params.get("value"))
        self.assertEqual(result.get("unit"), params.get("unit"))
        self.assertEqual(result.get("message"), params.get("message"))
        self.assertIn("result_id", result)
        self.assertIn("execution_id", result)
        self.assertIn("criteria_id", result)

    def test_set_to_progressing(self):
        result = self.__result
        result.set_status_to_progressing()
        result.criteria = Criteria()
        result = result.get()
        self.assertEqual(result["status"], STATUS_PROCESSING)

    def test_set_status_to_done(self):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
        }
        result = self.__result
        result.set_status_to_done(params)
        result.criteria = Criteria()
        result = result.get()
        self.assertEqual(result["status"], STATUS_DONE)

    def test_set_status_to_warning(self):
        result = self.__result
        message = 'mock_warning_message'
        result.set_status_to_warning(message)
        result.criteria = Criteria()
        result = result.get()
        self.assertEqual(result["status"], STATUS_WARNING)
        self.assertEqual(result["message"], message)

    def test_set_status_to_error(self):
        result = self.__result
        message = 'mock_warning_message'
        result.set_status_to_error(message)
        result.criteria = Criteria()
        result = result.get()
        self.assertEqual(result["status"], STATUS_ERROR)
        self.assertEqual(result["message"], message)