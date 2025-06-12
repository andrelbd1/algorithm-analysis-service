import mock
from src.common import Singleton
from src.controllers.result import ControllerResult
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution
from src.models.tb_result import Result, STATUS_DONE, STATUS_ERROR, STATUS_PROCESSING, STATUS_QUEUE, STATUS_WARNING
from tests import BaseTestClass


class TestControllerResult(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_result(self):
        return ControllerResult()
    
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
        mock_result = Result()
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_done_result(params)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_progress_result(self, mock_orm):
        mock_result = Result()
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_progress_result(params)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_warning_result(self, mock_orm):
        mock_result = Result()
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_warning_result(params)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)

    @mock.patch("src.controllers.OrmConnect")
    def test_set_error_result(self, mock_orm):
        mock_result = Result()
        mock_orm().orm.session.query().filter_by.return_value = [mock_result]
        params = {
            "value": "mock_value",
            "unit": "mock_unit",
            "message": "mock_message",
            "execution": Execution(),
            "criteria":  Criteria(),
        }
        self.__controller_result.set_error_result(params)
        self.assertTrue(mock_orm().orm.object_commit.called)
        self.assertTrue(mock_orm().orm.remove_session.called)