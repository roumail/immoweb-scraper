from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from immoweb_scraper.db.sqlalchemy import Base


class DBConnection:
    def __init__(self, path2db):
        self.path2db = path2db
        connection_string = f"sqlite:///{self.path2db}"
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = Session()

    @contextmanager
    def cursor(self):
        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception as e:  # noqa
            raise

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.session
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

    def close(self):
        self.session.close()
