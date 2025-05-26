from src.exceptions import ParamInvalid
from src.models.tb_algorithm_criteria import AlgorithmCriteria
from src.models.tb_algorithm import Algorithm
from src.models.tb_criteria import Criteria
from tests import BaseTestClass

class TestAlgorithmCriteria(BaseTestClass):

    @property
    def __algorithm_criteria(self):
        return AlgorithmCriteria()
    
    def test_add_get(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": Criteria(),
        }
        algorithm_criteria = self.__algorithm_criteria
        algorithm_criteria.add(params)
        result = algorithm_criteria.get()
        self.assertIsNotNone(result)
        self.assertIn("algorithm_criteria_id", result)
    
    def test_add_algorithm_null(self):
        params = {
            "algorithm": None,
            "criteria": Criteria(),
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.add(params)

    def test_add_algorithm_invalid(self):
        params = {
            "algorithm": Criteria(),
            "criteria": Criteria(),
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.add(params)

    def test_add_criteria_null(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": None,
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.add(params)

    def test_add_criteria_invalid(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": Algorithm(),
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.add(params)

    def test_update(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": Criteria(),
        }
        algorithm_criteria = self.__algorithm_criteria
        algorithm_criteria.update(params)
        result = algorithm_criteria.get()
        self.assertIsNotNone(result)
        self.assertIn("algorithm_criteria_id", result)

    def test_update_criteria_null(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": None,
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.update(params)

    def test_update_criteria_invalid(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": Algorithm(),
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.update(params)

    def test_update_criteria_null(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": None,
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.update(params)

    def test_update_criteria_invalid(self):
        params = {
            "algorithm": Algorithm(),
            "criteria": Algorithm(),
        }
        algorithm_criteria = self.__algorithm_criteria
        with self.assertRaises(ParamInvalid):
            algorithm_criteria.update(params)
