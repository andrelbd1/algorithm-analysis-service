import mock

from src.evaluation import Evaluation
from src.codes.base import BaseCode
from src.evaluation.base import BaseEvaluation

from tests import BaseTestClass

class TestEvaluation(BaseTestClass):

    @property
    def __evaluation(self):
        return Evaluation()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_get_evaluation_null(self, mock_cont_default, mock_cont_result, mock_base_code):
        with self.assertRaises(NotImplementedError):
            evaluation = self.__evaluation.get_instance(None)

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_get_evaluation_not_exist(self, mock_cont_default, mock_cont_result, mock_base_code):
        with self.assertRaises(NotImplementedError):
            evaluation = self.__evaluation.get_instance("not_exist")

    def test_get_base_evaluation_process_not_implemented(self):
        with self.assertRaises(Exception):
            BaseEvaluation().process(None, [], "")

    def test_get_base_evaluation_run_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseEvaluation().run(BaseCode(), {})

    def test_get_count_edges(self):
        evaluation = self.__evaluation.get_instance("Count Edges")
        self.assertIsInstance(evaluation, BaseEvaluation)
    
    def test_get_count_nodes(self):
        evaluation = self.__evaluation.get_instance("Count Nodes")
        self.assertIsInstance(evaluation, BaseEvaluation)
    
    def test_get_detect_cycle(self):
        evaluation = self.__evaluation.get_instance("Detect Cycle")
        self.assertIsInstance(evaluation, BaseEvaluation)

    def test_get_memory_consume(self):
        evaluation = self.__evaluation.get_instance("Memory Consume")
        self.assertIsInstance(evaluation, BaseEvaluation)

    def test_get_running_time(self):
        evaluation = self.__evaluation.get_instance("Running Time")
        self.assertIsInstance(evaluation, BaseEvaluation)

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_count_nodes(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Count Nodes")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [4, 0, 8, 0, 0, 0, 0, 11, 0],
                                    [0, 8, 0, 7, 0, 4, 0, 0, 2],
                                    [0, 0, 7, 0, 9, 14, 0, 0, 0],
                                    [0, 0, 0, 9, 0, 10, 0, 0, 0],
                                    [0, 0, 4, 14, 10, 0, 2, 0, 0],
                                    [0, 0, 0, 0, 0, 2, 0, 1, 6],
                                    [8, 11, 0, 0, 0, 0, 1, 0, 7],
                                    [0, 0, 2, 0, 0, 0, 6, 7, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_count_edges(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Count Edges")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [4, 0, 8, 0, 0, 0, 0, 11, 0],
                                    [0, 8, 0, 7, 0, 4, 0, 0, 2],
                                    [0, 0, 7, 0, 9, 14, 0, 0, 0],
                                    [0, 0, 0, 9, 0, 10, 0, 0, 0],
                                    [0, 0, 4, 14, 10, 0, 2, 0, 0],
                                    [0, 0, 0, 0, 0, 2, 0, 1, 6],
                                    [8, 11, 0, 0, 0, 0, 1, 0, 7],
                                    [0, 0, 2, 0, 0, 0, 6, 7, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_detect_cycle_true(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Detect Cycle")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [4, 0, 8, 0, 0, 0, 0, 11, 0],
                                    [0, 8, 0, 7, 0, 4, 0, 0, 2],
                                    [0, 0, 7, 0, 9, 14, 0, 0, 0],
                                    [0, 0, 0, 9, 0, 10, 0, 0, 0],
                                    [0, 0, 4, 14, 10, 0, 2, 0, 0],
                                    [0, 0, 0, 0, 0, 2, 0, 1, 6],
                                    [8, 11, 0, 0, 0, 0, 1, 0, 7],
                                    [0, 0, 2, 0, 0, 0, 6, 7, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_detect_cycle_false(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Detect Cycle")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 2],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [8, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_running_time(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Running Time")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 2],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [8, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()

    @mock.patch('src.evaluation.base.BaseCode')
    @mock.patch('src.evaluation.base.ControllerResult')
    @mock.patch('src.evaluation.base.ControllerDefault')
    def test_process_memory_consume(self, mock_cont_default, mock_cont_result, mock_base_code):
        mock_instance_code = mock.Mock(spec=BaseCode)
        evaluation = self.__evaluation.get_instance("Memory Consume")
        payload = [{'payload_id': '0195e2e4-5079-c5f4-1b8a-c33287607035',
                    'input': {
                         'input_id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                         'name': 'number of nodes',
                         'description': 'number of nodes to build a random graph',
                         'input_type': 'integer',
                         },
                    'input_value': '9',
                    'enabled': True
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'source',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 0
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'target',
                         'description': None,
                         'input_type': 'integer',
                         },
                    'input_value': 4
                   },
                   {'payload_id': None,
                    'input': {
                         'input_id': None,
                         'name': 'graph',
                         'description': None,
                         'input_type': 'list',
                         },
                    'input_value': [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 2],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [8, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                   }]
        result_id = "019747a2-eece-ca62-b2d5-88e95cc3fee0"
        evaluation.process(mock_instance_code, payload, result_id)
        mock_cont_result().set_progress_result.assert_called_once()
        mock_cont_result().set_done_result.assert_called_once()