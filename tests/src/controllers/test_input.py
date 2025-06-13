import mock
from src.common import Singleton
from src.controllers.input import ControllerInput
from src.models.tb_input import Input
from tests import BaseTestClass

class TestControllerInput(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_input(self):
        return ControllerInput()
    
    @mock.patch("src.controllers.OrmConnect")
    def test_get_instance(self, mock_orm):
        mock_query_result = Input()
        mock_orm().orm.session.query().filter_by.return_value = [mock_query_result]
        p_id = "4a00110b-8fbd-4e1d-81da-169e259f92d4"
        result = self.__controller_input.get_instance(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsInstance(result, Input)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_get_input_by_algorithm_id(self, mock_orm):
        mock_query_result = ("mock_input_id", "mock_input_type", "mock_name", "mock_description")
        mock_orm().orm.session.query().filter.return_value = [mock_query_result]
        p_id = "4a00110b-8fbd-4e1d-81da-169e259f92d4"
        result = self.__controller_input.get_input_by_algorithm_id(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        result = result[0]
        self.assertIn('input_id', result.keys())
        self.assertIn('input_type', result.keys())
        self.assertIn('name', result.keys())
        self.assertIn('description', result.keys())
