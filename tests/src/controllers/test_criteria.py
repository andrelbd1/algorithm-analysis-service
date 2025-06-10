import mock
from src.common import Singleton
from src.controllers.criteria import ControllerCriteria
from src.models.tb_criteria import Criteria
from tests import BaseTestClass

class TestControllerCriteria(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_criteria(self):
        return ControllerCriteria()
    
    @mock.patch("src.controllers.OrmConnect")
    def test_get_criteria_by_algorithm_id(self, mock_orm):
        mock_query_result = ("mock_algorithm_name", "mock_criteria_id", "mock_criteria_name")                       
        mock_orm().orm.session.query().join().join().filter.return_value = [mock_query_result]
        p_id = "4a00110b-8fbd-4e1d-81da-169e259f92d4"
        result = self.__controller_criteria.get_criteria_by_algorithm_id(p_id)
        self.assertTrue(mock_orm().orm.session.query().join().join().filter.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        print(result)
        result = result[0]
        self.assertIn('algorithm_name', result.keys())
        self.assertIn('criteria_id', result.keys())
        self.assertIn('criteria_name', result.keys())
        
    @mock.patch("src.controllers.OrmConnect")
    def test_get_instance(self, mock_orm):
        mock_query_result = Criteria()
        mock_orm().orm.session.query().filter_by.return_value = [mock_query_result]
        p_id = "4a00110b-8fbd-4e1d-81da-169e259f92d4"
        result = self.__controller_criteria.get_instance(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsInstance(result, Criteria)