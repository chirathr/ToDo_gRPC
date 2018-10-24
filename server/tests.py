import os
import sqlite3

import pytest
from unittest.mock import Mock

from server.models.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.server_util_lib.main import ServerUtils
from server.models import models

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


# Test models
    class TestToDoDb:
        @pytest.fixture
        def db_path(self, tmpdir):
            return os.path.join(tmpdir.strpath, "test.db")


        @pytest.fixture
        def db_conn(self, db_path):
            if os.path.exists(db_path):
                os.remove(db_path)
            conn = sqlite3.connect(db_path)
            yield conn

        @staticmethod
        def _add_user(conn, name):
            create_user_sql = 'insert into user (name) values("{name}");'.format(name=name)
            cursor = conn.cursor()
            cursor.execute(create_user_sql)
            user_id = cursor.lastrowid
            conn.commit()
            return user_id

        @staticmethod
        def _get_user(conn, id):
            get_user_sql = 'select * from user where id = "{id}";'.format(id=id)
            cursor = conn.cursor()
            cursor.execute(get_user_sql)
            return cursor.fetchone()

        @staticmethod
        def _add_todo(conn, user_id, text):
            create_todo_sql = 'insert into todo (user_id, text, is_done) ' \
                              'values ({user_id}, "{text}", {is_done})' \
                              ''.format(user_id=user_id, text=text, is_done=0)
            cursor = conn.cursor()
            cursor.execute(create_todo_sql)
            todo_id = cursor.lastrowid
            conn.commit()
            return todo_id

        @staticmethod
        def _get_todo(conn, id):
            get_todo_sql = 'select * from todo where id = "{id}";'.format(id=id)
            cursor = conn.cursor()
            cursor.execute(get_todo_sql)
            return cursor.fetchone()

        @staticmethod
        def _get_todo_list(db_path, user_id):
            session = models.get_session(db_path)
            user = session.query(models.User).filter(models.User.id == user_id).one()
            return session.query(models.ToDo).filter(models.ToDo.user == user).all()

        def test_get_user(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = self._add_user(db_conn, "Test user")

            assert todo_db.get_user("Test user") == user_id

        def test_get_user_empty_db(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            assert todo_db.get_user("Test user") is None

        def test_add_user(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = todo_db.add_user_if_not_exist("Test user")
            user = self._get_user(db_conn, user_id)

            assert user[1] == "Test user"

        def test_add_user_if_exists(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            self._add_user(db_conn, "Test user")
            user_id = todo_db.add_user_if_not_exist("Test user")
            user = self._get_user(db_conn, user_id)

            assert user[1] == "Test user"

        def test_add_todo(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = self._add_user(db_conn, "Test user")

            todo_id = todo_db.add_todo(user_id, "Test todo")
            todo = self._get_todo(db_conn, todo_id)

            assert todo[3] == user_id
            assert todo[1] == "Test todo"

        def test_add_todo_invalid_user_id(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            with pytest.raises(ValueError):
                todo_db.add_todo(None, "")
            with pytest.raises(ValueError):
                todo_db.add_todo(-1, "")

        def test_update_todo_is_done(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = self._add_user(db_conn, "Test user")
            todo_id = self._add_todo(db_conn, user_id, "Test Todo")

            assert todo_db.update_todo(todo_id, user_id, is_done=True)

            assert self._get_todo(db_conn, todo_id)[3] == 1

        def test_update_todo_is_done_raises_value_error(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            with pytest.raises(ValueError):
                todo_db.update_todo(-1, 1, is_done=True)
            with pytest.raises(ValueError):
                todo_db.update_todo(1, -1, is_done=True)

            assert todo_db.update_todo(1, 1) is False

        def test_update_todo_delete(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = self._add_user(db_conn, "Test user")
            todo_id = self._add_todo(db_conn, user_id, "Test Todo")

            assert todo_db.update_todo(todo_id)
            assert self._get_todo(db_conn, todo_id) is None

        def test_get_todo_list(self, db_conn, db_path):
            todo_db = ToDoDb(db_path=db_path)
            user_id = self._add_user(db_conn, "Test user")
            self._add_todo(db_conn, user_id, "Test Todo 1")
            self._add_todo(db_conn, user_id, "Test Todo 2")

            todo_list = self._get_todo_list(db_path, user_id)
            actual_todo_list = todo_db.get_todo_list(user_id)

            for i in range(len(todo_list)):
                assert todo_list[i].id == actual_todo_list[i].id
                assert todo_list[i].text == actual_todo_list[i].text
