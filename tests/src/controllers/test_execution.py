import json
import mock
from datetime import datetime
from src.common import Singleton
from src.controllers.execution import ControllerExecution
from src.exceptions import ObjectNotFound
from src.models.tb_algorithm import Algorithm
from src.models.tb_execution import Execution, STATUS_DONE, STATUS_ERROR, STATUS_PROCESSING, STATUS_WARNING
from tests import BaseTestClass


class TestControllerExecution(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_execution(self):
        return ControllerExecution()
    
    @mock.patch("src.controllers.execution.ControllerPayload")
    @mock.patch("src.controllers.execution.ControllerAlgorithm")
    @mock.patch("src.controllers.OrmConnect")
    def test_add(self, mock_orm, mock_algorithm, mock_payload):
        mock_algorithm().get_instance.return_value = Algorithm()
        mock_payload().add.return_value = True
        params = {
            "algorithm_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
        }
        result = self.__controller_execution.add(params)        
        self.assertIsNotNone(result)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.execution.ControllerPayload")
    @mock.patch("src.controllers.execution.ControllerAlgorithm")
    @mock.patch("src.controllers.OrmConnect")
    def test_add_algorithm_invalid(self, mock_orm, mock_algorithm, mock_payload):
        mock_algorithm().get_instance.return_value = Algorithm()
        mock_payload().add.return_value = False
        params = {
            "algorithm_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
        }
        result = self.__controller_execution.add(params)        
        self.assertIsNotNone(result)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_get(self, mock_orm):
        result_get = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
            "status": "mock_status",
            "message": "mock_message",
            "created_at": datetime.now(),
            "payload": [
                {
                    "input": {
                        "input_id": "mock_input_id",
                        "name": "mock_name",
                    },
                    "input_value": "mock_input_value",
                }
            ],
            "alias": "mock_alias",
            "execution": {
                'criteria': "mock_criteria",
                'value': "mock_value",
                'unit': "mock_unit",
                'message': "mock_message",
            }
        }
        mock_report = mock.MagicMock()
        mock_report.get.return_value = result_get
        mock_orm().orm.session.query().filter_by.return_value = mock_report
        p_id = '21d88834-5021-5fff-a66f-0069f40ec3e7'
        result = self.__controller_execution.get(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_execution_id(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "execution_id": "019774be-31d2-4ea9-1493-f0cd729e0406"}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_algorithm_id(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "algorithm_id": "0195316b-d5ca-431a-8d95-f3f65e3ec1dd"}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_execution_status(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "execution_status": "DONE"}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_request_date(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "request_date": datetime.strftime(datetime.now(), "%Y-%m-%d")}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_created_at(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "created_at": datetime.strftime(datetime.now(), "%Y-%m-%d")}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_alias(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "alias": "VALUE_100"}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_list_objects_not_exist_param(self, mock_orm):
        mock_executions = (1, "019774be-31d2-4ea9-1493-f0cd729e0406", "0195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                           "Fibonacci sequence", "0195316d-80fc-40c2-b3ca-44a90d8c6851", "fibonacci number",
                           "100", "VALUE_100", "DONE", None, datetime.now(), "Running Time",
                           "664.9029433", "secs", None, "DONE")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "not_exist_param": ""}
        result = json.loads(self.__controller_execution.list_objects(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("executions", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['executions'][0]['result'], list)

    @mock.patch("src.controllers.execution.Evaluation")
    @mock.patch("src.controllers.execution.ControllerResult")
    @mock.patch("src.controllers.execution.ControllerCriteria")
    @mock.patch("src.controllers.execution.Codes")
    @mock.patch("src.controllers.OrmConnect")
    def test_run(self, mock_orm, mock_code, mock_control_criteria, mock_control_result, mock_evaluation):
        mock_algorithm = mock.MagicMock()
        mock_algorithm.get.return_value = {"algorithm_id": "mock_id", "name": "mock_algorithm"}
        mock_input = mock.MagicMock()
        mock_input.get.return_value = {"input_id": "mock_input_id", "name": "mock_input"}
        mock_payload = mock.MagicMock()
        mock_payload.get.return_value = {"payload_id": "mock_payload_id", "input": mock_input, "input_value": "mock_input_value", "enabled": True}
        mock_base_code = mock.MagicMock()
        mock_code = mock.MagicMock()
        mock_code.get_instance.return_value = mock_base_code
        mock_criteria = mock.MagicMock()
        mock_execution = Execution()
        mock_execution.algorithm = mock_algorithm
        mock_execution.payload = mock_payload
        mock_orm().orm.session.query().filter_by.return_value = [mock_execution]
        mock_control_criteria().get_criteria_by_algorithm_id.return_value = [{"algorithm_name": "mock_algorithm", "criteria_id": "mock_criteria_id", "criteria_name": "mock_criteria_name"}]
        mock_control_criteria().get_instance.return_value = mock_criteria
        mock_control_result().add.return_value = "mock_result_id"
        mock_base_evaluation = mock.MagicMock()
        mock_evaluation().get_instance.return_value = mock_base_evaluation
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
        }
        self.__controller_execution.run(params)
        result = mock_execution.get()
        self.assertEqual(result['status'], STATUS_DONE)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_run_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_execution.set_warning_execution(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_set_warning_execution(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [Execution()]
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
            "warning": "Warning xpto"
        }
        mock_algorithm = mock.MagicMock()
        mock_algorithm.get.return_value = {"name": "mock_algorithm", "algorithm_id": "mock_id"}
        mock_execution = Execution()
        mock_execution.algorithm = mock_algorithm
        mock_orm().orm.session.query().filter_by.return_value = [mock_execution]
        self.__controller_execution.set_warning_execution(params)
        result = mock_execution.get()
        self.assertEqual(result['status'], STATUS_WARNING)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_warning_execution_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
            "warning": "Warning xpto"
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_execution.set_warning_execution(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_set_enabled_to_false(self, mock_orm):
        mock_algorithm = mock.MagicMock()
        mock_algorithm.get.return_value = {"name": "mock_algorithm", "algorithm_id": "mock_id"}
        mock_execution = Execution()
        mock_execution.algorithm = mock_algorithm
        mock_orm().orm.session.query().filter_by.return_value = [mock_execution]
        p_id = "21d88834-5021-5fff-a66f-0069f40ec3e7"        
        self.__controller_execution.set_enabled_to_false(p_id)
        result = mock_execution.get()
        self.assertFalse(result['enabled'])
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_enabled_to_false_invalid_execution_object(self, mock_orm):
        mock_execution = None
        mock_orm().orm.session.query().filter_by.return_value = [mock_execution]
        p_id = "21d88834-5021-5fff-a66f-0069f40ec3e7"
        with self.assertRaises(ObjectNotFound):
            self.__controller_execution.set_enabled_to_false(p_id)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_error_execution(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [Execution()]
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
            "error": "Error xpto"
        }
        mock_algorithm = mock.MagicMock()
        mock_algorithm.get.return_value = {"name": "mock_algorithm", "algorithm_id": "mock_id"}
        mock_execution = Execution()
        mock_execution.algorithm = mock_algorithm
        mock_orm().orm.session.query().filter_by.return_value = [mock_execution]
        self.__controller_execution.set_error_execution(params)
        result = mock_execution.get()
        self.assertEqual(result['status'], STATUS_ERROR)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_error_report_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "execution_id": "21d88834-5021-5fff-a66f-0069f40ec3e7",
            "warning": "Warning xpto"
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_execution.set_error_execution(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_db_disconnect(self, mock_orm,):
        self.__controller_execution.db_disconnect()
        self.assertTrue(mock_orm().orm.remove_session.called)
