import datetime

from uuid import UUID
from ulid import ULID

from src.common import Singleton
from src.internal_services.app_ulid import AppUlid
from tests import BaseTestClass


class TestAppUlid(BaseTestClass):

    def setUp(self):
        Singleton.drop()

    @property
    def __ulid(self):
        return AppUlid()

    def test_ulid(self):
        result = self.__ulid.ulid()
        self.assertIsInstance(result, ULID)

    def test_ulid_to_datetime(self):
        ulid = self.__ulid.ulid()
        result = self.__ulid.ulid_to_datetime(str(ulid))
        self.assertIsInstance(result, datetime.datetime)

    def test_ulid_to_uuid(self):
        result = self.__ulid.ulid_to_uuid()
        self.assertIsInstance(result, UUID)
