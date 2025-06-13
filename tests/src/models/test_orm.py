from mock import mock

from src.models.orm import Orm
from tests import BaseTestClass


class TestOrm(BaseTestClass):

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    def test_get_session(self, mock_create_engine, mock_scoped_session):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.session
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_scoped_session.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    def test_get_db_connection(self, mock_create_engine, mock_scoped_session):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.db_connection
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_create_engine.connect)
        self.assertTrue(mock_scoped_session.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    def test_get_db_engine(self, mock_create_engine, mock_scoped_session):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.db_engine
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_scoped_session.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_object_commit_success(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.object_commit(object)
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.session.flush.called)
        self.assertTrue(db_driver.session.commit.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_object_commit_exception(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        message_error = 'not flush'
        db_driver.session.flush.side_effect = Exception(message_error)
        with self.assertRaises(Exception) as context:
            db_driver.object_commit(object)
        self.assertEqual(context.exception.args[0], message_error)
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.session.flush.called)
        self.assertTrue(db_driver.session.expunge_all.called)
        self.assertTrue(db_driver.session.rollback.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_remove_session(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.remove_session()
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.session.remove.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_delete_object(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.delete_object(object)

        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.session.delete.called)

    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_connection_database(self, mock_sessionmaker, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.test_connection_database()
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
    
    @mock.patch('src.models.orm.create_engine')
    def test_execute_query(self, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.execute_query("query")
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(db_driver.db_engine.connect.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_bulk_save_objects(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.bulk_save_objects(object)
        self.assertTrue(db_driver.session.bulk_save_objects.called)
        self.assertTrue(db_driver.session.commit.called)

    @mock.patch('src.models.orm.scoped_session')
    @mock.patch('src.models.orm.create_engine')
    @mock.patch('src.models.orm.sessionmaker')
    def test_bulk_update_mappings(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        mappings = [{"id": 134, "x": 10}]
        db_driver = Orm('database', 'timeout', 'pool_size')
        db_driver.bulk_update_mappings(object, mappings)
        self.assertTrue(db_driver.session.bulk_update_mappings.called)
        self.assertTrue(db_driver.session.commit.called)
