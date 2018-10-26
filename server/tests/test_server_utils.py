from unittest.mock import Mock

from server.models.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo
from protobuf import todo_pb2
from server.server_util_lib.main import ServerUtils
from server.models import models


# TestServerUtil class
class TestServerUtils:
    todo_db = Mock(spec=ToDoDb())

    def test_add_user(self):
        user_id = 1
        self.todo_db.add_user.return_value = {
            'status': ToDoDb.SUCCESS,
            'user': models.User(id=user_id)
            }
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(user=User(name="Test user"))

        assert user.id == user_id
        assert user.name == "Test user"
        assert user.status == todo_pb2.SUCCESS

    def test_add_user_fails(self):
        self.todo_db.add_user.return_value = {'status': ToDoDb.FAILED}
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(User(name="Test user"))

        assert user.status == todo_pb2.FAILED

    def test_add_user_fails_with_wrong_argument_type(self):
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user("")

        assert user.status == todo_pb2.FAILED

    def test_add_user_fails_with_empty_name(self):
        server_utils = ServerUtils(todo_db=self.todo_db)
        user = server_utils.add_user(User())

        assert user.status == todo_pb2.FAILED

    def test_add_todo(self):
        user_id = 1
        self.todo_db.add_todo.return_value = {
            'status': ToDoDb.SUCCESS,
            'todo': models.ToDo(id=user_id)
        }
        server_utils = ServerUtils(todo_db=self.todo_db)
        todo = server_utils.add_todo(ToDo(text="Todo", user=User(id=1)))

        assert todo.status == todo_pb2.SUCCESS
        assert todo.id == user_id

    def test_add_todo_fails_without_text(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=1)))
        assert todo.status == todo_pb2.FAILED

    def test_add_todo_fails_on_invalid_user_id(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(user=User(id=0)))
        assert todo.status == todo_pb2.FAILED

        todo = server_utils.add_todo(ToDo(user=User(id=-2)))
        assert todo.status == todo_pb2.FAILED

    def test_add_todo_fails_on_invalid_todo(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo())
        assert todo.status == todo_pb2.FAILED

        todo = server_utils.add_todo(1)
        assert todo.status == todo_pb2.FAILED

        todo = server_utils.add_todo("")
        assert todo.status == todo_pb2.FAILED

    def test_add_todo_fails_on_db_failed_status(self):
        self.todo_db.add_todo.return_value = {'status': ToDoDb.FAILED}
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.add_todo(ToDo(text="Todo", user=User(id=1)))
        assert todo.status == todo_pb2.FAILED

    def test_update_todo_is_done(self):
        self.todo_db.update_todo.return_value = {
            'status': ToDoDb.MARKED_AS_DONE
        }
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, user=User(id=1), is_done=True))
        assert todo.status == todo_pb2.SUCCESS

    def test_update_todo_delete(self):
        self.todo_db.update_todo.return_value = {
            'status': ToDoDb.DELETED
        }
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, is_done=True))
        assert todo.status == todo_pb2.SUCCESS

    def test_update_todo_fails_on_db_failed_status(self):
        self.todo_db.update_todo.return_value = {
            'status': ToDoDb.FAILED
        }
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(ToDo(id=1, is_done=True))
        assert todo.status == todo_pb2.FAILED

    def test_update_todo_fails_on_wrong_arguments(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo = server_utils.update_todo(None)
        assert todo.status == todo_pb2.FAILED

        todo = server_utils.update_todo("Test")
        assert todo.status == todo_pb2.FAILED

        todo = server_utils.update_todo(ToDo(id=-5))
        assert todo.status == todo_pb2.FAILED

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
                status=todo_pb2.SUCCESS
            )
            todo_list.append(todo)

        self.todo_db.get_todo_list.return_value = {
            'todo_list': todo_list_data,
            'status': ToDoDb.SUCCESS
        }
        server_utils = ServerUtils(todo_db=self.todo_db)
        assert server_utils.get_todo_list(User(id=1)) == todo_list

    def test_todo_list_db_failed_status(self):
        self.todo_db.get_todo_list.return_value = {'status': ToDoDb.FAILED}
        server_utils = ServerUtils(todo_db=self.todo_db)
        todo_list = server_utils.get_todo_list(User(id=1))

        assert todo_list[0].status == todo_pb2.FAILED

    def test_todo_list_wrong_arguments(self):
        server_utils = ServerUtils(todo_db=self.todo_db)

        todo_list = server_utils.get_todo_list(None)
        assert todo_list[0].status == todo_pb2.FAILED

        todo_list = server_utils.get_todo_list("Test")
        assert todo_list[0].status == todo_pb2.FAILED

        todo_list = server_utils.get_todo_list(User(id=0))
        assert todo_list[0].status == todo_pb2.FAILED
