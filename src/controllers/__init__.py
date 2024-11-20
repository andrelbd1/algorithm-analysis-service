import datetime
import json
import logging

from src.common import Singleton
from src.config import ApplicationConfig
from src.exceptions import ObjectNotFound, ParamInvalid
from src.models.src_orm import OrmConnect

log = logging.getLogger(__file__)
config_app = ApplicationConfig()


class ControllerDefault(metaclass=Singleton):

    def __init__(self):
        self.__instance_orm = OrmConnect()

    @property
    def _orm(self):
        return self.__instance_orm.orm

    @staticmethod
    def _transform_datetime_to_isoformat(date):
        if isinstance(date, (datetime.date, datetime.datetime)):
            return date.isoformat()

    @staticmethod
    def _validate_object(p_id, p_object):
        if not p_object:
            raise ObjectNotFound("Object Not found for id {}".format(p_id))

    @staticmethod
    def _validate_item_dict(search_by, dict_search):
        if search_by not in dict_search:
            raise ParamInvalid(
                "Param {param} invalid for searched".format(param=search_by)
            )

    def _result_json(self, result):
        return json.loads(json.dumps(result, default=self._transform_datetime_to_isoformat))
    
    @staticmethod
    def _format_date():
        return "%Y-%m-%d"

    @staticmethod
    def _format_datetime():
        return "%Y-%m-%d %H:%M:%S"
