from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Orm:
    """Class the of access database connect."""

    def __init__(self, database, timeout, pool_size):
        self.__engine = create_engine(database,
                                      connect_args={'sslmode': 'prefer'},
                                      pool_recycle=timeout,
                                      pool_pre_ping=True,
                                      pool_size=pool_size,)

        self.__db_session = scoped_session(sessionmaker(bind=self.__engine, autocommit=False, autoflush=True))

    @property
    def session(self):
        """Property db_session."""
        return self.__db_session

    @property
    def db_connection(self):
        """Property engine."""
        return self.__engine.connect()

    @property
    def db_engine(self):
        """Property engine."""
        return self.__engine

    def commit(self):
        """Commit in Database"""
        try:
            self.session.flush()
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            self.session.expunge_all()
            raise error

    def object_commit(self, p_object):
        """Add object of the database."""
        self.session.add(p_object)
        self.commit()

    def delete_object(self, p_object):
        """Delete object of the database."""
        self.session.delete(p_object)
        self.commit()

    def remove_session(self):
        """remove session sql"""
        self.__db_session.remove()

    def bulk_save_objects(self, list_objects):
        if list_objects:
            self.session.bulk_save_objects(list_objects)
            self.commit()

    def bulk_update_mappings(self, p_class, p_mappings):
        if p_mappings:
            self.session.bulk_update_mappings(p_class, p_mappings)
            self.commit()

    def test_connection_database(self):
        """Test connection test_connection_database."""
        return self.execute_query("SELECT * FROM pg_stat_activity")

    def execute_query(self, query):
        with self.db_engine.connect() as connection:
            result = connection.execute(query)
            return result
