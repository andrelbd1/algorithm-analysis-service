from src.common.functions import validate_object
from src.config import ApplicationConfig
from src.models.tb_result import Result

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerResult(ControllerDefault):

    def __get_instance(self, p_id: str) -> Result:
        """
        Retrieve an instance of the Result model based on the given result ID.

        Args:
            p_id (str): The ID of the result to retrieve.

        Returns:
            Result: The instance of the Result model if found and enabled, otherwise None.
        """
        query = self._orm.session.query(Result).filter_by(result_id=p_id,
                                                          enabled=True)
        result = None
        for item in query:
            result = item
        return result

    def add(self, params: dict) -> str:
        result = Result()
        result.add(params)
        result_id = str(result.result_id)
        self._orm.object_commit(result)
        return result_id

    def set_done_result(self, params: dict):
        result_id = params.get("result_id")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.update(params)
        result.set_status_to_done()
        self._orm.object_commit(result)

    def set_progress_result(self, params: dict):
        result_id = params.get("result_id")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_progressing()
        self._orm.object_commit(result)

    def set_warning_result(self, params: dict):
        result_id = params.get("result_id")
        warning = params.get("warning")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_warning(warning)
        self._orm.object_commit(result)

    def set_error_result(self, params: dict):
        result_id = params.get("result_id")
        error = params.get("error")
        result = self.__get_instance(result_id)
        validate_object(result_id, result)
        result.set_status_to_error(error)
        self._orm.object_commit(result)
