from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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


class DataAccessLayer:
    def __init__(self, db_path='todo.sqlite3'):
        self.engine = None
        self.Session = None
        self.session = None
        self.conn_string = 'sqlite:////tmp/my.db'

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()
