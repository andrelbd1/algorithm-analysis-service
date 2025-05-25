import mock

from src.tasks.execution import process_algorithm, queue_execution
from tests import BaseTestClass


class TestTaskProcessCreateIndex(BaseTestClass):

    @mock.patch("src.tasks.execution.ControllerExecution")
    def test_process_algorithm(self, mock_controller):
        params = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41"
        }
        process_algorithm(**params)
        self.assertTrue(mock_controller().run.called)
        self.assertTrue(mock_controller().db_disconnect.called)

    @mock.patch("src.tasks.execution.ControllerExecution")
    def test_exception_process_report(self, mock_controller):
        params = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41"
        }
        mock_controller().run.side_effect = Exception("mock")
        with self.assertRaises(Exception):
            process_algorithm(**params)
        self.assertTrue(mock_controller().set_error_execution.called)
        self.assertTrue(mock_controller().db_disconnect.called)

    @mock.patch("src.tasks.execution.process_algorithm")
    def test_queue_create_report(self, mock_process):
        params = {
            "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
            "input": [
                {
                "id": "0192919b-2501-585f-1492-4f5d22c98267",
                "value": "20"
                }
            ],
            "alias": "Execution_2025_01_01_16_06_41"
        }
        queue_execution(params)
        self.assertTrue(mock_process.delay.called)
