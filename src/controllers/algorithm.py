import json
from sqlalchemy import Date, String, and_, func, null, select
from sqlalchemy.dialects.postgresql import UUID

from src.common.functions import result_json, validate_item_dict, validate_object, validate_uuid
from src.config import ApplicationConfig
from src.models.tb_algorithm import Algorithm
from src.models.tb_algorithm_criteria import AlgorithmCriteria
from src.models.tb_criteria import Criteria
from src.models.tb_input import Input

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerAlgorithm(ControllerDefault):

    def __get_options_search(self, search_by: str, value: str, page: int, amount: int):
        """
        Generates a query to search for algorithms and their inputs based on the provided search criteria.

        Args:
            search_by (str): The field to search by (e.g., "algorithm_id", "name").
            value (str): The value to search for.
            page (int): The page number for pagination.
            amount (int): The number of results per page.

        Returns:
            ResultProxy: The result of the executed query.
        """
        count = select(func.count(func.distinct(Algorithm.algorithm_id)).label("id"),
                       null().cast(UUID).label("algorithm_id"), null().cast(String).label("name"),
                       null().cast(String).label("description"), null().cast(String).label("source"),
                       null().cast(Date).label("created_at"),
                       null().cast(UUID).label("input_id"), null().cast(String).label("input_name"),
                       null().cast(String).label("input_type"), null().cast(String).label("input_description"),
                       null().cast(UUID).label("criteria_id"), null().cast(String).label("criteria_name"),
                       null().cast(String).label("criteria_description")
                       ).filter(Algorithm.enabled.is_(True))
        data_query = select(func.row_number().over(order_by=Algorithm.algorithm_id).label('id'),
                            Algorithm.algorithm_id, Algorithm.name, Algorithm.description,
                            Algorithm.source, Algorithm.created_at,
                            null().cast(UUID).label("input_id"), null().cast(String).label("input_name"),
                            null().cast(String).label("input_type"), null().cast(String).label("input_description"),
                            null().cast(UUID).label("criteria_id"), null().cast(String).label("criteria_name"),
                            null().cast(String).label("criteria_description")). \
            filter(Algorithm.enabled.is_(True)). \
            order_by(Algorithm.name.asc(), Algorithm.created_at.desc())
        if search_by and value:
            filters = {
                "algorithm_id": (
                    Algorithm.algorithm_id == value
                    if search_by == "algorithm_id" and (validate_uuid(value) or True)
                    else True
                ),
                "name": func.lower(Algorithm.name).like(f"%{value.strip().lower()}%"),
                "": True  # No filter
            }
            validate_item_dict(search_by, filters)
            data_query = data_query.filter(filters[search_by])
            count = count.filter(filters[search_by])
        count = count.cte("count")
        data_query = data_query.limit(amount).offset(page * amount).cte("data_query")
        input_query = select(func.row_number().over(order_by=Input.algorithm_id).label('id'),
                             Input.algorithm_id, null().cast(String).label("name"),
                             null().cast(String).label("description"), null().cast(String).label("source"),
                             null().cast(Date).label("created_at"),
                             Input.input_id, Input.name.label("input_name"),
                             Input.input_type, Input.description.label("input_description"),
                             null().cast(UUID).label("criteria_id"), null().cast(String).label("criteria_name"),
                             null().cast(String).label("criteria_description")). \
            join(data_query, and_(Input.algorithm_id == data_query.c.algorithm_id)). \
            filter(Input.enabled.is_(True)). \
            cte("input_query")
        criteria_query = select(func.row_number().over(order_by=Criteria.criteria_id).label('id'),
                                AlgorithmCriteria.algorithm_id, null().cast(String).label("name"),
                                null().cast(String).label("description"), null().cast(String).label("source"),
                                null().cast(Date).label("created_at"),
                                null().cast(UUID).label("input_id"), null().cast(String).label("input_name"),
                                null().cast(String).label("input_type"), null().cast(String).label("input_description"),
                                Criteria.criteria_id.label("criteria_id"), Criteria.name.label("criteria_name"),
                                Criteria.name.label("criteria_description")). \
            select_from(AlgorithmCriteria). \
            join(data_query, data_query.c.algorithm_id == AlgorithmCriteria.algorithm_id). \
            join(Criteria, AlgorithmCriteria.criteria_id == Criteria.criteria_id). \
            filter(AlgorithmCriteria.enabled.is_(True), Criteria.enabled.is_(True)). \
            cte("criteria_query")

        qry = select(data_query.c.id, data_query.c.algorithm_id, data_query.c.name,
                     data_query.c.description, data_query.c.source, data_query.c.created_at,
                     data_query.c.input_id, data_query.c.input_name, data_query.c.input_type,
                     data_query.c.input_description, data_query.c.criteria_id, data_query.c.criteria_name,
                     data_query.c.criteria_description). \
            union_all(select(input_query.c.id, input_query.c.algorithm_id, input_query.c.name,
                             input_query.c.description, input_query.c.source, input_query.c.created_at,
                             input_query.c.input_id, input_query.c.input_name, input_query.c.input_type,
                             input_query.c.input_description, input_query.c.criteria_id,
                             input_query.c.criteria_name, input_query.c.criteria_description),
                      select(criteria_query.c.id, criteria_query.c.algorithm_id, criteria_query.c.name,
                             criteria_query.c.description, criteria_query.c.source, criteria_query.c.created_at,
                             criteria_query.c.input_id, criteria_query.c.input_name, criteria_query.c.input_type,
                             criteria_query.c.input_description, criteria_query.c.criteria_id,
                             criteria_query.c.criteria_name, criteria_query.c.criteria_description),
                      select(count.c.id, count.c.algorithm_id, count.c.name,
                             count.c.description, count.c.source, count.c.created_at,
                             count.c.input_id, count.c.input_name, count.c.input_type,
                             count.c.input_description, count.c.criteria_id,
                             count.c.criteria_name, count.c.criteria_description))
        return self._orm.execute_query(qry)

    def delete(self, algorithm_id: str):
        """
        Deletes an algorithm instance by setting its enabled status to false and committing the change to the database.

        Args:
            algorithm_id (str): The ID of the algorithm instance to delete.

        Raises:
            ValueError: If the algorithm instance is not found or validation fails.
        """
        instance = self.get_instance(algorithm_id)
        validate_object(algorithm_id, instance)
        instance.set_enabled_to_false()
        self._orm.object_commit(instance)
        self._orm_disconnect()

    def get_instance(self, p_id: str) -> Algorithm:
        """
        Retrieve an instance of the Algorithm model based on the provided algorithm ID.

        Args:
            p_id (str): The ID of the algorithm to retrieve.

        Returns:
            Algorithm: The instance of the Algorithm model with the specified ID and enabled status,
                       or None if no such instance is found.
        """
        query = self._orm.session.query(Algorithm).filter_by(algorithm_id=p_id,
                                                             enabled=True)
        result = None
        for item in query:
            result = item
        self._orm_disconnect()
        return result

    def list_objects(self, kwargs: dict) -> str:
        """
        Lists algorithm objects based on the provided search criteria.

        Args:
            kwargs (dict): A dictionary of search parameters which may include:
                - "amount" (int): The number of items to return per page (default is 20).
                - "page" (int): The page number to return (default is 0).
                - "value" (str): The value to search for (default is an empty string).
                - "search_by" (str): The field to search by (default is an empty string).

        Returns:
            str: A JSON string containing the total number of items and a list of algorithms with their details.
        """
        amount_item = kwargs.get("amount", 20)
        page = kwargs.get("page", 0)
        value = kwargs.get("value", "")
        search_by = kwargs.get("search_by", "")
        query = self.__get_options_search(search_by, value, page, amount_item)
        list_execution = []
        total_items = None
        for execution in query:
            if not execution[1]:
                total_items = execution[0]
                break
            if not execution[6] and not execution[10]:
                list_execution.append({
                    "algorithm_id": str(execution[1]),
                    "name": execution[2],
                    "description": execution[3],
                    "source": str(execution[4]),
                    "input": [],
                    "criteria": []
                    })
                continue
            for i in list_execution:
                if i['algorithm_id'] != str(execution[1]):
                    continue
                if execution[6]:
                    dct_input = {
                                "input_id": str(execution[6]),
                                "name": execution[7],
                                "input_type": execution[8],
                                "description": execution[9],
                                }
                    i["input"].append(dct_input)
                    break
                if execution[10]:
                    dct_criteria = {
                                   "criteria_id": str(execution[10]),
                                   "name": execution[11],
                                   "description": execution[12],
                                   }
                    i["criteria"].append(dct_criteria)
                    break
        result = {"total_items": total_items,
                  "algorithms": list_execution}
        self._orm_disconnect()
        return json.dumps(result_json(result))
