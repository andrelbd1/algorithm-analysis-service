import mock
from src.common import Singleton
from src.controllers.execution import ControllerExecution
from src.exceptions import ParamInvalid, ObjectNotFound
from src.models.tb_criteria import Criteria
from src.models.tb_execution import Execution, STATUS_DONE, STATUS_ERROR, STATUS_PROCESSING, STATUS_WARNING
from tests import BaseTestClass


class TestControllerExecution(BaseTestClass):
    
    def setUp(self):
        Singleton.drop()

    @property
    def __controller_execution(self):
        return ControllerExecution()
    
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