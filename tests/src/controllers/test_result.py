import json
import mock
from datetime import datetime
from src.common import Singleton
from src.controllers.result import ControllerResult
from src.exceptions import ObjectNotFound
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution
from src.models.tb_result import Result, STATUS_DONE, STATUS_ERROR, STATUS_PROCESSING, STATUS_WARNING
from tests import BaseTestClass


class TestControllerResult(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_result(self):
        return ControllerResult()
    
    @mock.patch("src.controllers.OrmConnect")
    def test_report(self, mock_orm):
        mock_executions = (0, "5", "0.000002165000000000000000", "secs")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "algorithm_id": "00195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                  "criteria_id": 'f6465865-d1a3-496c-82b7-5d7d67adf927',
                  "input_id": "0195316d-80fc-40c2-b3ca-44a90d8c6851"}
        result = json.loads(self.__controller_result.report(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("report", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['report'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_report_request_date(self, mock_orm):
        mock_executions = (1, "5", "0.000002165000000000000000", "secs")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "algorithm_id": "00195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                  "criteria_id": 'f6465865-d1a3-496c-82b7-5d7d67adf927',
                  "input_id": "0195316d-80fc-40c2-b3ca-44a90d8c6851",
                  "request_date": datetime.strftime(datetime.now(), "%Y-%m-%d")}
        result = json.loads(self.__controller_result.report(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("report", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['report'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_report_created_at(self, mock_orm):
        mock_executions = (1, "5", "0.000002165000000000000000", "secs")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "algorithm_id": "00195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                  "criteria_id": 'f6465865-d1a3-496c-82b7-5d7d67adf927',
                  "input_id": "0195316d-80fc-40c2-b3ca-44a90d8c6851",
                  "created_at": datetime.strftime(datetime.now(), "%Y-%m-%d")}
        result = json.loads(self.__controller_result.report(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("report", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['report'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_report_alias(self, mock_orm):
        mock_executions = (1, "5", "0.000002165000000000000000", "secs")
        mock_count = tuple([1]+[None]*(len(mock_executions)-1))
        mock_orm().orm.execute_query.return_value= [mock_executions, mock_count]
        params = {"amount": 100,
                  "page": 0,
                  "algorithm_id": "00195316b-d5ca-431a-8d95-f3f65e3ec1dd",
                  "criteria_id": 'f6465865-d1a3-496c-82b7-5d7d67adf927',
                  "input_id": "0195316d-80fc-40c2-b3ca-44a90d8c6851",
                  "alias": datetime.strftime(datetime.now(), "%Y-%m-%d")}
        result = json.loads(self.__controller_result.report(params))
        self.assertTrue(mock_orm().orm.remove_session.called)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("report", result.keys())
        self.assertIn("total_items", result.keys())
        self.assertIsInstance(result['report'], list)

    @mock.patch("src.controllers.OrmConnect")
    def test_add(self, mock_orm):
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria": Criteria(),
        }
        result = self.__controller_result.add(params)
        self.assertIsNotNone(result)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_done_result(self, mock_orm):
        mock_criteria = mock.MagicMock()
        mock_criteria.get.return_value = {"name": "mock_criteria", "criteria_id": "mock_id"}
        mock_result = Result()
        mock_result.criteria = mock_criteria
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_done_result(params)
        result = mock_result.get()
        self.assertEqual(result['status'], STATUS_DONE)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_done_result_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_result.set_done_result(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_progress_result(self, mock_orm):
        mock_criteria = mock.MagicMock()
        mock_criteria.get.return_value = {"name": "mock_criteria", "criteria_id": "mock_id"}
        mock_result = Result()
        mock_result.criteria = mock_criteria
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_progress_result(params)
        result = mock_result.get()
        self.assertEqual(result['status'], STATUS_PROCESSING)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_progress_result_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_result.set_progress_result(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_warning_result(self, mock_orm):
        mock_criteria = mock.MagicMock()
        mock_criteria.get.return_value = {"name": "mock_criteria", "criteria_id": "mock_id"}
        mock_result = Result()
        mock_result.criteria = mock_criteria
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_warning_result(params)
        result = mock_result.get()
        self.assertEqual(result['status'], STATUS_WARNING)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_warning_result_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_result.set_warning_result(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)
    
    @mock.patch("src.controllers.OrmConnect")
    def test_set_error_result(self, mock_orm):
        mock_criteria = mock.MagicMock()
        mock_criteria.get.return_value = {"name": "mock_criteria", "criteria_id": "mock_id"}
        mock_result = Result()
        mock_result.criteria = mock_criteria
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_error_result(params)
        result = mock_result.get()
        self.assertEqual(result['status'], STATUS_ERROR)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_error_result_invalid_execution_object(self, mock_orm):
        mock_orm().orm.session.query().filter_by.return_value = [None]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        with self.assertRaises(ObjectNotFound):
            self.__controller_result.set_error_result(params)
        self.assertTrue(mock_orm().orm.session.query().filter_by.called)
        self.assertFalse(mock_orm().orm.object_commit.called)
        self.assertFalse(mock_orm().orm.remove_session.called)
