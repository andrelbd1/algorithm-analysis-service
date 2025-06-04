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
