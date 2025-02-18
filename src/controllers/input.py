from src.config import ApplicationConfig
from src.models.tb_input import Input

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerInput(ControllerDefault):

    def __query_input_by_algorithm_id(self, algorithm_id):
        return self._orm.session.query(Input.input_id,
                                       Input.input_type,
                                       Input.name,
                                       Input.description,
                                       ).filter(Input.algorithm_id == algorithm_id,
                                                Input.enabled.is_(True))

    def get_instance(self, p_id):
        query = self._orm.session.query(Input).filter_by(input_id=p_id,
                                                         enabled=True)
        result = None
        for item in query:
            result = item
        return result

    def get_input_by_algorithm_id(self, algorithm_id):
        query = self.__query_input_by_algorithm_id(algorithm_id)
        items = []
        for i in query:
            items.append({"input_id": str(i[0]),
                          "input_type": i[1],
                          "name": i[2],
                          "description": i[3],
                          })
        self._orm.remove_session()
        return items
