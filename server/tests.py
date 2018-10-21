from unittest.mock import Mock

from server.models.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.server_util_lib.main import ServerUtils


# TestServerUtil class
class TestServerUtils:
    todo_db = Mock(spec=ToDoDb())

    def test_add_user(self):
        self.todo_db.add_user_if_not_exist.return_value = 1
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(User(name="Test user"))

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

    def test_todo_fails_without_text(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=1)))
        assert todo.status == FAILED

    def test_todo_fails_on_invalid_user_id(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=0)))
        assert todo.status == FAILED

        todo = server_utils.add_todo(ToDo(user=User(id=-2)))
        assert todo.status == FAILED

    def test_todo_fails_on_invalid_todo(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo())
        assert todo.status == FAILED

        todo = server_utils.add_todo(1)
        assert todo.status == FAILED

        todo = server_utils.add_todo("")
        assert todo.status == FAILED

    def test_todo_fails_on_value_error_from_db(self):
        self.todo_db.add_todo.side_effect = ValueError()
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(text="Todo", user=User(id=1)))
        assert todo.status == FAILED
