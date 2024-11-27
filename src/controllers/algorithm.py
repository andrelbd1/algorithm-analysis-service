import json
from sqlalchemy import Date, String, and_, func, null, select
from sqlalchemy.dialects.postgresql import UUID

from src.config import ApplicationConfig
from src.common.functions import result_json, validate_item_dict, validate_object
from src.models.tb_algorithm import Algorithm
from src.models.tb_input import Input

from . import ControllerDefault

config_app = ApplicationConfig()


class ControllerAlgorithm(ControllerDefault):

    def __get_instance(self, p_id):
        query = self._orm.session.query(Algorithm).filter_by(algorithm_id=p_id)
        result = None
        for item in query:
            result = item
        return result

    def __get_options_search(self, search_by, value, page, amount):
        """Query to search."""
        data_query = select(func.row_number().over(order_by=Algorithm.algorithm_id).label('id'),
                            Algorithm.algorithm_id, Algorithm.name, Algorithm.description,
                            Algorithm.source, Algorithm.created_at,
                            null().cast(UUID).label("input_id"), null().cast(String).label("input_name"),
                            null().cast(String).label("input_type"), null().cast(String).label("input_description")). \
            filter(Algorithm.enabled.is_(True)). \
            order_by(Algorithm.created_at.desc())
        param = {
            "algorithm_id": data_query.where(Algorithm.algorithm_id == value),
            "name": data_query.where(func.lower(Algorithm.name).like("%{}%".format(value.strip().lower()))),
            "": data_query
        }
        data_query = param[""]
        if value:
            validate_item_dict(search_by, param)
            data_query = param[search_by]
        data_query = data_query.limit(amount).offset(page * amount).cte("data_query")
        input_query = select(func.row_number().over(order_by=Input.algorithm_id).label('id'),
                             Input.algorithm_id, null().cast(String).label("name"),
                             null().cast(String).label("description"), null().cast(String).label("source"),
                             null().cast(Date).label("created_at"),
                             Input.input_id, Input.name.label("input_name"),
                             Input.input_type, Input.description.label("input_description")). \
            join(data_query, and_(Input.algorithm_id == data_query.c.algorithm_id)). \
            filter(Input.enabled.is_(True)). \
            cte("input_query")
        count = select(func.count(data_query.c.id).label("id"),
                       null().cast(UUID).label("algorithm_id"), null().cast(String).label("name"),
                       null().cast(String).label("description"), null().cast(String).label("source"),
                       null().cast(Date).label("created_at"),
                       null().cast(UUID).label("input_id"), null().cast(String).label("input_name"),
                       null().cast(String).label("input_type"), null().cast(String).label("input_description")
                       ).limit(1).cte("count")
        qry = select(data_query.c.id, data_query.c.algorithm_id, data_query.c.name,
                     data_query.c.description, data_query.c.source, data_query.c.created_at,
                     data_query.c.input_id, data_query.c.input_name, data_query.c.input_type,
                     data_query.c.input_description
                     ). \
            union_all(select(input_query.c.id, input_query.c.algorithm_id, input_query.c.name,
                             input_query.c.description, input_query.c.source, input_query.c.created_at,
                             input_query.c.input_id, input_query.c.input_name, input_query.c.input_type,
                             input_query.c.input_description),
                      select(count.c.id, count.c.algorithm_id, count.c.name,
                             count.c.description, count.c.source, count.c.created_at,
                             count.c.input_id, count.c.input_name, count.c.input_type,
                             count.c.input_description))
        return self._orm.execute_query(qry)

    def delete(self, algorithm_id):
        instance = self.__get_instance(algorithm_id)
        validate_object(algorithm_id, instance)
        instance.set_enabled_to_false()
        self._orm.object_commit(instance)

    def list_objects(self, kwargs):
        amount_item = kwargs.get("amount", 20)
        page = kwargs.get("page", 0)
        value = kwargs.get("value", "")
        search_by = kwargs.get("search_by", "")
        query = self.__get_options_search(search_by, value, page, amount_item)
        list_report = []
        total_items = None
        for report in query:
            if not report[1]:
                total_items = report[0]
                break
            if not report[6]:
                list_report.append({
                    "algorithm_id": str(report[1]),
                    "name": report[2],
                    "description": report[3],
                    "input": []
                    # "source": str(report[4]),
                    })
                continue
            for i in list_report:
                if i['algorithm_id'] == str(report[1]):
                    dct_input = {
                                    "input_id": str(report[6]),
                                    "name": report[7],
                                    "input_type": report[8],
                                    "description": report[9],
                                }
                    i["input"].append(dct_input)
                    break
        result = {"total_items": total_items,
                  "algorithms": list_report}
        self._orm.remove_session()
        return json.dumps(result_json(result))
