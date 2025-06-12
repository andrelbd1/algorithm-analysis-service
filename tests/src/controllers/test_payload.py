import mock
from src.common import Singleton
from src.controllers.payload import ControllerPayload
from src.models.tb_algorithm import Algorithm
from src.models.tb_execution import Execution
from src.models.tb_input import Input
from src.models.tb_payload import Payload
from tests import BaseTestClass

class TestControllerPayload(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_payload(self):
        return ControllerPayload()
    
    @mock.patch("src.controllers.OrmConnect")
    def test_get_payload_by_execution_id(self, mock_orm):
        mock_query_result = ("mock_type", "mock_name", "mock_value")
        mock_orm().orm.session.query().join().filter.return_value = [mock_query_result]
        p_id = "4a00110b-8fbd-4e1d-81da-169e259f92d4"
        result = self.__controller_payload.get_payload_by_execution_id(p_id)
        self.assertTrue(mock_orm().orm.session.query().join().filter.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        result = result[0]
        self.assertIn('type', result.keys())
        self.assertIn('name', result.keys())
        self.assertIn('value', result.keys())

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_input_None(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': None, 'value': 'true'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'bool',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(result)
    
    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_input_not_found(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': 'true'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'not_exist',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_input_not_required(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-2fea-1492-5d5541c4002b', 'value': 'true'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'bool',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_true(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': 'true'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'bool',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_false(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': 'FALSE'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'bool',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_bool_invalid(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': 'invalid'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'bool',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()        
        result = self.__controller_payload.add(params, mock_execution)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_integer(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': '20'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'integer',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_int(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': '20'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'int',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(result)

    @mock.patch("src.controllers.payload.ControllerInput")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_input_int(self, mock_orm, mock_cont_input):        
        mock_execution = Execution()
        params = {'algorithm_id': '0192919b-2501-2fea-a93d-5d5541c4002b',
                  'input': [{'id': '0192919b-2501-585f-1492-4f5d22c98267', 'value': '25.55'}],
                  'alias': 'Execution_2025_06_10_20_40_35',
                  'algorithm': Algorithm()}
        mock_input = [{'input_id': '0192919b-2501-585f-1492-4f5d22c98267',
                       'input_type': 'float',
                       'name': 'factorial number',
                       'description': 'number to calculate factorial'}]                
        mock_cont_input().get_input_by_algorithm_id.return_value = mock_input
        mock_cont_input().get_instance.return_value = Input()
        result = self.__controller_payload.add(params, mock_execution)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(result)

    @mock.patch("src.controllers.OrmConnect")
    def test_add_payload_empty(self, mock_orm):
        mock_execution = mock.Mock(spec=Execution)
        params = {}
        result = self.__controller_payload.add(params, mock_execution)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(result)