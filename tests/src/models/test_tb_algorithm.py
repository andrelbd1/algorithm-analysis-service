import mock
from src.exceptions import ParamInvalid
from src.models.tb_algorithm import Algorithm
from tests import BaseTestClass

class TestAlgorithm(BaseTestClass):

    @property
    def __algorithm(self):
        return Algorithm()
    
    def test_add_get(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "source": "mock_source"
        }
        get_input = {
            "input_id": "mock_input_id",
            "name": "mock_input_name",
            "input_type": "mock_input_type",
            "description": "mock_input_description"
        }
        mock_input = mock.MagicMock()
        mock_input.get.return_value = get_input
        algorithm = self.__algorithm
        algorithm.add(params)
        algorithm.input = [mock_input]
        result = algorithm.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertEqual(result.get("source"), params.get("source"))
        self.assertEqual(result.get("input"), [get_input])
        self.assertIn("algorithm_id", result)

    def test_add_algorithm_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
            "source": "mock_source"
        }
        algorithm = self.__algorithm
        with self.assertRaises(ParamInvalid):
            algorithm.add(params)

    def test_add_algorithm_name_invalid(self):
        params = {
            "name": 1111,
            "description": "mock_description",
            "source": "mock_source"
        }
        algorithm = self.__algorithm
        with self.assertRaises(ParamInvalid):
            algorithm.add(params)

    def test_update(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
            "source": "mock_source"
        }
        algorithm = self.__algorithm
        algorithm.update(params)
        result = algorithm.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertEqual(result.get("source"), params.get("source"))
        self.assertIn("algorithm_id", result)

    def test_update_algorithm_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
            "source": "mock_source"
        }
        algorithm = self.__algorithm
        with self.assertRaises(ParamInvalid):
            algorithm.update(params)

    def test_update_algorithm_name_invalid(self):
        params = {
            "name": 1111,
            "description": "mock_description",
            "source": "mock_source"
        }
        algorithm = self.__algorithm
        with self.assertRaises(ParamInvalid):
            algorithm.update(params)