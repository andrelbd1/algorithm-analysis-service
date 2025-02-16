from src.config import ApplicationConfig
from src.models.tb_input import Input

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerInput(ControllerDefault):

    def get_instance(self, p_id):
        query = self._orm.session.query(Input).filter_by(input_id=p_id,
                                                         enabled=True)
        result = None
        for item in query:
            result = item
        return result

    def query_input_by_algorithm_id(self, algorithm_id):
        return self._orm.session.query(Input).filter_by(algorithm_id=algorithm_id,
                                                        enabled=True)
