from sqlalchemy import and_
from src.config import ApplicationConfig
from src.models.tb_algorithm import Algorithm
from src.models.tb_algorithm_criteria import AlgorithmCriteria
from src.models.tb_criteria import Criteria

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerCriteria(ControllerDefault):

    def __query_criteria_by_algorithm_id(self, algorithm_id: str):
        return self._orm.session.query(Algorithm.name,
                                       Criteria.criteria_id,
                                       Criteria.name) \
            .join(AlgorithmCriteria, AlgorithmCriteria.algorithm_id == Algorithm.algorithm_id) \
            .join(Criteria, AlgorithmCriteria.criteria_id == Criteria.criteria_id) \
            .filter(Algorithm.algorithm_id == algorithm_id,
                    Algorithm.enabled.is_(True),
                    AlgorithmCriteria.enabled.is_(True),
                    Criteria.enabled.is_(True))

    def get_criteria_by_algorithm_id(self, algorithm_id: str) -> list[dict]:
        query = self.__query_criteria_by_algorithm_id(algorithm_id)
        criteria = []
        for i in query:
            criteria.append({"algorithm_name": i[0],
                             "criteria_id": str(i[1]),
                             "criteria_name": i[2],
                             })
        self._orm.remove_session()
        return criteria
