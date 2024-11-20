import json
from sqlalchemy import Boolean, Date, Float, String, and_, func, null, select
from sqlalchemy.dialects.postgresql import UUID

from src.config import ApplicationConfig
from src.models.tb_algorithm import Algorithm

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
                            Algorithm.source, Algorithm.created_at). \
            filter(Algorithm.enabled.is_(True)). \
            order_by(Algorithm.created_at.desc())
        param = {
            "algorithm_id": data_query.where(Algorithm.algorithm_id == value),
            "name": data_query.where(func.lower(Algorithm.name).like("%{}%".format(value))),
            "": data_query
        }
        data_query = param[""]
        if value:
            self._validate_item_dict(search_by, param)
            data_query = param[search_by]
        data_query = data_query.cte("data_query")
        count = select(func.count(data_query.c.id).label("id"),
                       null().cast(UUID).label("algorithm_id"), null().cast(String).label("name"),
                       null().cast(String).label("description"), null().cast(String).label("source"),
                       null().cast(Date).label("created_at"),
                       ).limit(1).cte("count")
        smt = select(data_query.c.id, data_query.c.algorithm_id, data_query.c.name,
                     data_query.c.description, data_query.c.source, data_query.c.created_at
                     ).limit(amount).offset(page * amount).order_by(data_query.c.created_at.desc()). \
            union_all(select(count.c.id, count.c.algorithm_id, count.c.name,
                             count.c.description, count.c.source, count.c.created_at))
        return self._orm.execute_query(smt)

    def delete(self, algorithm_id):
        instance = self.__get_instance(algorithm_id)
        self._validate_object(algorithm_id, instance)
        instance.set_enabled_to_false()
        self._orm.object_commit(instance)

    def list_objects(self, kwargs):
        amount_item = kwargs.get("amount", 20)
        page = kwargs.get("page", 0)
        value = kwargs.get("value", "")
        search_by = kwargs.get("search_by", "")
        query = self.__get_options_search(search_by, value, page, amount_item)
        list_report = []
        for report in query:
            if not report[1]:
                total_items = report[0]
                break
            list_report.append({
                "algorithm_id": str(report[1]),
                "name": report[2],
                "description": report[3],
                "source": str(report[4]),
                })
        result = {"total_items": total_items,
                  "algorithms": list_report}
        self._orm.remove_session()
        return json.dumps(self._result_json(result))
