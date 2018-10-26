import pytest
from sqlalchemy.orm import exc, scoped_session

from server.models import models
from server.models.models import dal, Base


@pytest.fixture(scope='session')
def session(request):
    dal.conn_string = 'sqlite:///:memory:'
    dal.connect()

    dal.Session = scoped_session(dal.Session)
    dal.session = dal.Session()
    dal.Session.registry.clear()

    request.addfinalizer(Base.metadata.drop_all)
    return dal.session


@pytest.fixture(scope='function')
def db_session(request, session):
    session.query(models.User).delete()
    session.query(models.ToDo).delete()
    return session


class ServerTestHelper:
    @staticmethod
    def mock_add_user(db_session, name):
        user = models.User(name=name)
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    def mock_get_user(db_session, user_id):
        try:
            return db_session.query(models.User).filter(models.User.id == user_id).one()
        except exc.NoResultFound:
            return None

    @staticmethod
    def mock_add_todo(db_session, user_id, text):
        user = db_session.query(models.User).filter(models.User.id == user_id).one()
        todo = models.ToDo(user=user, text=text)
        db_session.add(todo)
        db_session.commit()
        return todo

    @staticmethod
    def mock_get_todo(db_session, todo_id):
        try:
            return db_session.query(models.ToDo).filter(models.ToDo.id == todo_id).one()
        except exc.NoResultFound:
            return None

    @staticmethod
    def mock_get_todo_list(db_session, user_id):
        user = db_session.query(models.User).filter(models.User.id == user_id).one()
        return db_session.query(models.ToDo).filter(models.ToDo.user == user).all()

    @staticmethod
    def mock_get_user_list(db_session):
        return db_session.query(models.User).all()
