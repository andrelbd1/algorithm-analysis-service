import mock

from src.common import Singleton
from src.models.src_orm import OrmConnect
from tests import BaseTestClass


class TestModelOrmGeneric(BaseTestClass):

    def setUp(self):
        Singleton.drop()

    @property
    def __orm_generic(self):
        return OrmConnect()

    @mock.patch('src.models.src_orm.Orm')
    def test_orm_generic(self, mock_db_driver):
        self.__orm_generic.orm
        self.assertTrue(mock_db_driver.called)
