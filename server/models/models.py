from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __str__(self):
        return "{0}. {1}".format(self.id, self.name)


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        User,
        backref=backref(
            'todos',
            uselist=True,
            cascade='delete,all'
        )
    )

    def __str__(self):
        return '{0}. {1}'.format(self.id, self.text)


def create_db_tables(database_path='todo.sqlite3'):
    sqlite_db={'drivername': 'sqlite', 'database': database_path}
    url = URL(**sqlite_db)
    engine = create_engine(url)

    Base.metadata.create_all(engine)


def get_session(database_path='todo.sqlite3'):
    sqlite_db={'drivername': 'sqlite', 'database': database_path}
    url = URL(**sqlite_db)
    engine = create_engine(url)

    DBSession = sessionmaker(bind=engine)
    return DBSession()
