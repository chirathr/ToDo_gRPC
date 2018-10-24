import os
import sqlite3

import pytest
from unittest.mock import Mock

from server.models.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.server_util_lib.main import ServerUtils
from server.models import models
from sqlalchemy.orm import scoped_session, exc
from server.models.models import dal, Base


# Test models
class TestToDoDb:
    @pytest.fixture(scope='class')
    def session(self, request):
        dal.conn_string = 'sqlite:///:memory:'
        dal.connect()

        dal.Session = scoped_session(dal.Session)
        dal.session = dal.Session()
        dal.Session.registry.clear()

        request.addfinalizer(Base.metadata.drop_all)
        return dal.session

    @pytest.fixture(scope='function')
    def db_session(self, request, session):
        session.query(models.User).delete()
        session.query(models.ToDo).delete()
        return session

    @staticmethod
    def _add_user(db_session, name):
        user = models.User(name=name)
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    def _get_user(db_session, user_id):
        try:
            return db_session.query(models.User).filter(models.User.id == user_id).one()
        except exc.NoResultFound:
            return None

    @staticmethod
    def _add_todo(db_session, user_id, text):
        user = db_session.query(models.User).filter(models.User.id == user_id).one()
        todo = models.ToDo(user=user, text=text)
        db_session.add(todo)
        db_session.commit()
        return todo

    @staticmethod
    def _get_todo(db_session, todo_id):
        try:
            return db_session.query(models.ToDo).filter(models.ToDo.id == todo_id).one()
        except exc.NoResultFound:
            return None

    @staticmethod
    def _get_todo_list(db_session, user_id):
        user = db_session.query(models.User).filter(models.User.id == user_id).one()
        return db_session.query(models.ToDo).filter(models.ToDo.user == user).all()

    def test_get_user(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self._add_user(db_session, "Test user")

        assert todo_db.get_user("Test user") == user.id

    def test_get_user_empty_db(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.get_user("Test user") is None

    def test_get_user_empty_name_raises_value_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        with pytest.raises(ValueError):
            todo_db.get_user("")

    def test_add_user(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user_id = todo_db.add_user_if_not_exist("Test user")
        user = self._get_user(db_session, user_id)

        assert user.name == "Test user"

    def test_add_user_if_exists(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        self._add_user(db_session, "Test user")
        user_id = todo_db.add_user_if_not_exist("Test user")
        user = self._get_user(db_session, user_id)

        assert user.id == user_id
        assert user.name == "Test user"

    def test_add_user_empty_name_raises_value_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        with pytest.raises(ValueError):
            todo_db.add_user_if_not_exist("")

    def test_add_todo(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self._add_user(db_session, "Test user")

        todo_id = todo_db.add_todo(user.id, "Test todo")
        todo = self._get_todo(db_session, todo_id)

        assert todo.id == todo_id
        assert todo.user.id == user.id
        assert todo.text == "Test todo"
    
    def test_add_todo_empty_text_raises_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        with pytest.raises(ValueError):
            todo_db.add_todo(1, "")

    def test_add_todo_invalid_user_id(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        with pytest.raises(ValueError):
            todo_db.add_todo(None, "")
        with pytest.raises(ValueError):
            todo_db.add_todo(-1, "")

    def test_update_todo_is_done(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self._add_user(db_session, "Test user")
        todo = self._add_todo(db_session, user.id, "Test Todo")

        assert todo_db.update_todo(todo.id, user.id, is_done=True)
        assert self._get_todo(db_session, todo.id).is_done

    def test_update_todo_is_done_raises_value_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        with pytest.raises(ValueError):
            todo_db.update_todo(-1, 1, is_done=True)
        with pytest.raises(ValueError):
            todo_db.update_todo(1, -1, is_done=True)

        assert todo_db.update_todo(1, 1) is False

    def test_update_todo_delete(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self._add_user(db_session, "Test user")
        todo = self._add_todo(db_session, user.id, "Test Todo")

        assert todo_db.update_todo(todo.id)
        assert self._get_todo(db_session, todo.id) is None

    def test_get_todo_list(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self._add_user(db_session, "Test user")
        self._add_todo(db_session, user.id, "Test Todo 1")
        self._add_todo(db_session, user.id, "Test Todo 2")

        todo_list = self._get_todo_list(db_session, user.id)
        actual_todo_list = todo_db.get_todo_list(user.id)

        for i in range(len(todo_list)):
            assert todo_list[i].id == actual_todo_list[i].id
            assert todo_list[i].text == actual_todo_list[i].text

    def test_get_todo_list_user_not_found_raises_exception(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        with pytest.raises(ValueError):
            todo_db.get_todo_list(1)


# TestServerUtil class
class TestServerUtils:
    todo_db = Mock(spec=ToDoDb())

    def test_add_user(self):
        self.todo_db.add_user_if_not_exist.return_value = 1
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(user=User(name="Test user"))

        assert user.id == 1
        assert user.name == "Test user"
        assert user.status == SUCCESS

    def test_add_user_fails(self):
        self.todo_db.add_user_if_not_exist.return_value = 0
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(User(name="Test user"))

        assert user.status == FAILED

    def test_add_user_fails_with_wrong_argument_type(self):
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user("")

        assert user.status == FAILED

    def test_add_user_fails_with_empty_name(self):
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(User())

        assert user.status == FAILED

    def test_add_todo(self):
        self.todo_db.add_todo.return_value = 1
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(text="Todo", user=User(id=1)))

        assert todo.status == SUCCESS
        assert todo.id == 1

    def test_add_todo_fails_without_text(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=1)))
        assert todo.status == FAILED

    def test_add_todo_fails_on_invalid_user_id(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=0)))
        assert todo.status == FAILED

        todo = server_utils.add_todo(ToDo(user=User(id=-2)))
        assert todo.status == FAILED

    def test_add_todo_fails_on_invalid_todo(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo())
        assert todo.status == FAILED

        todo = server_utils.add_todo(1)
        assert todo.status == FAILED

        todo = server_utils.add_todo("")
        assert todo.status == FAILED

    def test_add_todo_fails_on_value_error_from_db(self):
        self.todo_db.add_todo.side_effect = ValueError()
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(text="Todo", user=User(id=1)))
        assert todo.status == FAILED

    def test_update_todo_is_done(self):
        self.todo_db.update_todo.return_value = SUCCESS
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, user=User(id=1), is_done=True))
        assert todo.status == SUCCESS

    def test_update_todo_delete(self):
        self.todo_db.update_todo.return_value = SUCCESS
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, is_done=True))
        assert todo.status == SUCCESS

    def test_update_todo_fails_on_value_error(self):
        self.todo_db.update_todo.side_effect = ValueError
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, is_done=True))
        assert todo.status == FAILED

    def test_update_todo_fails_on_wrong_arguments(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(None)
        assert todo.status == FAILED

        todo = server_utils.update_todo("Test")
        assert todo.status == FAILED

        todo = server_utils.update_todo(ToDo(id=-5))
        assert todo.status == FAILED

    def test_get_todo_list(self):
        todo_list_data = [
            models.ToDo(id=1, user=models.User(id=1), text="Todo 1", is_done=True),
            models.ToDo(id=1, user=models.User(id=1), text="Todo 1", is_done=True),
        ]
        todo_list = []
        for todo_item in todo_list_data:
            todo = ToDo(
                id=todo_item.id,
                user=User(id=todo_item.user.id),
                text=todo_item.text,
                is_done=todo_item.is_done,
                status=SUCCESS
            )
            todo_list.append(todo)

        self.todo_db.get_todo_list.return_value = todo_list_data
        server_utils = ServerUtils(todo_db=self.todo_db)

        assert server_utils.get_todo_list(User(id=1)) == todo_list

    def test_todo_list_value_error(self):
        self.todo_db.get_todo_list.side_effect = ValueError
        server_utils = ServerUtils(todo_db=self.todo_db)
        todo_list = server_utils.get_todo_list(User(id=1))

        assert todo_list[0].status == FAILED

    def test_todo_list_wrong_arguments(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo_list = server_utils.get_todo_list(None)
        assert todo_list[0].status == FAILED

        todo_list = server_utils.get_todo_list("Test")
        assert todo_list[0].status == FAILED

        todo_list = server_utils.get_todo_list(User(id=0))
        assert todo_list[0].status == FAILED
