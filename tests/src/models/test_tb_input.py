from src.exceptions import ParamInvalid
from src.models.tb_algorithm import Algorithm
from src.models.tb_input import Input
from tests import BaseTestClass

class TestInput(BaseTestClass):

    @property
    def __input(self):
        return Input()
    
    def test_add_get(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        input.add(params)
        result = input.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertEqual(result.get("input_type"), params.get("input_type"))
        self.assertIn("input_id", result)
    
    def test_add_algorithm_null(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": None,
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)

    def test_add_algorithm_invalid(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Input(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)

    def test_add_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)

    def test_add_name_invalid(self):
        params = {
            "name": 123,
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)


    def test_add_input_type_null(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": None,
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)

    def test_add_input_type_invalid(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": 123,
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.add(params)

    def test_update(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        input.update(params)
        result = input.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertEqual(result.get("input_type"), params.get("input_type"))
        self.assertIn("input_id", result)

    def test_update_algorithm_null(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": None,
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)

    def test_update_algorithm_invalid(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Input(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)

    def test_update_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)

    def test_update_name_invalid(self):
        params = {
            "name": 123,
            "description": "mock_description",
            "input_type": "mock_input_type",
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)

    def test_update_input_type_null(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": None,
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)

    def test_update_input_type_invalid(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "input_type": 123,
            "algorithm": Algorithm(),
        }
        input = self.__input
        with self.assertRaises(ParamInvalid):
            input.update(params)