from src.config import ApplicationConfig
from src.models.tb_input import Input

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerInput(ControllerDefault):

    def __query_input_by_algorithm_id(self, algorithm_id: str):
        """
        Query inputs by algorithm ID.

        This method queries the database for inputs associated with a given algorithm ID
        that are enabled. It returns the input ID, input type, name, and description.

        Args:
            algorithm_id (str): The ID of the algorithm to query inputs for.

        Returns:
            sqlalchemy.orm.query.Query: A query object containing the input details.
        """
        return self._orm.session.query(Input.input_id,
                                       Input.input_type,
                                       Input.name,
                                       Input.description,
                                       ).filter(Input.algorithm_id == algorithm_id,
                                                Input.enabled.is_(True))

    def get_instance(self, p_id: str) -> Input:
        """
        Retrieve an instance of Input from the database based on the provided input ID.

        Args:
            p_id (str): The ID of the input to retrieve.

        Returns:
            Input: The instance of Input with the specified ID if found and enabled, otherwise None.
        """
        query = self._orm.session.query(Input).filter_by(input_id=p_id,
                                                         enabled=True)
        result = None
        for item in query:
            result = item
        self._orm_disconnect()
        return result

    def get_input_by_algorithm_id(self, algorithm_id: str) -> list[str]:
        """
        Retrieve input details associated with a specific algorithm ID.

        Args:
            algorithm_id (str): The ID of the algorithm for which to retrieve input details.

        Returns:
            list: A list of dictionaries, each containing the following keys:
            - input_id (str): The ID of the input.
            - input_type (str): The type of the input.
            - name (str): The name of the input.
            - description (str): The description of the input.
        """
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
