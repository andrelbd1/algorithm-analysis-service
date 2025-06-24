import json
import mock
from datetime import datetime
from src.common import Singleton
from src.controllers.algorithm import ControllerAlgorithm
from src.exceptions import ObjectNotFound, ParamInvalid
from src.models.tb_algorithm import Algorithm
from tests import BaseTestClass

class TestControllerAlgorithm(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_algorithm(self):
        return ControllerAlgorithm()

    @mock.patch("src.controllers.OrmConnect")
    def test_delete(self, mock_orm):
        mock_algorithm = Algorithm()
        mock_orm().orm.session.query().filter_by.return_value = [mock_algorithm]
        p_id = "1e5eeaa7-099b-5844-882e-310eccedbe89"
        self.__controller_algorithm.delete(p_id)
        algorithm = mock_algorithm.get()
        self.assertFalse(algorithm['enabled'])
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_delete_invalid(self, mock_orm):
        mock_schedule = None
        mock_orm().orm.session.query().filter_by.return_value = [mock_schedule]
        p_id = "1e5eeaa7-099b-5844-882e-310eccedbe89"
        with self.assertRaises(ObjectNotFound):
            self.__controller_algorithm.delete(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects(self, mock_orm):
        mock_execution = (1, "mock_algorithm_id", "mock_algorithm_name", "mock_algorithm_description",
                           "mock_algorithm_source", datetime.now(), None, None, None, None, None, None, None)
        mock_input = (1, 'mock_algorithm_id', None, None, None, None, "mock_input_id", "mock_input_name", "mock_input_type", "mock_input_description", None, None, None)
        mock_criteria = (1, 'mock_algorithm_id', None, None, None, None, None, None, None, None, "mock_criteria_id", "mock_criteria_name", "mock_input_description")
        mock_count = (1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        mock_orm().orm.execute_query.return_value= [mock_execution, mock_input, mock_criteria, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "value": "4a00110b-8fbd-4e1d-81da-169e259f92d4",
                  "search_by": "algorithm_id"}
        result = json.loads(self.__controller_algorithm.list_objects(params))
        print(result)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("total_items", result.keys())
        self.assertIn("algorithms", result.keys())
        self.assertEqual(result['total_items'], 1)
        self.assertEqual(len(result['algorithms']), 1)
        result = result['algorithms'][0]        
        self.assertIn("algorithm_id", result.keys())
        self.assertIn("name", result.keys())
        self.assertIn("description", result.keys())
        self.assertIn("source", result.keys())
        self.assertIn("input", result.keys())
        self.assertIsInstance(result['input'], list)
        self.assertEqual(len(result['input']), 1)
        result_input = result['input'][0]
        self.assertIn("input_id", result_input.keys())
        self.assertIn("name", result_input.keys())
        self.assertIn("input_type", result_input.keys())
        self.assertIn("description", result_input.keys())
        result_criteria = result['criteria'][0]
        self.assertIn("criteria_id", result_criteria.keys())
        self.assertIn("name", result_criteria.keys())
        self.assertIn("description", result_criteria.keys())

    @mock.patch("src.controllers.OrmConnect")
    def test_param_invalid_to_list_objects(self, mock_orm):
        params = {"amount": 100,
                  "page": 0,
                  "value": "value",
                  "search_by": "cdb"}
        with self.assertRaises(ParamInvalid):
            self.__controller_algorithm.list_objects(params)
        self.assertFalse(mock_orm().orm.remove_session.called)