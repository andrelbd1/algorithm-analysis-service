from src.exceptions import ParamInvalid
from src.models.tb_execution import Execution
from src.models.tb_input import Input
from src.models.tb_payload import Payload
from tests import BaseTestClass

class TestPayload(BaseTestClass):

    @property
    def __payload(self):
        return Payload()
    
    def test_add_get(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        payload.add(params)
        result = payload.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("input_value"), params.get("input_value"))
        self.assertIn("payload_id", result)
    
    def test_add_execution_null(self):
        params = {
            "input_value": "mock_input_value",
            "execution": None,
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_add_execution_invalid(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Input(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_add_input_null(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": None,
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_add_input_invalid(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": Execution(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_add_input_value_null(self):
        params = {
            "input_value": None,
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_add_input_value_invalid(self):
        params = {
            "input_value": 123,
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.add(params)

    def test_update(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        payload.update(params)
        result = payload.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("input_value"), params.get("input_value"))
        self.assertIn("payload_id", result)

    def test_update_execution_null(self):
        params = {
            "input_value": "mock_input_value",
            "execution": None,
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)

    def test_update_execution_invalid(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Input(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)

    def test_update_input_null(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": None,
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)

    def test_update_input_invalid(self):
        params = {
            "input_value": "mock_input_value",
            "execution": Execution(),
            "input": Execution(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)

    def test_update_input_value_null(self):
        params = {
            "input_value": None,
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)

    def test_update_input_value_invalid(self):
        params = {
            "input_value": 123,
            "execution": Execution(),
            "input": Input(),
        }
        payload = self.__payload
        with self.assertRaises(ParamInvalid):
            payload.update(params)