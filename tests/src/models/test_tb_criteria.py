from src.exceptions import ParamInvalid
from src.models.tb_criteria import Criteria
from tests import BaseTestClass

class TestCriteria(BaseTestClass):

    @property
    def __criteria(self):
        return Criteria()
    
    def test_add_get(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
        }
        criteria = self.__criteria
        criteria.add(params)
        result = criteria.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertIn("criteria_id", result)

    def test_add_criteria_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
        }
        criteria = self.__criteria
        with self.assertRaises(ParamInvalid):
            criteria.add(params)

    def test_add_criteria_name_invalid(self):
        params = {
            "name": 1111,
            "description": "mock_description",
        }
        criteria = self.__criteria
        with self.assertRaises(ParamInvalid):
            criteria.add(params)

    def test_update(self):
        params = {
            "name": "mock_name",
            "description": "mock_description",
        }
        criteria = self.__criteria
        criteria.update(params)
        result = criteria.get()
        self.assertIsNotNone(result)
        self.assertEqual(result.get("name"), params.get("name"))
        self.assertEqual(result.get("description"), params.get("description"))
        self.assertIn("criteria_id", result)

    def test_update_criteria_name_null(self):
        params = {
            "name": None,
            "description": "mock_description",
        }
        criteria = self.__criteria
        with self.assertRaises(ParamInvalid):
            criteria.update(params)

    def test_update_criteria_name_invalid(self):
        params = {
            "name": 1111,
            "description": "mock_description",
        }
        criteria = self.__criteria
        with self.assertRaises(ParamInvalid):
            criteria.update(params)