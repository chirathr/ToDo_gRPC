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
