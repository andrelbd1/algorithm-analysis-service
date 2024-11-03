from ulid import ULID

from src.common import Singleton


class AppUlid(metaclass=Singleton):

    @staticmethod
    def ulid_to_uuid():
        return ULID().to_uuid()

    @staticmethod
    def ulid():
        return ULID()

    @staticmethod
    def ulid_to_datetime(str_ulid):
        ulid = ULID().from_str(str_ulid)
        return ulid.datetime
